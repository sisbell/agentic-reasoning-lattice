// Registry properties (ASN-0040): B0, B0a, B₀ conf., B1, B2, B4, B6, B8, B9, B10,
// Bop (RegistryGrowth), Bop (OnlyRegistryModified)
module BaptismRegistry {
  import opened TumblerAlgebra
  import opened TumblerBaptism
  import TumblerHierarchy
  import TumblerAllocation
  import BaptismBranching

  // ---------------------------------------------------------------------------
  // B0 — Irrevocability
  // ---------------------------------------------------------------------------

  ghost predicate Irrevocable(s: BaptismState, s': BaptismState) {
    s.B <= s'.B
  }

  lemma IrrevocableTransitive(s1: BaptismState, s2: BaptismState, s3: BaptismState)
    requires Irrevocable(s1, s2)
    requires Irrevocable(s2, s3)
    ensures Irrevocable(s1, s3)
  { }

  // ---------------------------------------------------------------------------
  // B0a — BaptismalClosure
  // ---------------------------------------------------------------------------

  ghost predicate ProducedByBaptism(B: set<Tumbler>, p: Tumbler, d: nat, t: Tumbler) {
    ValidBaptism(p, d) &&
    InStream(t, p, d) &&
    t == Next(B, p, d)
  }

  ghost predicate BaptismalClosure(before: BaptismState, after: BaptismState) {
    forall t :: t in after.B && t !in before.B ==>
      exists p: Tumbler, d: nat :: ProducedByBaptism(before.B, p, d, t)
  }

  // ---------------------------------------------------------------------------
  // B₀ — SeedConformance
  // ---------------------------------------------------------------------------

  ghost predicate SeedConformance(B0: set<Tumbler>) {
    (forall t :: t in B0 ==> TumblerHierarchy.ValidAddress(t)) &&
    (forall p: Tumbler, d: nat, n: nat ::
      d >= 1 && n >= 1 && StreamElement(p, d, n) in B0 ==>
      forall i :: 1 <= i < n ==> StreamElement(p, d, i) in B0)
  }

  // ---------------------------------------------------------------------------
  // B1 — ContiguousPrefix
  // ---------------------------------------------------------------------------

  ghost predicate ContiguousPrefix(B: set<Tumbler>) {
    forall p: Tumbler, d: nat, n: nat ::
      d >= 1 && n >= 1 && StreamElement(p, d, n) in B ==>
      forall i :: 1 <= i < n ==> StreamElement(p, d, i) in B
  }

  // ---------------------------------------------------------------------------
  // B2 — HighWaterMarkSufficiency
  // ---------------------------------------------------------------------------

  lemma HighWaterMarkSufficiency(p: Tumbler, d: nat, m: nat)
    requires PositiveTumbler(p)
    requires |p.components| > 0
    requires d >= 1
    requires m >= 0
    ensures m == 0 ==> StreamElement(p, d, 1) == AllocationInc(p, d)
    ensures m >= 1 ==>
      PositiveTumbler(StreamElement(p, d, m)) &&
      |StreamElement(p, d, m).components| > 0 &&
      StreamElement(p, d, m + 1) == AllocationInc(StreamElement(p, d, m), 0)
  {
    StreamMatchesInc(p, d, if m == 0 then 1 else m + 1);
  }

  // ---------------------------------------------------------------------------
  // B4 — NamespaceSerialized
  // ---------------------------------------------------------------------------

  datatype Namespace = Namespace(parent: Tumbler, depth: nat)

  datatype BaptismEvent = BaptismEvent(
    ns: Namespace,
    readRegistry: set<Tumbler>,
    commitRegistry: set<Tumbler>
  )

  ghost predicate CommitPrecedesRead(e1: BaptismEvent, e2: BaptismEvent) {
    e1.commitRegistry <= e2.readRegistry
  }

  ghost predicate Serialized(trace: seq<BaptismEvent>) {
    forall i, j :: 0 <= i < j < |trace| &&
      trace[i].ns == trace[j].ns ==>
      CommitPrecedesRead(trace[i], trace[j])
  }

  // ---------------------------------------------------------------------------
  // B6 — ValidDepth (defined in TumblerBaptism.dfy as ValidBaptism)
  // ---------------------------------------------------------------------------

  // ValidBaptism is the canonical B6 predicate, defined in TumblerBaptism.dfy.

  // ---------------------------------------------------------------------------
  // B8 — GlobalUniqueness
  // ---------------------------------------------------------------------------

  lemma GlobalUniqueness(
    p1: Tumbler, d1: nat, n1: nat,
    p2: Tumbler, d2: nat, n2: nat
  )
    requires ValidBaptism(p1, d1)
    requires ValidBaptism(p2, d2)
    requires n1 >= 1 && n2 >= 1
    requires p1 != p2 || d1 != d2 || n1 != n2
    ensures StreamElement(p1, d1, n1) != StreamElement(p2, d2, n2)
  {
    if p1 != p2 || d1 != d2 {
      BaptismBranching.NamespaceDisjointness(p1, d1, p2, d2, n1, n2);
    } else {
      // Same namespace, different index
      if n1 < n2 {
        BaptismBranching.StreamStrictlyOrdered(p1, d1, n1, n2);
      } else {
        BaptismBranching.StreamStrictlyOrdered(p1, d1, n2, n1);
      }
    }
  }

  // ---------------------------------------------------------------------------
  // B9 — UnboundedExtent
  // ---------------------------------------------------------------------------

  lemma UnboundedExtent(p: Tumbler, d: nat, M: nat)
    requires d >= 1
    requires M >= 1
    ensures forall i, j :: 1 <= i < j <= M ==>
              StreamElement(p, d, i) != StreamElement(p, d, j)
  {
    forall i, j | 1 <= i < j <= M
      ensures StreamElement(p, d, i) != StreamElement(p, d, j)
    {
      var ei := StreamElement(p, d, i);
      var ej := StreamElement(p, d, j);
      var last := |p.components| + d - 1;
      assert ei.components[last] == i;
      assert ej.components[last] == j;
    }
  }

  // ---------------------------------------------------------------------------
  // B10 — RegistryT4Validity
  // ---------------------------------------------------------------------------

  ghost predicate AllValid(B: set<Tumbler>) {
    forall t :: t in B ==> TumblerHierarchy.ValidAddress(t)
  }

  lemma ValidImpliesPositive(t: Tumbler)
    requires TumblerHierarchy.ValidAddress(t)
    ensures PositiveTumbler(t)
    ensures |t.components| > 0
  {
    assert t.components[0] != 0;
  }

  lemma FirstChildValid(p: Tumbler, d: nat)
    requires ValidBaptism(p, d)
    ensures TumblerHierarchy.ValidAddress(AllocationInc(p, d))
  {
    ValidImpliesPositive(p);
    TumblerAllocation.IncrementPreservesValidity(p, d);
  }

  lemma NextSiblingValid(t: Tumbler)
    requires TumblerHierarchy.ValidAddress(t)
    ensures TumblerHierarchy.ValidAddress(AllocationInc(t, 0))
  {
    ValidImpliesPositive(t);
    TumblerAllocation.IncrementPreservesValidity(t, 0);
  }

  lemma RegistryT4Validity(
    B: set<Tumbler>, p: Tumbler, d: nat,
    maxChild: Tumbler, childrenEmpty: bool
  )
    requires AllValid(B)
    requires TumblerHierarchy.ValidAddress(p)
    requires d == 1 || d == 2
    requires TumblerHierarchy.ZeroCount(p.components) + (d - 1) <= 3
    requires !childrenEmpty ==> maxChild in B
    ensures childrenEmpty ==>
              TumblerHierarchy.ValidAddress(AllocationInc(p, d)) &&
              AllValid(B + {AllocationInc(p, d)})
    ensures !childrenEmpty ==>
              TumblerHierarchy.ValidAddress(AllocationInc(maxChild, 0)) &&
              AllValid(B + {AllocationInc(maxChild, 0)})
  {
    if childrenEmpty {
      FirstChildValid(p, d);
    } else {
      NextSiblingValid(maxChild);
    }
  }

  // ---------------------------------------------------------------------------
  // Bop (POST) — RegistryGrowth
  // ---------------------------------------------------------------------------

  ghost predicate RegistryGrowth(s: BaptismState, s': BaptismState, p: Tumbler, d: nat)
    requires ValidBaptism(p, d)
  {
    s'.B == s.B + {Next(s.B, p, d)}
  }

  // ---------------------------------------------------------------------------
  // Bop (FRAME) — OnlyRegistryModified
  // ---------------------------------------------------------------------------

  datatype SystemState<R> = SystemState(B: set<Tumbler>, rest: R)

  ghost predicate OnlyRegistryModified<R>(s: SystemState<R>, s': SystemState<R>) {
    s'.rest == s.rest
  }
}
