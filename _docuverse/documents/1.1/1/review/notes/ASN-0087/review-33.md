# Review of ASN-0087

## REVISE

### Issue 1: Foundation claims cited under wrong labels/names
**ASN-0087, Preconditions**: "L14 (StoreDisjointness, ASN-0093) confirms internal consistency at `Σ_mid`"
**Problem**: ASN-0093 names this invariant **SD**, not L14. L14 is the *ASN-0047* label for the same content. The citation pairs an ASN-0047 label with an ASN-0093 source.
**Required**: Cite either "SD (ASN-0093)" or "L14 (ASN-0047)" — not the mismatched pair.

Additional naming drift against the foundation (each confuses a reader cross-referencing the source):
- "P4a (HistoricalFidelity)" (Composite-Boundary Properties) — ASN-0047 names P4a **TraceWitnessing**.
- "J0 (AllocationRequiresPlacement)" — ASN-0047 J0 is **AllocationPlacementCoupling**.
- "J1★ (ExtensionRecordsProvenanceContentSubspace)", "J1'★ (ProvenanceRequiresExtensionContentSubspace)", "P4★ (ProvenanceBoundsContentSubspace)" — foundation names are **ExtensionRecordsProvenance**, **ProvenanceRequiresExtension**, **ProvenanceBounds**.
**Required**: Use the foundation's labels/names verbatim, or drop the parenthetical gloss.

### Issue 2: M-DepthConv stated twice, with internal self-repetition
**ASN-0087, Inputs / Claims table**: The full M-DepthConv argument ("commits to the minimal admissible depth `m = 2` … S8-depth pins `m_L(d) = 2` … scoped universal … normative commitment, not a system-wide invariant") appears in the Inputs prose and is then restated nearly verbatim in the M-DepthConv claims-table row.
**Problem**: Duplicate content; the Inputs paragraph also repeats its own conclusion ("normative commitment, not a system-wide invariant") which the table row repeats again ("Not a system-wide invariant").
**Required**: State the convention once in prose; let the table row be a one-line pointer.

### Issue 3: Reflexive-endset reasoning repeated across five sites
**ASN-0087, Worked Example (Reflexive variant) / Weakest Precondition (Case 2) / Reflexive Endsets / Atomicity / M-Reflexive**
**Problem**: The same fact — "`ℓ ∈ coverage(eᵢ)` forces `discoverable_from(ℓ, d, Σ')` via `v_ℓ`, and standard authoring structurally excludes it" — is restated in five locations in different words. The standalone "Reflexive Endsets" section adds nothing the wp Case 2 disjunct and M-Reflexive do not already carry.
**Required**: Consolidate to one derivation (the wp Case 2 reflexive disjunct is the natural home); reduce the others to references.

### Issue 4: Defensive / meta-prose that does not advance the argument
**ASN-0087, Inputs (Standard authoring) / Reflexive Endsets / Inputs (Endsets and emptiness) / Weakest Precondition (Operation enabledness)**: e.g. "This is a *structural* constraint … not an epistemic constraint on the caller's knowledge"; "Standard authoring is a construction discipline, not an architectural barrier"; "The analysis below covers this case implicitly through the existential … empty slots simply fail to witness"; the "Operation enabledness" paragraph explaining *why* `enabled(op)` is conjoined.
**Problem**: These justify or pre-empt rather than state the claim; the reader must skip past them to follow the reasoning.
**Required**: Delete the defensive framing; keep only the operative statements (`StandardAuthoring(e, Σ) ≡ …`; `coverage(∅) = ∅`; the wp definition).

### Issue 5: Claim asserted without derivation
**ASN-0087, M-PriorLinkDisc (claims table)**: "Composition across MAKELINK sequences preserves all per-state invariants (LP9, LP13, L12)."
**Problem**: "All per-state invariants" is not derived anywhere, and the three cited lemmas (extension monotonicity, link persistence, link immutability) establish only discoverability/store facts — not the full per-state invariant package. The sentence is a tacked-on assertion beyond what M-PriorLinkDisc's body proves.
**Required**: Either derive the claim (name the invariants and the chain) or delete it; M-Inv-State already carries the actual per-state preservation result.

### Issue 6: Open Questions restating matters resolved in the body
**ASN-0087, Open Questions**: "At what abstraction layer is MAKELINK's composite-level atomicity guaranteed…" is answered in *Atomicity* (protocol layer); "Under what conditions may a link's V-position move within the home document's link subspace…" is answered in *Permanence* (K.μ~ fixes link positions by admissibility (v); only K.μ⁻ removes).
**Problem**: Posing already-resolved questions as open inflates the section and contradicts the body.
**Required**: Remove the resolved questions or recast them as the residual genuinely-open part (e.g. cross-document V-position movement, if any).

## OUT_OF_SCOPE

None. The note stays within MAKELINK mechanics; INSERT/DELETE/COPY/REARRANGE/version/replication are correctly absent.

VERDICT: REVISE
