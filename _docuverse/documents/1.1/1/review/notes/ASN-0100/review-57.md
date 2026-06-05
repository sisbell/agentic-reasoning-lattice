# Review of ASN-0100

This is a thorough, largely rigorous ASN. The three-effect decomposition, the worked examples (interior, append, empty), the wp analysis, and the per-intermediate invariant discharge in §Atomicity meet the depth bar. The references are confined to the foundation ASNs (no stray cross-references). Findings below are a citation-precision gap and accumulated meta-prose flagged under the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Shifted-right provenance grounded in the wrong invariant
**ASN-0100, §Verifying the Invariants → Provenance (R, P4★, P4a, P7a)**: "The pair `(a, d)` was already in R via the historical state (preserved by P2, ProvenancePermanence; ASN-0047)."
**Problem**: For a Shifted-right address `a = M(d)(v)`, the conclusion required is `(a, d) ∈ R'`. P2 only *preserves* existing R entries — it does not *establish* that `(a, d)` was ever in R. The existence step is missing from this clause. The rigorous grounding is pre-state P4★: `(a, d) ∈ Contains_C(Σ) ⊆ R` (because `a` was in `d`'s content-subspace range at the composite boundary Σ), then P2 lifts it to R'. The note in fact uses pre-state P4★ correctly two paragraphs later in the P4★ discharge, which makes this looser P2-only citation an internal inconsistency in justification rigor.
**Required**: Replace the P2-only citation with the chain "pre-state P4★ gives `(a, d) ∈ R`; P2 preserves to R'," or cross-reference the P4★ paragraph that already does this.

### Issue 2: §INSERT vs. COPY specifies an out-of-scope operation in prose
**ASN-0100, §INSERT vs. COPY: Identity Through Allocation**: "COPY (out of scope here) creates V→I mappings to *existing* I-addresses without allocating new content. The original document remains the home of the bytes; attribution stays with the original author. The Vstream effect can be made indistinguishable from an INSERT..."
**Problem**: COPY mechanics are explicitly OUT OF SCOPE. Per the anti-bloat lens, the legitimate content here is the single contrast that *fixes INSERT's identity character* (INSERT allocates fresh I-addresses). That point is already carried by claim INS.identity and the cross-doc / version / tight-survival corollaries. The multi-paragraph exposition of COPY's home-document semantics, attribution flow, and Vstream-indistinguishability is specifying the out-of-scope operation, not advancing INSERT's argument — a reader must skip past it to reach the corollaries.
**Required**: Collapse the COPY description to the one-sentence contrast needed for INS.identity; remove the paragraphs that specify COPY's own semantics.

### Issue 3: Narrative/editorial meta-prose in structural slots
**ASN-0100, §Background: The Two-Stream Asymmetry**: "This asymmetry is the architectural pivot." / "We shall see that every constraint on INSERT — what may shift, what must be preserved, what counts as atomic — flows from this single asymmetry." And §Effect One: "That last guarantee is the most important."
**Problem**: These sentences make rhetorical claims about the argument rather than advancing it; the "flows from this single asymmetry" promise is never discharged as a structural dependency and reads as essay framing. They are the residue the anti-bloat classifier is meant to catch.
**Required**: Delete the editorializing sentences, or replace with the concrete object-level fact (e.g., "INSERT never reassigns an existing I-address," which is already stated).

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion, COPY, DELETE/REARRANGE, version derivation, replication
**Why out of scope**: The §Bounding the Scope and Open Questions sections correctly fence these off; no remediation needed. INS.identity.version is acceptable as an INSERT-identity corollary because it states INSERT's allocation independence *given* a version exists rather than specifying version creation.

META: not applicable — the ASN defines an operation on state in terms of abstract substrate transitions and post-state invariants; it has not drifted into implementation mechanics (the "knife" appears only as illustration).

VERDICT: REVISE
