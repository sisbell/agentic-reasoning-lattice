-- A3.range — RearrangeRangePreservation
-- range(Σ'.V(d)) = range(Σ.V(d))
-- A bijection preserves the multiset of values, hence the range (set of values).
-- Positions are 0-indexed to match Alloy seq convention.

sig Addr {}

sig Doc {
  slots: seq Addr
}

sig State {
  docs: set Doc
}

fun nd[d: Doc]: Int {
  #(d.slots)
}

-- Range of a document: the set of Addr values appearing in its slots
fun docRange[d: Doc]: set Addr {
  Int.(d.slots)
}

---------- Pivot sigma (m = 3) ----------

pred validPivotCuts[c1, c2, c3, n: Int] {
  0 =< c1
  c1 < c2
  c2 < c3
  c3 =< n
}

fun pivotSigma[c1, c2, c3, j: Int]: Int {
  (j >= c1 and j < c2) => plus[j, minus[c3, c2]]
    else ((j >= c2 and j < c3) => minus[j, minus[c2, c1]]
    else j)
}

---------- Swap sigma (m = 4) ----------

pred validSwapCuts[c1, c2, c3, c4, n: Int] {
  0 =< c1
  c1 < c2
  c2 < c3
  c3 < c4
  c4 =< n
}

fun swapSigma[c1, c2, c3, c4, j: Int]: Int {
  (j >= c1 and j < c2) => plus[j, minus[c4, c2]]
    else ((j >= c2 and j < c3) => plus[j, minus[minus[c4, c3], minus[c2, c1]]]
    else ((j >= c3 and j < c4) => minus[j, minus[c3, c1]]
    else j))
}

---------- Rearrange operations ----------

pred PivotRearrange[d, dPost: Doc, s: State, c1, c2, c3: Int] {
  d in s.docs
  validPivotCuts[c1, c2, c3, nd[d]]
  -- A3.perm: dPost.slots[σ(j)] = d.slots[j]
  all j: Int | j >= 0 and j < nd[d] implies
    dPost.slots[pivotSigma[c1, c2, c3, j]] = d.slots[j]
  -- frame: no slots outside range
  all i: Int | some dPost.slots[i] implies (i >= 0 and i < nd[d])
}

pred SwapRearrange[d, dPost: Doc, s: State, c1, c2, c3, c4: Int] {
  d in s.docs
  validSwapCuts[c1, c2, c3, c4, nd[d]]
  -- A3.perm: dPost.slots[σ(j)] = d.slots[j]
  all j: Int | j >= 0 and j < nd[d] implies
    dPost.slots[swapSigma[c1, c2, c3, c4, j]] = d.slots[j]
  -- frame: no slots outside range
  all i: Int | some dPost.slots[i] implies (i >= 0 and i < nd[d])
}

---------- Assertions ----------

-- Pivot rearrange preserves range of document values
assert PivotPreservesRange {
  all d, dPost: Doc, s: State, c1, c2, c3: Int |
    PivotRearrange[d, dPost, s, c1, c2, c3] implies
      docRange[dPost] = docRange[d]
}

-- Swap rearrange preserves range of document values
assert SwapPreservesRange {
  all d, dPost: Doc, s: State, c1, c2, c3, c4: Int |
    SwapRearrange[d, dPost, s, c1, c2, c3, c4] implies
      docRange[dPost] = docRange[d]
}

---------- Non-vacuity ----------

run FindPivotRange {
  some d, dPost: Doc, s: State, c1, c2, c3: Int |
    PivotRearrange[d, dPost, s, c1, c2, c3] and d.slots != dPost.slots
} for 4 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int

---------- Checks ----------

check PivotPreservesRange for 5 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int
check SwapPreservesRange for 5 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int
