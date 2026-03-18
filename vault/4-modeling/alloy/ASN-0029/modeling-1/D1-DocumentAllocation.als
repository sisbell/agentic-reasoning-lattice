-- D1-DocumentAllocation.als
-- Property D1: within each allocator stream, allocation order ⊆ address order.
--
-- Two allocator kinds per account (ASN-0029):
--   Root allocator  — inc(account,2) then inc(·,0): root docs
--   Child allocator — inc(parent,1) then inc(·,0): child docs
--
-- D1: ∀ d₁,d₂ : same_allocator(d₁,d₂) ∧ allocated_before(d₁,d₂) ⇒ d₁ < d₂

sig Account {}

sig Doc {
  account : one Account,
  parent  : lone Doc,
  level1  : one Int,      -- first document-address component
  level2  : lone Int       -- second component (children only)
}

one sig Timeline {
  allocBefore : Doc -> Doc  -- allocation order within allocator groups
}

----------------------------------------------------------------------
-- Predicates
----------------------------------------------------------------------

pred isRoot[d: Doc] { no d.parent }

-- same_allocator per ASN-0029:
--   both root under same account, OR share the same parent
pred sameAllocator[d1, d2: Doc] {
  (isRoot[d1] and isRoot[d2] and d1.account = d2.account)
  or
  (some d1.parent and some d2.parent and d1.parent = d2.parent)
}

-- Tumbler lexicographic order on (level1, level2)
-- Absent level2 sorts before present level2 (prefix < extension)
pred addrLt[d1, d2: Doc] {
  d1.account = d2.account and (
    lt[d1.level1, d2.level1]
    or (d1.level1 = d2.level1 and no d1.level2 and some d2.level2)
    or (d1.level1 = d2.level1 and some d1.level2 and some d2.level2
        and lt[d1.level2, d2.level2])
  )
}

----------------------------------------------------------------------
-- Structural axioms
----------------------------------------------------------------------

fact DocStructure {
  -- root ↔ no level2
  all d: Doc | isRoot[d] iff no d.level2
  -- children reference a root parent in same account, inherit level1
  all d: Doc | some d.parent implies {
    isRoot[d.parent]
    d.parent.account = d.account
    d.level1 = d.parent.level1
  }
  -- positive components
  all d: Doc | d.level1 > 0
  all d: Doc | some d.level2 implies d.level2 > 0
  -- distinct addresses within each account
  all disj d1, d2: Doc | d1.account = d2.account implies
    not (d1.level1 = d2.level1 and d1.level2 = d2.level2)
}

-- allocBefore: strict total order within each allocator group
fact AllocOrderWF {
  let ab = Timeline.allocBefore {
    all d1, d2: Doc | d1 -> d2 in ab implies sameAllocator[d1, d2]
    no d: Doc | d -> d in ab
    all d1, d2, d3: Doc |
      (d1 -> d2 in ab and d2 -> d3 in ab) implies d1 -> d3 in ab
    all d1, d2: Doc |
      (sameAllocator[d1, d2] and d1 != d2) implies
        (d1 -> d2 in ab or d2 -> d1 in ab)
  }
}

-- inc is monotone: sequential allocations produce increasing addresses
fact IncMonotone {
  let ab = Timeline.allocBefore |
    all d1, d2: Doc | d1 -> d2 in ab implies {
      (isRoot[d1] and isRoot[d2])
        implies lt[d1.level1, d2.level1]
      (some d1.parent and some d2.parent and d1.parent = d2.parent)
        implies lt[d1.level2, d2.level2]
    }
}

----------------------------------------------------------------------
-- D1 assertion and checks
----------------------------------------------------------------------

assert DocumentAllocation {
  all d1, d2: Doc |
    (sameAllocator[d1, d2] and d1 -> d2 in Timeline.allocBefore)
      implies addrLt[d1, d2]
}

check DocumentAllocation for 6 but exactly 1 Account, 4 Int

-- Non-vacuity: instance with both allocator kinds active
run NonVacuity {
  some disj d1, d2: Doc {
    isRoot[d1] and isRoot[d2]
    d1 -> d2 in Timeline.allocBefore
  }
  some disj d3, d4: Doc {
    some d3.parent and some d4.parent
    d3.parent = d4.parent
    d3 -> d4 in Timeline.allocBefore
  }
} for 6 but exactly 1 Account, 4 Int
