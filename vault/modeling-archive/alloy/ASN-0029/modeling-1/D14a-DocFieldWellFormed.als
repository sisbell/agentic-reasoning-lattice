-- D14a — DocFieldWellFormed (INV, predicate(DocId))
--
-- (∀ d ∈ Σ.D : let (N, U, D) = fields(d) :
--     #D ≥ 1 ∧ (∀ i : 1 ≤ i ≤ #D : Dᵢ > 0))
--
-- Every document address in the state has at least one document-field
-- component, and each component is strictly positive.

open util/integer

sig DocId {
    -- count of document-field components (#D)
    numFields : one Int,
    -- 1-indexed field values: dfld[i] = Dᵢ
    dfld : Int -> lone Int
} {
    numFields >= 0
    -- dfld defined exactly on indices 1..numFields
    all i : Int | some dfld[i] iff (i >= 1 and i =< numFields)
}

one sig Sigma {
    docs : set DocId
}

-- D14a predicate
pred DocFieldWellFormed[s : Sigma] {
    all d : s.docs {
        d.numFields >= 1
        all i : Int | (i >= 1 and i =< d.numFields) implies d.dfld[i] > 0
    }
}

-- Conjunct 1: well-formedness implies non-empty field sequence
assert WFImpliesNonempty {
    DocFieldWellFormed[Sigma] implies
        (all d : Sigma.docs | d.numFields >= 1)
}

-- Conjunct 2: well-formedness implies all field values strictly positive
assert WFImpliesAllPositive {
    DocFieldWellFormed[Sigma] implies
        (all d : Sigma.docs, i : Int |
            (i >= 1 and i =< d.numFields) implies d.dfld[i] > 0)
}

-- Non-vacuity: well-formed state with multiple documents exists
run NonVacuity {
    #Sigma.docs > 1
    DocFieldWellFormed[Sigma]
} for 5 but exactly 1 Sigma, 5 Int

check WFImpliesNonempty for 5 but exactly 1 Sigma, 5 Int
check WFImpliesAllPositive for 5 but exactly 1 Sigma, 5 Int
