__author__ = "Dominik Kozaczko"
__all__ = ['timerange']


import datetime


"""
Module for time calculations - mostly for time spans calculations
"""


class TimeFrame(object):
    """Helper object acting as uninterrupted timeframe. Supposed only for internal use in TimeRange class."""
    def __init__(self, start, end):
        assert isinstance(start, datetime.time), "Wrong data type for start"
        assert isinstance(end, datetime.time), "Wrong data type for end"
        assert start <= end, "Please split it"
        self.start = start
        self.end = end

    def __repr__(self):
        return "[%s - %s]" % self.start, self.end

    def __contains__(self, item):
        if isinstance(item, datetime.time):
            return self.start <= item <= self.end
        elif isinstance(item, TimeFrame):
            return self.start >= item.start and self.end >= item.end
        else:
            raise TypeError("Unsupported type: %s" % type(item))

    def __add__(self, other):
        if self.joinable(other):
            return TimeFrame(min(self.start, other.start), max(self.end, other.end))
        raise ValueError("TimeFrames not joinable")

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def joinable(self, other):
        return self.start in other or self.end in other or other.start in self or other.end in self


class TimeRange(object):
    def __init__(self, *args):
        self.ranges = []
        if args:
            if len(args) == 1 and isinstance(args[0], TimeFrame):
                self.ranges.append(args[0])
            elif len(args) % 2 == 0:
                for i, v in enumerate(args[::2]):
                    self.ranges.append(TimeFrame(v, args[2*i+1]))
            else:
                raise AttributeError("Wrong input attributes")

    def __add__(self, other):
        obj = TimeRange()
        obj.ranges = self.ranges + other.ranges
        obj._optimize()
        return obj

    def __contains__(self, item):
        if not isinstance(item, (TimeRange, TimeFrame, datetime.time)):
            raise TypeError("Unsuppoted type: %s" % type(item))
        if isinstance(item, (TimeFrame, datetime.time)):
            for frame in self:
                if item in frame:
                    return True
            return False
        else:
            for frame in item:
                if frame not in self:
                    return False
            return True

    def __iter__(self):
        return iter(self.ranges)

    def __repr__(self):
        return repr(self.ranges)

    def __sub__(self, other):
        obj = TimeRange()
        result = []
        for their in other:
            for mine in self:
                if not mine.joinable(their):
                    continue
                if mine.start <= their.start:
                    start = mine.start
                    end = their.start
                    if start != end:
                        result.append(TimeFrame(start, end))
                if mine.end >= their.end:
                    start = their.end
                    end = mine.end
                    if start != end:
                        result.append(TimeFrame(start, end))
        obj.ranges = result
        obj._optimize()
        return obj

    def __and__(self, other):
        return self.intersection(other)

    def __or__(self, other):
        return self + other

    def __len__(self):
        return len(self.ranges)

    def difference(self, other):
        return self - other

    def intersection(self, other):
        obj = TimeRange()
        result = []
        for their in other:
            for mine in self:
                if not their.joinable(mine):
                    continue
                start, end = max(their.start, mine.start), min(their.end, mine.end)
                if start != end:
                    result.append(TimeFrame(start, end))
        obj.ranges = result
        obj._optimize()
        return obj

    def isdisjoint(self, other):
        return not (self and other)

    def issubset(self, other):
        return self in other

    def issuperset(self, other):
        return other in self

    def symmetric_difference(self, other):
        (self + other) - self.intersection(other)

    def union(self, other):
        return self + other

    def _optimize(self):
        changed = True
        while changed:
            result = []
            changed = False
            while self.ranges:
                orig = self.ranges.pop()
                for i, frame in enumerate(result):
                    try:
                        result[i] += orig
                        changed = True
                        break
                    except ValueError:
                        continue
                else:
                    result.append(orig)
            self.ranges = result


timerange = TimeRange
