-- A7.corollary — FullRestoration
-- After DELETE(d, p, k) then a restoring COPY back into d at p,
-- the entire document d is restored: Sigma_2.V(d) = Sigma_0.V(d).
-- Sub-parts: left frame, restored positions, right frame, length.

open util/integer

sig Addr {}
sig Doc {}

sig State {
    V: Doc -> Int -> lone Addr,
    len: Doc -> one Int
}

pred wellFormed[s: State] {
    all d: Doc {
        s.len[d] >= 1
        all j: Int | (j >= 1 and j =< s.len[d]) implies one s.V[d][j]
        all j: Int | (j < 1 or j > s.len[d]) implies no s.V[d][j]
    }
}

-- DELETE: remove k elements starting at position p from document d
pred Delete[s0, s1: State, d: Doc, p, k: Int] {
    k >= 1
    p >= 1
    plus[p, minus[k, 1]] =< s0.len[d]

    s1.len[d] = minus[s0.len[d], k]

    -- left frame: positions 1..p-1 unchanged
    all j: Int | (j >= 1 and j < p) implies
        s1.V[d][j] = s0.V[d][j]

    -- shift: positions p..new_len come from p+k..old_len
    all j: Int | (j >= p and j =< s1.len[d]) implies
        s1.V[d][j] = s0.V[d][plus[j, k]]

    -- nothing outside new range
    all j: Int | (j < 1 or j > s1.len[d]) implies
        no s1.V[d][j]

    -- other documents unchanged
    all d2: Doc - d {
        s1.len[d2] = s0.len[d2]
        s1.V[d2] = s0.V[d2]
    }
}

-- COPY: insert k elements from source doc ds at position ps
-- into target doc dt at position pt
pred Copy[s0, s1: State, ds: Doc, ps, k: Int, dt: Doc, pt: Int] {
    k >= 1
    ps >= 1
    plus[ps, minus[k, 1]] =< s0.len[ds]
    pt >= 1
    pt =< plus[s0.len[dt], 1]

    s1.len[dt] = plus[s0.len[dt], k]

    -- left frame: positions 1..pt-1 unchanged
    all j: Int | (j >= 1 and j < pt) implies
        s1.V[dt][j] = s0.V[dt][j]

    -- copied span: dt[pt+j] = ds[ps+j] for j in 0..k-1
    all j: Int | (j >= 0 and j < k) implies
        s1.V[dt][plus[pt, j]] = s0.V[ds][plus[ps, j]]

    -- right shift: old positions pt..old_len shift up by k
    all j: Int | (j >= pt and j =< s0.len[dt]) implies
        s1.V[dt][plus[j, k]] = s0.V[dt][j]

    -- nothing outside new range
    all j: Int | (j < 1 or j > s1.len[dt]) implies
        no s1.V[dt][j]

    -- other documents unchanged
    all d2: Doc - dt {
        s1.len[d2] = s0.len[d2]
        s1.V[d2] = s0.V[d2]
    }
}

-- A7 setup: Delete from d, then copy back from d' which holds
-- the deleted addresses, restoring d fully.
pred A7Setup[s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int] {
    wellFormed[s0]
    Delete[s0, s1, d, p, k]

    -- d' holds the deleted addresses at positions q..q+k-1 in s1
    q >= 1
    plus[q, minus[k, 1]] =< s1.len[dPrime]
    all j: Int | (j >= 0 and j < k) implies
        s1.V[dPrime][plus[q, j]] = s0.V[d][plus[p, j]]

    -- restoring copy: copy from d'[q..q+k-1] into d at position p
    Copy[s1, s2, dPrime, q, k, d, p]
}

-- Main assertion: entire document is restored
assert FullRestoration {
    all s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int |
        A7Setup[s0, s1, s2, d, dPrime, p, q, k]
        implies
            (s2.V[d] = s0.V[d] and s2.len[d] = s0.len[d])
}

-- Sub-part: left frame preserved through both operations
assert LeftFrame {
    all s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int |
        A7Setup[s0, s1, s2, d, dPrime, p, q, k]
        implies
            (all j: Int | (j >= 1 and j < p) implies
                s2.V[d][j] = s0.V[d][j])
}

-- Sub-part: deleted positions are restored
assert RestoredPositions {
    all s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int |
        A7Setup[s0, s1, s2, d, dPrime, p, q, k]
        implies
            (all j: Int | (j >= p and j < plus[p, k]) implies
                s2.V[d][j] = s0.V[d][j])
}

-- Sub-part: right frame restored
assert RightFrame {
    all s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int |
        A7Setup[s0, s1, s2, d, dPrime, p, q, k]
        implies
            (all j: Int | (j >= plus[p, k] and j =< s0.len[d]) implies
                s2.V[d][j] = s0.V[d][j])
}

-- Sub-part: length restored
assert LengthRestored {
    all s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int |
        A7Setup[s0, s1, s2, d, dPrime, p, q, k]
        implies
            s2.len[d] = s0.len[d]
}

-- Non-vacuity: find a scenario with non-trivial delete+restore
run NonVacuity {
    some s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int |
        A7Setup[s0, s1, s2, d, dPrime, p, q, k] and
        s0.len[d] >= 3 and k >= 1
} for 5 but exactly 3 State, 5 Int

check FullRestoration for 5 but exactly 3 State, 5 Int
check LeftFrame for 5 but exactly 3 State, 5 Int
check RestoredPositions for 5 but exactly 3 State, 5 Int
check RightFrame for 5 but exactly 3 State, 5 Int
check LengthRestored for 5 but exactly 3 State, 5 Int
