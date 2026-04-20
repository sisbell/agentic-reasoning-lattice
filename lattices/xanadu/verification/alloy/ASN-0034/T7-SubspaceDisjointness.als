open util/integer

-- A tumbler represented by its field structure and component values.
-- Element-level tumblers have 4 fields (node, user, document, element)
-- separated by 3 zero-valued delimiters.
sig Tumbler {
    nLen: one Int,   -- node field length
    uLen: one Int,   -- user field length
    dLen: one Int,   -- document field length
    eLen: one Int,   -- element field length
    val: Int -> lone Int   -- position -> component value (1-indexed)
}

-- Total length: nLen + uLen + dLen + eLen + 3 separators
fun totalLen[t: Tumbler]: Int {
    plus[plus[plus[t.nLen, t.uLen], plus[t.dLen, t.eLen]], 3]
}

-- Separator positions (1-indexed)
fun sep1Pos[t: Tumbler]: Int { plus[t.nLen, 1] }
fun sep2Pos[t: Tumbler]: Int { plus[plus[t.nLen, t.uLen], 2] }
fun sep3Pos[t: Tumbler]: Int { plus[plus[plus[t.nLen, t.uLen], t.dLen], 3] }

-- Position of E1: first component of the element field
fun e1Pos[t: Tumbler]: Int { plus[sep3Pos[t], 1] }

-- Value of E1
fun e1Val[t: Tumbler]: Int { t.val[e1Pos[t]] }

-- Well-formed element-level tumbler (T4: exactly 3 zeros as separators,
-- all other components strictly positive)
pred wellFormed[t: Tumbler] {
    -- Field lengths in [1, 3] to stay within Int bitwidth
    t.nLen >= 1 and t.nLen =< 3
    t.uLen >= 1 and t.uLen =< 3
    t.dLen >= 1 and t.dLen =< 3
    t.eLen >= 1 and t.eLen =< 3

    -- val is defined exactly on positions 1..totalLen
    all i: Int | (i >= 1 and i =< totalLen[t]) implies one t.val[i]
    all i: Int | (i < 1 or i > totalLen[t]) implies no t.val[i]

    -- Three separators are zero-valued
    t.val[sep1Pos[t]] = 0
    t.val[sep2Pos[t]] = 0
    t.val[sep3Pos[t]] = 0

    -- Every non-separator position has a strictly positive value
    all i: Int |
        (i >= 1 and i =< totalLen[t]
         and not (i = sep1Pos[t])
         and not (i = sep2Pos[t])
         and not (i = sep3Pos[t]))
        implies t.val[i] > 0
}

-- Structural equality per T3: same length and same component at every position
pred tumblerEq[a, b: Tumbler] {
    totalLen[a] = totalLen[b]
    all i: Int | (i >= 1 and i =< totalLen[a]) implies a.val[i] = b.val[i]
}

-- T7 (SubspaceDisjointness): different E1 implies structurally distinct
assert SubspaceDisjointness {
    all a, b: Tumbler |
        (wellFormed[a] and wellFormed[b] and not (e1Val[a] = e1Val[b]))
        implies not tumblerEq[a, b]
}

-- Non-vacuity: two well-formed tumblers with different E1 values exist
run NonVacuity {
    some disj a, b: Tumbler |
        wellFormed[a] and wellFormed[b] and not (e1Val[a] = e1Val[b])
} for 5 but exactly 2 Tumbler, 5 Int

check SubspaceDisjointness for 5 but exactly 2 Tumbler, 5 Int
