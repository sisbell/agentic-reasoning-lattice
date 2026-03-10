-- A3.frame-doc — RearrangeCrossDocFrame (FRAME, ensures)
-- Property: (A d' : d' in S.D /\ d' != d : S'.V(d') = S.V(d'))
-- Rearrange preserves the value mapping of every document other than the target.

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

-- Abstract bijection on {1, ..., n}: maps each position to a unique position in range.
pred bijection[sigma: Int -> Int, n: Int] {
    let P = {i: Int | i >= 1 and i =< n} | {
        all i: P | one i.sigma and i.sigma in P
        all i: Int - P | no i.sigma
        all disj i, j: P | i.sigma != j.sigma
    }
}

-- Rearrange document d using bijection sigma.
-- Models both pivot (m=3) and swap (m=4) abstractly: any bijection on positions.
pred Rearrange[s, sPost: State, d: Doc, sigma: Int -> Int] {
    -- precondition
    d in s.docs

    -- sigma is a bijection on {1, ..., len(d)}
    bijection[sigma, s.len[d]]

    -- target document: length preserved
    sPost.len[d] = s.len[d]

    -- permutation: sPost.V(d)(sigma(j)) = s.V(d)(j)
    all j: Int | (j >= 1 and j =< s.len[d]) implies
        sPost.V[d][j.sigma] = s.V[d][j]

    -- no values outside valid range for target
    all j: Int | (j < 1 or j > sPost.len[d]) implies no sPost.V[d][j]

    -- document set unchanged (rearrange does not add or remove documents)
    sPost.docs = s.docs

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

-- A3.frame-doc: every document other than the target is unchanged
assert RearrangeCrossDocFrame {
    all s, sPost: State, d: Doc, sigma: Int -> Int |
        (wellFormed[s] and Rearrange[s, sPost, d, sigma]) implies
            (all d2: Doc | (d2 in s.docs and d2 != d) implies
                sPost.V[d2] = s.V[d2])
}

-- Non-vacuity: find an instance with multiple documents and a non-trivial rearrange
run NonVacuity {
    some s, sPost: State, d: Doc, sigma: Int -> Int |
        wellFormed[s] and Rearrange[s, sPost, d, sigma]
        and some (s.docs - d)
        and s.V[d] != sPost.V[d]
} for 5 but exactly 2 State, 4 Int

check RearrangeCrossDocFrame for 5 but exactly 2 State, 4 Int
