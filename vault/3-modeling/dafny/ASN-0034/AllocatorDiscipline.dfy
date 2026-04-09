module AllocatorDiscipline {
  // T10a — AllocatorDiscipline (AXIOM)
  // Design requirement: allocators produce sibling outputs exclusively
  // by inc(·, 0); child-spawning uses exactly one inc(·, k') with k' ∈ {1, 2}.

  datatype Tumbler = Tumbler(components: seq<nat>)

  ghost predicate ValidTumbler(t: Tumbler) {
    |t.components| >= 1
  }

  ghost predicate IsPrefix(p: Tumbler, q: Tumbler) {
    |p.components| <= |q.components| &&
    forall i :: 0 <= i < |p.components| ==> p.components[i] == q.components[i]
  }

  // Count zero-valued components: zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}
  function CountZeros(s: seq<nat>): nat {
    if |s| == 0 then 0
    else (if s[0] == 0 then 1 else 0) + CountZeros(s[1..])
  }

  function Zeros(t: Tumbler): nat
    requires ValidTumbler(t)
  {
    CountZeros(t.components)
  }

  // T4 (HierarchicalParsing): non-empty field constraint.
  // No trailing zero and no two consecutive zeros in the component sequence.
  ghost predicate SatisfiesT4(t: Tumbler)
    requires ValidTumbler(t)
  {
    t.components[|t.components| - 1] > 0 &&
    (forall i :: 0 <= i < |t.components| - 1 ==>
      !(t.components[i] == 0 && t.components[i + 1] == 0))
  }

  function SumNats(ks: seq<nat>): nat {
    if |ks| == 0 then 0
    else ks[0] + SumNats(ks[1..])
  }

  // inc(t, 0): increment at last position, preserving length (TA5c)
  function IncSibling(t: Tumbler): Tumbler
    requires ValidTumbler(t)
    ensures ValidTumbler(IncSibling(t))
    ensures |IncSibling(t).components| == |t.components|
  {
    var n := |t.components|;
    Tumbler(t.components[..n - 1] + [t.components[n - 1] + 1])
  }

  // inc(t, k') for k' ∈ {1, 2}: append k'-1 zeros and trailing 1 (TA5d)
  // TA5a bounds: k'=1 requires zeros(t) ≤ 3, k'=2 requires zeros(t) ≤ 2
  function IncChild(t: Tumbler, k: nat): Tumbler
    requires ValidTumbler(t)
    requires k == 1 || k == 2
    requires k == 1 ==> Zeros(t) <= 3
    requires k == 2 ==> Zeros(t) <= 2
    ensures ValidTumbler(IncChild(t, k))
    ensures |IncChild(t, k).components| == |t.components| + k
  {
    Tumbler(t.components + seq(k - 1, _ => 0) + [1])
  }

  // Structural child increment — TA5(b) prefix agreement and TA5(d) length
  // without TA5a zero-count bounds. Used for the necessity argument, which
  // reasons only about prefix/length properties of inc, not T4 preservation.
  function IncChildRaw(t: Tumbler, k: nat): Tumbler
    requires ValidTumbler(t)
    requires k >= 1
    ensures ValidTumbler(IncChildRaw(t, k))
    ensures |IncChildRaw(t, k).components| == |t.components| + k
  {
    Tumbler(t.components + seq(k - 1, _ => 0) + [1])
  }

  // ValidChildChain: a sequence of child-spawning increments with TA5a bounds
  ghost predicate ValidChildChain(base: Tumbler, ks: seq<nat>)
    decreases |ks|
  {
    ValidTumbler(base) &&
    (|ks| == 0 ||
      ((ks[0] == 1 || ks[0] == 2) &&
       (ks[0] == 1 ==> Zeros(base) <= 3) &&
       (ks[0] == 2 ==> Zeros(base) <= 2) &&
       ValidChildChain(IncChild(base, ks[0]), ks[1..])))
  }

  // Apply a chain of child-spawning increments across d nesting levels
  function ChildChain(base: Tumbler, ks: seq<nat>): Tumbler
    requires ValidChildChain(base, ks)
    ensures ValidTumbler(ChildChain(base, ks))
    decreases |ks|
  {
    if |ks| == 0 then base
    else ChildChain(IncChild(base, ks[0]), ks[1..])
  }

  // T10a.1 — Uniform sibling length
  // inc(·, 0) preserves length, so all siblings have equal length.
  lemma UniformSiblingLength(t: Tumbler)
    requires ValidTumbler(t)
    ensures |IncSibling(t).components| == |t.components|
  { }

  // T10a.2 — Non-nesting sibling prefixes
  // Equal-length distinct tumblers cannot be prefixes of each other.
  lemma NonNestingSiblings(a: Tumbler, b: Tumbler)
    requires |a.components| == |b.components|
    requires a != b
    ensures !IsPrefix(a, b)
    ensures !IsPrefix(b, a)
  { }

  // T10a.3 — Length separation (exact, single level)
  lemma LengthSeparation(t: Tumbler, k: nat)
    requires ValidTumbler(t)
    requires k == 1 || k == 2
    requires k == 1 ==> Zeros(t) <= 3
    requires k == 2 ==> Zeros(t) <= 2
    ensures |IncChild(t, k).components| == |t.components| + k
  { }

  // T10a.3 — Multi-level additive separation
  // Across d nesting levels: #output = m + k'₁ + k'₂ + … + k'_d
  lemma MultiLevelSeparation(base: Tumbler, ks: seq<nat>)
    requires ValidChildChain(base, ks)
    ensures |ChildChain(base, ks).components| == |base.components| + SumNats(ks)
    decreases |ks|
  {
    if |ks| == 0 {
    } else {
      MultiLevelSeparation(IncChild(base, ks[0]), ks[1..]);
    }
  }

  // T10a.4 — T4 preservation under the allocator discipline.
  // inc(·, 0) unconditionally preserves T4 (TA5a, case k = 0).
  lemma IncSiblingPreservesT4(t: Tumbler)
    requires ValidTumbler(t)
    requires SatisfiesT4(t)
    ensures SatisfiesT4(IncSibling(t))
  {
  }

  // inc(·, k') for k' ∈ {1, 2} preserves T4 under TA5a bounds.
  // k=1: appends [1], no new zeros.
  // k=2: appends [0, 1], the zero is preceded by t's non-zero last component.
  lemma IncChildPreservesT4(t: Tumbler, k: nat)
    requires ValidTumbler(t)
    requires SatisfiesT4(t)
    requires k == 1 || k == 2
    requires k == 1 ==> Zeros(t) <= 3
    requires k == 2 ==> Zeros(t) <= 2
    ensures SatisfiesT4(IncChild(t, k))
  {
  }

  // T10a-N — Necessity: relaxing the discipline admits prefix-nested siblings.
  // Under the relaxed rule (any k ≥ 0 in sibling stream), a₁ = inc(b, 0)
  // and a₂ = inc(a₁, k') with k' > 0 satisfy a₁ ≺ a₂:
  // TA5(b): a₂ agrees with a₁ on all positions of a₁.
  // TA5(d): #a₂ = #a₁ + k' > #a₁.
  // This is T1 case (ii), violating the T10 precondition.
  lemma Necessity(b: Tumbler, k: nat)
    requires ValidTumbler(b)
    requires k >= 1
    ensures IsPrefix(IncSibling(b), IncChildRaw(IncSibling(b), k))
    ensures IncSibling(b) != IncChildRaw(IncSibling(b), k)
  {
    var a1 := IncSibling(b);
    var a2 := IncChildRaw(a1, k);
    // a2.components starts with a1.components (by IncChildRaw concatenation)
    assert a2.components == a1.components + seq(k - 1, _ => 0) + [1];
  }
}
