import datetime

from timeutil import timerange


def test_timerange_contains_time():
    rng1 = timerange(datetime.time(8), datetime.time(12))
    rng2 = timerange(datetime.time(14), datetime.time(20))
    assert datetime.time(10, 30) in rng1
    assert datetime.time(10, 30) not in rng2


def test_timerange_contains_timerange():
    rng1 = timerange(datetime.time(11), datetime.time(12))
    rng2 = timerange(datetime.time(8), datetime.time(22))
    assert rng1 in rng2


def test_timerange_sum():
    rng1 = timerange(datetime.time(8), datetime.time(12))
    rng2 = timerange(datetime.time(14), datetime.time(20))
    sum_rng = rng1+rng2
    assert datetime.time(10, 30) in sum_rng
    assert datetime.time(18, 30) in sum_rng
    assert datetime.time(13) not in sum_rng


def test_timerange_empty_intersection():
    rng1 = timerange(datetime.time(8), datetime.time(12))
    rng2 = timerange(datetime.time(14), datetime.time(20))
    inter = rng1.intersection(rng2)
    assert inter.ranges == []


def test_timerange_good_intersection():
    rng1 = timerange(datetime.time(8), datetime.time(15))
    rng2 = timerange(datetime.time(11), datetime.time(20))
    inter1 = rng1.intersection(rng2)
    inter2 = rng2.intersection(rng1)
    assert datetime.time(11) in inter1
    assert datetime.time(11) in inter2
    assert datetime.time(10) not in inter1
    assert datetime.time(10) not in inter2
    assert datetime.time(16) not in inter1
    assert datetime.time(16) not in inter2


def test_timerange_complex_intersection():
    rng1 = timerange(datetime.time(8), datetime.time(12))
    rng2 = timerange(datetime.time(14), datetime.time(22))
    sum_rng = rng1+rng2
    rng3 = timerange(datetime.time(10), datetime.time(18))
    rng4 = timerange(datetime.time(20), datetime.time(23))
    scond_sum_rng = rng3 + rng4
    inter = sum_rng.intersection(scond_sum_rng)     # [10-12] + [14-18] + [20-22]
    assert datetime.time(11) in inter
    assert datetime.time(15) in inter
    assert datetime.time(17) in inter
    assert datetime.time(21) in inter
    assert datetime.time(9) not in inter
    assert datetime.time(13) not in inter
    assert datetime.time(19) not in inter
    assert datetime.time(23) not in inter


def test_timerange_tricky_intersection():
    rng1 = timerange(datetime.time(8), datetime.time(12))
    rng2 = timerange(datetime.time(12), datetime.time(22))
    inter = rng1.intersection(rng2)
    assert datetime.time(12) not in inter

# NOT IMPLEMENTED YET

def _test_difference():
    rng1 = timerange(datetime.time(8), datetime.time(20))
    rng2 = timerange(datetime.time(11), datetime.time(17))
    diff1 = rng1 - rng2
    diff2 = rng2 - rng1
    assert datetime.time(10) in diff1
    assert datetime.time(12) not in diff1
    assert datetime.time(16) not in diff1
    assert datetime.time(18) in diff1
    assert not diff2     # empty


def _test_complex_diff():
    rng1 = timerange(datetime.time(8), datetime.time(10), datetime.time(15), datetime.time(22))
    rng2 = timerange(datetime.time(10), datetime.time(17), datetime.time(21), datetime.time(23))
    diff1 = rng1 - rng2
    diff2 = rng2 - rng1
    assert datetime.time(9) in diff1
    assert datetime.time(10) in diff1
    assert datetime.time(13) not in diff1
    assert datetime.time(15) not in diff1
    assert datetime.time(16) not in diff1
    assert datetime.time(17) in diff1
    assert datetime.time(20) in diff1
    assert datetime.time(21) not in diff1
    assert datetime.time(22) not in diff1
    assert datetime.time(23) not in diff1

