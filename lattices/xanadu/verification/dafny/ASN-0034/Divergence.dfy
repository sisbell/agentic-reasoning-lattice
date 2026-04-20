include "./LexicographicOrder.dfy"

module Divergence {
  // Divergence — Divergence point of two unequal tumblers

  import opened CarrierSetDefinition
  import opened LexicographicOrder

  // divergence(a, b) = first 1-based position where two unequal tumblers differ.
  // Case (i): first shared index k where aₖ != bₖ.
  // Case (ii): all shared positions agree but lengths differ; k = min(#a, #b) + 1.
  ghost function Divergence(a: Tumbler, b: Tumbler): nat
    requires ValidTumbler(a) && ValidTumbler(b)
    requires a != b
  {
    FirstDivergence(a.components, b.components, 0) + 1
  }
}
