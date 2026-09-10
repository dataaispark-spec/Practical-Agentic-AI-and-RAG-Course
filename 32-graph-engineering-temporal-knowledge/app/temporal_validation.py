from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Interval:
    valid_from: date
    valid_to: date | None = None

    def contains(self, when: date) -> bool:
        return self.valid_from <= when and (self.valid_to is None or when <= self.valid_to)


def overlaps(a: Interval, b: Interval) -> bool:
    a_end = a.valid_to or date.max
    b_end = b.valid_to or date.max
    return a.valid_from <= b_end and b.valid_from <= a_end


def validate_interval(interval: Interval) -> None:
    if interval.valid_to is not None and interval.valid_to < interval.valid_from:
        raise ValueError("valid_to cannot precede valid_from")


def reject_overlapping_exclusive(intervals: list[Interval]) -> None:
    for i, left in enumerate(intervals):
        validate_interval(left)
        for right in intervals[i + 1 :]:
            validate_interval(right)
            if overlaps(left, right):
                raise ValueError("overlapping exclusive validity intervals")
