# Review of ASN-0036

The mathematics here is mature and largely sound — S1, S4, S5, S7, S8, S8a, D-CTG-depth, and D-SEQ all carry explicit, case-complete proofs; boundaries (empty arrangement, single position, m=2 vs m≥3) are handled; and a concrete worked example exercises S0/S3/S5/S7/S8/D-SEQ across three states. My findings are concentrated in the anti-bloat dimension this note's classifier flags, plus a near-duplication.

## REVISE

### Issue 1: S5 verification opens with proof-methodology essay
**ASN-0036, S5 proof ("We verify each invariant")**: "S5 is a non-entailment result — it asserts that unbounded sharing is *consistent* with S0∧S1∧S2∧S3, not that any particular operation set reaches Σ_N; hence any model of S0∧S1∧S2∧S3 exhibiting the sharing multiplicity is a sufficient witness, and the witness need not be a reachable state. A state Σ satisfies a transition invariant iff every transition incident to Σ does; we exhibit Σ_N as an isolated state with no incident transition, so the universal quantification is vacuous."
**Problem**: Two of these three sentences explain *why the proof technique is legitimate* (non-entailment, witness-need-not-be-reachable) rather than executing the verification. This is defensive justification in a structural slot — the reviser-drift pattern. The only load-bearing fact is the third clause: S0/S1 quantify over transitions, Σ_N has none, so they hold vacuously. (The git history records this as the recently-touched "S5 witness rationale.")
**Required**: Collapse to the operative sentence: "S0 and S1 quantify over transitions; Σ_N is exhibited with no incident transition, so both hold vacuously." Drop the meta-commentary on non-entailment and reachability.

### Issue 2: "Document as arrangement" Remark restates the section body
**ASN-0036, The document as arrangement / Remark**: body says "Two documents d₁ ≠ d₂ may render identically … Yet they remain distinct documents"; the Remark says "Document identity does not rest on rendered content. Two documents that render identically may arise from different arrangements … so identity rests on document identifiers … not on rendered content."
**Problem**: The conclusion ("render identically yet distinct; identity ≠ rendered content") is stated twice in different words — the "two paragraphs say the same thing" pattern. The Remark's only genuinely new content is the *different-I-addresses-with-equal-values* scenario (the body covers only the *same-I-address* case).
**Required**: Merge. Keep one statement of the conclusion and fold the distinct second scenario (different I-addresses, equal values) into the body rather than carrying it as a separate Remark.

### Issue 3: Redundant aside in S5 cross-document construction
**ASN-0036, S5 cross-document construction**: "The pairs `(dᵢ, v)` are pairwise distinct because the first coordinates `dᵢ` are pairwise distinct, which suffices for distinctness of pairs."
**Problem**: "which suffices for distinctness of pairs" restates the sentence's own claim; and "all S5 requires of them, since S0–S3 treat `d` only as an index into `M`" is an explanatory aside that does not advance the construction.
**Required**: Trim to "The pairs `(dᵢ, v)` are distinct since the `dᵢ` are distinct."

## OUT_OF_SCOPE

### Topic 1: Editing operations preserving D-CTG/D-MIN/S2 and subspace alignment
The Open Questions correctly defer (a) what INSERT/DELETE/COPY/REARRANGE must guarantee to preserve the contiguity invariants, and (b) the V-position↔I-address subspace-alignment obligation. These are operation-layer concerns, properly out of scope per the ASN's own Scope section, and are not errors in this ASN.

META: not applicable — the ASN defines state (Σ.C, Σ.M), invariants on that state (S0–S8, D-CTG family), and abstract well-formedness, all stated implementation-independently; it has not drifted into mechanics.

VERDICT: REVISE
