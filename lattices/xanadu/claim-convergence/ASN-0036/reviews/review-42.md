# Contract Review — ASN-0036 (cycle 2)

*2026-04-13 14:13*

### S8-depth

- `MISSING_POSTCONDITION: V-position depth preservation — the proof explicitly establishes that both v+k and a+k have depth and prefix preservation via TumblerAdd's component-wise definition ("both v + k and a + k are ordinal displacements whose depth and prefix preservation follow from TumblerAdd's component-wise definition"), making (A k : 0 ≤ k < n : #(v + k) = #v) a proven result. The contract captures I-address depth preservation (postcondition 3) but has no parallel postcondition for V-positions.`

1 mismatches.
