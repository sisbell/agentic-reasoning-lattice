-- T4 (HierarchicalParsing): address tumblers have hierarchical structure
-- defined by zero-valued field separators.
--
-- Axiom: zeros(t) <= 3, positive-component constraint, non-empty field constraint
-- T4a: non-empty field constraint <=> syntactic conditions
-- T4b: field decomposition is unique
-- T4c: zeros count determines hierarchical level bijectively

open util/integer

------------------------------------------------------------
-- Domain: tumbler components
------------------------------------------------------------

abstract sig Comp {}
one sig ZeroC extends Comp {}     -- field separator (value 0)
sig PosC extends Comp {}          -- positive component (value > 0)

sig Tumbler {
  comp: seq Comp
} {
  some comp
}

------------------------------------------------------------
-- Helper functions
------------------------------------------------------------

-- Indices of zero-valued (separator) components
fun zeroInds[t: Tumbler]: set Int {
  {i: t.comp.inds | t.comp[i] in ZeroC}
}

-- Number of separators
fun zeroCount[t: Tumbler]: Int {
  #zeroInds[t]
}

-- Length of tumbler
fun tLen[t: Tumbler]: Int {
  #t.comp
}

-- Last valid index
fun lastIdx[t: Tumbler]: Int {
  minus[tLen[t], 1]
}

-- Field number of non-separator position i: count of separators before i
fun fieldNum[t: Tumbler, i: Int]: Int {
  #{j: zeroInds[t] | j < i}
}

------------------------------------------------------------
-- Non-empty field constraint (field-centric formulation)
-- Each field delimited by separators has >= 1 component
------------------------------------------------------------

pred nonEmptyFields[t: Tumbler] {
  -- First separator (if any) not at position 0
  all i: zeroInds[t] |
    (no j: zeroInds[t] | j < i) implies i > 0

  -- Consecutive separators have gap > 1 (interior field non-empty)
  all i, j: zeroInds[t] |
    (i < j and no k: zeroInds[t] | i < k and k < j) implies
      j > plus[i, 1]

  -- Last separator (if any) not at last position
  all i: zeroInds[t] |
    (no j: zeroInds[t] | j > i) implies i < lastIdx[t]
}

------------------------------------------------------------
-- Syntactic conditions (component-centric formulation)
------------------------------------------------------------

pred syntacticConds[t: Tumbler] {
  -- No adjacent separators
  no i: zeroInds[t] | plus[i, 1] in zeroInds[t]
  -- First component not a separator
  not (0 in zeroInds[t])
  -- Last component not a separator
  not (lastIdx[t] in zeroInds[t])
}

------------------------------------------------------------
-- T4 Axiom: valid address tumbler
------------------------------------------------------------

pred validAddress[t: Tumbler] {
  zeroCount[t] =< 3
  nonEmptyFields[t]
}

------------------------------------------------------------
-- Hierarchical levels
------------------------------------------------------------

abstract sig Level {}
one sig NodeL, UserL, DocL, ElemL extends Level {}

fun hierLevel[t: Tumbler]: Level {
  zeroCount[t] = 0 => NodeL else
  zeroCount[t] = 1 => UserL else
  zeroCount[t] = 2 => DocL else
  ElemL
}

------------------------------------------------------------
-- Assertions
------------------------------------------------------------

-- T4a: non-empty field constraint <=> three syntactic conditions
assert T4a_SyntacticEquivalence {
  all t: Tumbler |
    nonEmptyFields[t] iff syntacticConds[t]
}

-- T4b: each field in [0..zeroCount] has at least one non-separator position
assert T4b_UniqueParse {
  all t: Tumbler | validAddress[t] implies
    all n: Int | n >= 0 and n =< zeroCount[t] implies
      some i: t.comp.inds |
        not (i in zeroInds[t]) and fieldNum[t, i] = n
}

-- T4c: zero count determines level bijectively
assert T4c_LevelBijection {
  all t1, t2: Tumbler |
    (validAddress[t1] and validAddress[t2]) implies
      (zeroCount[t1] = zeroCount[t2] iff hierLevel[t1] = hierLevel[t2])
}

------------------------------------------------------------
-- Non-vacuity: valid addresses exist at all four levels
------------------------------------------------------------

run NonVacuity {
  some disj t0, t1, t2, t3: Tumbler |
    validAddress[t0] and zeroCount[t0] = 0 and
    validAddress[t1] and zeroCount[t1] = 1 and
    validAddress[t2] and zeroCount[t2] = 2 and
    validAddress[t3] and zeroCount[t3] = 3
} for 5 but exactly 4 Tumbler, exactly 1 PosC, 7 seq, 5 Int

check T4a_SyntacticEquivalence for 5 but exactly 1 Tumbler, exactly 1 PosC, 7 seq, 5 Int
check T4b_UniqueParse for 5 but exactly 1 Tumbler, exactly 1 PosC, 7 seq, 5 Int
check T4c_LevelBijection for 5 but exactly 2 Tumbler, exactly 1 PosC, 7 seq, 5 Int
