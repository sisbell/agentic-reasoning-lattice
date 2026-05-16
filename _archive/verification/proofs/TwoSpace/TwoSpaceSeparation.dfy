// Two-space separation theorem (ASN-0036): S9
module TwoSpaceSeparation {
  import opened TumblerAlgebra
  import opened TwoSpace

  // ---------------------------------------------------------------------------
  // S9 — TwoSpaceSeparation
  // No modification to any arrangement can alter the content store.
  // Theorem: follows directly from S0 (ContentImmutability).
  // ---------------------------------------------------------------------------

  lemma TwoSpaceSeparation(s: TwoSpaceState, s': TwoSpaceState)
    requires ContentImmutability(s, s')
    ensures forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
  { }
}
