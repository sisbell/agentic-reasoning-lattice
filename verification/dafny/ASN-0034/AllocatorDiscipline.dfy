// ASN-0034: T10a — AllocatorDiscipline (AXIOM)
// design-requirement: the discipline constraining allocator behavior.
// Encoded as a ghost predicate over an inductively-defined allocator tree.
// Downstream lemmas (T10a.1–T10a.8, T10a-N) assume AllocatorDiscipline(a)
// as a precondition.
include "./CarrierSetDefinition.dfy"
include "./HierarchicalParsing.dfy"
include "./HierarchicalIncrement.dfy"

module AllocatorDiscipline {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing
  import opened HierarchicalIncrement

  // Allocator tree node. The root carries its base address; each non-root
  // carries the spawning triple (parent, spawnPt, spawnParam). Structural
  // equality on this datatype enforces the at-most-once child-spawning
  // constraint: identical spawning triples ↔ identical allocators.
  datatype Allocator =
    | RootAllocator(rootBase: Tumbler)
    | ChildAllocator(parent: Allocator, spawnPt: Tumbler, spawnParam: nat)

  // Tree depth: root at 0, each child one deeper than its parent.
  function Depth(a: Allocator): nat
    decreases a
  {
    match a
    case RootAllocator(_) => 0
    case ChildAllocator(p, _, _) => Depth(p) + 1
  }

  // Base address: root's stored base, or inc(spawnPt, spawnParam) for a child.
  // Total via a structural fallback when the spawn point is ill-formed;
  // AllocatorDiscipline rules out the fallback case on conforming inputs.
  ghost function BaseAddress(a: Allocator): Tumbler
  {
    match a
    case RootAllocator(b) => b
    case ChildAllocator(_, sp, k) =>
      if InT(sp) then HierarchicalIncrement.HierarchicalIncrement(sp, k)
      else sp
  }

  // Sibling stream: t₀ = BaseAddress(a); tₙ₊₁ = inc(tₙ, 0).
  ghost function SiblingAt(a: Allocator, n: nat): Tumbler
    decreases n
  {
    if n == 0 then BaseAddress(a)
    else
      var prev := SiblingAt(a, n - 1);
      if InT(prev) then HierarchicalIncrement.HierarchicalIncrement(prev, 0)
      else prev
  }

  // dom(A) — the set of A's sibling outputs.
  ghost predicate InDomain(t: Tumbler, a: Allocator)
  {
    exists n: nat :: SiblingAt(a, n) == t
  }

  // same_allocator(a, b) ≡ ∃A ∈ 𝒯 : a ∈ dom(A) ∧ b ∈ dom(A).
  ghost predicate SameAllocator(a: Tumbler, b: Tumbler)
  {
    exists A: Allocator :: InDomain(a, A) && InDomain(b, A)
  }

  // T10a axiom — the discipline on allocator behavior.
  //   (1) Root's base address is in T and satisfies T4.
  //   (2) Siblings produced exclusively by inc(·, 0) — built into SiblingAt.
  //   (3) Child-spawning uses inc(·, k') with k' ∈ {1, 2}.
  //   (4) zeros(spawnPt) ≤ 2 when spawnParam = 2.
  //   (5) Spawn point lies in parent's domain.
  //   (6) Parent itself conforms.
  // At-most-once: automatic from Dafny's structural equality on
  // ChildAllocator(parent, spawnPt, spawnParam).
  ghost predicate AllocatorDiscipline(a: Allocator)
    decreases a
  {
    match a
    case RootAllocator(b) =>
      InT(b) && HierarchicalParsing.HierarchicalParsing(b)
    case ChildAllocator(p, sp, k) =>
      AllocatorDiscipline(p) &&
      InT(sp) &&
      InDomain(sp, p) &&
      (k == 1 || k == 2) &&
      (k == 2 ==> Zeros(sp) <= 2)
  }
}
