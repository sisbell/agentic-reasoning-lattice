-- A3.perm — RearrangePermutation
-- The pivot (m=3) and swap (m=4) sigma formulas define bijections
-- that correctly permute document values: Σ'.V(d)(σ(j)) = Σ.V(d)(j).
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

---------- Pivot sigma (m = 3) ----------

-- 0-indexed cuts: 0 ≤ c1 < c2 < c3 ≤ nd
pred validPivotCuts[c1, c2, c3, n: Int] {
  0 =< c1
  c1 < c2
  c2 < c3
  c3 =< n
}

fun pivotSigma[c1, c2, c3, j: Int]: Int {
  (j >= c1 and j < c2) => plus[j, minus[c3, c2]] else ((j >= c2 and j < c3) => minus[j, minus[c2, c1]] else j)
}

---------- Swap sigma (m = 4) ----------

-- 0-indexed cuts: 0 ≤ c1 < c2 < c3 < c4 ≤ nd
pred validSwapCuts[c1, c2, c3, c4, n: Int] {
  0 =< c1
  c1 < c2
  c2 < c3
  c3 < c4
  c4 =< n
}

fun swapSigma[c1, c2, c3, c4, j: Int]: Int {
  (j >= c1 and j < c2) => plus[j, minus[c4, c2]] else ((j >= c2 and j < c3) => plus[j, minus[minus[c4, c3], minus[c2, c1]]] else ((j >= c3 and j < c4) => minus[j, minus[c3, c1]] else j))
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

-- Pivot sigma maps {0..n-1} into itself injectively
assert PivotSigmaBijection {
  all c1, c2, c3, n: Int |
    validPivotCuts[c1, c2, c3, n] implies
      let P = {j: Int | j >= 0 and j < n} | {
        all j: P | pivotSigma[c1, c2, c3, j] in P
        all disj j1, j2: P |
          pivotSigma[c1, c2, c3, j1] != pivotSigma[c1, c2, c3, j2]
      }
}

-- Swap sigma maps {0..n-1} into itself injectively
assert SwapSigmaBijection {
  all c1, c2, c3, c4, n: Int |
    validSwapCuts[c1, c2, c3, c4, n] implies
      let P = {j: Int | j >= 0 and j < n} | {
        all j: P | swapSigma[c1, c2, c3, c4, j] in P
        all disj j1, j2: P |
          swapSigma[c1, c2, c3, c4, j1] != swapSigma[c1, c2, c3, c4, j2]
      }
}

-- Pivot rearrange preserves document length
assert PivotPreservesLength {
  all d, dPost: Doc, s: State, c1, c2, c3: Int |
    PivotRearrange[d, dPost, s, c1, c2, c3] implies nd[dPost] = nd[d]
}

-- Swap rearrange preserves document length
assert SwapPreservesLength {
  all d, dPost: Doc, s: State, c1, c2, c3, c4: Int |
    SwapRearrange[d, dPost, s, c1, c2, c3, c4] implies nd[dPost] = nd[d]
}

---------- Non-vacuity ----------

run FindPivot {
  some d, dPost: Doc, s: State, c1, c2, c3: Int |
    PivotRearrange[d, dPost, s, c1, c2, c3] and d.slots != dPost.slots
} for 4 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int

run FindSwap {
  some d, dPost: Doc, s: State, c1, c2, c3, c4: Int |
    SwapRearrange[d, dPost, s, c1, c2, c3, c4] and d.slots != dPost.slots
} for 4 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int

check PivotSigmaBijection for 5 but 5 Int
check SwapSigmaBijection for 5 but 5 Int
check PivotPreservesLength for 5 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int
check SwapPreservesLength for 5 but exactly 1 State, exactly 2 Doc, 4 seq, 5 Int
