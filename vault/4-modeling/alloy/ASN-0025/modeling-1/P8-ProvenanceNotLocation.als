-- P8 — ProvenanceNotLocation
--
-- The node component of IAddr encodes the originating node (provenance),
-- not the current physical storage location.  The resolution mapping
-- (IAddr -> physical node) is state-dependent and independent of origin.
--
-- (A a : a in Sigma.A : fields(a).node = originating_node(a))
-- The resolution mapping is not a component of a or of Sigma.iota.

sig Node {}

sig IAddr {
  origin: one Node   -- fields(a).node = originating_node(a), immutable by type
}

sig Value {}

sig State {
  iota: IAddr -> lone Value,       -- content function
  resolution: IAddr -> lone Node   -- physical location (external to address)
}

-- Allocated addresses = dom(iota)
fun allocated[s: State]: set IAddr {
  s.iota.Value
}

-- Well-formedness: allocated addresses have resolution; unallocated do not
pred wellFormed[s: State] {
  all a: allocated[s] | one s.resolution[a]
  all a: IAddr - allocated[s] | no s.resolution[a]
}

-- P1: content permanence (addresses keep their content across transitions)
pred contentPermanence[s, sPost: State] {
  all a: allocated[s] | a in allocated[sPost] and s.iota[a] = sPost.iota[a]
}

-- Migration: move content to a different physical node
pred Migrate[s, sPost: State, a: IAddr, target: Node] {
  a in allocated[s]
  contentPermanence[s, sPost]
  allocated[sPost] = allocated[s]
  sPost.resolution[a] = target
  all a2: allocated[s] - a | sPost.resolution[a2] = s.resolution[a2]
  all a2: IAddr - allocated[sPost] | no sPost.resolution[a2]
}

-- P8(a): Migration preserves well-formedness
assert MigratePreservesWF {
  all s, sPost: State, a: IAddr, target: Node |
    (wellFormed[s] and Migrate[s, sPost, a, target]) implies
      wellFormed[sPost]
}

-- P8(b): Migration preserves content (consequence of P1 within Migrate)
assert MigratePreservesContent {
  all s, sPost: State, a: IAddr, target: Node |
    (wellFormed[s] and Migrate[s, sPost, a, target]) implies
      s.iota[a] = sPost.iota[a]
}

-- P8(c): Resolution is NOT constrained to equal origin
-- Expect counterexample: an allocated address whose resolution differs from origin
assert ResolutionEqualsOrigin {
  all s: State |
    wellFormed[s] implies
      (all a: allocated[s] | s.resolution[a] = a.origin)
}

-- Non-vacuity: migration to a node different from origin
run ShowMigration {
  some s, sPost: State, a: IAddr, target: Node |
    wellFormed[s] and Migrate[s, sPost, a, target] and target != a.origin
} for 4 but exactly 2 State

check MigratePreservesWF for 5 but exactly 2 State
check MigratePreservesContent for 5 but exactly 2 State
check ResolutionEqualsOrigin for 5 but exactly 2 State
