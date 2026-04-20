include "./HierarchicalParsing.dfy"

module DecidableContainment {
  // T6 — DecidableContainment
  // Corollary of T4: containment relations are decidable from addresses alone.

  import HP = HierarchicalParsing
  import SE = SyntacticEquivalence
  import LD = LevelDetermination

  // --- Field boundary computation ---

  // Position of the (k+1)th zero-valued component in s (0-indexed k),
  // or |s| if fewer than k+1 zeros exist.
  function FieldBoundary(s: seq<nat>, k: nat): (r: nat)
    ensures r <= |s|
    ensures r < |s| ==> s[r] == 0
    decreases |s|
  {
    if |s| == 0 then 0
    else if s[0] == 0 then
      if k == 0 then 0
      else 1 + FieldBoundary(s[1..], k - 1)
    else 1 + FieldBoundary(s[1..], k)
  }

  // If at least k+1 zeros exist, the (k+1)th zero is within bounds
  lemma ZeroCountImpliesBound(s: seq<nat>, k: nat)
    requires LD.ZeroCount(s) >= k + 1
    ensures FieldBoundary(s, k) < |s|
    decreases |s|
  {
    if |s| == 0 {
    } else if s[0] == 0 {
      if k == 0 {
      } else {
        ZeroCountImpliesBound(s[1..], k - 1);
      }
    } else {
      ZeroCountImpliesBound(s[1..], k);
    }
  }

  // Consecutive field boundaries are strictly increasing
  lemma FieldBoundaryMonotone(s: seq<nat>, k: nat)
    requires FieldBoundary(s, k) < |s|
    ensures FieldBoundary(s, k) + 1 <= FieldBoundary(s, k + 1)
    decreases |s|
  {
    if |s| == 0 {
    } else if s[0] == 0 {
      if k == 0 {
      } else {
        FieldBoundaryMonotone(s[1..], k - 1);
      }
    } else {
      FieldBoundaryMonotone(s[1..], k);
    }
  }

  // --- Computable field extraction ---

  // Node field N(t): components before first zero
  function NodeField(s: seq<nat>): seq<nat> {
    s[..FieldBoundary(s, 0)]
  }

  // User field U(t): components between 1st and 2nd zero
  function UserField(s: seq<nat>): seq<nat>
    requires FieldBoundary(s, 0) < |s|
    requires FieldBoundary(s, 0) + 1 <= FieldBoundary(s, 1)
  {
    s[FieldBoundary(s, 0) + 1..FieldBoundary(s, 1)]
  }

  // Document field D(t): components between 2nd and 3rd zero
  function DocField(s: seq<nat>): seq<nat>
    requires FieldBoundary(s, 1) < |s|
    requires FieldBoundary(s, 1) + 1 <= FieldBoundary(s, 2)
  {
    s[FieldBoundary(s, 1) + 1..FieldBoundary(s, 2)]
  }

  // Sequence prefix relation
  predicate IsSeqPrefix(s: seq<nat>, r: seq<nat>) {
    |s| <= |r| && s == r[..|s|]
  }

  // --- T6: DecidableContainment ---

  // Helper: field extraction preconditions hold for any valid address
  lemma FieldsExtractable(s: seq<nat>)
    requires |s| >= 1
    requires SE.SyntacticWF(s)
    requires LD.ZeroCount(s) <= 3
    ensures FieldBoundary(s, 0) >= 1
    ensures LD.ZeroCount(s) >= 1 ==>
      FieldBoundary(s, 0) < |s| &&
      FieldBoundary(s, 0) + 1 <= FieldBoundary(s, 1)
    ensures LD.ZeroCount(s) >= 2 ==>
      FieldBoundary(s, 1) < |s| &&
      FieldBoundary(s, 1) + 1 <= FieldBoundary(s, 2)
  {
    assert s[0] != 0;
    if LD.ZeroCount(s) >= 1 {
      ZeroCountImpliesBound(s, 0);
      FieldBoundaryMonotone(s, 0);
    }
    if LD.ZeroCount(s) >= 2 {
      ZeroCountImpliesBound(s, 1);
      FieldBoundaryMonotone(s, 1);
    }
  }

  // T6: All four containment relations are decidable from the addresses alone.
  // The non-ghost functions NodeField, UserField, DocField, IsSeqPrefix witness
  // decidability; this lemma proves their preconditions hold for valid addresses.
  lemma DecidableContainment(a: SE.Tumbler, b: SE.Tumbler)
    requires HP.ValidAddress(a) && HP.ValidAddress(b)
    // (a) Node field always extractable and non-empty
    ensures |NodeField(a.components)| >= 1
    ensures |NodeField(b.components)| >= 1
    // (b) User field extractable when user-level or deeper
    ensures LD.ZeroCount(a.components) >= 1 ==>
      FieldBoundary(a.components, 0) < |a.components| &&
      FieldBoundary(a.components, 0) + 1 <= FieldBoundary(a.components, 1)
    ensures LD.ZeroCount(b.components) >= 1 ==>
      FieldBoundary(b.components, 0) < |b.components| &&
      FieldBoundary(b.components, 0) + 1 <= FieldBoundary(b.components, 1)
    // (c) Document field extractable when document-level or deeper
    ensures LD.ZeroCount(a.components) >= 2 ==>
      FieldBoundary(a.components, 1) < |a.components| &&
      FieldBoundary(a.components, 1) + 1 <= FieldBoundary(a.components, 2)
    ensures LD.ZeroCount(b.components) >= 2 ==>
      FieldBoundary(b.components, 1) < |b.components| &&
      FieldBoundary(b.components, 1) + 1 <= FieldBoundary(b.components, 2)
    // (d) Sequence prefix decidable by IsSeqPrefix
  {
    FieldsExtractable(a.components);
    FieldsExtractable(b.components);
  }
}
