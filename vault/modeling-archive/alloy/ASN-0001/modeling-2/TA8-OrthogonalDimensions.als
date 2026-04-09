-- TA8 — OrthogonalDimensions
-- 2D enfilade displacement operations are component-wise:
-- V and I dimensions are independent; no cross-dimensional coupling.

sig Tumbler {}

-- 2D Displacement: independent V-tumbler and I-tumbler
sig Disp2D {
  v: one Tumbler,
  i: one Tumbler
}

-- Abstract tumbler binary operations modeled as total functions.
-- The solver explores all valid function assignments.
one sig Ops {
  tadd: Tumbler -> Tumbler -> Tumbler,
  tmin: Tumbler -> Tumbler -> Tumbler
}

fact TaddIsTotal {
  all a, b: Tumbler | one Ops.tadd[a][b]
}

fact TminIsTotal {
  all a, b: Tumbler | one Ops.tmin[a][b]
}

-- 2D add: component-wise application of tumbler addition
pred add2D[a, b, r: Disp2D] {
  r.v = Ops.tadd[a.v][b.v]
  r.i = Ops.tadd[a.i][b.i]
}

-- 2D min: component-wise application of tumbler min
pred min2D[a, b, r: Disp2D] {
  r.v = Ops.tmin[a.v][b.v]
  r.i = Ops.tmin[a.i][b.i]
}

-- ORTHOGONALITY: V-result of add depends only on V-inputs
assert AddVOrthogonal {
  all a1, b1, r1, a2, b2, r2: Disp2D |
    (add2D[a1, b1, r1] and add2D[a2, b2, r2]
     and a1.v = a2.v and b1.v = b2.v)
    implies r1.v = r2.v
}

-- ORTHOGONALITY: I-result of add depends only on I-inputs
assert AddIOrthogonal {
  all a1, b1, r1, a2, b2, r2: Disp2D |
    (add2D[a1, b1, r1] and add2D[a2, b2, r2]
     and a1.i = a2.i and b1.i = b2.i)
    implies r1.i = r2.i
}

-- ORTHOGONALITY: V-result of min depends only on V-inputs
assert MinVOrthogonal {
  all a1, b1, r1, a2, b2, r2: Disp2D |
    (min2D[a1, b1, r1] and min2D[a2, b2, r2]
     and a1.v = a2.v and b1.v = b2.v)
    implies r1.v = r2.v
}

-- ORTHOGONALITY: I-result of min depends only on I-inputs
assert MinIOrthogonal {
  all a1, b1, r1, a2, b2, r2: Disp2D |
    (min2D[a1, b1, r1] and min2D[a2, b2, r2]
     and a1.i = a2.i and b1.i = b2.i)
    implies r1.i = r2.i
}

-- DETERMINISM: same inputs to add2D yield same result
assert AddDeterministic {
  all a, b, r1, r2: Disp2D |
    (add2D[a, b, r1] and add2D[a, b, r2])
    implies (r1.v = r2.v and r1.i = r2.i)
}

-- DETERMINISM: same inputs to min2D yield same result
assert MinDeterministic {
  all a, b, r1, r2: Disp2D |
    (min2D[a, b, r1] and min2D[a, b, r2])
    implies (r1.v = r2.v and r1.i = r2.i)
}

-- Non-vacuity: a valid add2D triple exists
run FindAdd {
  some disj a, b, r: Disp2D | add2D[a, b, r]
} for 4 but exactly 3 Disp2D, exactly 3 Tumbler

-- Non-vacuity: a valid min2D triple exists
run FindMin {
  some disj a, b, r: Disp2D | min2D[a, b, r]
} for 4 but exactly 3 Disp2D, exactly 3 Tumbler

check AddVOrthogonal for 5
check AddIOrthogonal for 5
check MinVOrthogonal for 5
check MinIOrthogonal for 5
check AddDeterministic for 5
check MinDeterministic for 5
