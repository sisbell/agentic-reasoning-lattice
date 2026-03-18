include "Link.dfy"

// L7 — DirectionalFlexibility
// Meta-property of L0–L14: the from/to slots carry no inherent directional
// constraint. Swapping from↔to preserves all structural invariants;
// directional semantics are determined by the link type, external to the
// link structure.
module DirectionalFlexibility {
  import opened Endset
  import opened LinkDef

  // Swap from and to endsets, preserving type
  function SwapDirection(l: Link): Link {
    Link(l.to, l.from, l.typ)
  }

  // Involution: swap . swap = id
  lemma SwapInvolution(l: Link)
    ensures SwapDirection(SwapDirection(l)) == l
  { }

  // Type endset is invariant under swap
  lemma SwapPreservesType(l: Link)
    ensures SwapDirection(l).typ == l.typ
  { }

  // Total span content is preserved: union of all endsets unchanged
  lemma SwapPreservesCoverage(l: Link)
    ensures l.from + l.to + l.typ ==
            SwapDirection(l).from + SwapDirection(l).to + SwapDirection(l).typ
  { }

  // Swap produces a different link iff from != to (connects to L6)
  lemma SwapDistinct(l: Link)
    ensures (l.from != l.to) <==> (SwapDirection(l) != l)
  { }
}
