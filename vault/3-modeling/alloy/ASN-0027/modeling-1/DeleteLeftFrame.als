-- A2.left — DeleteLeftFrame
-- Positions left of the deletion point are unchanged.

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

-- Source position: maps new position j to old position when deleting at p.
-- For j < p the source is j itself; for j >= p the source is j+1.
fun src[j: Int, p: Int]: Int {
    (j < p) implies j else plus[j, 1]
}

pred Delete[s, sPost: State, d: Doc, p: Int] {
    -- precondition: p is a valid position
    p >= 1
    p =< s.len[d]

    -- length decreases by one
    sPost.len[d] = minus[s.len[d], 1]

    -- each surviving position gets value from its source
    all j: Int | (j >= 1 and j =< sPost.len[d]) implies
        sPost.V[d][j] = s.V[d][src[j, p]]

    -- no values outside valid range
    all j: Int | (j < 1 or j > sPost.len[d]) implies no sPost.V[d][j]

    -- frame: other documents unchanged
    all d2: Doc - d {
        sPost.len[d2] = s.len[d2]
        sPost.V[d2] = s.V[d2]
    }
}

-- A2.left: values left of the deletion point are preserved
assert DeleteLeftFrame {
    all s, sPost: State, d: Doc, p: Int |
        (wellFormed[s] and Delete[s, sPost, d, p]) implies
            (all j: Int | (j >= 1 and j < p) implies
                sPost.V[d][j] = s.V[d][j])
}

-- Non-vacuity
run FindDelete {
    some s, sPost: State, d: Doc, p: Int |
        wellFormed[s] and Delete[s, sPost, d, p] and wellFormed[sPost]
} for 5 but exactly 2 State, exactly 1 Doc, 4 Int

check DeleteLeftFrame for 5 but exactly 2 State, exactly 1 Doc, 4 Int
