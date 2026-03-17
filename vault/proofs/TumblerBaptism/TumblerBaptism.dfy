// Shared definitions for tumbler baptism (ASN-0040). Stream elements,
// namespace membership, children, high water mark, next address,
// validity predicates, and state model.
module TumblerBaptism {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // ---------------------------------------------------------------------------
  // StreamElement — closed-form n-th element of sibling stream S(p, d)
  // ---------------------------------------------------------------------------

  function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  // ---------------------------------------------------------------------------
  // InStream — membership in sibling stream S(p, d)
  // ---------------------------------------------------------------------------

  ghost predicate InStream(t: Tumbler, p: Tumbler, d: nat) {
    d >= 1 &&
    |t.components| == |p.components| + d &&
    t.components[..|p.components|] == p.components &&
    (forall i :: |p.components| <= i < |p.components| + d - 1 ==> t.components[i] == 0) &&
    t.components[|t.components| - 1] >= 1
  }

  // ---------------------------------------------------------------------------
  // Children — baptized elements in a namespace
  // ---------------------------------------------------------------------------

  ghost function Children(B: set<Tumbler>, p: Tumbler, d: nat): set<Tumbler> {
    set t | t in B && InStream(t, p, d)
  }

  // ---------------------------------------------------------------------------
  // ValidBaptism — precondition for baptism (B6)
  // ---------------------------------------------------------------------------

  ghost predicate ValidBaptism(p: Tumbler, d: nat) {
    TumblerHierarchy.ValidAddress(p) &&
    1 <= d <= 2 &&
    TumblerHierarchy.ZeroCount(p.components) + (d - 1) <= 3
  }

  // ---------------------------------------------------------------------------
  // Next — deterministic next address in a namespace (B2)
  // ---------------------------------------------------------------------------

  ghost function Next(B: set<Tumbler>, p: Tumbler, d: nat): Tumbler
    requires d >= 1
  {
    StreamElement(p, d, |Children(B, p, d)| + 1)
  }

  // ---------------------------------------------------------------------------
  // BaptismState — the baptismal registry
  // ---------------------------------------------------------------------------

  datatype BaptismState = BaptismState(B: set<Tumbler>)

  // ---------------------------------------------------------------------------
  // Baptize — the operation
  // ---------------------------------------------------------------------------

  ghost function Baptize(s: BaptismState, p: Tumbler, d: nat): BaptismState
    requires ValidBaptism(p, d)
  {
    BaptismState(s.B + {Next(s.B, p, d)})
  }

  // ---------------------------------------------------------------------------
  // StreamMatchesInc — equivalence between closed form and AllocationInc
  // ---------------------------------------------------------------------------

  lemma StreamMatchesInc(p: Tumbler, d: nat, n: nat)
    requires PositiveTumbler(p)
    requires |p.components| > 0
    requires d >= 1
    requires n >= 1
    ensures StreamElement(p, d, 1) == AllocationInc(p, d)
    ensures n >= 2 ==>
      PositiveTumbler(StreamElement(p, d, n - 1)) &&
      |StreamElement(p, d, n - 1).components| > 0 &&
      StreamElement(p, d, n) == AllocationInc(StreamElement(p, d, n - 1), 0)
  {
    if n >= 2 {
      var prev := StreamElement(p, d, n - 1);
      var last := |prev.components| - 1;
      assert prev.components[last] == n - 1;
      LastNonzeroAt(prev, last);
    }
  }
}
