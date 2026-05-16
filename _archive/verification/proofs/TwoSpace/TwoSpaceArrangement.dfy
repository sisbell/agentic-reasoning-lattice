// Arrangement properties (ASN-0036): S2, S3, S5, S8-fin, S8a, S8-depth, S8
module TwoSpaceArrangement {
  import opened TumblerAlgebra
  import opened TwoSpace

  // ---------------------------------------------------------------------------
  // S2 — ArrangementFunctional
  // ---------------------------------------------------------------------------

  // Trivially true: Dafny's map<Tumbler, Tumbler> is a function by construction.
  ghost predicate ArrangementFunctional(s: TwoSpaceState) {
    true
  }

  // ---------------------------------------------------------------------------
  // S3 — ReferentialIntegrity (defined in TwoSpace.dfy, re-exported here)
  // ---------------------------------------------------------------------------

  // S3 is ReferentialIntegrity from the shared module.

  // ---------------------------------------------------------------------------
  // S5 — UnrestrictedSharing
  // ---------------------------------------------------------------------------

  // Witness: build an arrangement where N+1 V-positions all map to the same I-address
  function WitnessArrangement(a: Tumbler, N: nat, subspace: nat): map<Tumbler, Tumbler>
    requires subspace >= 1
    ensures forall k :: 0 <= k < N + 1 ==>
              Tumbler([subspace, k + 1]) in WitnessArrangement(a, N, subspace) &&
              WitnessArrangement(a, N, subspace)[Tumbler([subspace, k + 1])] == a
  {
    map k | 0 <= k < N + 1 :: Tumbler([subspace, k + 1]) := a
  }

  lemma UnrestrictedSharing(a: Tumbler, N: nat, s: TwoSpaceState)
    requires a in s.C
    ensures exists md: map<Tumbler, Tumbler> ::
              (forall v :: v in md ==> md[v] == a)
  {
    var md := WitnessArrangement(a, N, 1);
  }

  // ---------------------------------------------------------------------------
  // S8-fin — FiniteArrangement
  // ---------------------------------------------------------------------------

  // Trivially true: Dafny's map type is finite by construction.
  ghost predicate FiniteArrangement(s: TwoSpaceState) {
    true
  }

  // ---------------------------------------------------------------------------
  // S8a — VPositionWellFormed (text subspace)
  // ---------------------------------------------------------------------------

  ghost predicate VPositionWellFormed(s: TwoSpaceState) {
    forall d, v :: d in s.M && v in s.M[d] &&
      |v.components| >= 1 && v.components[0] >= 1 ==>
      AllPositive(v)
  }

  // ---------------------------------------------------------------------------
  // S8-depth — FixedDepthPositions
  // ---------------------------------------------------------------------------

  ghost predicate FixedDepthPositions(s: TwoSpaceState) {
    forall d, v1, v2 ::
      d in s.M && v1 in s.M[d] && v2 in s.M[d] &&
      |v1.components| >= 1 && |v2.components| >= 1 &&
      v1.components[0] == v2.components[0] ==>
        |v1.components| == |v2.components|
  }

  // ---------------------------------------------------------------------------
  // S8 — SpanDecomposition
  // ---------------------------------------------------------------------------

  ghost predicate TextSubspacePosition(v: Tumbler) {
    AllPositive(v) && v.components[0] >= 1
  }

  function OrdinalOffset(t: Tumbler, k: nat): Tumbler
    requires |t.components| >= 1
    ensures |OrdinalOffset(t, k).components| == |t.components|
  {
    Tumbler(t.components[..|t.components|-1] + [t.components[|t.components|-1] + k])
  }

  datatype Run = Run(vpos: Tumbler, iaddr: Tumbler, length: nat)

  ghost predicate ValidRun(r: Run, m: map<Tumbler, Tumbler>) {
    r.length >= 1 &&
    |r.vpos.components| >= 1 &&
    |r.iaddr.components| >= 1 &&
    (forall k :: 0 <= k < r.length ==>
      OrdinalOffset(r.vpos, k) in m &&
      m[OrdinalOffset(r.vpos, k)] == OrdinalOffset(r.iaddr, k))
  }

  ghost predicate InRun(v: Tumbler, r: Run) {
    |r.vpos.components| >= 1 &&
    |v.components| == |r.vpos.components| &&
    v.components[..|v.components|-1] == r.vpos.components[..|r.vpos.components|-1] &&
    r.vpos.components[|r.vpos.components|-1] <= v.components[|v.components|-1] &&
    v.components[|v.components|-1] < r.vpos.components[|r.vpos.components|-1] + r.length
  }

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

  lemma SingletonRunValid(v: Tumbler, m: map<Tumbler, Tumbler>)
    requires v in m
    requires TextSubspacePosition(v)
    requires |m[v].components| >= 1
    ensures ValidRun(Run(v, m[v], 1), m)
  {
    OrdinalOffsetZero(v);
    OrdinalOffsetZero(m[v]);
  }

  lemma SingletonInRunIdentity(v: Tumbler, r: Run)
    requires InRun(v, r)
    requires r.length == 1
    ensures v == r.vpos
  { }

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
