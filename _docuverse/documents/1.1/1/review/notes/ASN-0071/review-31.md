# Review of ASN-0071

## REVISE

### Issue 1: Multiple forward references to the same worked-scenario subsections
**ASN-0071, "The query"**: "...the over-collection C0's `actionPoint = m` exists to prevent, exhibited concretely against a live arrangement under *Interior action point, rejected against an arrangement*" and "...the *prefix names subtree* semantics, exhibited concretely under *A cross-depth query*".
**Problem**: This is forward-reference accretion. Two separate deferrals point downstream into worked-scenario subsections to promise that the present claim will be demonstrated later. The reader must hold the promise and jump forward to discharge it. The definitional section should state the precondition and its effect; the worked scenario can exhibit it without an explicit back-pointer being planted upstream.
**Required**: Remove the "exhibited concretely under *...*" deferrals. Let the worked-scenario subsections stand on their own; the precondition discussion does not need to advertise them.

### Issue 2: Defensive justification imagining a case the precondition already excludes
**ASN-0071, "The query"**: "Take `u = [s_C] = [1]` with `ℓ = [2]`: it satisfies `Pos(ℓ)`, `#ℓ = #u = 1`, and `actionPoint(ℓ) = 1 = #u`, so it clears every vspec precondition except `actionPoint(ℓ) ≥ 2`, yet its action point falls on position 1 itself."
**Problem**: This paragraph constructs a depth-1 anchor in order to argue why `actionPoint(ℓ) ≥ 2` is needed — a case the precondition itself excludes by construction. This is the "imagines a case the precondition already excludes" reviser-drift pattern: prose explaining *why a precondition exists* rather than *what the operation does*. The precondition list already states `actionPoint(ℓ) ≥ 2` and that it forces `#u ≥ 2`; that statement is sufficient.
**Required**: Cut the worked counterexample motivating the precondition. State the precondition and the prefix-confinement consequence (`subspace(t) = s_C` for `t ∈ ⟦σ⟧`); do not litigate the excluded case.

### Issue 3: Duplicated motivation for accepting vspecs
**ASN-0071, "The query"**: opens with "Content can be named in two registers. By I-address... By V-position with source... We accept the latter," then closes with "Why vspecs and not direct I-addresses? Because users name content from where they encounter it... The operation accepts the user's name; resolution to I-addresses is its first task."
**Problem**: Two paragraphs in the same section make the same point in different words — content has two naming registers, vspecs use the V-position register because that is what users know. The closing paragraph adds no new reasoning.
**Required**: Delete the closing "Why vspecs and not direct I-addresses?" paragraph; the opening already establishes the choice.

### Issue 4: Duplicated currency-vs-history reconciliation
**ASN-0071, "Currency: state dependence"**: "Completeness is over the *currently-containing* set, not over the historically-containing set." **And "Permanence and currency reconciled"**: "The completeness guarantee of `find` is over *currency*. The completeness guarantee of `R` is over *history*."
**Problem**: Two sections deliver the same conclusion — `find` is present-tense, `R` is historical, and `find` does not consult `R`. The second section largely re-states the first with added versioning narration.
**Required**: Consolidate the find-vs-`R` distinction into one location. Keep the precise claim (F-CUR plus the `R`-coincidence condition) and remove the restatement.

### Issue 5: Implementation-conformance essay in the soundness section
**ASN-0071, "Completeness and soundness"**: "A specific failure mode is worth flagging. An implementation that maintains an auxiliary index... returns a *superset*... We do not adjudicate whether such relaxation is acceptable in practice..."
**Problem**: This is essay content about a hypothetical implementation's index-maintenance strategy, sitting in the slot that should state the abstract soundness guarantee. F-SOUND is fully characterized by the biconditional; the append-only-index narrative and the "we do not adjudicate" hedge do not advance the specification.
**Required**: Reduce to the structural point — any returned `d` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) = ∅` violates F-SOUND — and drop the index-implementation walkthrough.

### Issue 6: Use-site inventory appended to the composite-structure proof
**ASN-0071, "A worked scenario" (Composite structure)**: "...so ASN-0047's per-state and composite-boundary invariants hold at `Σ` — the foundation the home/transcluding recovery and F-FIN rely on."
**Problem**: The trailing clause enumerates downstream consumers of the reachability fact rather than advancing it. Reachability of `Σ` is what the paragraph establishes; naming which later claims lean on it is accretion.
**Required**: End the sentence at "hence reachable, so ASN-0047's invariants hold at `Σ`."

## OUT_OF_SCOPE

### Topic 1: Versioning-convention mechanics in "Permanence and currency reconciled"
**Why out of scope**: The detailed narration of deriving a new version-document and initializing its arrangement by transclusion ("When a document is to be modified, the design convention is to derive a new version-document...") is version-creation mechanics, which the scope list excludes. The *point* it serves (current vs historical containment) is in scope, but the version-derivation walkthrough belongs to a version-operation ASN, not here.

VERDICT: REVISE
