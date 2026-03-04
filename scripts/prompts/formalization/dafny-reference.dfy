// Reference Dafny module: demonstrates idiomatic patterns
// (datatype, function, predicate, lemma, ghost, seq, quantifiers)

module DafnyReference {

  // --- Datatypes ---

  datatype Color = Red | Green | Blue
  datatype Pair = Pair(fst: nat, snd: nat)
  datatype Tree = Leaf | Node(left: Tree, val: nat, right: Tree)

  // --- Sequences ---

  // Length, index, slice, concatenate
  function SeqOps(s: seq<nat>): nat
    requires |s| >= 3
  {
    s[0] + s[1] + |s[1..3]|   // index, slice, length
  }

  // Build a sequence from a function
  function Iota(n: nat): seq<nat> {
    seq(n, i => i)
  }

  // Functional update — Dafny has NO s[i := v] syntax for sequences
  function ReplaceAt(s: seq<nat>, i: nat, v: nat): seq<nat>
    requires i < |s|
    ensures |ReplaceAt(s, i, v)| == |s|
    ensures ReplaceAt(s, i, v)[i] == v
    ensures forall j :: 0 <= j < |s| && j != i ==> ReplaceAt(s, i, v)[j] == s[j]
  {
    s[..i] + [v] + s[i+1..]
  }

  // Append, prepend
  function Append(s: seq<nat>, v: nat): seq<nat>
    ensures |Append(s, v)| == |s| + 1
  {
    s + [v]
  }

  // Zero-pad to length n
  function Pad(s: seq<nat>, n: nat): seq<nat>
    requires n >= |s|
    ensures |Pad(s, n)| == n
  {
    s + seq(n - |s|, _ => 0)
  }

  // --- Predicates ---

  // Regular predicate: body is computable
  predicate IsSorted(s: seq<nat>) {
    forall i, j :: 0 <= i < j < |s| ==> s[i] <= s[j]
  }

  // Ghost predicate: body has unbounded quantifiers over non-finite domains
  ghost predicate Unbounded(s: seq<nat>) {
    forall i :: 0 <= i < |s| ==>
      exists t: seq<nat> :: |t| == |s| && t[i] > s[i]
  }

  // --- Functions ---

  // Pure function with requires/ensures
  function Max(a: nat, b: nat): nat
    ensures Max(a, b) >= a
    ensures Max(a, b) >= b
  {
    if a >= b then a else b
  }

  // Recursive function with decreases
  function Sum(s: seq<nat>): nat
    decreases |s|
  {
    if |s| == 0 then 0
    else s[0] + Sum(s[1..])
  }

  // --- Lemmas ---

  // Simple lemma — verifier proves automatically
  lemma MaxCommutative(a: nat, b: nat)
    ensures Max(a, b) == Max(b, a)
  { }

  // Lemma with explicit witness for existential
  lemma WitnessExample(s: seq<nat>, i: nat)
    requires i < |s|
    ensures exists t: seq<nat> :: |t| == |s| && t[i] > s[i]
  {
    // Construct the witness explicitly
    var t := s[..i] + [s[i] + 1] + s[i+1..];
    assert |t| == |s|;
    assert t[i] == s[i] + 1 > s[i];
  }

  // Forall-ensures pattern
  lemma AllNatsNonNeg(s: seq<nat>)
    ensures forall i :: 0 <= i < |s| ==> s[i] >= 0
  {
    forall i | 0 <= i < |s|
      ensures s[i] >= 0
    { }
  }

  // Lemma with assert hints for intermediate steps
  lemma ReplacePreservesLength(s: seq<nat>, i: nat, v: nat)
    requires i < |s|
    ensures |s[..i] + [v] + s[i+1..]| == |s|
  {
    assert |s[..i]| == i;
    assert |[v]| == 1;
    assert |s[i+1..]| == |s| - i - 1;
  }

  // Inductive lemma
  lemma SumAppend(s: seq<nat>, v: nat)
    ensures Sum(s + [v]) == Sum(s) + v
    decreases |s|
  {
    if |s| == 0 {
      assert s + [v] == [v];
    } else {
      calc {
        Sum(s + [v]);
        == (s + [v])[0] + Sum((s + [v])[1..]);
        == { assert (s + [v])[0] == s[0];
             assert (s + [v])[1..] == s[1..] + [v]; }
           s[0] + Sum(s[1..] + [v]);
        == { SumAppend(s[1..], v); }
           s[0] + Sum(s[1..]) + v;
        == Sum(s) + v;
      }
    }
  }
}
