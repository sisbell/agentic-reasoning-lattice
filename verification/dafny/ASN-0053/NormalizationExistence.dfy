// ASN-0053: S8 — NormalizationExistence (DEF/theorem)
// Every span-set Σ whose component spans are level-uniform and mutually
// level-compatible has a normalized equivalent Σ̂ with ⟦Σ̂⟧ = ⟦Σ⟧.
// Construction: sort by start (T1), then sweep merging overlapping intervals.
include "./SpanDefs.dfy"
include "./WellFormedSpanFromEndpoints.dfy"
include "./LevelConstraint.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/LexicographicOrder.dfy"
include "../ASN-0034/TumblerAdd.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"
include "../ASN-0034/Span.dfy"
include "../ASN-0034/DisplacementRoundTrip.dfy"

module NormalizationExistence {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import LO = LexicographicOrder
  import S6 = LevelConstraint
  import WF = WellFormedSpanFromEndpoints
  import SWD = SpanWellDefinedness
  import TA = TumblerAdd
  import TS = TumblerSub
  import IC = IntrinsicComparison
  import S = Span
  import D1 = DisplacementRoundTrip

  // ─── Ghost predicates ──────────────────────────────────────────────────────

  ghost predicate AllValid(spans: seq<SpanEntry>) {
    forall i :: 0 <= i < |spans| ==> ValidSpan(spans[i])
  }

  ghost predicate AllLevelUniform(spans: seq<SpanEntry>) {
    forall i :: 0 <= i < |spans| ==> S6.LevelUniform(spans[i])
  }

  ghost predicate MutuallyLevelCompatible(spans: seq<SpanEntry>) {
    forall i, j :: 0 <= i < |spans| && 0 <= j < |spans| ==>
      S6.LevelCompat(spans[i].start, spans[j].start)
  }

  ghost predicate NonDecreasing(spans: seq<SpanEntry>) {
    forall i :: 0 <= i < |spans| - 1 ==>
      spans[i].start == spans[i+1].start ||
      LO.LexicographicOrder(spans[i].start, spans[i+1].start)
  }

  ghost predicate StrictlyNormalized(spans: seq<SpanEntry>)
    requires AllValid(spans)
  {
    forall i :: 0 <= i < |spans| - 1 ==>
      LO.LexicographicOrder(spans[i].start, spans[i+1].start) &&
      LO.LexicographicOrder(Reach(spans[i]), spans[i+1].start)
  }

  // Denotation: union of individual span denotations
  ghost function Denote(spans: seq<SpanEntry>): iset<Tumbler>
    requires AllValid(spans)
    decreases |spans|
  {
    if |spans| == 0 then iset{}
    else S.Span(spans[0].start, spans[0].width) + Denote(spans[1..])
  }

  // ─── Helpers ───────────────────────────────────────────────────────────────

  lemma AllValidTail(spans: seq<SpanEntry>)
    requires |spans| > 0 && AllValid(spans)
    ensures AllValid(spans[1..])
  {
    forall i | 0 <= i < |spans[1..]| ensures ValidSpan(spans[1..][i]) {
      assert spans[1..][i] == spans[i+1];
    }
  }

  lemma AllValidConcat(a: seq<SpanEntry>, b: seq<SpanEntry>)
    requires AllValid(a) && AllValid(b)
    ensures AllValid(a + b)
  {
    forall i | 0 <= i < |a + b| ensures ValidSpan((a + b)[i]) {
      if i < |a| { assert (a + b)[i] == a[i]; }
      else { assert (a + b)[i] == b[i - |a|]; }
    }
  }

  lemma LexTrans(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires LO.LexicographicOrder(a, b) && LO.LexicographicOrder(b, c)
    ensures LO.LexicographicOrder(a, c)
  {
    SWD.LexicographicTransitive(a, b, c);
  }

  // Under level uniformity, Length(start) == Length(reach).
  lemma ReachSameLength(sigma: SpanEntry)
    requires ValidSpan(sigma) && S6.LevelUniform(sigma)
    ensures Length(Reach(sigma)) == Length(sigma.start)
  {
    S6.LevelConstraint(sigma);
  }

  // All spans in a mutually-compatible uniform set share start and reach length.
  lemma AllSameLength(spans: seq<SpanEntry>)
    requires AllValid(spans) && AllLevelUniform(spans) && MutuallyLevelCompatible(spans)
    ensures |spans| > 0 ==>
      forall i :: 0 <= i < |spans| ==>
        Length(spans[i].start) == Length(spans[0].start) &&
        Length(Reach(spans[i])) == Length(spans[0].start)
  {
    if |spans| > 0 {
      forall i | 0 <= i < |spans|
        ensures Length(spans[i].start) == Length(spans[0].start)
        ensures Length(Reach(spans[i])) == Length(spans[0].start)
      {
        assert S6.LevelCompat(spans[i].start, spans[0].start);
        ReachSameLength(spans[i]);
      }
    }
  }

  // ─── Sort (axiomatized: existence follows from T1 total order) ─────────────

  ghost function {:axiom} Sort(spans: seq<SpanEntry>): (sorted: seq<SpanEntry>)
    requires AllValid(spans) && AllLevelUniform(spans) && MutuallyLevelCompatible(spans)
    ensures |sorted| == |spans|
    ensures AllValid(sorted) && AllLevelUniform(sorted) && MutuallyLevelCompatible(sorted)
    ensures NonDecreasing(sorted)
    ensures multiset(sorted) == multiset(spans)

  lemma {:axiom} SortDenotePreserved(spans: seq<SpanEntry>)
    requires AllValid(spans) && AllLevelUniform(spans) && MutuallyLevelCompatible(spans)
    ensures Denote(Sort(spans)) == Denote(spans)

  // ─── Sweep precondition packaging ─────────────────────────────────────────

  // Invariant: every remaining start is ≥ s, and every remaining reach is > s.
  // Packaged as predicates to avoid repetition.
  ghost predicate StartsAfterS(s: Tumbler, spans: seq<SpanEntry>)
    requires InT(s)
  {
    forall i :: 0 <= i < |spans| ==>
      spans[i].start == s || LO.LexicographicOrder(s, spans[i].start)
  }

  ghost predicate ReachesAfterS(s: Tumbler, spans: seq<SpanEntry>)
    requires InT(s) && AllValid(spans)
  {
    forall i :: 0 <= i < |spans| ==> LO.LexicographicOrder(s, Reach(spans[i]))
  }

  // Pairwise: every earlier start < every later reach in the sequence.
  ghost predicate PairwiseReach(spans: seq<SpanEntry>)
    requires AllValid(spans)
  {
    forall i, j :: 0 <= i <= j < |spans| ==>
      LO.LexicographicOrder(spans[i].start, Reach(spans[j]))
  }

  // ─── Sweep ─────────────────────────────────────────────────────────────────

  // Sweep processes sorted spans. [s, r) is the current interval.
  // Merge: start(σ) ≤ r → extend r. Emit: start(σ) > r → output [s,r), new interval.
  // Rich preconditions avoid transitivity in the function body.
  ghost function Sweep(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>): seq<SpanEntry>
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    decreases |remaining|
  {
    if |remaining| == 0 then
      [SpanEntry(s, TS.TumblerSub(r, s))]
    else
      var sigma := remaining[0];
      var r_sigma := Reach(sigma);
      // r_sigma ∈ T, Length(r_sigma) == Length(s), LO(sigma.start, r_sigma) from Reach ensures.
      if sigma.start == r || LO.LexicographicOrder(sigma.start, r) then
        // Merge: extend reach.
        if LO.LexicographicOrder(r, r_sigma) then
          // new_r = r_sigma > r > s; LO(s, r_sigma) from ReachesAfterS at i=0.
          Sweep(s, r_sigma, remaining[1..])
        else
          // new_r = r (unchanged); LO(s, r) from precondition.
          Sweep(s, r, remaining[1..])
      else
        // Emit [s, r), start new interval at sigma.start.
        // LO(sigma.start, r_sigma) from Reach ensures; Length(sigma.start) == Length(r_sigma).
        [SpanEntry(s, TS.TumblerSub(r, s))] + Sweep(sigma.start, r_sigma, remaining[1..])
  }

  // ─── Sweep correctness: AllValid ──────────────────────────────────────────

  // Helper: extract AllValid/precond facts for remaining[1..]
  lemma RestPrecond(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires |remaining| > 0
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    ensures AllValid(remaining[1..]) && AllLevelUniform(remaining[1..])
    ensures forall i :: 0 <= i < |remaining[1..]| ==> Length(remaining[1..][i].start) == Length(s)
    ensures forall i :: 0 <= i < |remaining[1..]| ==> Length(Reach(remaining[1..][i])) == Length(s)
    ensures NonDecreasing(remaining[1..])
    ensures StartsAfterS(s, remaining[1..])
    ensures ReachesAfterS(s, remaining[1..])
    ensures PairwiseReach(remaining[1..])
  {
    AllValidTail(remaining);
    forall i | 0 <= i < |remaining[1..]|
      ensures AllLevelUniform([remaining[1..][i]])
      ensures Length(remaining[1..][i].start) == Length(s)
      ensures Length(Reach(remaining[1..][i])) == Length(s)
      ensures remaining[1..][i].start == s || LO.LexicographicOrder(s, remaining[1..][i].start)
      ensures LO.LexicographicOrder(s, Reach(remaining[1..][i]))
    {
      assert remaining[1..][i] == remaining[i+1];
    }
    forall i | 0 <= i < |remaining[1..]| - 1
      ensures remaining[1..][i].start == remaining[1..][i+1].start ||
              LO.LexicographicOrder(remaining[1..][i].start, remaining[1..][i+1].start)
    {
      assert remaining[1..][i] == remaining[i+1] && remaining[1..][i+1] == remaining[i+2];
    }
    forall i, j | 0 <= i <= j < |remaining[1..]|
      ensures LO.LexicographicOrder(remaining[1..][i].start, Reach(remaining[1..][j]))
    {
      assert remaining[1..][i] == remaining[i+1] && remaining[1..][j] == remaining[j+1];
    }
  }

  // Helper: for the emit case, rest inherits the pairwise preconditions from sigma.start.
  lemma EmitRestPrecond(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires |remaining| > 0
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    // Emit case: start(remaining[0]) > r
    requires LO.LexicographicOrder(r, remaining[0].start)
    ensures
      var sigma := remaining[0];
      var r_sigma := Reach(sigma);
      var rest := remaining[1..];
      AllValid(rest) && AllLevelUniform(rest) &&
      (forall i :: 0 <= i < |rest| ==> Length(rest[i].start) == Length(sigma.start)) &&
      (forall i :: 0 <= i < |rest| ==> Length(Reach(rest[i])) == Length(sigma.start)) &&
      NonDecreasing(rest) &&
      StartsAfterS(sigma.start, rest) &&
      ReachesAfterS(sigma.start, rest) &&
      PairwiseReach(rest) &&
      LO.LexicographicOrder(sigma.start, r_sigma) &&
      Length(sigma.start) == Length(r_sigma)
  {
    var sigma := remaining[0];
    var r_sigma := Reach(sigma);
    var rest := remaining[1..];
    AllValidTail(remaining);
    // Length facts
    assert Length(sigma.start) == Length(s);
    assert Length(r_sigma) == Length(s);
    // rest lengths
    forall i | 0 <= i < |rest|
      ensures Length(rest[i].start) == Length(sigma.start)
      ensures Length(Reach(rest[i])) == Length(sigma.start)
    {
      assert rest[i] == remaining[i+1];
    }
    // NonDecreasing rest
    forall i | 0 <= i < |rest| - 1
      ensures rest[i].start == rest[i+1].start || LO.LexicographicOrder(rest[i].start, rest[i+1].start)
    {
      assert rest[i] == remaining[i+1] && rest[i+1] == remaining[i+2];
    }
    // StartsAfterS(sigma.start, rest): sigma.start ≤ rest[i].start from NonDecreasing
    forall i | 0 <= i < |rest|
      ensures rest[i].start == sigma.start || LO.LexicographicOrder(sigma.start, rest[i].start)
    {
      assert rest[i] == remaining[i+1];
      // remaining[0].start ≤ remaining[i+1].start from NonDecreasing
    }
    // ReachesAfterS(sigma.start, rest): from PairwiseReach(remaining) at (0, i+1)
    forall i | 0 <= i < |rest|
      ensures LO.LexicographicOrder(sigma.start, Reach(rest[i]))
    {
      assert rest[i] == remaining[i+1];
      assert LO.LexicographicOrder(remaining[0].start, Reach(remaining[i+1]));
    }
    // PairwiseReach(rest)
    forall i, j | 0 <= i <= j < |rest|
      ensures LO.LexicographicOrder(rest[i].start, Reach(rest[j]))
    {
      assert rest[i] == remaining[i+1] && rest[j] == remaining[j+1];
    }
    // AllLevelUniform rest
    forall i | 0 <= i < |rest| ensures S6.LevelUniform(rest[i]) {
      assert rest[i] == remaining[i+1];
    }
  }

  lemma SweepValid(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    ensures AllValid(Sweep(s, r, remaining))
    decreases |remaining|
  {
    if |remaining| == 0 {
      WF.WellFormedSpanFromEndpoints(s, r);
    } else {
      var sigma := remaining[0];
      var r_sigma := Reach(sigma);
      var rest := remaining[1..];
      if sigma.start == r || LO.LexicographicOrder(sigma.start, r) {
        // Merge case
        RestPrecond(s, r, remaining);
        if LO.LexicographicOrder(r, r_sigma) {
          // new_r = r_sigma, LO(s, r_sigma) from ReachesAfterS
          assert LO.LexicographicOrder(s, r_sigma);
          assert Length(r_sigma) == Length(s);
          SweepValid(s, r_sigma, rest);
        } else {
          SweepValid(s, r, rest);
        }
      } else {
        // Emit case: sigma.start > r
        assert LO.LexicographicOrder(r, sigma.start);
        WF.WellFormedSpanFromEndpoints(s, r);
        EmitRestPrecond(s, r, remaining);
        SweepValid(sigma.start, r_sigma, rest);
        AllValidConcat([SpanEntry(s, TS.TumblerSub(r, s))], Sweep(sigma.start, r_sigma, rest));
      }
    }
  }

  // ─── Sweep correctness: StrictlyNormalized (axiom) ────────────────────────

  // The sweep produces a strictly normalized output: N1 (increasing starts)
  // and N2 (separated reaches). Proof is by induction on |remaining|;
  // the emit condition (start > r) directly gives the separation between
  // the emitted span and the next interval's start.
  lemma {:axiom} SweepNormalized(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    ensures AllValid(Sweep(s, r, remaining))
    ensures StrictlyNormalized(Sweep(s, r, remaining))

  // ─── Sweep correctness: denotation (axiom) ────────────────────────────────

  // Sweep denotation invariant J: Denote(Sweep(s,r,remaining)) = Span(s,r⊖s) + Denote(remaining).
  // Proof: by induction on |remaining|.
  //   Base: Sweep returns [SpanEntry(s,r⊖s)]; Denote = S.Span(s,r⊖s) = S.Span(s,r⊖s) + {} ✓
  //   Merge: IH gives Denote(Sweep(s,new_r,rest)) = Span(s,new_r⊖s)+Denote(rest).
  //     Need: Span(s,new_r⊖s) = Span(s,r⊖s) ∪ Span(sigma.start,sigma.width).
  //     This is MergeEquivalence with start(sigma)≤r (overlap/adjacent condition).
  //   Emit: result = [SpanEntry(s,r⊖s)] ++ Sweep(sigma.start,r_sigma,rest).
  //     IH: Denote(Sweep(...)) = Span(sigma.start,sigma.width)+Denote(rest).
  //     Total = Span(s,r⊖s) + Span(sigma.start,sigma.width) + Denote(rest)
  //           = Span(s,r⊖s) + Denote(remaining) ✓
  lemma {:axiom} SweepDenote(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    ensures AllValid(Sweep(s, r, remaining))
    ensures Denote(Sweep(s, r, remaining)) ==
      S.Span(s, TS.TumblerSub(r, s)) + Denote(remaining)

  // ─── Establishing Sweep preconditions for the first call ──────────────────

  lemma SweepInitPrecond(sorted: seq<SpanEntry>)
    requires |sorted| > 0
    requires AllValid(sorted) && AllLevelUniform(sorted) && MutuallyLevelCompatible(sorted)
    requires NonDecreasing(sorted)
    ensures
      var s0 := sorted[0].start;
      var r0 := Reach(sorted[0]);
      var rest := sorted[1..];
      AllValid(rest) && AllLevelUniform(rest) &&
      (forall i :: 0 <= i < |rest| ==> Length(rest[i].start) == Length(s0)) &&
      (forall i :: 0 <= i < |rest| ==> Length(Reach(rest[i])) == Length(s0)) &&
      NonDecreasing(rest) &&
      StartsAfterS(s0, rest) &&
      ReachesAfterS(s0, rest) &&
      PairwiseReach(rest) &&
      LO.LexicographicOrder(s0, r0) &&
      Length(s0) == Length(r0)
  {
    var s0 := sorted[0].start;
    AllSameLength(sorted);
    AllValidTail(sorted);
    // NonDecreasing rest
    forall i | 0 <= i < |sorted[1..]| - 1
      ensures sorted[1..][i].start == sorted[1..][i+1].start ||
              LO.LexicographicOrder(sorted[1..][i].start, sorted[1..][i+1].start)
    {
      assert sorted[1..][i] == sorted[i+1] && sorted[1..][i+1] == sorted[i+2];
    }
    // AllLevelUniform rest
    forall i | 0 <= i < |sorted[1..]|
      ensures S6.LevelUniform(sorted[1..][i])
    {
      assert sorted[1..][i] == sorted[i+1];
    }
    // Length facts for rest
    forall i | 0 <= i < |sorted[1..]|
      ensures Length(sorted[1..][i].start) == Length(s0)
      ensures Length(Reach(sorted[1..][i])) == Length(s0)
    {
      assert sorted[1..][i] == sorted[i+1];
    }
    // StartsAfterS(s0, rest): s0 ≤ rest[i].start from NonDecreasing
    forall i | 0 <= i < |sorted[1..]|
      ensures sorted[1..][i].start == s0 || LO.LexicographicOrder(s0, sorted[1..][i].start)
    {
      assert sorted[1..][i] == sorted[i+1];
    }
    // ReachesAfterS(s0, rest): s0 < Reach(rest[i]) since s0 ≤ rest[i].start < Reach(rest[i])
    forall i | 0 <= i < |sorted[1..]|
      ensures LO.LexicographicOrder(s0, Reach(sorted[1..][i]))
    {
      assert sorted[1..][i] == sorted[i+1];
      var sigma := sorted[i+1];
      // s0 ≤ sigma.start (from NonDecreasing / StartsAfterS)
      assert sigma.start == s0 || LO.LexicographicOrder(s0, sigma.start);
      // sigma.start < Reach(sigma) (from Reach ensures)
      assert LO.LexicographicOrder(sigma.start, Reach(sigma));
      if sigma.start == s0 {
        // LO(s0, Reach(sigma)) directly
      } else {
        LexTrans(s0, sigma.start, Reach(sigma));
      }
    }
    // PairwiseReach: rest[i].start < Reach(rest[j]) for i ≤ j
    forall i, j | 0 <= i <= j < |sorted[1..]|
      ensures LO.LexicographicOrder(sorted[1..][i].start, Reach(sorted[1..][j]))
    {
      assert sorted[1..][i] == sorted[i+1] && sorted[1..][j] == sorted[j+1];
      // sorted[i+1].start ≤ sorted[j+1].start (from NonDecreasing, transitivity)
      // sorted[j+1].start < Reach(sorted[j+1])
      var a := sorted[i+1];
      var b := sorted[j+1];
      // Build: a.start ≤ b.start < Reach(b)
      if i == j {
        assert LO.LexicographicOrder(a.start, Reach(a));
      } else {
        // Need: a.start ≤ b.start and b.start < Reach(b)
        // From NonDecreasing: chain a.start ≤ sorted[i+2].start ≤ ... ≤ b.start
        // But chains need transitivity. Use ReachesAfterS established above for a.start.
        // sorted[i+1].start == s0 || LO(s0, sorted[i+1].start)
        // sorted[j+1].start == s0 || LO(s0, sorted[j+1].start)
        // LO(sorted[j+1].start, Reach(sorted[j+1]))
        // Show LO(sorted[i+1].start, Reach(sorted[j+1])):
        //   Case a.start == s0: LO(s0, Reach(b)) from ReachesAfterS (established above)
        //   Case LO(s0, a.start): We need LO(a.start, Reach(b)).
        //     From NonDecreasing (inductively): a.start ≤ b.start.
        //     Case a.start == b.start: LO(a.start, Reach(b)) directly.
        //     Case LO(a.start, b.start): LexTrans(a.start, b.start, Reach(b)).
        assert a.start == s0 || LO.LexicographicOrder(s0, a.start);
        assert b.start == s0 || LO.LexicographicOrder(s0, b.start);
        assert LO.LexicographicOrder(b.start, Reach(b));
        // Chain from NonDecreasing: a.start ≤ b.start by induction over i..j
        PairwiseNonDecreasingStarts(sorted, i+1, j+1);
        assert a.start == b.start || LO.LexicographicOrder(a.start, b.start);
        if a.start == b.start {
          assert LO.LexicographicOrder(a.start, Reach(b));
        } else {
          LexTrans(a.start, b.start, Reach(b));
        }
      }
    }
  }

  // Helper: non-decreasing sequence has a.start ≤ b.start for i ≤ j.
  lemma PairwiseNonDecreasingStarts(spans: seq<SpanEntry>, i: nat, j: nat)
    requires NonDecreasing(spans)
    requires 0 <= i <= j < |spans|
    ensures spans[i].start == spans[j].start || LO.LexicographicOrder(spans[i].start, spans[j].start)
    decreases j - i
  {
    if i == j { }
    else {
      PairwiseNonDecreasingStarts(spans, i, j-1);
      var a := spans[i]; var b := spans[j-1]; var c := spans[j];
      assert b.start == c.start || LO.LexicographicOrder(b.start, c.start);
      assert a.start == b.start || LO.LexicographicOrder(a.start, b.start);
      if a.start == b.start && b.start == c.start { }
      else if a.start == b.start { assert LO.LexicographicOrder(a.start, c.start); }
      else if b.start == c.start { }
      else { LexTrans(a.start, b.start, c.start); }
    }
  }

  // ─── Denotation connection ─────────────────────────────────────────────────

  // Denote([SpanEntry(s0, w0)] ++ rest) == S.Span(s0, w0) + Denote(rest)
  lemma DenoteConsElim(s0: Tumbler, w0: Tumbler, rest: seq<SpanEntry>)
    requires ValidSpan(SpanEntry(s0, w0))
    requires AllValid(rest)
    ensures AllValid([SpanEntry(s0, w0)] + rest)
    ensures Denote([SpanEntry(s0, w0)] + rest) == S.Span(s0, w0) + Denote(rest)
  {
    AllValidConcat([SpanEntry(s0, w0)], rest);
    assert ([SpanEntry(s0, w0)] + rest)[0] == SpanEntry(s0, w0);
    assert ([SpanEntry(s0, w0)] + rest)[1..] == rest;
  }

  // Span(s, r⊖s) + Span(s0, w0) + Denote(rest) = Span(s0, w0) + (Span(s,r⊖s) + Denote(rest))
  // Used to reorganize denotation in the emit case.
  lemma ISetUnionAssocComm(A: iset<Tumbler>, B: iset<Tumbler>, C: iset<Tumbler>)
    ensures A + B + C == B + A + C
  { }

  // The head span's denotation plus the tail gives the full denotation.
  lemma DenoteHead(spans: seq<SpanEntry>)
    requires |spans| > 0 && AllValid(spans)
    ensures AllValid(spans[1..])
    ensures Denote(spans) == S.Span(spans[0].start, spans[0].width) + Denote(spans[1..])
  {
    AllValidTail(spans);
  }

  // ─── Main theorem: NormalizationExistence ─────────────────────────────────

  lemma NormalizationExistence(spans: seq<SpanEntry>)
    requires AllValid(spans) && AllLevelUniform(spans) && MutuallyLevelCompatible(spans)
    ensures exists hat: seq<SpanEntry> ::
      AllValid(hat) && StrictlyNormalized(hat) && Denote(hat) == Denote(spans)
  {
    if |spans| == 0 {
      // Σ̂ = ⟨⟩ vacuously satisfies N1, N2, and Denote(⟨⟩) = ∅ = Denote(spans).
      var hat: seq<SpanEntry> := [];
      assert AllValid(hat);
      assert StrictlyNormalized(hat);
      assert Denote(hat) == Denote(spans);
    } else {
      // Step 1: sort spans (T1 guarantees existence of total order, hence sort).
      var sorted := Sort(spans);
      SortDenotePreserved(spans);
      assert Denote(sorted) == Denote(spans);
      AllSameLength(sorted);

      // Step 2: seed first interval from sorted[0].
      var s0 := sorted[0].start;
      var r0 := Reach(sorted[0]);
      var rest := sorted[1..];

      // Step 3: establish Sweep preconditions for (s0, r0, rest).
      SweepInitPrecond(sorted);

      // Step 4: run the sweep.
      var hat := Sweep(s0, r0, rest);

      // Step 5: prove AllValid.
      SweepValid(s0, r0, rest);

      // Step 6: prove StrictlyNormalized.
      SweepNormalized(s0, r0, rest);

      // Step 7: prove denotation equality.
      // SweepDenote gives: Denote(hat) = S.Span(s0, r0⊖s0) + Denote(rest)
      SweepDenote(s0, r0, rest);
      WF.WellFormedSpanFromEndpoints(s0, r0);
      assert Length(s0) == Length(r0) by { AllSameLength(sorted); }
      var w0 := TS.TumblerSub(r0, s0);
      assert ValidSpan(SpanEntry(s0, w0));
      assert Reach(SpanEntry(s0, w0)) == r0;
      // Denote(hat) = S.Span(s0, w0) + Denote(rest)
      // Denote(sorted) = S.Span(s0, w0) + Denote(rest) [from DenoteHead on sorted]
      DenoteHead(sorted);
      assert sorted[0] == SpanEntry(s0, sorted[0].width);
      // sorted[0].width gives Reach(sorted[0]) == r0, so Span(s0, sorted[0].width) == S.Span(s0, w0)?
      // Actually: Reach(sorted[0]) = TumblerAdd(s0, sorted[0].width) = r0
      // So S.Span(s0, sorted[0].width) uses sorted[0].width, not w0 = r0⊖s0.
      // But Reach(SpanEntry(s0, w0)) = TumblerAdd(s0, w0) = r0 = TumblerAdd(s0, sorted[0].width)
      // So sorted[0].width = w0 iff the width representation is canonical.
      // Actually we need: S.Span(s0, w0) == S.Span(s0, sorted[0].width).
      // This holds iff TumblerAdd(s0, w0) == TumblerAdd(s0, sorted[0].width),
      // which holds iff w0 == sorted[0].width (left cancellation).
      // But w0 = TumblerSub(r0, s0) and sorted[0].width is the original width.
      // They both give Reach = r0, so by left cancellation, w0 == sorted[0].width.
      // However, proving this requires LeftCancellation (from ASN-0034).
      // Simpler: use Span extensionality — they define the same set since s⊕w1 = s⊕w2 = r0.
      assert S.Span(s0, w0) == S.Span(s0, sorted[0].width) by {
        SpansSameReach(s0, w0, sorted[0].width, r0);
      }
      // Now: Denote(hat) = S.Span(s0, w0) + Denote(rest)
      //                   = S.Span(s0, sorted[0].width) + Denote(rest)
      //                   = Denote(sorted)
      //                   = Denote(spans)
      assert Denote(hat) == Denote(sorted);
    }
  }

  // Two spans with the same start and same reach have the same denotation.
  lemma SpansSameReach(s: Tumbler, w1: Tumbler, w2: Tumbler, r: Tumbler)
    requires InT(s) && InT(w1) && InT(w2) && InT(r)
    requires ValidSpan(SpanEntry(s, w1)) && ValidSpan(SpanEntry(s, w2))
    requires Reach(SpanEntry(s, w1)) == r && Reach(SpanEntry(s, w2)) == r
    ensures S.Span(s, w1) == S.Span(s, w2)
  {
    // S.Span(s, w) = {t | s ≤ t < TumblerAdd(s, w)}
    // Both have TumblerAdd(s, w1) = r = TumblerAdd(s, w2), so same set.
    assert TA.TumblerAdd(s, w1) == r;
    assert TA.TumblerAdd(s, w2) == r;
  }
}
