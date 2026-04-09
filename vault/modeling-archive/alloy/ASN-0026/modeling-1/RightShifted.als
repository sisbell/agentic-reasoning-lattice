-- P9 (right) — RightShifted (FRAME, ensures)
-- (A j : p <= j <= n_d : Sigma'.V(d)(j + k) = Sigma.V(d)(j))
--
-- After inserting k elements at position p in a document,
-- every original position j in [p..n_d] appears at j+k in the new state.

sig Addr {}

-- Single-document v-space: position -> address
sig State {
    vmap: Int -> lone Addr
}

-- Document length = number of mapped positions
fun docLen[s: State]: Int {
    #(s.vmap)
}

-- V-space is a dense interval [1..n]
pred wellFormed[s: State] {
    all i: Int | some s.vmap[i] iff (i >= 1 and i =< docLen[s])
}

-- P9 right: positions p..n_d shift right by k
pred rightShifted[s, sPost: State, p, k: Int] {
    all j: Int | (j >= p and j =< docLen[s]) implies
        sPost.vmap[plus[j, k]] = s.vmap[j]
}

-- Left frame: positions 1..p-1 unchanged
pred leftUnchanged[s, sPost: State, p: Int] {
    all j: Int | (j >= 1 and j < p) implies
        sPost.vmap[j] = s.vmap[j]
}

-- Insert operation: insert k elements at position p
pred Insert[s, sPost: State, p, k: Int] {
    wellFormed[s]
    wellFormed[sPost]
    k >= 1
    p >= 1
    p =< plus[docLen[s], 1]
    docLen[sPost] = plus[docLen[s], k]
    leftUnchanged[s, sPost, p]
    rightShifted[s, sPost, p, k]
}

-- Derived property: every address in the old state survives in the new state.
-- Follows from leftUnchanged (covers 1..p-1) and rightShifted (covers p..n_d).
assert InsertPreservesRefs {
    all s, sPost: State, p, k: Int |
        Insert[s, sPost, p, k] implies
            (all a: Addr | a in Int.(s.vmap) implies a in Int.(sPost.vmap))
}

-- Non-vacuity: can we find a valid Insert?
run FindInsert {
    some s, sPost: State, p, k: Int |
        Insert[s, sPost, p, k]
} for 5 but exactly 2 State, 5 Int

check InsertPreservesRefs for 5 but exactly 2 State, 5 Int
