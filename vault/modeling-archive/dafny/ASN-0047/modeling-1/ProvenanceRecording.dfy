include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// K.ρ — ProvenanceRecording (POST)
// R' = R ∪ {(a, d)} where a ∈ dom(C) ∧ d ∈ E_doc
// Frame: C' = C; E' = E; (A d :: M'(d) = M(d))
module ProvenanceRecording {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Arr = map<Tumbler, Tumbler>

  datatype State = State(
    C: map<Tumbler, nat>,
    E: set<Tumbler>,
    M: map<Tumbler, Arr>,
    R: set<(Tumbler, Tumbler)>
  )

  function E_doc(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.DocumentAddress(e)
  }

  // ---------------------------------------------------------------------------
  // K.ρ — ProvenanceRecording
  //
  // R' = R ∪ {(a, d)} where a ∈ dom(C) ∧ d ∈ E_doc
  // Frame: C' = C; E' = E; (A d :: M'(d) = M(d))
  // ---------------------------------------------------------------------------

  ghost predicate Post(s: State, s': State, a: Tumbler, d: Tumbler) {
    a in s.C &&
    d in E_doc(s) &&
    s'.R == s.R + {(a, d)} &&
    s'.C == s.C &&
    s'.E == s.E &&
    s'.M == s.M
  }

  // The new pair is in provenance
  lemma RecordingAddsEntry(s: State, s': State, a: Tumbler, d: Tumbler)
    requires Post(s, s', a, d)
    ensures (a, d) in s'.R
  { }

  // Existing provenance is preserved
  lemma RecordingPreservesExisting(s: State, s': State, a: Tumbler, d: Tumbler)
    requires Post(s, s', a, d)
    ensures s.R <= s'.R
  { }

  // Provenance grows by exactly {(a, d)}
  lemma RecordingExactGrowth(s: State, s': State, a: Tumbler, d: Tumbler)
    requires Post(s, s', a, d)
    ensures s'.R == s.R + {(a, d)}
  { }

  // Frame: content unchanged
  lemma RecordingFrameContent(s: State, s': State, a: Tumbler, d: Tumbler)
    requires Post(s, s', a, d)
    ensures s'.C == s.C
  { }

  // Frame: entities unchanged
  lemma RecordingFrameEntities(s: State, s': State, a: Tumbler, d: Tumbler)
    requires Post(s, s', a, d)
    ensures s'.E == s.E
  { }

  // Frame: arrangements unchanged
  lemma RecordingFrameMapping(s: State, s': State, a: Tumbler, d: Tumbler)
    requires Post(s, s', a, d)
    ensures s'.M == s.M
  { }
}
