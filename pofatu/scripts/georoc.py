# coding: utf8
from __future__ import unicode_literals, print_function, division

from csvw.dsv import reader


def iter_samples(d):
    for p in d.iterdir():
        for sample in reader(p, dicts=True, encoding='latin1'):
            if sample.get('LAND OR SEA') == 'SAE':
                # only consider samples from above sea level
                try:
                    assert sample['LATITUDE MIN'] and sample['LONGITUDE MIN']
                    yield p.name, sample['SAMPLE NAME'], sample['LOCATION'], sample['TECTONIC SETTING'], float(sample['LATITUDE MIN']), float(sample['LONGITUDE MIN'])
                except (KeyError, AssertionError):
                    pass
