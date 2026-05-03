"""Tumbler addresses and the inc() operator.

ASN-0034 T0 fixes the carrier (sequences of ℕ); T4 stratifies addresses
by zero-count (node/user/document/element); TA5 defines inc(t, k):

  inc(t, 0): increment the last position by 1 (length unchanged)
  inc(t, 1): append .1                         (length + 1)
  inc(t, 2): append .0.1                       (length + 2)

For k ≥ 3, inc would require multiple zero separators in succession,
which T4 forbids; the allocator (T10a) restricts callers to k ∈ {0,1,2}.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple


@dataclass(frozen=True)
class Address:
    digits: Tuple[int, ...]

    def __init__(self, source):
        if isinstance(source, str):
            digits = tuple(int(d) for d in source.split("."))
        elif isinstance(source, Address):
            digits = source.digits
        else:
            digits = tuple(int(d) for d in source)
        for d in digits:
            if d < 0:
                raise ValueError(f"tumbler digits must be ≥ 0, got {digits}")
        object.__setattr__(self, "digits", digits)

    def __str__(self) -> str:
        return ".".join(str(d) for d in self.digits)

    def __repr__(self) -> str:
        return f"Address({str(self)!r})"

    def __len__(self) -> int:
        return len(self.digits)

    def __iter__(self) -> Iterable[int]:
        return iter(self.digits)

    def zeros(self) -> int:
        """Zero-count from T4 — determines address kind via T4c."""
        return sum(1 for d in self.digits if d == 0)

    def has_prefix(self, other: "Address") -> bool:
        """VER3-style prefix check: does `other` precede self in the tumbler?"""
        return (
            len(other) < len(self)
            and self.digits[: len(other)] == other.digits
        )

    def split(self) -> Tuple["Address", "Address"]:
        """Nelson's Address.split: cut at the last zero into (docid, local).

        For an element-level address (zeros=3), the docid is the
        homedoc and the local part is the in-doc address. For a
        doc-level address (zeros=2), the docid is the user prefix and
        the local part is the doc-field portion. Etc.
        """
        if not self.digits:
            raise ValueError("cannot split empty tumbler")
        delim = len(self.digits) - 1
        while delim >= 0 and self.digits[delim] != 0:
            delim -= 1
        if delim < 0:
            raise ValueError(f"{self} has no zero separator to split on")
        return (
            Address(self.digits[:delim]),
            Address(self.digits[delim + 1:]),
        )


def inc(t: Address, k: int) -> Address:
    """TA5: HierarchicalIncrement.

    Length increases by exactly k (TA5(d)). For k > 0, the appended
    suffix is (k−1) zeros followed by a 1, which preserves the
    field-segment constraint when the input is T4-valid.
    """
    if k == 0:
        if not t.digits:
            raise ValueError("cannot inc(·, 0) on empty tumbler")
        return Address(t.digits[:-1] + (t.digits[-1] + 1,))
    if k < 0:
        raise ValueError(f"k must be ≥ 0, got {k}")
    suffix = (0,) * (k - 1) + (1,)
    return Address(t.digits + suffix)
