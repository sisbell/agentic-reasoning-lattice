
module ISpaceImmutable {
  import opened Foundation

  // ASN-0026 P0 — ISpaceImmutable (INV, predicate(State, State))
  // [a in dom(Sigma.I) ==> Sigma'.I(a) = Sigma.I(a)]
  ghost predicate ISpaceImmutable(s: State, s': State) {
    forall a :: a in s.iota ==> a in s'.iota && s'.iota[a] == s.iota[a]
  }
}
