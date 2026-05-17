// ASN-0034: T10a.5 — CrossAllocatorIncomparability (LEMMA, corollary)
// Allocators X and Y on the same allocator tree (Root(X) == Root(Y)) that
// are not in an ancestor–descendant relationship produce mutually
// prefix-incomparable outputs.
//   Strong induction on Depth(X) + Depth(Y). Base case: X and Y share a
//   parent — differing spawn points use T10a.2; same spawn point with
//   differing spawn params is forced apart by T4 (last component nonzero)
//   versus inc(·, 2) filler zero. Inductive cases (different depths or
//   different equal-depth parents) reduce to ancestors and lift via
//   component preservation across inc(·, k).
include "./AllocatorDiscipline.dfy"
include "./UniformSiblingLength.dfy"
include "./LengthSeparation.dfy"
include "./NonNestingSiblingPrefixes.dfy"
include "./T4PreservationUnderDiscipline.dfy"
include "./HierarchicalParsing.dfy"
include "./HierarchicalIncrement.dfy"
include "./LastSignificantPosition.dfy"
include "./SigOnValidAddresses.dfy"
include "./PrefixRelation.dfy"

module CrossAllocatorIncomparability {
  import opened AllocatorDiscipline
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened PrefixRelation
  import opened LengthSeparation
  import opened HierarchicalParsing
  import opened HierarchicalIncrement
  import opened LastSignificantPosition
  import opened SigOnValidAddresses
  import USL = UniformSiblingLength
  import NNSP = NonNestingSiblingPrefixes
  import T4PD = T4PreservationUnderDiscipline

  // Equal-depth nodes on a shared lineage must coincide.
  lemma OnLineageEqualDepthIsEqual(a: Allocator, b: Allocator)
    requires OnLineage(a, b)
    requires Depth(a) == Depth(b)
    ensures a == b
    decreases b
  {
    if a != b {
      OnLineageDepth(a, b.parent);
    }
  }

  // Sibling outputs preserve the spawn point on positions
  // [1..Length(spawnPt)] and have length Length(spawnPt) + spawnParam.
  lemma SiblingPrefixMatchesSpawnPt(a: Allocator, n: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    requires a.ChildAllocator?
    ensures InT(SiblingAt(a, n))
    ensures Length(SiblingAt(a, n)) == Length(a.spawnPt) + a.spawnParam
    ensures forall i :: 1 <= i <= Length(a.spawnPt) ==>
              Component(SiblingAt(a, n), i) == Component(a.spawnPt, i)
    decreases n
  {
    USL.SiblingInT(a, n);
    if n == 0 {
      assert SiblingAt(a, 0) == BaseAddress(a);
      assert BaseAddress(a) ==
        HierarchicalIncrement.HierarchicalIncrement(a.spawnPt, a.spawnParam);
      assert a.spawnParam >= 1;
    } else {
      SiblingPrefixMatchesSpawnPt(a, n - 1);
      var prev := SiblingAt(a, n - 1);
      T4PD.SiblingT4(a, n - 1);
      SigOnValidAddresses.SigOnValidAddresses(prev);
      assert SiblingAt(a, n) == HierarchicalIncrement.HierarchicalIncrement(prev, 0);
      assert Length(prev) == Length(a.spawnPt) + a.spawnParam;
      assert a.spawnParam >= 1;
      forall i | 1 <= i <= Length(a.spawnPt)
        ensures Component(SiblingAt(a, n), i) == Component(a.spawnPt, i)
      {
        assert i <= Length(a.spawnPt) < Length(prev);
        assert i != LastSignificantPosition.LastSignificantPosition(prev);
      }
    }
  }

  // For spawnParam == 2, position Length(spawnPt) + 1 of every sibling
  // is zero (the filler from inc(spawnPt, 2), preserved by subsequent
  // inc(·, 0) which only modifies the final non-zero position).
  lemma SiblingFillerZero(a: Allocator, n: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    requires a.ChildAllocator?
    requires a.spawnParam == 2
    ensures InT(SiblingAt(a, n))
    ensures Length(SiblingAt(a, n)) == Length(a.spawnPt) + 2
    ensures Component(SiblingAt(a, n), Length(a.spawnPt) + 1) == 0
    decreases n
  {
    USL.SiblingInT(a, n);
    SiblingPrefixMatchesSpawnPt(a, n);
    var p := Length(a.spawnPt) + 1;
    if n == 0 {
      assert SiblingAt(a, 0) == BaseAddress(a);
      assert BaseAddress(a) ==
        HierarchicalIncrement.HierarchicalIncrement(a.spawnPt, 2);
      assert Length(a.spawnPt) + 1 <= p < Length(a.spawnPt) + 2;
    } else {
      SiblingFillerZero(a, n - 1);
      var prev := SiblingAt(a, n - 1);
      T4PD.SiblingT4(a, n - 1);
      SigOnValidAddresses.SigOnValidAddresses(prev);
      assert SiblingAt(a, n) == HierarchicalIncrement.HierarchicalIncrement(prev, 0);
      assert Length(prev) == Length(a.spawnPt) + 2;
      assert p < Length(prev);
      assert p != LastSignificantPosition.LastSignificantPosition(prev);
    }
  }

  // Extending s to x (strictly longer, matching on s's positions) preserves
  // prefix-incomparability with any third tumbler y.
  lemma LiftDescentNonPrefix(s: Tumbler, x: Tumbler, y: Tumbler)
    requires InT(s) && InT(x) && InT(y)
    requires Length(x) > Length(s)
    requires forall i :: 1 <= i <= Length(s) ==> Component(x, i) == Component(s, i)
    requires !PrefixOf(s, y) && !PrefixOf(y, s)
    ensures !PrefixOf(x, y) && !PrefixOf(y, x)
  {
    if PrefixOf(x, y) {
      assert Length(s) < Length(x) <= Length(y);
      forall i | 1 <= i <= Length(s)
        ensures Component(y, i) == Component(s, i)
      {
        assert i <= Length(s) < Length(x);
        assert Component(y, i) == Component(x, i);
        assert Component(x, i) == Component(s, i);
      }
      assert PrefixOf(s, y);
      assert false;
    }
    if PrefixOf(y, x) {
      if Length(y) <= Length(s) {
        forall i | 1 <= i <= Length(y)
          ensures Component(s, i) == Component(y, i)
        {
          assert i <= Length(y) <= Length(s);
          assert i <= Length(y) <= Length(x);
          assert Component(s, i) == Component(x, i);
          assert Component(x, i) == Component(y, i);
        }
        assert PrefixOf(y, s);
        assert false;
      } else {
        assert Length(s) < Length(y) <= Length(x);
        forall i | 1 <= i <= Length(s)
          ensures Component(y, i) == Component(s, i)
        {
          assert i <= Length(s) < Length(y);
          assert Component(y, i) == Component(x, i);
          assert Component(x, i) == Component(s, i);
        }
        assert PrefixOf(s, y);
        assert false;
      }
    }
  }

  // Base case: two distinct child allocators sharing the same parent.
  lemma SameParentBase(X: Allocator, Y: Allocator, x: Tumbler, y: Tumbler)
    requires AllocatorDiscipline.AllocatorDiscipline(X)
    requires AllocatorDiscipline.AllocatorDiscipline(Y)
    requires X.ChildAllocator? && Y.ChildAllocator?
    requires X.parent == Y.parent
    requires X != Y
    requires InDomain(x, X)
    requires InDomain(y, Y)
    ensures InT(x) && InT(y)
    ensures !PrefixOf(x, y) && !PrefixOf(y, x)
  {
    var P := X.parent;
    var spX := X.spawnPt;
    var spY := Y.spawnPt;
    var kX := X.spawnParam;
    var kY := Y.spawnParam;

    var nx :| SiblingAt(X, nx) == x;
    var ny :| SiblingAt(Y, ny) == y;
    SiblingPrefixMatchesSpawnPt(X, nx);
    SiblingPrefixMatchesSpawnPt(Y, ny);

    if spX != spY {
      // Sub-case A: distinct spawn points — apply T10a.2 at the parent,
      // then double-lift to the child outputs.
      var mX :| SiblingAt(P, mX) == spX;
      var mY :| SiblingAt(P, mY) == spY;
      USL.SiblingInT(P, mX);
      USL.SiblingInT(P, mY);
      USL.UniformSiblingLength(P, mX);
      USL.UniformSiblingLength(P, mY);
      NNSP.NonNestingSiblingPrefixes(P, mX, mY);
      LiftDescentNonPrefix(spX, x, spY);
      LiftDescentNonPrefix(spY, y, x);
    } else {
      // spX == spY ⇒ (kX, kY) must differ (else X == Y by structural eq).
      assert kX != kY;
      var sp := spX;
      if kX == 1 && kY == 2 {
        T4PD.SiblingT4(X, nx);
        SiblingFillerZero(Y, ny);
        var p := Length(sp) + 1;
        assert Length(x) == Length(sp) + 1;
        assert Length(y) == Length(sp) + 2;
        assert p == Length(x);
        assert p <= Length(y);
        assert Component(x, p) == Component(x, Length(x));
        assert Component(x, Length(x)) != 0;
        assert Component(y, p) == 0;
        if PrefixOf(x, y) {
          assert Component(y, p) == Component(x, p);
          assert false;
        }
        if PrefixOf(y, x) {
          assert Length(y) <= Length(x);
          assert false;
        }
      } else {
        assert kX == 2 && kY == 1;
        T4PD.SiblingT4(Y, ny);
        SiblingFillerZero(X, nx);
        var p := Length(sp) + 1;
        assert Length(x) == Length(sp) + 2;
        assert Length(y) == Length(sp) + 1;
        assert p == Length(y);
        assert p <= Length(x);
        assert Component(y, p) == Component(y, Length(y));
        assert Component(y, Length(y)) != 0;
        assert Component(x, p) == 0;
        if PrefixOf(x, y) {
          assert Length(x) <= Length(y);
          assert false;
        }
        if PrefixOf(y, x) {
          assert Component(x, p) == Component(y, p);
          assert false;
        }
      }
    }
  }

  // T10a.5: non-ancestor–descendant allocators on the same tree produce
  // mutually prefix-incomparable outputs.
  lemma CrossAllocatorIncomparability(X: Allocator, Y: Allocator,
                                      x: Tumbler, y: Tumbler)
    requires AllocatorDiscipline.AllocatorDiscipline(X)
    requires AllocatorDiscipline.AllocatorDiscipline(Y)
    requires Root(X) == Root(Y)
    requires !OnLineage(X, Y) && !OnLineage(Y, X)
    requires InDomain(x, X) && InDomain(y, Y)
    ensures InT(x) && InT(y)
    ensures !PrefixOf(x, y) && !PrefixOf(y, x)
    decreases Depth(X) + Depth(Y)
  {
    T4PD.T4PreservationUnderDiscipline(X, x);
    T4PD.T4PreservationUnderDiscipline(Y, y);

    if Depth(X) > Depth(Y) {
      assert X.ChildAllocator?;
      var spX := X.spawnPt;
      var nx :| SiblingAt(X, nx) == x;
      SiblingPrefixMatchesSpawnPt(X, nx);

      if OnLineage(X.parent, Y) {
        OnLineageDepth(X.parent, Y);
        OnLineageEqualDepthIsEqual(X.parent, Y);
        assert OnLineage(Y, X);
        assert false;
      }
      if OnLineage(Y, X.parent) {
        assert OnLineage(Y, X);
        assert false;
      }

      CrossAllocatorIncomparability(X.parent, Y, spX, y);
      LiftDescentNonPrefix(spX, x, y);
    } else if Depth(Y) > Depth(X) {
      assert Y.ChildAllocator?;
      var spY := Y.spawnPt;
      var ny :| SiblingAt(Y, ny) == y;
      SiblingPrefixMatchesSpawnPt(Y, ny);

      if OnLineage(Y.parent, X) {
        OnLineageDepth(Y.parent, X);
        OnLineageEqualDepthIsEqual(Y.parent, X);
        assert OnLineage(X, Y);
        assert false;
      }
      if OnLineage(X, Y.parent) {
        assert OnLineage(X, Y);
        assert false;
      }

      CrossAllocatorIncomparability(X, Y.parent, x, spY);
      LiftDescentNonPrefix(spY, y, x);
    } else {
      assert Depth(X) == Depth(Y);
      if Depth(X) == 0 {
        assert X.RootAllocator? && Y.RootAllocator?;
        assert Root(X) == X && Root(Y) == Y;
        assert X == Y;
        assert OnLineage(X, Y);
        assert false;
      }
      assert X.ChildAllocator? && Y.ChildAllocator?;
      if X.parent == Y.parent {
        assert X != Y;
        SameParentBase(X, Y, x, y);
      } else {
        var spX := X.spawnPt;
        var spY := Y.spawnPt;
        var nx :| SiblingAt(X, nx) == x;
        var ny :| SiblingAt(Y, ny) == y;
        SiblingPrefixMatchesSpawnPt(X, nx);
        SiblingPrefixMatchesSpawnPt(Y, ny);

        if OnLineage(X.parent, Y.parent) {
          OnLineageDepth(X.parent, Y.parent);
          OnLineageEqualDepthIsEqual(X.parent, Y.parent);
          assert false;
        }
        if OnLineage(Y.parent, X.parent) {
          OnLineageDepth(Y.parent, X.parent);
          OnLineageEqualDepthIsEqual(Y.parent, X.parent);
          assert false;
        }

        CrossAllocatorIncomparability(X.parent, Y.parent, spX, spY);
        LiftDescentNonPrefix(spX, x, spY);
        LiftDescentNonPrefix(spY, y, x);
      }
    }
  }
}
