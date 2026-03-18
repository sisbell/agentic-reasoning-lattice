-- A4.frame-doc — CopyCrossDocFrame (FRAME, ensures)
-- Property: (A d' : d' in S.D /\ d' != d_t : S'.V(d') = S.V(d'))
-- Copy preserves the value mapping of every document other than the target.

open util/integer

sig Addr {}
sig Doc {}

sig State {
    V: Doc -> Int -> lone Addr,
    len: Doc -> one Int
}

pred wellFormed[s: State] {
    all d: Doc {
        s.len[d] >= 0
        all j: Int | (j >= 1 and j =< s.len[d]) implies one s.V[d][j]
        all j: Int | (j < 1 or j > s.len[d]) implies no s.V[d][j]
    }
}

-- Overflow guard: keep arithmetic within 6-bit Int range
pred bounded[ps: Int, k: Int, pt: Int] {
    ps >= 0 and ps =< 10
    k >= 0 and k =< 10
    pt >= 0 and pt =< 10
}

-- Copy: insert k positions from source doc ds starting at ps
-- into target doc dt at position pt.
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
}

-- A4.frame-doc: every document other than the target is unchanged
assert CopyCrossDocFrame {
    all s, sPost: State, ds, dt: Doc, ps, k, pt: Int |
        (wellFormed[s] and bounded[ps, k, pt] and
         Copy[s, sPost, ds, dt, ps, k, pt])
        implies
            (all d2: Doc | d2 != dt implies
                sPost.V[d2] = s.V[d2])
}

-- Non-vacuity: find a cross-doc copy (ds != dt) with another bystander doc
run NonVacuity {
    some s, sPost: State, ds, dt: Doc, ps, k, pt: Int |
        wellFormed[s] and bounded[ps, k, pt] and
        Copy[s, sPost, ds, dt, ps, k, pt] and
        ds != dt and some (Doc - dt - ds)
} for 5 but exactly 2 State, 6 Int

check CopyCrossDocFrame for 5 but exactly 2 State, 6 Int
