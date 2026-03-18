include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// P4a — HistoricalFidelity (ASN-0047)
// (A (a, d) ∈ R :: (E Σ_k in the transition history : a ∈ ran(M_k(d))))
// derived from J1', P2
module HistoricalFidelity {
  import opened TumblerAlgebra

  // Minimal state projection: arrangement containment and provenance
  datatype State = State(
    contained: set<(Tumbler, Tumbler)>,  // {(a, d) : a ∈ ran(M(d))}
    R: set<(Tumbler, Tumbler)>           // provenance
  )

  ghost predicate InitialState(s: State) {
    s.R == {}
  }

  ghost predicate ValidStep(s: State, s': State) {
    // P2: provenance is monotonic
    s.R <= s'.R &&
    // J1' (sufficient): new provenance entries witnessed in post-state arrangement
    (forall p :: p in s'.R && p !in s.R ==> p in s'.contained)
  }

  ghost predicate ValidTrace(trace: seq<State>) {
    |trace| >= 1 &&
    InitialState(trace[0]) &&
    (forall i :: 0 <= i < |trace| - 1 ==> ValidStep(trace[i], trace[i+1]))
  }

  // P4a — HistoricalFidelity
  lemma HistoricalFidelity(trace: seq<State>, n: nat, a: Tumbler, d: Tumbler)
    requires ValidTrace(trace)
    requires n < |trace|
    requires (a, d) in trace[n].R
    ensures exists k :: 0 <= k <= n && (a, d) in trace[k].contained
    decreases n
  {
    if n == 0 {
    } else {
      assert ValidStep(trace[n-1], trace[n]);
      if (a, d) in trace[n-1].R {
        HistoricalFidelity(trace, n-1, a, d);
      }
    }
  }
}
