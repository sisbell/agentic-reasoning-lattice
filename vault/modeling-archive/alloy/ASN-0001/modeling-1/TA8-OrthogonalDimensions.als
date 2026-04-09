-- TA8 — OrthogonalDimensions
-- V-displacements and I-displacements are combined independently.
-- No operation mixes a V-value with an I-value.
--
-- Checks: for both add and min, the V-component of the result
-- depends only on V-inputs, and the I-component only on I-inputs.

sig Tumbler {}

-- Abstract 1D operations: total binary functions on Tumbler.
one sig Ops {
  tAdd: Tumbler -> Tumbler -> Tumbler,
  tMin: Tumbler -> Tumbler -> Tumbler
}

fact TotalFunctions {
  all a, b: Tumbler | one Ops.tAdd[a][b]
  all a, b: Tumbler | one Ops.tMin[a][b]
}

-- 2D displacement: a pair of independent tumblers.
sig Displacement {
  v: Tumbler,
  i: Tumbler
}

-- 2D add: component-wise 1D add.
pred add2D[d1, d2, r: Displacement] {
  r.v = Ops.tAdd[d1.v][d2.v]
  r.i = Ops.tAdd[d1.i][d2.i]
}

-- 2D min: component-wise 1D min.
pred min2D[d1, d2, r: Displacement] {
  r.v = Ops.tMin[d1.v][d2.v]
  r.i = Ops.tMin[d1.i][d2.i]
}

-- V-result of add depends only on V-inputs (not on I-inputs).
-- Two invocations with matching V-inputs must yield matching V-outputs.
assert OrthogonalAdd_V {
  all d1, d2, d1b, d2b, r, rb: Displacement |
    (add2D[d1, d2, r] and add2D[d1b, d2b, rb] and d1.v = d1b.v and d2.v = d2b.v)
    implies r.v = rb.v
}

-- I-result of add depends only on I-inputs (not on V-inputs).
assert OrthogonalAdd_I {
  all d1, d2, d1b, d2b, r, rb: Displacement |
    (add2D[d1, d2, r] and add2D[d1b, d2b, rb] and d1.i = d1b.i and d2.i = d2b.i)
    implies r.i = rb.i
}

-- V-result of min depends only on V-inputs.
assert OrthogonalMin_V {
  all d1, d2, d1b, d2b, r, rb: Displacement |
    (min2D[d1, d2, r] and min2D[d1b, d2b, rb] and d1.v = d1b.v and d2.v = d2b.v)
    implies r.v = rb.v
}

-- I-result of min depends only on I-inputs.
assert OrthogonalMin_I {
  all d1, d2, d1b, d2b, r, rb: Displacement |
    (min2D[d1, d2, r] and min2D[d1b, d2b, rb] and d1.i = d1b.i and d2.i = d2b.i)
    implies r.i = rb.i
}

-- Non-vacuity: both operations are satisfiable with distinct inputs and result.
run NonVacuous {
  some disj d1, d2, r: Displacement |
    add2D[d1, d2, r] and
    some r2: Displacement | min2D[d1, d2, r2]
} for 5 but exactly 4 Displacement, exactly 3 Tumbler

check OrthogonalAdd_V for 5 but exactly 4 Displacement, exactly 3 Tumbler
check OrthogonalAdd_I for 5 but exactly 4 Displacement, exactly 3 Tumbler
check OrthogonalMin_V for 5 but exactly 4 Displacement, exactly 3 Tumbler
check OrthogonalMin_I for 5 but exactly 4 Displacement, exactly 3 Tumbler
