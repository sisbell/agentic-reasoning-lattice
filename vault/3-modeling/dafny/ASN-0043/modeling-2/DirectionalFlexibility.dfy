// L7 — DirectionalFlexibility (ASN-0043)
// META: L0–L14 impose no constraint on which of the from/to slots carries
// directional significance. Any directional interpretation is determined by
// the link type, outside the link structure.
//
// Demonstrated by: swapping from ↔ to is a well-typed involution that
// preserves link well-formedness.

include "Link.dfy"

module DirectionalFlexibility {
  import opened LinkDef
  import opened Endset

  function SwapDirection(link: Link): Link {
    Link(link.to, link.from, link.typ)
  }

  // Swapping from ↔ to preserves well-formedness
  lemma SwapPreservesValidity(link: Link)
    requires WellFormedLink(link)
    ensures WellFormedLink(SwapDirection(link))
  { }

  // Swap is an involution — applying it twice recovers the original
  lemma SwapInvolution(link: Link)
    ensures SwapDirection(SwapDirection(link)) == link
  { }
}
