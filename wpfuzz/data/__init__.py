from . import basic, fixkeys, fixdata, large


def get_known_fuzzdata():
    return {
        'basic': basic.Fuzzdata,
        'fixkey': fixkeys.Fuzzdata,
        'fixdata': fixdata.Fuzzdata,
        'largekey': large.KeyFuzzdata,
        'largedata': large.ValueFuzzdata,
    }
