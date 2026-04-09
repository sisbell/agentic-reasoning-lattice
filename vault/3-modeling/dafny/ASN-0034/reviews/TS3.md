# TS3 — Contract FLAG

*2026-04-09 09:06*

Frame condition not encoded as ensures clause

The formal contract specifies:
  *Frame:* #shift(shift(v, n₁), n₂) = #v = m (shift preserves tumbler length)

The Dafny code has:
  ensures OS.OrdinalShift(OS.OrdinalShift(v, n1), n2) == OS.OrdinalShift(v, n1 + n2)
  (no frame ensures)

Missing:
  The frame `#shift(shift(v, n₁), n₂) = #v` must be encoded as an `ensures` clause, e.g.:
  `ensures |OS.OrdinalShift(OS.OrdinalShift(v, n1), n2)| == |v|`
