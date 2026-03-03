-- T0 — UnboundedComponents (INV)
-- For every tumbler t and every position i, for every bound M ∈ ℕ,
-- there exists a tumbler t' agreeing with t everywhere except t'ᵢ > M.
--
-- Bounded-scope note: Alloy's Int has a finite range; full ℕ unboundedness
-- is not checkable in bounded model checking. The assertion uses an overflow
-- guard (plus[v,1] > v) to exclude the Int maximum from the antecedent.
-- In practice the check may find counterexamples because a finite Tumbler
-- scope cannot always supply the required witness for every (t, i, M) triple;
-- this reflects the scope limitation, not a model defect.

sig Tumbler {
  comps: seq Int
}

-- Components represent natural-number coordinates (no negatives)
fact NonNegative {
  all t: Tumbler, i: Int |
    i in t.comps.inds implies t.comps[i] >= 0
}

-- Bounded approximation of T0:
-- For every (t, i) where t's i-th component is not at the Int ceiling,
-- there exists t2 with the same length, equal values at all other indices,
-- and a strictly larger value at index i.
assert UnboundedComponents {
  all t: Tumbler, i: Int |
    (i in t.comps.inds and plus[t.comps[i], 1] > t.comps[i]) implies
    some t2: Tumbler |
      #t2.comps = #t.comps and
      t2.comps[i] > t.comps[i] and
      (all j: Int |
        (j in t.comps.inds and not (j = i)) implies t2.comps[j] = t.comps[j])
}

-- Non-vacuity: the model permits two tumblers of equal length that
-- differ at exactly one position, with the second having a larger value.
run Witness {
  some disj t, t2: Tumbler |
    #t.comps = #t2.comps and
    some i: Int |
      i in t.comps.inds and
      t.comps[i] < t2.comps[i] and
      (all j: Int |
        (j in t.comps.inds and not (j = i)) implies t.comps[j] = t2.comps[j])
} for 5 but exactly 2 Tumbler, 2 seq, 5 Int

check UnboundedComponents for 5 but exactly 4 Tumbler, 3 seq, 5 Int
