include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// S8 — SpanDecomposition
module SpanDecomposition {
  import opened TumblerAlgebra

  // V-position well-formedness (from S8a)
  ghost predicate AllPositive(t: Tumbler) {
    |t.components| >= 1 &&
    forall i :: 0 <= i < |t.components| ==> t.components[i] > 0
  }

  // Text-subspace V-position: first component >= 1, all positive
  ghost predicate TextSubspacePosition(v: Tumbler) {
    AllPositive(v) && v.components[0] >= 1
  }

  // Ordinal offset: increment last component by k
  function OrdinalOffset(t: Tumbler, k: nat): Tumbler
    requires |t.components| >= 1
    ensures |OrdinalOffset(t, k).components| == |t.components|
  {
    Tumbler(t.components[..|t.components|-1] + [t.components[|t.components|-1] + k])
  }

  // Correspondence run (Definition — CorrespondenceRun)
  datatype Run = Run(vpos: Tumbler, iaddr: Tumbler, length: nat)

  // A run is valid w.r.t. arrangement m
  ghost predicate ValidRun(r: Run, m: map<Tumbler, Tumbler>) {
    r.length >= 1 &&
    |r.vpos.components| >= 1 &&
    |r.iaddr.components| >= 1 &&
    (forall k :: 0 <= k < r.length ==>
      OrdinalOffset(r.vpos, k) in m &&
      m[OrdinalOffset(r.vpos, k)] == OrdinalOffset(r.iaddr, k))
  }

  // v falls within the range of run r
  ghost predicate InRun(v: Tumbler, r: Run) {
    |r.vpos.components| >= 1 &&
    |v.components| == |r.vpos.components| &&
    v.components[..|v.components|-1] == r.vpos.components[..|r.vpos.components|-1] &&
    r.vpos.components[|r.vpos.components|-1] <= v.components[|v.components|-1] &&
    v.components[|v.components|-1] < r.vpos.components[|r.vpos.components|-1] + r.length
  }

  // Runs form a valid decomposition: all valid, partition text V-positions
  ghost predicate Decomposable(runs: set<Run>, m: map<Tumbler, Tumbler>) {
    (forall r :: r in runs ==> ValidRun(r, m)) &&
    (forall v :: v in m && TextSubspacePosition(v) ==>
      exists r :: r in runs && InRun(v, r)) &&
    (forall v, r1, r2 ::
      (r1 in runs && r2 in runs && InRun(v, r1) && InRun(v, r2)) ==> r1 == r2)
  }

  lemma OrdinalOffsetZero(t: Tumbler)
    requires |t.components| >= 1
    ensures OrdinalOffset(t, 0) == t
  { }

  // Singleton runs at k=0 reduce to identity: M(v) = M(v)
  lemma SingletonRunValid(v: Tumbler, m: map<Tumbler, Tumbler>)
    requires v in m
    requires TextSubspacePosition(v)
    requires |m[v].components| >= 1
    ensures ValidRun(Run(v, m[v], 1), m)
  {
    OrdinalOffsetZero(v);
    OrdinalOffsetZero(m[v]);
  }

  // InRun with length 1 forces v == r.vpos
  lemma SingletonInRunIdentity(v: Tumbler, r: Run)
    requires InRun(v, r)
    requires r.length == 1
    ensures v == r.vpos
  { }

  // S8 — SpanDecomposition
  // Degenerate decomposition: each V-position v forms singleton run (v, M(v), 1).
  // Derived from S8-fin (finiteness — automatic for Dafny maps), S8a
  // (well-formed positions), S2 (functional — automatic for Dafny maps),
  // and S8-depth.
  lemma SpanDecomposition(m: map<Tumbler, Tumbler>)
    requires forall v :: v in m ==> |m[v].components| >= 1
    ensures exists runs: set<Run> :: Decomposable(runs, m)
  {
    var runs := set v | v in m && TextSubspacePosition(v) :: Run(v, m[v], 1);

    forall r | r in runs
      ensures ValidRun(r, m)
    {
      var v :| v in m && TextSubspacePosition(v) && r == Run(v, m[v], 1);
      SingletonRunValid(v, m);
    }

    forall v | v in m && TextSubspacePosition(v)
      ensures exists r :: r in runs && InRun(v, r)
    {
      assert Run(v, m[v], 1) in runs;
    }

    forall v, r1, r2 | r1 in runs && r2 in runs && InRun(v, r1) && InRun(v, r2)
      ensures r1 == r2
    {
      SingletonInRunIdentity(v, r1);
      SingletonInRunIdentity(v, r2);
    }

    assert Decomposable(runs, m);
  }
}
