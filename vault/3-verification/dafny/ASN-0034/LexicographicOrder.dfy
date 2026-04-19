include "./CarrierSetDefinition.dfy"

module LexicographicOrder {
  // T1 — LexicographicOrder
  // a < b iff ∃ k ≥ 1 with (A i : 1 ≤ i < k : aᵢ = bᵢ)
  // and either (i) k ≤ min(m,n) ∧ aₖ < bₖ, or (ii) k = m+1 ≤ n.

  import opened CarrierSetDefinition

  ghost predicate LessThan(a: Tumbler, b: Tumbler) {
    exists k :: 0 <= k &&
      (forall i :: 0 <= i < k ==>
        i < |a.components| && i < |b.components| &&
        a.components[i] == b.components[i]) &&
      ((k < |a.components| && k < |b.components| && a.components[k] < b.components[k]) ||
       (k == |a.components| && k < |b.components|))
  }

  // (a) Irreflexivity — (A a ∈ T :: ¬(a < a))
  lemma LessThanIrreflexive(a: Tumbler)
    ensures !LessThan(a, a)
  {
  }

  // First position where a and b differ, or min(|a|,|b|) if all shared positions agree
  ghost function FirstDivergence(a: seq<nat>, b: seq<nat>, pos: nat): nat
    requires pos <= |a| && pos <= |b|
    decreases |a| - pos
  {
    if pos == |a| || pos == |b| then pos
    else if a[pos] != b[pos] then pos
    else FirstDivergence(a, b, pos + 1)
  }

  lemma FirstDivergenceProperties(a: seq<nat>, b: seq<nat>, pos: nat)
    requires pos <= |a| && pos <= |b|
    decreases |a| - pos
    ensures var k := FirstDivergence(a, b, pos);
      pos <= k <= (if |a| <= |b| then |a| else |b|) &&
      (forall i :: pos <= i < k ==> i < |a| && i < |b| && a[i] == b[i]) &&
      (k < |a| && k < |b| ==> a[k] != b[k])
  {
    if pos == |a| || pos == |b| {
    } else if a[pos] != b[pos] {
    } else {
      FirstDivergenceProperties(a, b, pos + 1);
    }
  }

  // (b) Trichotomy — exactly one of a < b, a = b, b < a
  lemma LessThanTrichotomy(a: Tumbler, b: Tumbler)
    ensures LessThan(a, b) || a == b || LessThan(b, a)
    ensures !(LessThan(a, b) && a == b)
    ensures !(LessThan(b, a) && a == b)
    ensures !(LessThan(a, b) && LessThan(b, a))
  {
    var k := FirstDivergence(a.components, b.components, 0);
    FirstDivergenceProperties(a.components, b.components, 0);
    if k < |a.components| && k < |b.components| {
      if a.components[k] < b.components[k] {
        assert LessThan(a, b);
      } else {
        assert LessThan(b, a);
      }
    } else if k == |a.components| && k == |b.components| {
      assert a.components == b.components;
    } else if k == |a.components| && k < |b.components| {
      assert LessThan(a, b);
    } else {
      assert k < |a.components| && k == |b.components|;
      assert LessThan(b, a);
    }
    LessThanIrreflexive(a);
    LessThanIrreflexive(b);
  }

  // (c) Transitivity — (A a,b,c ∈ T : a < b ∧ b < c : a < c)
  lemma LessThanTransitive(a: Tumbler, b: Tumbler, c: Tumbler)
    requires LessThan(a, b) && LessThan(b, c)
    ensures LessThan(a, c)
  {
  }
}
