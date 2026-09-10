from datetime import date

import pytest

from app.temporal_validation import Interval, overlaps, reject_overlapping_exclusive


def test_interval_contains_and_overlap():
    a = Interval(date(2025, 1, 1), date(2025, 6, 30))
    b = Interval(date(2025, 6, 1), None)
    assert overlaps(a, b)


def test_exclusive_overlap_is_rejected():
    with pytest.raises(ValueError):
        reject_overlapping_exclusive([Interval(date(2025, 1, 1), date(2025, 6, 30)), Interval(date(2025, 6, 1), None)])
