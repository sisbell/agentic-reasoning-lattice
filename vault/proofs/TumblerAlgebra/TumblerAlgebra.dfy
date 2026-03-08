module TumblerAlgebra {

  // Core datatype
  datatype Tumbler = Tumbler(components: seq<nat>)

  // ---------------------------------------------------------------------------
  // Utility helpers
  // ---------------------------------------------------------------------------

  function Max(a: nat, b: nat): nat {
    if a >= b then a else b
  }

  // Zero-pad a sequence to length n
  function Pad(s: seq<nat>, n: nat): seq<nat>
    requires n >= |s|
    ensures |Pad(s, n)| == n
    ensures forall i :: 0 <= i < |s| ==> Pad(s, n)[i] == s[i]
    ensures forall i :: |s| <= i < n ==> Pad(s, n)[i] == 0
  {
    s + seq(n - |s|, i => 0)
  }

  // Sequence of n zeros
  function Zeros(n: nat): seq<nat>
    ensures |Zeros(n)| == n
    ensures forall i :: 0 <= i < n ==> Zeros(n)[i] == 0
  {
    seq(n, i => 0)
  }

  // ---------------------------------------------------------------------------
  // PositiveTumbler — at least one nonzero component
  // ---------------------------------------------------------------------------

  ghost predicate PositiveTumbler(t: Tumbler) {
    exists i :: 0 <= i < |t.components| && t.components[i] != 0
  }

  // ---------------------------------------------------------------------------
  // ActionPoint — index of first nonzero component (0-indexed)
  // ---------------------------------------------------------------------------

  function ActionPoint(w: Tumbler): nat
    requires PositiveTumbler(w)
    ensures ActionPoint(w) < |w.components|
    ensures w.components[ActionPoint(w)] != 0
    ensures forall j :: 0 <= j < ActionPoint(w) ==> w.components[j] == 0
  {
    ActionPointRec(w.components, 0)
  }

  function ActionPointRec(s: seq<nat>, i: nat): nat
    requires i <= |s|
    requires exists j :: i <= j < |s| && s[j] != 0
    ensures i <= ActionPointRec(s, i) < |s|
    ensures s[ActionPointRec(s, i)] != 0
    ensures forall j :: i <= j < ActionPointRec(s, i) ==> s[j] == 0
    decreases |s| - i
  {
    if s[i] != 0 then i
    else ActionPointRec(s, i + 1)
  }

  // ---------------------------------------------------------------------------
  // FirstDiff — index of first position where two equal-length sequences differ
  // ---------------------------------------------------------------------------

  function FirstDiff(a: seq<nat>, b: seq<nat>): nat
    requires |a| == |b|
    requires a != b
    ensures FirstDiff(a, b) < |a|
    ensures a[FirstDiff(a, b)] != b[FirstDiff(a, b)]
    ensures forall j :: 0 <= j < FirstDiff(a, b) ==> a[j] == b[j]
  {
    FirstDiffRec(a, b, 0)
  }

  function FirstDiffRec(a: seq<nat>, b: seq<nat>, i: nat): nat
    requires |a| == |b|
    requires i <= |a|
    requires exists j :: i <= j < |a| && a[j] != b[j]
    ensures i <= FirstDiffRec(a, b, i) < |a|
    ensures a[FirstDiffRec(a, b, i)] != b[FirstDiffRec(a, b, i)]
    ensures forall j :: i <= j < FirstDiffRec(a, b, i) ==> a[j] == b[j]
    decreases |a| - i
  {
    if a[i] != b[i] then i
    else FirstDiffRec(a, b, i + 1)
  }

  // ---------------------------------------------------------------------------
  // T1 — Lexicographic ordering
  //
  // a < b iff there exists k such that all components before k agree and either:
  //   (i)  both have a k-th component and a[k] < b[k], or
  //   (ii) a is a proper prefix of b (a has exactly k components, b has more)
  // ---------------------------------------------------------------------------

  // Witness predicate: the body of the LessThan existential, named so Z3
  // can use it as a trigger. Without this, the nested forall inside exists
  // leaves Z3 without a matching pattern, causing proof failures in larger
  // project contexts.
  ghost predicate LessThanAt(a: Tumbler, b: Tumbler, k: nat) {
    k <= |a.components| && k <= |b.components| &&
    (forall i :: 0 <= i < k ==> a.components[i] == b.components[i]) &&
    ((k < |a.components| && k < |b.components| && a.components[k] < b.components[k]) ||
     (k == |a.components| && k < |b.components|))
  }

  ghost predicate LessThan(a: Tumbler, b: Tumbler) {
    exists k: nat :: LessThanAt(a, b, k)
  }

  // Introduction lemma: provide an explicit witness k to prove LessThan
  lemma LessThanIntro(a: Tumbler, b: Tumbler, k: nat)
    requires LessThanAt(a, b, k)
    ensures LessThan(a, b)
  {}

  // ---------------------------------------------------------------------------
  // Prefix relation — p is a prefix of t
  // ---------------------------------------------------------------------------

  ghost predicate IsPrefix(p: Tumbler, t: Tumbler) {
    |p.components| <= |t.components| &&
    forall i :: 0 <= i < |p.components| ==> p.components[i] == t.components[i]
  }

  // ---------------------------------------------------------------------------
  // TumblerAdd — piecewise addition (⊕)
  //
  // Given start position a and positive displacement w with action point k:
  //   r[i] = a[i]         if i < k     (copy prefix from start)
  //   r[k] = a[k] + w[k]               (single-component advance)
  //   r[i] = w[i]         if i > k     (copy suffix from displacement)
  // Result length = |w.components|
  // ---------------------------------------------------------------------------

  function TumblerAdd(a: Tumbler, w: Tumbler): Tumbler
    requires PositiveTumbler(w)
    requires ActionPoint(w) < |a.components|
  {
    var k := ActionPoint(w);
    Tumbler(
      a.components[..k] +
      [a.components[k] + w.components[k]] +
      w.components[k+1..]
    )
  }

  // ---------------------------------------------------------------------------
  // Subtractable — precondition for TumblerSubtract
  //
  // After zero-padding both operands to the same length, for any divergence
  // point k the end position's component must be >= the displacement's.
  // ---------------------------------------------------------------------------

  ghost predicate Subtractable(a: Tumbler, w: Tumbler) {
    var len := Max(|a.components|, |w.components|);
    var pa := Pad(a.components, len);
    var pw := Pad(w.components, len);
    forall k :: 0 <= k < len &&
      (forall j :: 0 <= j < k ==> pa[j] == pw[j]) &&
      pa[k] != pw[k]
      ==> pa[k] >= pw[k]
  }

  // ---------------------------------------------------------------------------
  // TumblerSubtract — piecewise subtraction (⊖)
  //
  // Given end position a and displacement w, zero-pad to max length.
  // If equal after padding, result is the zero tumbler.
  // Otherwise let k be first divergence point:
  //   r[i] = 0            if i < k     (matched levels zeroed)
  //   r[k] = a[k] - w[k]               (reverse the advance)
  //   r[i] = a[i]         if i > k     (copy from end position)
  // Result length = max(|a|, |w|)
  // ---------------------------------------------------------------------------

  function TumblerSubtract(a: Tumbler, w: Tumbler): Tumbler
    requires Subtractable(a, w)
  {
    var len := Max(|a.components|, |w.components|);
    var pa := Pad(a.components, len);
    var pw := Pad(w.components, len);
    if pa == pw then
      Tumbler(Zeros(len))
    else
      var k := FirstDiff(pa, pw);
      Tumbler(Zeros(k) + [pa[k] - pw[k]] + pa[k+1..])
  }
}
