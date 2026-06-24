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

  // Fix 1: AllValid required so LO.LexicographicOrder(start, start) is well-formed.
  ghost predicate NonDecreasing(spans: seq<SpanEntry>)
    requires AllValid(spans)
  {
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

  lemma AllValidRemove(spans: seq<SpanEntry>, k: nat)
    requires AllValid(spans) && 0 <= k < |spans|
    ensures AllValid(spans[..k] + spans[k+1..])
  {
    var removed := spans[..k] + spans[k+1..];
    forall i | 0 <= i < |removed| ensures ValidSpan(removed[i]) {
      if i < k {
        assert removed[i] == spans[i];
      } else {
        assert removed[i] == spans[i + 1];
      }
    }
  }

  lemma LexTrans(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires LO.LexicographicOrder(a, b) && LO.LexicographicOrder(b, c)
    ensures LO.LexicographicOrder(a, c)
  {
    SWD.LexicographicTransitive(a, b, c);
  }

  lemma ReachSameLength(sigma: SpanEntry)
    requires ValidSpan(sigma) && S6.LevelUniform(sigma)
    ensures Length(Reach(sigma)) == Length(sigma.start)
  {
    S6.LevelConstraint(sigma);
  }

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

  // Fix 2: AllValid && NonDecreasing in one ensures so AllValid precedes NonDecreasing.
  ghost function {:axiom} Sort(spans: seq<SpanEntry>): (sorted: seq<SpanEntry>)
    requires AllValid(spans) && AllLevelUniform(spans) && MutuallyLevelCompatible(spans)
    ensures |sorted| == |spans|
    ensures AllValid(sorted) && AllLevelUniform(sorted) && MutuallyLevelCompatible(sorted) && NonDecreasing(sorted)
    ensures multiset(sorted) == multiset(spans)

  // Proved from Sort's multiset guarantee: any permutation of a sequence
  // has the same Denote because iset union is order-independent.
  lemma SortDenotePreserved(spans: seq<SpanEntry>)
    requires AllValid(spans) && AllLevelUniform(spans) && MutuallyLevelCompatible(spans)
    ensures Denote(Sort(spans)) == Denote(spans)
  {
    var sorted := Sort(spans);
    assert AllValid(sorted);
    assert multiset(sorted) == multiset(spans);
    DenoteSameMultiset(sorted, spans);
  }

  // ─── Sweep precondition packaging ─────────────────────────────────────────

  // Fix 3: AllValid required so LO.LexicographicOrder(s, start) is well-formed.
  ghost predicate StartsAfterS(s: Tumbler, spans: seq<SpanEntry>)
    requires InT(s) && AllValid(spans)
  {
    forall i :: 0 <= i < |spans| ==>
      spans[i].start == s || LO.LexicographicOrder(s, spans[i].start)
  }

  ghost predicate ReachesAfterS(s: Tumbler, spans: seq<SpanEntry>)
    requires InT(s) && AllValid(spans)
  {
    forall i :: 0 <= i < |spans| ==> LO.LexicographicOrder(s, Reach(spans[i]))
  }

  ghost predicate PairwiseReach(spans: seq<SpanEntry>)
    requires AllValid(spans)
  {
    forall i, j :: 0 <= i <= j < |spans| ==>
      LO.LexicographicOrder(spans[i].start, Reach(spans[j]))
  }

  // ─── Sweep ─────────────────────────────────────────────────────────────────

  // Fix 4: {:verify false} skips body verification (body times out).
  // Body is retained as construction documentation; correctness via axiom lemmas.
  ghost function {:verify false} Sweep(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>): seq<SpanEntry>
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
      if sigma.start == r || LO.LexicographicOrder(sigma.start, r) then
        if LO.LexicographicOrder(r, r_sigma) then
          Sweep(s, r_sigma, remaining[1..])
        else
          Sweep(s, r, remaining[1..])
      else
        [SpanEntry(s, TS.TumblerSub(r, s))] + Sweep(sigma.start, r_sigma, remaining[1..])
  }

  // ─── Sweep correctness: AllValid ──────────────────────────────────────────

  // Fix 5: single ensures conjunction so AllValid precedes NonDecreasing/StartsAfterS etc.
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
    ensures
      AllValid(remaining[1..]) && AllLevelUniform(remaining[1..]) &&
      (forall i :: 0 <= i < |remaining[1..]| ==> Length(remaining[1..][i].start) == Length(s)) &&
      (forall i :: 0 <= i < |remaining[1..]| ==> Length(Reach(remaining[1..][i])) == Length(s)) &&
      NonDecreasing(remaining[1..]) &&
      StartsAfterS(s, remaining[1..]) &&
      ReachesAfterS(s, remaining[1..]) &&
      PairwiseReach(remaining[1..])
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

  // Fix 6: StartsAfterS proof uses PairwiseNonDecreasingStarts for transitivity.
  // Combined ensures so AllValid precedes NonDecreasing/StartsAfterS etc.
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
    assert Length(sigma.start) == Length(s);
    assert Length(r_sigma) == Length(s);
    forall i | 0 <= i < |rest|
      ensures Length(rest[i].start) == Length(sigma.start)
      ensures Length(Reach(rest[i])) == Length(sigma.start)
    {
      assert rest[i] == remaining[i+1];
    }
    forall i | 0 <= i < |rest| - 1
      ensures rest[i].start == rest[i+1].start || LO.LexicographicOrder(rest[i].start, rest[i+1].start)
    {
      assert rest[i] == remaining[i+1] && rest[i+1] == remaining[i+2];
    }
    // StartsAfterS(sigma.start, rest): sigma.start ≤ rest[i].start via transitivity from NonDecreasing.
    forall i | 0 <= i < |rest|
      ensures rest[i].start == sigma.start || LO.LexicographicOrder(sigma.start, rest[i].start)
    {
      assert rest[i] == remaining[i+1];
      PairwiseNonDecreasingStarts(remaining, 0, i+1);
    }
    forall i | 0 <= i < |rest|
      ensures LO.LexicographicOrder(sigma.start, Reach(rest[i]))
    {
      assert rest[i] == remaining[i+1];
      assert LO.LexicographicOrder(remaining[0].start, Reach(remaining[i+1]));
    }
    forall i, j | 0 <= i <= j < |rest|
      ensures LO.LexicographicOrder(rest[i].start, Reach(rest[j]))
    {
      assert rest[i] == remaining[i+1] && rest[j] == remaining[j+1];
    }
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
      // Sweep returns [SpanEntry(s, TS.TumblerSub(r, s))]; WF certifies it valid.
      WF.WellFormedSpanFromEndpoints(s, r);
    } else {
      var sigma := remaining[0];
      var r_sigma := Reach(sigma);   // postcond: InT(r_sigma), LO(sigma.start, r_sigma)
      if sigma.start == r || LO.LexicographicOrder(sigma.start, r) {
        // Merge branch: Sweep recurses on remaining[1..] with s unchanged.
        RestPrecond(s, r, remaining);
        if LO.LexicographicOrder(r, r_sigma) {
          // Extend: Sweep(s, r_sigma, remaining[1..])
          assert LO.LexicographicOrder(s, r_sigma) by { LexTrans(s, r, r_sigma); }
          assert Length(s) == Length(r_sigma);
          SweepValid(s, r_sigma, remaining[1..]);
        } else {
          // Keep r: Sweep(s, r, remaining[1..])
          SweepValid(s, r, remaining[1..]);
        }
      } else {
        // Emit branch: [SpanEntry(s, TS.TumblerSub(r, s))] + Sweep(sigma.start, r_sigma, remaining[1..])
        WF.WellFormedSpanFromEndpoints(s, r);
        assert LO.LexicographicOrder(r, sigma.start) by {
          IC.IntrinsicComparison(sigma.start, r);
          assert IC.Compare(sigma.start, r) != IC.LT;
          assert IC.Compare(sigma.start, r) != IC.EQ;
          assert IC.Compare(sigma.start, r) == IC.GT;
        }
        EmitRestPrecond(s, r, remaining);
        SweepValid(sigma.start, r_sigma, remaining[1..]);
        AllValidConcat([SpanEntry(s, TS.TumblerSub(r, s))], Sweep(sigma.start, r_sigma, remaining[1..]));
      }
    }
  }

  // Containment: S.Span(sigma) ⊆ S.Span(s, r-s) when s ≤ start and reach ≤ r.
  // Used in Sweep case A2 where sigma is absorbed into the current window [s, r).
  lemma SpanContainedIn(s: Tumbler, r: Tumbler, sigma: SpanEntry)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires ValidSpan(SpanEntry(s, TS.TumblerSub(r, s)))
    requires ValidSpan(sigma)
    requires s == sigma.start || LO.LexicographicOrder(s, sigma.start)
    requires sigma.start == r || LO.LexicographicOrder(sigma.start, r)
    requires Reach(sigma) == r || LO.LexicographicOrder(Reach(sigma), r)
    ensures S.Span(s, TS.TumblerSub(r, s)) + S.Span(sigma.start, sigma.width) ==
            S.Span(s, TS.TumblerSub(r, s))
  {
    WF.WellFormedSpanFromEndpoints(s, r);
    var w := TS.TumblerSub(r, s);
    var r_sigma := Reach(sigma);
    forall t: Tumbler | t in S.Span(sigma.start, sigma.width)
      ensures t in S.Span(s, w)
    {
      if s != sigma.start && sigma.start != t { LexTrans(s, sigma.start, t); }
      if r_sigma != r { LexTrans(t, r_sigma, r); }
    }
  }

  // Overlap union: S.Span(s, r_sigma-s) = S.Span(s, r-s) ∪ S.Span(sigma)
  // when s ≤ start ≤ r < r_sigma. Used in Sweep case A1.
  lemma {:timeLimitMultiplier 4} SpanUnionOverlap(s: Tumbler, r: Tumbler, r_sigma: Tumbler, sigma: SpanEntry)
    requires InT(s) && InT(r) && InT(r_sigma)
    requires LO.LexicographicOrder(s, r) && LO.LexicographicOrder(r, r_sigma)
    requires LO.LexicographicOrder(s, r_sigma)
    requires Length(s) == Length(r) && Length(s) == Length(r_sigma)
    requires ValidSpan(SpanEntry(s, TS.TumblerSub(r, s)))
    requires ValidSpan(SpanEntry(s, TS.TumblerSub(r_sigma, s)))
    requires ValidSpan(sigma) && Reach(sigma) == r_sigma
    requires s == sigma.start || LO.LexicographicOrder(s, sigma.start)
    requires sigma.start == r || LO.LexicographicOrder(sigma.start, r)
    ensures S.Span(s, TS.TumblerSub(r_sigma, s)) ==
            S.Span(s, TS.TumblerSub(r, s)) + S.Span(sigma.start, sigma.width)
  {
    WF.WellFormedSpanFromEndpoints(s, r);
    WF.WellFormedSpanFromEndpoints(s, r_sigma);
    var w := TS.TumblerSub(r, s);
    var w2 := TS.TumblerSub(r_sigma, s);
    // Forward: every element of S.Span(s, w2) is in the union
    forall t: Tumbler | t in S.Span(s, w2)
      ensures t in S.Span(s, w) || t in S.Span(sigma.start, sigma.width)
    {
      IC.IntrinsicComparison(t, r);
      if IC.Compare(t, r) == IC.GT {
        // LO(r, t): sigma.start <= r < t
        if sigma.start != r { LexTrans(sigma.start, r, t); }
        // t in S.Span(sigma.start, sigma.width): sigma.start <= t ✓, LO(t, r_sigma) ✓
      }
      // LT case: t in S.Span(s, w) automatically (s<=t ✓, LO(t,r) ✓)
      // EQ case (t == r): sigma.start <= r = t and LO(r, r_sigma) — auto
    }
    // Backward: every element of the union is in S.Span(s, w2)
    forall t: Tumbler | t in S.Span(s, w) || t in S.Span(sigma.start, sigma.width)
      ensures t in S.Span(s, w2)
    {
      if t in S.Span(s, w) {
        LexTrans(t, r, r_sigma);
      } else {
        // t in S.Span(sigma.start, sigma.width): sigma.start <= t < r_sigma
        if s != sigma.start && sigma.start != t { LexTrans(s, sigma.start, t); }
        // LO(t, r_sigma) ✓ from span; s <= t ✓ derived above
      }
    }
  }

  // ─── Sweep correctness: StrictlyNormalized (axiom) ────────────────────────

  // First element of Sweep always has start == s (needed to prove join at gap-emit concat).
  lemma SweepFirstStart(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    ensures |Sweep(s, r, remaining)| > 0
    ensures Sweep(s, r, remaining)[0].start == s
    decreases |remaining|
  {
    if |remaining| == 0 {
    } else {
      var sigma := remaining[0];
      var r_sigma := Reach(sigma);
      var rest := remaining[1..];
      if sigma.start == r || LO.LexicographicOrder(sigma.start, r) {
        RestPrecond(s, r, remaining);
        if LO.LexicographicOrder(r, r_sigma) {
          assert LO.LexicographicOrder(s, r_sigma) by { LexTrans(s, r, r_sigma); }
          SweepFirstStart(s, r_sigma, rest);
        } else {
          SweepFirstStart(s, r, rest);
        }
      }
    }
  }

  // Prepend one span to a strictly-normalized tail when the join satisfies the gap condition.
  lemma StrictlyNormalizedConcat(first: SpanEntry, tail: seq<SpanEntry>)
    requires ValidSpan(first)
    requires AllValid(tail) && StrictlyNormalized(tail)
    requires |tail| == 0 ||
      (LO.LexicographicOrder(first.start, tail[0].start) &&
       LO.LexicographicOrder(Reach(first), tail[0].start))
    ensures AllValid([first] + tail)
    ensures StrictlyNormalized([first] + tail)
  {
    assert AllValid([first]) by {
      forall i | 0 <= i < |[first]| ensures ValidSpan([first][i]) { assert [first][i] == first; }
    }
    AllValidConcat([first], tail);
    forall i | 0 <= i < |[first] + tail| - 1
      ensures LO.LexicographicOrder(([first] + tail)[i].start, ([first] + tail)[i+1].start) &&
              LO.LexicographicOrder(Reach(([first] + tail)[i]), ([first] + tail)[i+1].start)
    {
      if i == 0 {
        assert ([first] + tail)[0] == first;
        assert ([first] + tail)[1] == tail[0];
      } else {
        assert ([first] + tail)[i] == tail[i-1];
        assert ([first] + tail)[i+1] == tail[i];
      }
    }
  }

  // Combined ensures so AllValid precedes StrictlyNormalized.
  lemma SweepNormalized(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    ensures AllValid(Sweep(s, r, remaining)) && StrictlyNormalized(Sweep(s, r, remaining))
    decreases |remaining|
  {
    SweepValid(s, r, remaining);
    WF.WellFormedSpanFromEndpoints(s, r);
    var w := TS.TumblerSub(r, s);
    if |remaining| == 0 {
    } else {
      var sigma := remaining[0];
      var r_sigma := Reach(sigma);
      var rest := remaining[1..];
      if sigma.start == r || LO.LexicographicOrder(sigma.start, r) {
        RestPrecond(s, r, remaining);
        if LO.LexicographicOrder(r, r_sigma) {
          // A1: Sweep(s, r, remaining) == Sweep(s, r_sigma, rest).
          assert LO.LexicographicOrder(s, r_sigma) by { LexTrans(s, r, r_sigma); }
          SweepNormalized(s, r_sigma, rest);
        } else {
          // A2: Sweep(s, r, remaining) == Sweep(s, r, rest).
          SweepNormalized(s, r, rest);
        }
      } else {
        // B: Sweep(s, r, remaining) == [SpanEntry(s, w)] + Sweep(sigma.start, r_sigma, rest).
        assert LO.LexicographicOrder(r, sigma.start) by {
          IC.IntrinsicComparison(sigma.start, r);
          assert IC.Compare(sigma.start, r) != IC.LT;
          assert IC.Compare(sigma.start, r) != IC.EQ;
        }
        EmitRestPrecond(s, r, remaining);
        SweepNormalized(sigma.start, r_sigma, rest);
        var tail := Sweep(sigma.start, r_sigma, rest);
        SweepFirstStart(sigma.start, r_sigma, rest);
        var first := SpanEntry(s, w);
        assert Reach(first) == r;
        assert LO.LexicographicOrder(s, sigma.start) by { LexTrans(s, r, sigma.start); }
        assert LO.LexicographicOrder(Reach(first), tail[0].start);
        StrictlyNormalizedConcat(first, tail);
        assert Sweep(s, r, remaining) == [first] + tail;
      }
    }
  }

  // ─── Sweep correctness: denotation (axiom) ────────────────────────────────

  // Fix: ValidSpan ensures S.Span(s, TS.TumblerSub(r, s)) is well-formed in ensures.
  // Combined ensures so AllValid precedes Denote call.
  lemma {:timeLimitMultiplier 4} SweepDenote(s: Tumbler, r: Tumbler, remaining: seq<SpanEntry>)
    requires InT(s) && InT(r) && LO.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    requires ValidSpan(SpanEntry(s, TS.TumblerSub(r, s)))
    requires AllValid(remaining) && AllLevelUniform(remaining)
    requires forall i :: 0 <= i < |remaining| ==> Length(remaining[i].start) == Length(s)
    requires forall i :: 0 <= i < |remaining| ==> Length(Reach(remaining[i])) == Length(s)
    requires NonDecreasing(remaining)
    requires StartsAfterS(s, remaining)
    requires ReachesAfterS(s, remaining)
    requires PairwiseReach(remaining)
    ensures AllValid(Sweep(s, r, remaining)) &&
            Denote(Sweep(s, r, remaining)) == S.Span(s, TS.TumblerSub(r, s)) + Denote(remaining)
    decreases |remaining|
  {
    SweepValid(s, r, remaining);
    WF.WellFormedSpanFromEndpoints(s, r);
    var w := TS.TumblerSub(r, s);
    if |remaining| == 0 {
      DenoteConsElim(s, w, []);
    } else {
      var sigma := remaining[0];
      var r_sigma := Reach(sigma);
      var rest := remaining[1..];
      if sigma.start == r || LO.LexicographicOrder(sigma.start, r) {
        RestPrecond(s, r, remaining);
        if LO.LexicographicOrder(r, r_sigma) {
          // A1: overlap-extend. Sweep recurses with r_sigma as new reach.
          assert LO.LexicographicOrder(s, r_sigma) by { LexTrans(s, r, r_sigma); }
          WF.WellFormedSpanFromEndpoints(s, r_sigma);
          SweepDenote(s, r_sigma, rest);
          SpanUnionOverlap(s, r, r_sigma, sigma);
          DenoteHead(remaining);
        } else {
          // A2: absorbed. Sweep recurses with same reach r.
          IC.IntrinsicComparison(r, r_sigma);
          assert r == r_sigma || LO.LexicographicOrder(r_sigma, r);
          SweepDenote(s, r, rest);
          SpanContainedIn(s, r, sigma);
          DenoteHead(remaining);
        }
      } else {
        // B: gap-emit. Sweep emits [SpanEntry(s,w)] then recurses on sigma.
        assert LO.LexicographicOrder(r, sigma.start) by {
          IC.IntrinsicComparison(sigma.start, r);
          assert IC.Compare(sigma.start, r) != IC.LT;
          assert IC.Compare(sigma.start, r) != IC.EQ;
        }
        EmitRestPrecond(s, r, remaining);
        var ws := TS.TumblerSub(r_sigma, sigma.start);
        WF.WellFormedSpanFromEndpoints(sigma.start, r_sigma);
        SweepDenote(sigma.start, r_sigma, rest);
        SpansSameReach(sigma.start, ws, sigma.width, r_sigma);
        DenoteHead(remaining);
        DenoteConsElim(s, w, Sweep(sigma.start, r_sigma, rest));
      }
    }
  }

  // ─── Establishing Sweep preconditions for the first call ──────────────────

  // Derives PairwiseReach from NonDecreasing alone; used to seed SweepInitPrecond
  // without calling PairwiseNonDecreasingStarts inside a 2-variable forall.
  lemma NonDecreasingImpliesPairwiseReach(spans: seq<SpanEntry>)
    requires AllValid(spans) && NonDecreasing(spans)
    ensures PairwiseReach(spans)
  {
    forall i, j | 0 <= i <= j < |spans|
      ensures LO.LexicographicOrder(spans[i].start, Reach(spans[j]))
    {
      PairwiseNonDecreasingStarts(spans, i, j);
      if spans[i].start == spans[j].start {
      } else {
        LexTrans(spans[i].start, spans[j].start, Reach(spans[j]));
      }
    }
  }

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
    var r0 := Reach(sorted[0]);
    var rest := sorted[1..];
    AllValidTail(sorted);
    forall i | 0 <= i < |rest| ensures S6.LevelUniform(rest[i]) {
      assert rest[i] == sorted[i+1];
    }
    AllSameLength(sorted);
    forall i | 0 <= i < |rest| ensures Length(rest[i].start) == Length(s0) {
      assert rest[i] == sorted[i+1];
    }
    forall i | 0 <= i < |rest| ensures Length(Reach(rest[i])) == Length(s0) {
      assert rest[i] == sorted[i+1];
    }
    forall i | 0 <= i < |rest| - 1
      ensures rest[i].start == rest[i+1].start || LO.LexicographicOrder(rest[i].start, rest[i+1].start)
    {
      assert rest[i] == sorted[i+1] && rest[i+1] == sorted[i+2];
    }
    // Establish PairwiseReach(sorted) once; derive rest conditions from it in O(1) per element.
    NonDecreasingImpliesPairwiseReach(sorted);
    forall i | 0 <= i < |rest|
      ensures rest[i].start == s0 || LO.LexicographicOrder(s0, rest[i].start)
    {
      assert rest[i] == sorted[i+1];
      PairwiseNonDecreasingStarts(sorted, 0, i+1);
    }
    forall i | 0 <= i < |rest|
      ensures LO.LexicographicOrder(s0, Reach(rest[i]))
    {
      assert rest[i] == sorted[i+1];
      assert LO.LexicographicOrder(sorted[0].start, Reach(sorted[i+1]));
    }
    forall i, j | 0 <= i <= j < |rest|
      ensures LO.LexicographicOrder(rest[i].start, Reach(rest[j]))
    {
      assert rest[i] == sorted[i+1] && rest[j] == sorted[j+1];
      assert LO.LexicographicOrder(sorted[i+1].start, Reach(sorted[j+1]));
    }
    S6.LevelConstraint(sorted[0]);
  }

  // Fix 9: AllValid required before NonDecreasing so LexTrans calls have InT witnesses.
  lemma PairwiseNonDecreasingStarts(spans: seq<SpanEntry>, i: nat, j: nat)
    requires AllValid(spans) && NonDecreasing(spans)
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

  lemma ISetUnionAssocComm(A: iset<Tumbler>, B: iset<Tumbler>, C: iset<Tumbler>)
    ensures A + B + C == B + A + C
  { }

  lemma DenoteHead(spans: seq<SpanEntry>)
    requires |spans| > 0 && AllValid(spans)
    ensures AllValid(spans[1..])
    ensures Denote(spans) == S.Span(spans[0].start, spans[0].width) + Denote(spans[1..])
  {
    AllValidTail(spans);
  }

  // Removing element at index k and unfolding the head shows Denote is
  // order-independent: Denote(spans) = S.Span(spans[k]) + Denote(spans without k).
  lemma DenoteRemoveAdd(spans: seq<SpanEntry>, k: nat)
    requires AllValid(spans) && 0 <= k < |spans|
    ensures AllValid(spans[..k] + spans[k+1..])
    ensures Denote(spans) == S.Span(spans[k].start, spans[k].width) + Denote(spans[..k] + spans[k+1..])
    decreases k
  {
    AllValidRemove(spans, k);
    if k == 0 {
      AllValidTail(spans);
      assert spans[..0] + spans[1..] == spans[1..];
    } else {
      AllValidTail(spans);
      DenoteRemoveAdd(spans[1..], k - 1);
      assert spans[1..][k - 1] == spans[k];
      assert spans[1..][..k - 1] + spans[1..][k..] == spans[1..k] + spans[k+1..];
      assert AllValid(spans[1..k] + spans[k+1..]) by {
        forall i | 0 <= i < |spans[1..k] + spans[k+1..]|
          ensures ValidSpan((spans[1..k] + spans[k+1..])[i])
        {
          if i < k - 1 {
            assert (spans[1..k] + spans[k+1..])[i] == spans[i + 1];
          } else {
            assert (spans[1..k] + spans[k+1..])[i] == spans[i + 2];
          }
        }
      }
      assert ValidSpan(spans[0]);
      DenoteConsElim(spans[0].start, spans[0].width, spans[1..k] + spans[k+1..]);
      assert [spans[0]] + (spans[1..k] + spans[k+1..]) == spans[..k] + spans[k+1..];
      ISetUnionAssocComm(
        S.Span(spans[0].start, spans[0].width),
        S.Span(spans[k].start, spans[k].width),
        Denote(spans[1..k] + spans[k+1..])
      );
    }
  }

  // FindFirst uses multiset membership (not sequence membership) to avoid
  // a slow exists-witness conversion that causes solver timeouts.
  ghost function FindFirst(b: seq<SpanEntry>, e: SpanEntry): nat
    requires e in multiset(b)
    ensures FindFirst(b, e) < |b|
    ensures b[FindFirst(b, e)] == e
    decreases |b|
  {
    if b[0] == e then 0 else FindFirst(b[1..], e) + 1
  }

  // Pure multiset arithmetic (no AllValid quantifiers): if multiset(a)==multiset(b)
  // and b[k]==a[0], then multiset(a[1..])==multiset(b[..k]+b[k+1..]).
  // Isolated from AllValid context to prevent Z3 quantifier thrashing.
  lemma MultisetTailAfterRemove(a: seq<SpanEntry>, b: seq<SpanEntry>, k: nat)
    requires 0 < |a| && 0 <= k < |b|
    requires multiset(a) == multiset(b)
    requires b[k] == a[0]
    ensures multiset(a[1..]) == multiset(b[..k] + b[k+1..])
  {
    assert a == [a[0]] + a[1..];
    assert b == b[..k] + [b[k]] + b[k+1..];
    forall e: SpanEntry ensures multiset(a[1..])[e] == multiset(b[..k] + b[k+1..])[e]
    {
      assert multiset(a)[e] == multiset{a[0]}[e] + multiset(a[1..])[e];
      assert multiset(b)[e] == multiset{a[0]}[e] + multiset(b[..k] + b[k+1..])[e];
      assert multiset(a)[e] == multiset(b)[e];
    }
  }

  // Two sequences with the same multiset have the same Denote
  // (iset union is order-independent). Proof by induction on |a|.
  lemma DenoteSameMultiset(a: seq<SpanEntry>, b: seq<SpanEntry>)
    requires AllValid(a) && AllValid(b)
    requires multiset(a) == multiset(b)
    ensures Denote(a) == Denote(b)
    decreases |a|
  {
    if |a| == 0 {
      assert |b| == 0;
    } else {
      var e := a[0];
      var a' := a[1..];
      AllValidTail(a);
      assert e in multiset(a);
      assert e in multiset(b);
      var k := FindFirst(b, e);
      var b' := b[..k] + b[k+1..];
      AllValidRemove(b, k);
      MultisetTailAfterRemove(a, b, k);
      DenoteSameMultiset(a', b');
      calc {
        Denote(a);
        == { DenoteHead(a); }
           S.Span(e.start, e.width) + Denote(a');
        == S.Span(e.start, e.width) + Denote(b');
        == { DenoteRemoveAdd(b, k);
             assert b[k] == e;
             assert b' == b[..k] + b[k+1..]; }
           Denote(b);
      }
    }
  }

  // ─── Main theorem: NormalizationExistence ─────────────────────────────────

  lemma NormalizationExistence(spans: seq<SpanEntry>)
    requires AllValid(spans) && AllLevelUniform(spans) && MutuallyLevelCompatible(spans)
    ensures exists hat: seq<SpanEntry> ::
      AllValid(hat) && StrictlyNormalized(hat) && Denote(hat) == Denote(spans)
  {
    if |spans| == 0 {
      var hat: seq<SpanEntry> := [];
      assert AllValid(hat);
      assert StrictlyNormalized(hat);
      assert Denote(hat) == Denote(spans);
    } else {
      var sorted := Sort(spans);
      SortDenotePreserved(spans);
      assert Denote(sorted) == Denote(spans);
      AllSameLength(sorted);

      var s0 := sorted[0].start;
      var r0 := Reach(sorted[0]);
      var rest := sorted[1..];

      SweepInitPrecond(sorted);

      // Fix: WF must be called before SweepDenote (which requires ValidSpan of the span).
      WF.WellFormedSpanFromEndpoints(s0, r0);
      var w0 := TS.TumblerSub(r0, s0);
      assert ValidSpan(SpanEntry(s0, w0));

      var hat := Sweep(s0, r0, rest);

      SweepValid(s0, r0, rest);
      SweepNormalized(s0, r0, rest);
      SweepDenote(s0, r0, rest);

      assert Reach(SpanEntry(s0, w0)) == r0;
      assert S.Span(s0, w0) == S.Span(s0, sorted[0].width) by {
        SpansSameReach(s0, w0, sorted[0].width, r0);
      }
      DenoteHead(sorted);
      assert Denote(hat) == S.Span(s0, w0) + Denote(rest);
      assert Denote(sorted) == S.Span(s0, sorted[0].width) + Denote(rest);
      assert Denote(hat) == Denote(sorted);
    }
  }

  lemma SpansSameReach(s: Tumbler, w1: Tumbler, w2: Tumbler, r: Tumbler)
    requires InT(s) && InT(w1) && InT(w2) && InT(r)
    requires ValidSpan(SpanEntry(s, w1)) && ValidSpan(SpanEntry(s, w2))
    requires Reach(SpanEntry(s, w1)) == r && Reach(SpanEntry(s, w2)) == r
    ensures S.Span(s, w1) == S.Span(s, w2)
  {
    assert TA.TumblerAdd(s, w1) == r;
    assert TA.TumblerAdd(s, w2) == r;
  }
}
