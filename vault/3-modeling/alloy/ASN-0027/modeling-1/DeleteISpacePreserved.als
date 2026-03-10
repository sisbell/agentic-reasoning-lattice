-- A2.frame-I — DeleteISpacePreserved (FRAME, ensures)
-- Property: Σ'.I = Σ.I
-- Delete does not modify I-space: the address-to-content mapping is identical
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
        s.len[d] >= 1
        all j: Int | (j >= 1 and j =< s.len[d]) implies one s.V[d][j]
        all j: Int | (j < 1 or j > s.len[d]) implies no s.V[d][j]
    }
    -- P2: every V-space address is in I-space domain
    all d: Doc, j: Int | (j >= 1 and j =< s.len[d]) implies
        s.V[d][j] in (s.ispace).Char
}

-- Source position: maps post-position j to pre-position, deleting at p
fun src[j: Int, p: Int]: Int {
    (j < p) implies j else plus[j, 1]
}

pred Delete[s, sPost: State, d: Doc, p: Int] {
    -- precondition
    p >= 1
    p =< s.len[d]

    -- length decreases by one
    sPost.len[d] = minus[s.len[d], 1]

    -- surviving positions get values from source positions
    all j: Int | (j >= 1 and j =< sPost.len[d]) implies
        sPost.V[d][j] = s.V[d][src[j, p]]

    -- no values outside valid range
    all j: Int | (j < 1 or j > sPost.len[d]) implies no sPost.V[d][j]

    -- cross-document frame
    all d2: Doc - d {
        sPost.len[d2] = s.len[d2]
        sPost.V[d2] = s.V[d2]
    }

    -- I-space frame (the property under test, built into the operation)
    sPost.ispace = s.ispace
}

-- A2.frame-I: Delete preserves I-space exactly
assert DeleteISpacePreserved {
    all s, sPost: State, d: Doc, p: Int |
        (wellFormed[s] and Delete[s, sPost, d, p]) implies
            sPost.ispace = s.ispace
}

-- Strengthened: I-space domain is identical
assert DeleteISpaceDomainPreserved {
    all s, sPost: State, d: Doc, p: Int |
        (wellFormed[s] and Delete[s, sPost, d, p]) implies
            (s.ispace).Char = (sPost.ispace).Char
}

-- Strengthened: every individual address retains its content
assert DeleteISpacePointwise {
    all s, sPost: State, d: Doc, p: Int |
        (wellFormed[s] and Delete[s, sPost, d, p]) implies
            (all a: Addr | sPost.ispace[a] = s.ispace[a])
}

-- Non-vacuity: Delete can fire on a well-formed state with non-trivial I-space
run FindDelete {
    some s, sPost: State, d: Doc, p: Int |
        wellFormed[s] and Delete[s, sPost, d, p] and
        some s.ispace
} for 5 but exactly 2 State, exactly 1 Doc, 4 Int

check DeleteISpacePreserved for 5 but exactly 2 State, exactly 1 Doc, 4 Int
check DeleteISpaceDomainPreserved for 5 but exactly 2 State, exactly 1 Doc, 4 Int
check DeleteISpacePointwise for 5 but exactly 2 State, exactly 1 Doc, 4 Int
