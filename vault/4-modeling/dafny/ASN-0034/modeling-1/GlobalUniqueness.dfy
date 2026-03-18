include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module GlobalUniqueness {

  import opened TumblerAlgebra

  // (Global uniqueness) — ASN-0034
  // No two distinct allocations, anywhere in the system, at any time,
  // produce the same address.
  //
  // Four cases (derived from T3, T4, T9, T10, T10a, TA5):
  //   Case 1: Same allocator — T9 gives strict ordering, hence a ≠ b
  //   Case 2: Different allocators, non-nesting prefixes — T10 gives a ≠ b
  //   Case 3: Nesting prefixes, different zero counts — T3/T4 give a ≠ b
  //   Case 4: Nesting prefixes, same zero count — T10a gives different
  //           output lengths, T3 gives a ≠ b
  //
  // Cases 3 and 4 both reduce to: different component-sequence lengths
  // imply a ≠ b. The allocation system guarantees that one of these
  // three structural discriminants holds for any pair of distinct
  // allocation events.

  // DIVERGENCE: The ASN states GlobalUniqueness as a system-level property
  // over all allocation events at all times. The Dafny model captures the
  // structural core: given that the allocation system provides one of three
  // discriminants (ordering, non-nesting prefixes, or length difference),
  // a ≠ b follows. The exhaustiveness argument — that every pair of distinct
  // allocations satisfies at least one discriminant — depends on T9, T10,
  // and T10a as system invariants, which cannot be expressed as a Dafny
  // precondition without modeling the full allocation state machine.

  lemma GlobalUniqueness(
    a: Tumbler, b: Tumbler,
    pa: Tumbler, pb: Tumbler
  )
    requires IsPrefix(pa, a) && IsPrefix(pb, b)
    requires
      // Case 1: Same allocator, strictly ordered (T9)
      (LessThan(a, b) || LessThan(b, a))
      ||
      // Case 2: Different allocators, non-nesting prefixes (T10)
      (!IsPrefix(pa, pb) && !IsPrefix(pb, pa))
      ||
      // Cases 3-4: Different output lengths (T10a + T3)
      |a.components| != |b.components|
    ensures a != b
  { }
}
