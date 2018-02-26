from __future__ import unicode_literals
import sys
from itertools import groupby

from six import text_type

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from xlrd import open_workbook
from clldutils.misc import nfilter

import pofatu
from pofatu import models


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

    wb = open_workbook(args.data_file('POFATU DB 220218.xlsx').as_posix())
    sheet = wb.sheet_by_name('POFATU Values')

    """
    CITATION [ANALYSIS]
    TECTONIC SETTING
    LOCATION
    LOCATION COMMENT
    LATITUDE (DD)
    LONGITUDE (DD)
    ALTITUDE (M)
    COLLECTION ORIGIN
    SAMPLE TYPE
    SAMPLE NAME
    SAMPLE COMMENT
    ARTEFACT NAME
    ARTEFACT TYPE 
    ARTEFACT COMMENTS
    SITE NAME
    SITE CONTEXT
    SITE COMMENTS
    CITATION [SITE]
    DEPTH BELOW SURFACE
    LEVEL LABEL
    ASSOCIATED FEATURE
    CRA YEARS BP
    CAL DATE
    CITATION [DATE]
    PLACE OF CONSERVATION
    TEXTURE
    MINERALS
    ROCK TYPE
    COMMENTS
    """
    # duplicate columns:
    #--> CO2
    #--> F
    #--> S
    #--> CL

    cols = []
    for i in range(sheet.ncols):
        cname = sheet.cell(1, i).value
        #if cname in cols:
        #    print('--> %s' % cname)
        cols.append(cname)

    for col in cols:
        print(col)

    rows = []
    for i in range(sheet.nrows):
        if i < 2:
            continue
        rows.append(dict(zip(cols, [val(sheet.cell(i, j), cols[j]) for j in range(sheet.ncols)])))

    def key(r):
        return r['SITE NAME'], r['CITATION [SITE]']

    i = 0
    for site, samples in groupby(sorted(rows, key=key), key):
        i += 1
        samples = list(samples)
        site = models.Site(id='s{0}'.format(i), name='{0} {1}'.format(*site))
        latitudes = nfilter(s['LATITUDE (DD)'] for s in samples)
        longitudes = nfilter(s['LONGITUDE (DD)'] for s in samples)
        site.latitude = sum(latitudes) / len(latitudes)
        site.longitude = sum(longitudes) / len(longitudes)
        DBSession.add(site)

        for j, sample in enumerate(samples):
            name = sample['SAMPLE NAME']
            if sample['ARTEFACT NAME']:
                name += ' {0}'.format(sample['ARTEFACT NAME'])
            DBSession.add(models.Sample(
                id='{0}-{1}'.format(i, j + 1),  # sample['UNIQUE_ID'],
                name=name,
                type=sample['SAMPLE TYPE'],
                latitude=sample['LATITUDE (DD)'],
                longitude=sample['LONGITUDE (DD)'],
                language=site,
                rock_type=sample['ROCK TYPE'] if sample['ROCK TYPE'] != 'NA' else None,
                tectonic_setting=sample['TECTONIC SETTING'],
                location=sample['LOCATION'],
            ))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
