from __future__ import unicode_literals
import sys
import re
from itertools import groupby
from collections import Counter

from six import text_type

from clld.scripts.util import initializedb, Data, bibtex2source
from clld.lib import bibtex
from clld.db.meta import DBSession
from clld.db.models import common
from csvw.dsv import reader
from clldutils.misc import slug
from pypofatu.dataset import Dataset

import pofatu
from pofatu import models
from pofatu.scripts import georoc


def refkey(s):
    return {
        'kahn-2008-nzja': 'kahn-2009-nzja',
        'metraux-1940-ethnology': 'metraux-1940-easter',
        'mcalister-2011-phd': 'mcalister-2011-nukuhiva',
        'weisler 1993 phd': 'weisler-1993-phd',
    }.get(s.lower(), s.lower())


def main(args):
    data = Data()
    ds = Dataset()

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

    # load sources from bibtex!
    for rec in bibtex.Database.from_file(ds.bib):
        data.add(common.Source, rec.id.replace('_', '-').lower(), _obj=bibtex2source(rec, lowercase_id=False))

    samples = list(ds.iterdata())
    for sample in samples:
        loc = sample.location
        if loc.name not in data['Location']:
            data.add(
                models.Location,
                loc.name,
                id=slug(loc.name),
                name=loc.name,
                loc1=loc.loc1,
                loc2=loc.loc2,
                loc3=loc.loc3,
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
            source=data['Source'][contrib.id.lower()],
        )
        for i, name in enumerate(contrib.contributors):
            cid = slug(name)
            co = data['Contributor'].get(cid)
            if not co:
                co = data.add(common.Contributor, cid, id=cid, name=name)
            common.ContributionContributor(ord=i, contribution=c, contributor=co)

    for method in ds.itermethods():
        data.add(
            models.Method,
            method.label.lower().replace('plosone', 'po'),
            id=slug(method.label),
            name=method.label,
            laboratory=method.laboratory,
            technique=method.technique,
            instrument=method.instrument,
        )

    # Add two Parameters: SOURCE and ARTEFACT
    data.add(common.Parameter, 'source', id='source', name='SOURCE')
    data.add(common.Parameter, 'artefact', id='artefact', name='ARTEFACT')

    # Add Samples and UnitParameters and Measurements
    missing_method = Counter()
    for sample in samples:
        if sample.uid in data['Sample']:
            print('duplicate: POFATU ID: "{0.id}", Method code: "{0.method_id}"'.format(sample))
            continue
        vsid = '{0}-{1}-{2}'.format(sample.category, sample.sample.source_id, slug(sample.location.name))
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet, vsid,
                id=vsid,
                language=data['Location'][sample.location.name],
                parameter=data['Parameter'][sample.category.lower()],
                contribution=data['PofatuContribution'][sample.sample.source_id],
            )
        v = data.add(models.Sample, sample.uid, id=slug(sample.uid), name=sample.uid, valueset=vs)
        DBSession.add(models.SampleReference(
            description='sample', sample=v, source=data['Source'][sample.sample.source_id.lower()]))

        for sid in sample.site.source_ids:
            DBSession.add(models.SampleReference(
                description='site', sample=v, source=data['Source'][refkey(sid)]))

        for sid in sample.artefact.source_ids:
            DBSession.add(models.SampleReference(
                description='artefact', sample=v, source=data['Source'][refkey(sid)]))

        for i, (k, val) in enumerate(sample.data.items(), start=1):
            val, less, precision = val
            if val is not None:
                pid = '{0}-{1}'.format(slug(k, lowercase=False), i)
                p = data['UnitParameter'].get(pid)
                if not p:
                    p = data.add(common.UnitParameter, pid, id=pid, name=k)
                mid = '{0} {1}'.format(sample.method_id, k.split()[0]).lower()
                m = data['Method'].get(mid)
                if not m:
                    missing_method.update([mid])
                else:
                    models.Measurement(
                        value=val,
                        less=less,
                        precision=precision,
                        sample=v,
                        unitparameter=p,
                        method=m,
                    )
    for k, v in missing_method.most_common(20):
        print(k, v)
    return





    seen = set()
    for item in sorted(reader(args.data_file('Pofatu-180518-refs.csv'), dicts=True), key=lambda i: i['SHORT CITATION']):
        res = re.split(',\s*([0-9]{4})\.\s*', item['COMPLETE CITATION'], 1)
        if len(res) == 3:
            kw = dict(author=res[0], year=res[1], title=res[2])
        else:
            kw = dict(description=res[0])
        id_ = slug(item['SHORT CITATION'])
        if id_ not in seen:
            data.add(
                common.Source,
                item['SHORT CITATION'],
                id=id_,
                name=item['SHORT CITATION'],
                **kw)
            seen.add(id_)

    items = list(reader(args.data_file('Pofatu-180518.csv'), dicts=True))
    for i, row in enumerate(items):
        row = {k: v.strip() for k, v in row.items()}
        if not row['LATITUDE_(DD)']:
            continue
        if row['SAMPLE_CATEGORY'] == 'ARTEFACT':
            art = models.Artefact(
                id='{0}'.format(i + 1),
                name=row['SAMPLE_NAME'],
                latitude=row['LATITUDE_(DD)'],
                longitude=row['LONGITUDE_(DD)'],
                site_context=row['SITE_CONTEXT'] if row['SITE_CONTEXT'] not in ['', 'NA', 'MISSING'] else None,
                site_name=row['SITE_NAME'] if row['SITE_NAME'] not in ['', 'NA', 'MISSING'] else None,
                type=row['ARTEFACT_TYPE_']
            )
            DBSession.add(art)
            if row['CITATION[ANALYSIS]'] in data['Source']:
                art.source = data['Source'][row['CITATION[ANALYSIS]']]
        elif row['SAMPLE_CATEGORY'] == 'SOURCE':
            src = models.RockSource(
                id='pofatu-{0}'.format(i + 1),
                name=row['SAMPLE_NAME'],
                latitude=row['LATITUDE_(DD)'],
                longitude=row['LONGITUDE_(DD)'],
                tectonic_setting=row['TECTONIC_SETTING'],
                location='{0} / {1}'.format(row['LOCATION1_(ARCHIPELAGO)'], row['LOCATION2_(ISLAND)']),
                type='POFATU',
            )
            DBSession.add(src)

    s, bins = set(), set()
    for p, n, l, t, lat, lon in georoc.iter_samples(args.data_file('..', '..', 'georoc', 'csv')):
        if abs(lat) > 90 or abs(lon) > 180:
            # ignore malformed coordinates
            print(p, n, lat, lon)
            continue
        if (-40 < lat < 30) and (lon > 160 or lon < -110) and not (lat > 20 and -130 < lon < -110):
            # ignore non-pacific island samples
            key = (l, round(lat, 2), round(lon, 2))
            # only include one sample per location and roughly-equal coordinate
            if key not in bins:
                s.add((n, l, t, lat, lon))
                bins.add(key)

    for i, (name, location, tectonic_setting, lat, lon) in enumerate(sorted(s)):
        src = models.RockSource(
            id='georoc-{0}'.format(i + 1),
            name=name,
            latitude=lat,
            longitude=lon,
            tectonic_setting=tectonic_setting,
            location=location,
            type='GEOROC',
        )
        DBSession.add(src)
    print(len(s))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
