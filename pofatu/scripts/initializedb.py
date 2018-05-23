from __future__ import unicode_literals
import sys
import re
from itertools import groupby

from six import text_type

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from xlrd import open_workbook
from csvw.dsv import reader
from clldutils.misc import slug

import pofatu
from pofatu import models
from pofatu.scripts import georoc


def val(cell, col):
    v = cell.value
    if isinstance(v, text_type):
        v = v.strip()
    if v == 'NA':
        v = None
    if col in ['LATITUDE (DD)', 'LONGITUDE (DD)']:
        v = float(v) if v is not None else v
    return v


def main(args):
    data = Data()

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

    """
1    CITATION[ANALYSIS],
2    TECTONIC_SETTING,
3    LOCATION1_(ARCHIPELAGO),
4    LOCATION2_(ISLAND),
5    LOCATION3_(LOCALITY),
6    LOCATION_COMMENT,
7    LATITUDE_(DD),
8    LONGITUDE_(DD),
9    ALTITUDE_(M),
->10    SAMPLE_NAME,
11    SAMPLE_CATEGORY,
12    COLLECTION_ORIGIN,
13    SAMPLE_COMMENT,
14    ARTEFACT_NAME,
->15    ARTEFACT_TYPE_,
16    ARTEFACT_COMMENTS,
17    PLACE_OF_CONSERVATION,
->18    SITE_NAME,
->19    SITE_CONTEXT,
    SITE_COMMENTS,
    CITATION[SITE],DEPTH_BELOW_SURFACE,LEVEL_LABEL,ASSOCIATED_FEATURE
    
    
    """
    # duplicate columns:
    #--> CO2
    #--> F
    #--> S
    #--> CL

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
