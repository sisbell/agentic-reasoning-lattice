-- P7 — CreationBasedIdentity
--
-- Each creation event allocates addresses within a single allocator's prefix.
-- Distinct creation events produce disjoint address sets.
-- A shared I-address traces to a single creation event.
--
-- Axioms: T9 (forward allocation), T10 (partition independence),
-- unique prefix ownership.

sig IAddr {
  home: one Prefix
}

sig Prefix {}

sig Allocator {
  prefix: one Prefix
}

sig CreationEvent {
  via: one Allocator,
  alloc: set IAddr
}

-- Each prefix is owned by at most one allocator
fact UniqueOwnership {
  all disj a1, a2: Allocator | a1.prefix != a2.prefix
}

-- T10: An event only allocates addresses in its allocator's prefix partition
fact PartitionIndependence {
  all e: CreationEvent, a: e.alloc | a.home = e.via.prefix
}

-- T9: Within one allocator, distinct events allocate disjoint addresses
-- (successive allocations are strictly monotonically increasing)
fact ForwardAllocation {
  all disj e1, e2: CreationEvent |
    e1.via = e2.via implies no (e1.alloc & e2.alloc)
}

-- P7(a): Distinct creation events produce disjoint address sets
assert DisjointAllocation {
  all disj e1, e2: CreationEvent |
    no (e1.alloc & e2.alloc)
}

-- P7(b): A shared I-address traces to a single creation event
assert SingleOrigin {
  all a: IAddr, e1, e2: CreationEvent |
    (a in e1.alloc and a in e2.alloc) implies e1 = e2
}

-- Corollary: Events under different prefixes produce disjoint addresses
assert IndependentCreation {
  all disj e1, e2: CreationEvent |
    e1.via.prefix != e2.via.prefix implies
      no (e1.alloc & e2.alloc)
}

-- Non-vacuity: two events each allocating addresses
run NonVacuity {
  some disj e1, e2: CreationEvent |
    some e1.alloc and some e2.alloc
} for 5 but exactly 2 CreationEvent

check DisjointAllocation for 5
check SingleOrigin for 5
check IndependentCreation for 5
