-- A2.frame-doc — DeleteCrossDocFrame (FRAME, ensures)
-- Property: (A d' : d' in S.D /\ d' != d : S'.V(d') = S.V(d'))
-- Delete preserves the value mapping of every document other than the target.

sig Addr {}
sig Doc {}

sig State {
    docs: set Doc,
    V: Doc -> Int -> lone Addr,
    len: Doc -> lone Int
}

pred wellFormed[s: State] {
    all d: s.docs {
        one s.len[d]
        s.len[d] >= 1
        all j: Int | (j >= 1 and j =< s.len[d]) implies one s.V[d][j]
        all j: Int | (j < 1 or j > s.len[d]) implies no s.V[d][j]
    }
    all d: Doc - s.docs {
        no s.len[d]
        no s.V[d]
    }
}

-- Delete a single character at position p in document d (k=1 case).
pred Delete[s, sPost: State, d: Doc, p: Int] {
    -- precondition
    d in s.docs
    p >= 1
    p =< s.len[d]

    -- target document: length decreases by one
    sPost.len[d] = minus[s.len[d], 1]

    -- surviving positions get shifted values
    all j: Int | (j >= 1 and j =< sPost.len[d]) implies
        sPost.V[d][j] = s.V[d][(j < p) implies j else plus[j, 1]]

    -- no values outside valid range for target
    all j: Int | (j < 1 or j > sPost.len[d]) implies no sPost.V[d][j]

    -- document set: d remains if length > 0, removed if length = 0
    s.len[d] = 1 implies sPost.docs = s.docs - d
                    else sPost.docs = s.docs

    -- frame: cross-document preservation
    all d2: s.docs - d {
        sPost.len[d2] = s.len[d2]
        sPost.V[d2] = s.V[d2]
    }

    -- no stray data for docs not in post-state
    all d2: Doc - sPost.docs {
        no sPost.len[d2]
        no sPost.V[d2]
    }
}

-- A2.frame-doc: every document other than the target is unchanged
assert DeleteCrossDocFrame {
    all s, sPost: State, d: Doc, p: Int |
        (wellFormed[s] and Delete[s, sPost, d, p]) implies
            (all d2: Doc | (d2 in s.docs and d2 != d) implies
                sPost.V[d2] = s.V[d2])
}

-- Non-vacuity: find an instance with multiple documents
run NonVacuity {
    some s, sPost: State, d: Doc, p: Int |
        wellFormed[s] and Delete[s, sPost, d, p] and some (s.docs - d)
} for 5 but exactly 2 State, 4 Int

check DeleteCrossDocFrame for 5 but exactly 2 State, 4 Int
