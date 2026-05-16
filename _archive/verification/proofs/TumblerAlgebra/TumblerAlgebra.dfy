// Shared definitions for tumbler algebra (ASN-0034). Datatypes, ordering,
// arithmetic, and allocation operations used by all property proof modules.
module TumblerAlgebra {

  // Core datatype
  datatype Tumbler = Tumbler(components: seq<nat>)

  // Role aliases — same datatype, different intent
  type Address = Tumbler
  type Displacement = Tumbler

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

  function ActionPoint(w: Displacement): nat
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
  // LastNonzero — index of last nonzero component (0-indexed)
  // ---------------------------------------------------------------------------

  function LastNonzeroRec(s: seq<nat>, i: nat): nat
    requires 0 < i <= |s|
    requires exists j :: 0 <= j < i && s[j] != 0
    ensures LastNonzeroRec(s, i) < i
    ensures s[LastNonzeroRec(s, i)] != 0
    ensures forall j :: LastNonzeroRec(s, i) < j < i ==> s[j] == 0
    decreases i
  {
    if s[i-1] != 0 then i - 1
    else LastNonzeroRec(s, i - 1)
  }

  function LastNonzero(t: Tumbler): nat
    requires PositiveTumbler(t)
    requires |t.components| > 0
    ensures LastNonzero(t) < |t.components|
    ensures t.components[LastNonzero(t)] != 0
    ensures forall j :: LastNonzero(t) < j < |t.components| ==> t.components[j] == 0
  {
    LastNonzeroRec(t.components, |t.components|)
  }

  // If position s is the last nonzero, LastNonzero returns s
  lemma LastNonzeroAt(t: Tumbler, s: nat)
    requires |t.components| > 0
    requires s < |t.components|
    requires t.components[s] != 0
    requires forall j :: s < j < |t.components| ==> t.components[j] == 0
    ensures PositiveTumbler(t)
    ensures LastNonzero(t) == s
  { }

  // ---------------------------------------------------------------------------
  // FindZero — index of first zero in sequence from position start onward
  // Returns |s| if none found.
  // ---------------------------------------------------------------------------

  function FindZero(s: seq<nat>, start: nat): nat
    requires start <= |s|
    ensures start <= FindZero(s, start) <= |s|
    ensures FindZero(s, start) < |s| ==> s[FindZero(s, start)] == 0
    ensures forall i :: start <= i < FindZero(s, start) ==> s[i] != 0
    decreases |s| - start
  {
    if start == |s| then |s|
    else if s[start] == 0 then start
    else FindZero(s, start + 1)
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

  ghost predicate LessEq(a: Tumbler, b: Tumbler) {
    a == b || LessThan(a, b)
  }

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

  function TumblerAdd(a: Address, w: Displacement): Address
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
  // AllocationInc — hierarchical increment (TA5)
  //
  // k=0: sibling — increment at LastNonzero, same length
  // k>0: child — extend with k-1 zero separators and child value 1
  // ---------------------------------------------------------------------------

  function AllocationInc(t: Address, k: nat): Address
    requires PositiveTumbler(t)
    requires |t.components| > 0
    ensures |AllocationInc(t, k).components| == (if k == 0 then |t.components| else |t.components| + k)
  {
    if k == 0 then
      var s := LastNonzero(t);
      Tumbler(t.components[..s] + [t.components[s] + 1] + t.components[s+1..])
    else
      Tumbler(t.components + Zeros(k - 1) + [1])
  }

  // inc(t, k) is strictly greater than t under T1
  lemma AllocationIncMonotone(t: Address, k: nat)
    requires PositiveTumbler(t)
    requires |t.components| > 0
    ensures LessThan(t, AllocationInc(t, k))
  {
    if k == 0 {
      LessThanIntro(t, AllocationInc(t, 0), LastNonzero(t));
    } else {
      LessThanIntro(t, AllocationInc(t, k), |t.components|);
    }
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

  // ---------------------------------------------------------------------------
  // SubtractResultAt — characterize each component of TumblerSubtract
  // ---------------------------------------------------------------------------

  lemma SubtractResultAt(x: Tumbler, w: Tumbler, i: nat)
    requires Subtractable(x, w)
    requires i < Max(|x.components|, |w.components|)
    ensures var len := Max(|x.components|, |w.components|);
            var px := Pad(x.components, len);
            var pw := Pad(w.components, len);
            TumblerSubtract(x, w).components[i] ==
              (if px == pw then 0
               else if i < FirstDiff(px, pw) then 0
               else if i == FirstDiff(px, pw) then px[i] - pw[i]
               else px[i])
  {
    var len := Max(|x.components|, |w.components|);
    var px := Pad(x.components, len);
    var pw := Pad(w.components, len);
    if px == pw {
    } else {
      var d := FirstDiff(px, pw);
      var result := Zeros(d) + [px[d] - pw[d]] + px[d+1..];
      assert TumblerSubtract(x, w) == Tumbler(result);
      if i < d {
      } else if i == d {
      } else {
        assert result[i] == px[i];
      }
    }
  }
}
