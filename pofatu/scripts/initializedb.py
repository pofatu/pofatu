import sys
import pathlib
import statistics
import collections

import attr
from sqlalchemy.orm import joinedload
from clld.scripts.util import initializedb, Data, bibtex2source
from clld.lib import bibtex
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.misc import slug
from shapely.geometry import MultiPoint
from pypofatu import Pofatu
import pypofatu.models

import pofatu
from pofatu import models


def refkey(s):
    return {
        'metraux-1940-ethnology': 'metraux-1940-easter',
        'mcalister-2017-plosone': 'mcalister-2017-po',
        'weisler 1993 phd': 'weisler-1993-phd',
        'mccoy-1993-kahoolawe': 'mccoy-1993-puumoiwi',
        'anderson 1981a': 'anderson-1981-jrsnz',
        'barber & walter 2002': 'barber-2002-anz',
        'gay 2004': 'gay-2004-ba',
    }.get(s.lower(), s.lower())


ENTRY_TYPES = {
    'thesis': 'phdthesis',
    'report': 'techreport',
    'collection': 'book',
    'mvbook': 'book',
}


def main(args):
    data = Data()
    ds = Pofatu(pathlib.Path(pofatu.__file__).parent.parent.parent / 'pofatu-data')

    dataset = common.Dataset(
        id=pofatu.__name__,
        name="POFATU",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="https://www.shh.mpg.de",
        license="https://creativecommons.org/licenses/by/4.0/",
        domain='pofatu.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    for i, (id_, name) in enumerate([
        ('hermannaymeric', 'Aymeric Hermann'),
        ('forkelrobert', 'Robert Forkel'),
    ]):
        ed = data.add(common.Contributor, id_, id=id_, name=name)
        common.Editor(dataset=dataset, contributor=ed, ord=i + 1)
    DBSession.add(dataset)

    for rec in ds.iterbib():
        rec.genre = bibtex.EntryType.from_string(ENTRY_TYPES.get(rec.genre, rec.genre))
        if 'date' in rec:
            rec['year'] = rec.pop('date')
        data.add(common.Source, rec.id.replace('_', '-').lower(), _obj=bibtex2source(rec, lowercase_id=False))

    analyses = list(ds.iterdata())

    def midpoint(coords):
        p = MultiPoint([(lat, lon + 360 if lon < 0 else lon) for lat, lon in coords]).convex_hull
        #geojson = {
        #    'type': 'Feature',
        #    'properties': {},
        #    'geometry': mapping(p)}
        c = p.centroid
        return c.x, (c.y - 360) if c.y > 180 else c.y

    artefacts = collections.defaultdict(dict)
    midpoints = {}
    for a in analyses:
        l = a.sample.location
        lid = l.id
        if lid not in midpoints:
            midpoints[lid] = set()
        if l.latitude is not None and l.longitude is not None:
            midpoints[lid].add((l.latitude, l.longitude))
        art = a.sample.artefact
        for attr_ in ['name', 'category', 'collection_type']:
            if not artefacts[slug(art.id)].get(attr_):
               artefacts[slug(art.id)][attr_] = getattr(art, attr_)

    midpoints = {k: midpoint(v) if v else (None, None) for k, v in midpoints.items()}

    for analysis in analyses:
        loc = analysis.sample.location
        if loc.id not in data['Location']:
            data.add(
                models.Location,
                loc.id,
                id=loc.id,
                name=loc.label,
                latitude=midpoints[loc.id][0],
                longitude=midpoints[loc.id][1],
                region=loc.loc1.replace('_', ' '),
                subregion=loc.loc2,
                location=loc.loc3,
            )

        site = analysis.sample.site
        if site.id not in data['Site']:
            s = data.add(
                models.Site,
                site.id,
                id=site.id,
                name=site.label,
            )
            for ref in site.source_ids:
                DBSession.add(models.SiteReference(site=s, source=data['Source'][refkey(ref)]))

        artefact = analysis.sample.artefact
        if slug(artefact.id) not in data['Artefact']:
            a = data.add(
                models.Artefact,
                slug(artefact.id),
                id=slug(artefact.id),
                **artefacts[slug(artefact.id)],
            )
            for ref in artefact.source_ids:
                DBSession.add(models.ArtefactReference(artefact=a, source=data['Source'][refkey(ref)]))

    # Add contributions
    for contrib in ds.itercontributions():
        contribution = data.add(
            common.Contribution, contrib.id,
            id=contrib.id,
            name=contrib.label,
            description=contrib.description,
        )
        DBSession.flush()
        for i, name in enumerate(contrib.contributors):
            cid = slug(name)
            co = data['Contributor'].get(cid)
            if not co:
                co = data.add(common.Contributor, cid, id=cid, name=name)
            common.ContributionContributor(ord=i, contribution=contribution, contributor=co)

        for ref in contrib.source_ids:
            DBSession.add(common.ContributionReference(
                contribution=contribution,
                source=data['Source'][refkey(ref)],
            ))
            data['Contribution'][ref] = contribution

    methods = collections.defaultdict(list)
    for method in ds.itermethods():
        m = data.add(
            models.Method,
            method.id,
            id=method.id,
            name=method.label,
            code=method.code,
            parameter=method.parameter.strip(),
            reference_sample='; '.join([r.sample_name for r in method.references]),
            laboratory=method.laboratory,
            technique=method.technique,
            instrument=method.instrument,
        )
        methods[(m.code.lower(), m.parameter.lower())].append(m)

    parameter = data.add(common.Parameter, 'c', id='category', name='Sample category')
    for i, opt in enumerate(attr.fields_dict(pypofatu.models.Sample)['category'].validator.options, start=1):
        data.add(common.DomainElement, opt, parameter=parameter, id=str(i), name=opt)

    DBSession.flush()
    assert parameter.pk

    # Add Samples and UnitParameters and Measurements
    for analysis in analyses:
        sample = analysis.sample
        vsid = '{0}-{1}'.format(sample.location.id, data['Contribution'][sample.source_id].id)
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id=vsid,
                language_pk=data['Location'][sample.location.id].pk,
                parameter_pk=parameter.pk,
                contribution_pk=data['Contribution'][sample.source_id].pk,
            )
        v = data['Sample'].get(sample.id)
        if not v:
            v = data.add(
                models.Sample,
                sample.id,
                id=sample.id.replace('.', '_'),
                name=sample.id,
                #petrography=,
                #analyzed_material=.
                latitude=sample.location.latitude,
                longitude=sample.location.longitude,
                elevation=sample.location.elevation,
                location_comment=sample.location.comment,
                site_context=sample.site.context,
                site_comment=sample.site.comment,
                site_stratigraphic_position=sample.site.stratigraphic_position,
                domainelement=data['DomainElement'][sample.category],
                valueset=vs,
                site=data['Site'][sample.site.id],
                artefact_comment=sample.artefact.comment,
                artefact_attributes=sample.artefact.attributes,
                artefact=data['Artefact'][slug(sample.artefact.id)],
            )
            DBSession.add(models.SampleReference(sample=v, source=data['Source'][refkey(sample.source_id)]))

        a = data.add(
            models.Analysis,
            analysis.id,
            id=slug(analysis.id, lowercase=False),
            name=analysis.id,
            sample=v,
        )

        for measurement in analysis.measurements:
            pid = slug(measurement.parameter, lowercase=False)
            p = data['Param'].get(pid)
            if not p:
                p = data.add(models.Param, pid, id=pid, name=measurement.parameter)
            data.add(
                models.Measurement, None,
                id='{0}-{1}'.format(a.id, p.id),
                analysis=a,
                method=data['Method'].get(measurement.method.id) if measurement.method else None,
                value=measurement.value,
                less=measurement.less,
                precision=measurement.precision,
                unitparameter=p,
            )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for p in DBSession.query(models.Param).options(joinedload(models.Param.values)):
        vals = [v.value for v in p.values]
        p.min = min(vals)
        p.max = max(vals)
        p.mean = statistics.mean(vals)
        p.median = statistics.median(vals)
        p.count_values = len(vals)


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
