include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "ValidComposite.dfy"

// Permanence lemma — PermanenceFromFrames (ASN-0047)
//
// Every valid composite transition satisfies P0 (content permanence),
// P1 (entity permanence), and P2 (provenance permanence). Each elementary
// transition's frame ensures C, E, R are monotone; transitivity over any
// finite sequence gives the composite all three permanence properties.
module PermanenceFromFrames {
  import opened TumblerAlgebra
  import ValidComposite

  type State = ValidComposite.State

  // Content sub-map: values agree on the smaller domain
  ghost predicate ContentSubmap(a: map<Tumbler, nat>, b: map<Tumbler, nat>) {
    forall k :: k in a ==> k in b && b[k] == a[k]
  }

  // Every elementary step is monotone in C, E, R
  lemma StepIsMonotone(s: State, s': State)
    requires ValidComposite.Step(s, s')
    ensures ContentSubmap(s.C, s'.C)
    ensures s.E <= s'.E
    ensures s.R <= s'.R
  { }

  // ContentSubmap is transitive
  lemma ContentSubmapTransitive(a: map<Tumbler, nat>, b: map<Tumbler, nat>, c: map<Tumbler, nat>)
    requires ContentSubmap(a, b)
    requires ContentSubmap(b, c)
    ensures ContentSubmap(a, c)
  { }

  // Main lemma: every valid trace satisfies P0, P1, P2 between endpoints
  lemma PermanenceFromFrames(trace: seq<State>)
    requires ValidComposite.ValidTrace(trace)
    ensures ContentSubmap(trace[0].C, trace[|trace|-1].C)
    ensures trace[0].E <= trace[|trace|-1].E
    ensures trace[0].R <= trace[|trace|-1].R
    decreases |trace|
  {
    if |trace| > 1 {
      StepIsMonotone(trace[0], trace[1]);
      PermanenceFromFrames(trace[1..]);
      ContentSubmapTransitive(trace[0].C, trace[1].C, trace[|trace|-1].C);
    }
  }
}
