import sys
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

from sqlalchemy.orm import joinedload
from clld.scripts.util import initializedb, Data, bibtex2source
from clld.lib import bibtex
from clld.db.meta import DBSession
from clld.db.models import common
from csvw.dsv import reader
from clldutils.misc import slug
from pypofatu import Pofatu

import pofatu
from pofatu import models
from pofatu.scripts import georoc


def refkey(s):
    return {
        'metraux-1940-ethnology': 'metraux-1940-easter',
        'mcalister-2017-plosone': 'mcalister-2017-po',
        'weisler 1993 phd': 'weisler-1993-phd',
        'mccoy-1993-kahoolawe': 'mccoy-1993-puumoiwi',
    }.get(s.lower(), s.lower())


def main(args):
    data = Data()
    ds = Pofatu(Path(pofatu.__file__).parent.parent.parent / 'pofatu-data')

    dataset = common.Dataset(
        id=pofatu.__name__,
        name="POFATU",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
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
        rec.genre = bibtex.EntryType.from_string(rec.genre)
        data.add(common.Source, rec.id.replace('_', '-').lower(), _obj=bibtex2source(rec, lowercase_id=False))

    samples = list(ds.iterdata())
    for sample, _ in samples:
        loc = sample.location
        if loc.name not in data['Location']:
            data.add(
                models.Location,
                loc.name,
                id=slug(loc.name),
                name=loc.name,
                region=loc.loc1.replace('_', ' '),
                subregion=loc.loc2,
                location=loc.loc3,
                description=loc.comment,
                latitude=loc.latitude,
                longitude=loc.longitude,
                elevation=loc.elevation,
            )

    # Add contributions
    for contrib in ds.itercontributions():
        c = data.add(
            models.PofatuContribution, contrib.id,
            id=contrib.id,
            name=contrib.label,
            description=contrib.description,
            source=data['Source'][refkey(contrib.id)],
        )
        for i, name in enumerate(contrib.contributors):
            cid = slug(name)
            co = data['Contributor'].get(cid)
            if not co:
                co = data.add(common.Contributor, cid, id=cid, name=name)
            common.ContributionContributor(ord=i, contribution=c, contributor=co)

    methods = defaultdict(list)
    for method in ds.itermethods():
        m = data.add(
            models.Method,
            method.uid,
            id=slug(method.uid),
            name=method.label,
            code=method.code,
            parameter=method.parameter.strip(),
            reference_sample='; '.join([r.sample_name for r in method.references]),
            laboratory=method.laboratory,
            technique=method.technique,
            instrument=method.instrument,
        )
        methods[(m.code.lower(), m.parameter.lower())].append(m)

    # Add two Parameters: SOURCE and ARTEFACT
    data.add(common.Parameter, 'source', id='source', name='SOURCE')
    data.add(common.Parameter, 'artefact', id='artefact', name='ARTEFACT')

    # Add Samples and UnitParameters and Measurements
    missing_method = Counter()
    for sample, measurements in samples:
        if sample.id in data['Sample']:
            print('duplicate: POFATU ID: "{0.id}"'.format(sample))
            continue
        vsid = '{0}-{1}-{2}'.format(sample.category, sample.source_id, slug(sample.location.name))
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet, vsid,
                id=vsid,
                language=data['Location'][sample.location.name],
                parameter=data['Parameter'][sample.category.lower()],
                contribution=data['PofatuContribution'][sample.source_id],
            )
        v = data.add(
            models.Sample,
            sample.id,
            id=slug(sample.id, lowercase=False),
            name=sample.id,
            valueset=vs)
        DBSession.add(models.SampleReference(
            description='sample', sample=v, source=data['Source'][refkey(sample.source_id)]))

        for sid in sample.site.source_ids:
            DBSession.add(models.SampleReference(
                description='site', sample=v, source=data['Source'][refkey(sid)]))

        for sid in sample.artefact.source_ids:
            DBSession.add(models.SampleReference(
                description='artefact', sample=v, source=data['Source'][refkey(sid)]))

        for measurement, analysis in measurements:
            pid = slug(measurement.parameter, lowercase=False)
            p = data['Param'].get(pid)
            if not p:
                p = data.add(models.Param, pid, id=pid, name=measurement.parameter)
            data.add(
                models.Measurement, None,
                value=measurement.value,
                less=measurement.less,
                precision=measurement.precision,
                sample=v,
                unitparameter=p,
                method=data['Method'].get(measurement.method_uid),
            )
    return


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for p in DBSession.query(models.Param).options(joinedload(common.UnitParameter.values)):
        vals = [v.value for v in p.values]
        p.min = min(vals)
        p.max = max(vals)
        p.mean = mean(vals)
        p.median = median(vals)
        p.count_values = len(vals)


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
