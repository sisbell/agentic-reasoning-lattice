module Span {
  // T12 — Span
  // span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}

  datatype Tumbler = Tumbler(components: seq<nat>)

  ghost predicate ValidTumbler(t: Tumbler) {
    |t.components| >= 1
  }

  predicate IsPositive(t: Tumbler) {
    exists i :: 0 <= i < |t.components| && t.components[i] != 0
  }

  function FindFirstNonZero(s: seq<nat>, i: nat): (k: nat)
    requires exists j :: i <= j < |s| && s[j] != 0
    ensures i <= k < |s|
    ensures s[k] != 0
    ensures forall j :: i <= j < k ==> s[j] == 0
    decreases |s| - i
  {
    if s[i] != 0 then i
    else FindFirstNonZero(s, i + 1)
  }

  function ActionPoint(w: Tumbler): (k: nat)
    requires ValidTumbler(w)
    requires IsPositive(w)
    ensures k < |w.components|
    ensures w.components[k] != 0
    ensures forall i :: 0 <= i < k ==> w.components[i] == 0
  {
    FindFirstNonZero(w.components, 0)
  }

  ghost predicate LessThan(a: Tumbler, b: Tumbler) {
    exists k :: 0 <= k &&
      (forall i :: 0 <= i < k ==>
        i < |a.components| && i < |b.components| &&
        a.components[i] == b.components[i]) &&
      ((k < |a.components| && k < |b.components| && a.components[k] < b.components[k]) ||
       (k == |a.components| && k < |b.components|))
  }

  ghost predicate LessEqual(a: Tumbler, b: Tumbler) {
    a == b || LessThan(a, b)
  }

  function TumblerAdd(a: Tumbler, w: Tumbler): (r: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(w)
    requires IsPositive(w)
    ensures |r.components| == |w.components|
    ensures ValidTumbler(r)
  {
    var k := ActionPoint(w);
    var prefix := if k <= |a.components| then a.components[..k]
                  else a.components + seq(k - |a.components|, _ => 0);
    var aK := if k < |a.components| then a.components[k] else 0;
    Tumbler(
      prefix + [aK + w.components[k]] + w.components[k+1..]
    )
  }

  ghost function Span(s: Tumbler, len: Tumbler): iset<Tumbler>
    requires ValidTumbler(s)
    requires ValidTumbler(len)
    requires IsPositive(len)
  {
    iset t: Tumbler | ValidTumbler(t) && LessEqual(s, t) && LessThan(t, TumblerAdd(s, len))
  }
}
