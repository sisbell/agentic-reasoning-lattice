open util/ordering[Tumbler]

-- Tumbler: a hierarchical address in the tumbler space
sig Tumbler {
  len: Int,
  prefixedBy: set Tumbler
}

-- p is a prefix of t  (p ≼ t)
pred isPrefix[p, t: Tumbler] {
  p in t.prefixedBy
}

-- Prefix axioms
fact {
  -- Reflexive
  all t: Tumbler | t in t.prefixedBy
  -- Antisymmetric
  all a, b: Tumbler | (isPrefix[a, b] and isPrefix[b, a]) implies a = b
  -- Transitive
  all a, b, c: Tumbler | (isPrefix[a, b] and isPrefix[b, c]) implies isPrefix[a, c]
  -- Proper prefix requires strictly shorter length
  all a, b: Tumbler | (isPrefix[a, b] and a != b) implies a.len < b.len
  -- T1: prefix implies leq in tumbler order
  all a, b: Tumbler | isPrefix[a, b] implies lte[a, b]
  -- Positive lengths
  all t: Tumbler | t.len > 0
}

-- T5: Prefix convexity
-- If p is prefix of both a and c, and a leq b leq c, then p is prefix of b
fact {
  all p, a, b, c: Tumbler |
    (isPrefix[p, a] and isPrefix[p, c] and lte[a, b] and lte[b, c])
    implies isPrefix[p, b]
}

-- PrefixOrderingExtension (from ASN-0034):
-- For non-nesting p < q, every descendant of p precedes every descendant of q
fact {
  all p, q, a, b: Tumbler |
    (lt[p, q] and not isPrefix[p, q] and not isPrefix[q, p]
     and isPrefix[p, a] and isPrefix[q, b])
    implies lt[a, b]
}

-- Sibling sub-partition prefix produced by the child allocator via inc(., 0)
sig SiblingPrefix {
  tum: one Tumbler
}

-- Allocated address within a sub-partition
sig Addr {
  tum: one Tumbler,
  partition: one SiblingPrefix,
  allocIdx: Int
}

-- TA5(a) + TA5(c): sibling prefixes have uniform length and distinct tumblers
fact {
  all sp1, sp2: SiblingPrefix | sp1.tum.len = sp2.tum.len
  all sp1, sp2: SiblingPrefix | sp1 != sp2 implies sp1.tum != sp2.tum
}

-- T9: Forward allocation — allocation order matches address order
fact {
  all a, b: Addr |
    (a.partition = b.partition and a.allocIdx < b.allocIdx)
    implies lt[a.tum, b.tum]
}

-- Address constraints
fact {
  -- Each address extends its sub-partition prefix
  all a: Addr | isPrefix[a.partition.tum, a.tum]
  -- Distinct addresses have distinct tumblers
  all a, b: Addr | a != b implies a.tum != b.tum
  -- Allocation indices distinct within a sub-partition
  all a, b: Addr |
    (a.partition = b.partition and a != b) implies a.allocIdx != b.allocIdx
  -- Non-negative allocation index
  all a: Addr | a.allocIdx >= 0
}

-- POSTCONDITION 1: Cross-partition ordering
-- For sibling prefixes ti < tj and any a extending ti, b extending tj: a < b
assert CrossPartitionOrdering {
  all sp1, sp2: SiblingPrefix, a, b: Addr |
    (lt[sp1.tum, sp2.tum] and a.partition = sp1 and b.partition = sp2)
    implies lt[a.tum, b.tum]
}

-- POSTCONDITION 2: Intra-partition ordering
-- Within each sub-partition: allocated_before(a, b) implies a < b
assert IntraPartitionOrdering {
  all a, b: Addr |
    (a.partition = b.partition and a.allocIdx < b.allocIdx)
    implies lt[a.tum, b.tum]
}

-- INVARIANT: Total order consistency
-- All allocated addresses are totally ordered by T1
assert TotalOrderConsistency {
  all a, b: Addr |
    a != b implies (lt[a.tum, b.tum] or gt[a.tum, b.tum])
}

-- Non-vacuity: model is satisfiable with meaningful structure
run NonVacuity {
  #SiblingPrefix >= 2
  #Addr >= 2
  some a, b: Addr | a.partition != b.partition
} for 5 but 4 Int

check CrossPartitionOrdering for 5 but 4 Int
check IntraPartitionOrdering for 5 but 4 Int
check TotalOrderConsistency for 5 but 4 Int
