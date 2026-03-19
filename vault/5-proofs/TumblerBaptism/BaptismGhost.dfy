// Ghost validity (ASN-0040 B3) — cross-cutting property.
//
// This property asserts that baptism (Σ.B membership) and content occupation
// are independent predicates. It belongs at the boundary between baptism
// and the content model (Two Space), not cleanly in either ASN. Placed here
// as an isolated module pending a future bridge specification that formalizes
// the relationship between Σ.B and Σ.C.
//
// The key constraint: content requires prior baptism (occupied ⊆ baptized).
// The key permission: baptism does not require content (ghost elements).
module BaptismGhost {
  import opened TumblerAlgebra

  datatype ContentState = ContentState(baptized: set<Tumbler>, occupied: set<Tumbler>)

  // B3 — GhostValidity
  // occupied ⊆ baptized: you cannot store content at an unbaptized position.
  // The reverse does not hold: a baptized position may be empty (ghost element).
  ghost predicate GhostValidity(s: ContentState) {
    s.occupied <= s.baptized
  }
}
