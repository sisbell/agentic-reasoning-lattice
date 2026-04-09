include "./HierarchicalParsing.dfy"
include "./LastSignificantPosition.dfy"

module SigOnValidAddresses {
  // TA5-SigValid — SigOnValidAddresses (LEMMA)
  // For valid addresses, sig(t) = |t| - 1 (the last index).
  // Corollary of TA5-SIG (LastSignificantPosition) and T4 (HierarchicalParsing).

  import HP = HierarchicalParsing
  import SE = SyntacticEquivalence
  import LSP = LastSignificantPosition

  lemma SigOnValidAddresses(t: SE.Tumbler)
    requires HP.ValidAddress(t)
    ensures LSP.Sig(LSP.Tumbler(t.components)) == |t.components| - 1
  { }
}
