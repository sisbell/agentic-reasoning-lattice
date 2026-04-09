-- A4.frame-I — CopyISpacePreserved (FRAME, ensures)
-- Property: Σ'.I = Σ.I
-- Copy does not modify I-space: the address-to-content mapping is identical
-- before and after the operation.

open util/integer

sig Addr {}
sig Char {}
sig Doc {}

sig State {
    ispace: Addr -> lone Char,
    V: Doc -> Int -> lone Addr,
    len: Doc -> one Int
}

pred wellFormed[s: State] {
    all d: Doc {
        s.len[d] >= 0
        all j: Int | (j >= 1 and j =< s.len[d]) implies one s.V[d][j]
        all j: Int | (j < 1 or j > s.len[d]) implies no s.V[d][j]
    }
    -- P2: every V-space address is in I-space domain
    all d: Doc, j: Int | (j >= 1 and j =< s.len[d]) implies
        s.V[d][j] in (s.ispace).Char
}

-- Overflow guard: keep arithmetic within 6-bit Int range
pred bounded[ps: Int, k: Int, pt: Int] {
    ps >= 0 and ps =< 10
    k >= 0 and k =< 10
    pt >= 0 and pt =< 10
}

pred Copy[s, sPost: State, ds: Doc, dt: Doc, ps: Int, k: Int, pt: Int] {
    -- preconditions
    k >= 1
    ps >= 1
    plus[ps, minus[k, 1]] =< s.len[ds]
    pt >= 1
    pt =< plus[s.len[dt], 1]

    -- post length increases by k
    sPost.len[dt] = plus[s.len[dt], k]

    -- positions before insertion point: unchanged
    all j: Int | (j >= 1 and j < pt) implies
        sPost.V[dt][j] = s.V[dt][j]

    -- inserted positions: copied from source
    all j: Int | (j >= 0 and j < k) implies
        sPost.V[dt][plus[pt, j]] = s.V[ds][plus[ps, j]]

    -- positions at pt and beyond shift right by k
    all j: Int | (j >= pt and j =< s.len[dt]) implies
        sPost.V[dt][plus[j, k]] = s.V[dt][j]

    -- nothing outside new range
    all j: Int | (j < 1 or j > sPost.len[dt]) implies
        no sPost.V[dt][j]

    -- frame: other documents unchanged
    all d: Doc - dt {
        sPost.len[d] = s.len[d]
        sPost.V[d] = s.V[d]
    }

    -- I-space frame (the property under test)
    sPost.ispace = s.ispace
}

-- A4.frame-I: Copy preserves I-space exactly
assert CopyISpacePreserved {
    all s, sPost: State, ds, dt: Doc, ps, k, pt: Int |
        (wellFormed[s] and bounded[ps, k, pt] and
         Copy[s, sPost, ds, dt, ps, k, pt])
        implies sPost.ispace = s.ispace
}

-- Strengthened: I-space domain is identical
assert CopyISpaceDomainPreserved {
    all s, sPost: State, ds, dt: Doc, ps, k, pt: Int |
        (wellFormed[s] and bounded[ps, k, pt] and
         Copy[s, sPost, ds, dt, ps, k, pt])
        implies (s.ispace).Char = (sPost.ispace).Char
}

-- Strengthened: every individual address retains its content
assert CopyISpacePointwise {
    all s, sPost: State, ds, dt: Doc, ps, k, pt: Int |
        (wellFormed[s] and bounded[ps, k, pt] and
         Copy[s, sPost, ds, dt, ps, k, pt])
        implies (all a: Addr | sPost.ispace[a] = s.ispace[a])
}

-- Non-vacuity: Copy can fire on a well-formed state with non-trivial I-space
run FindCopy {
    some s, sPost: State, ds, dt: Doc, ps, k, pt: Int |
        wellFormed[s] and bounded[ps, k, pt] and
        Copy[s, sPost, ds, dt, ps, k, pt] and
        some s.ispace
} for 5 but exactly 2 State, 6 Int

check CopyISpacePreserved for 5 but exactly 2 State, 6 Int
check CopyISpaceDomainPreserved for 5 but exactly 2 State, 6 Int
check CopyISpacePointwise for 5 but exactly 2 State, 6 Int
