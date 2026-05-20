# Review of ASN-0086

## REVISE

### Issue 1: R0's misleading forward reference to R2
**ASN-0086, R0 proof, "L-invariant preservation across the K.λ-step" block**: "we verify the ASN-0043 L-invariants by reading K.λ's contract together with R2 (TupleAddressPermanence, proved below from L12) and the consultation-derived chain lemmas."
**Problem**: R2 is not actually invoked anywhere in the L-invariant discharges that follow. L12, L12a, L12b, and L-fin are preserved by K.λ's effect directly. The forward reference is misleading and hints at circularity that doesn't actually occur.
**Required**: Remove the R2 mention from R0's opening sentence, or relocate it to a specific invariant discharge where R2 is actually used.

### Issue 2: R6b's framing conflates Definition consequence with separate claim
**ASN-0086, R6b — SingleDepthRetraction**: "Deciding `a ∈ nullified(Σ)` reduces to a single-pass existential check over `L_R^Σ`..."
**Problem**: R6b is labeled "DEF-Consequence" in the Properties table, and the Justification text says "R6b is a direct consequence of how the Definition of `nullified` quantifies its existential." If R6b reads directly off the Definition's quantification range, the headline claim is the wrong content to lead with — the substantive content is the decision-procedure flatness and the non-fixpoint semantics for retraction-of-retraction, not the membership reduction itself. The current framing leaves a reader unsure whether R6b is a tautology or a load-bearing lemma.
**Required**: Either fold R6b's substantive content into the Definition of `nullified` as a Notes section (titled "Decision procedure / non-fixpoint semantics on retraction-of-retraction"), or restructure R6b's body so the substantive content (flatness, non-fixpoint behavior on retraction-of-retraction) is the headline, with the membership reduction as supporting material.

### Issue 3: R7a's substrate-conforming Definition is partially formal
**ASN-0086, Definition — substrate-conforming layer**: "A layer is *substrate-conforming* iff every operation it publishes over `(Σ.C, Σ.M, Σ.L)` preserves every property the underlying substrate ASNs posit at each step."
**Problem**: The Definition has two parts (invariant catalog + chain-discipline extension), but the catalog is enumerated in narrative paragraphs interleaved with proof-discharge text, and the chain-discipline extension is presented later as a strengthening addendum. The phrase "every property the underlying substrate ASNs posit" is also vague — R7a's proof relies on specific predicates from ASN-0036/0043/0093 plus chain-discipline lemmas, and a reader has to bounce between the Definition and the proof's per-step discharge block to reconstruct the catalog.
**Required**: Reorganize the Definition into two named clauses — (a) Invariant Catalog (explicit list: L0–L14, L-fin, S0–S3, S7a–d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ, M0, M1, C0, C1, C1b, C1c, C-fin); (b) Chain Discipline Catalog (SubAllocatorAxiom, ChainMembershipForOrigin, and supporting lemmas). Make explicit that (b) is strict-strengthening over (a) — L1c alone admits non-chain emissions that (b) excludes — with the concrete example `a* = [d.0.s_L.1.1]` cited in (b)'s motivation.

### Issue 4: R5's proof structure buries the existence/admissibility claim
**ASN-0086, R5 — TupleSelfTargeting proof**: Five steps with most bulk dedicated to verifying L-invariants for the constructed self-targeting emission.
**Problem**: R5's substantive content is the admissibility of self-targeting endsets at slots 1 and 2 (Steps 1–3). Step 4's L-invariant verification largely recapitulates R0's invariant-preservation argument, which R5-Cor then generalizes for arbitrary L3-conforming triples. Steps 1–3 are load-bearing; Step 4 is verification that R5-Cor renders generic. The current ordering makes the load-bearing argument hard to find.
**Required**: Restructure to lead with admissibility (Steps 1–3), then cite R0 + R5-Cor for L-invariant verification. Alternatively, prove R5-Cor first and derive R5 as the application of R5-Cor at the specific self-targeting endset shape.

### Issue 5: Implementation Notes' informal introduction of layer-level commitment
**ASN-0086, Implementation Notes (Two Foundational Sets, sub-section "Unit-depth retraction discipline")**.
**Problem**: The unit-depth retraction discipline is the relational layer's principal layer-level commitment (per the Properties table COMMITMENT label) and is consumed by WP Case 2 regime (i), Definition of `relational layer`, and the relational-layer discharge of WP Case 2. But it's introduced in a section called "Implementation Notes" — an unusual location for a foundational commitment that downstream reasoning depends on. The scope ("every `L_R^Σ` tuple has unit-depth to-endset of the form `{(b, δ(1, #b))}`") is stated narratively rather than in a named clause.
**Required**: Promote the unit-depth retraction discipline to a top-level Definition (e.g., adjacent to the Three Operations section), with a precise scope statement. Move the "Implementation Notes" framing material to a footnote or to the closing discussion of WP Case 2.

### Issue 6: R0a-Cor1 framing as Corollary vs re-expression
**ASN-0086, R0a-Cor1 — ContiguousPrefix proof**: "This is a direct re-expression of ASN-0093's ChainMembershipForOrigin lemma applied to the link store."
**Problem**: A pure re-expression with index renaming (`J_d^Σ := n_d − 1`) doesn't carry substantive content beyond its source lemma. Presenting it as a Corollary/Lemma suggests there's mathematical content being established here, when the work is purely notational. Either there's content beyond the re-expression that should be made explicit, or this should be a Definition or a notation note.
**Required**: Either re-frame R0a-Cor1 as a Definition (with the notation translation `J_d^Σ := n_d − 1` stated explicitly), or add substantive content to the body (e.g., an explicit antichain consequence beyond what ChainMembershipForOrigin gives — perhaps the J_d^Σ = -1 empty-homed-set case has additional properties worth naming).

## OUT_OF_SCOPE

The ASN's Open Questions list captures legitimate out-of-scope items appropriately:
- Multi-arity links and `L_K^{(n)}` extension.
- Invariants between `L_K` and arrangements `Σ.M`.
- Operationally meaningful `Nullify(b)` for `b ∈ L_R`.
- Observe ordering and atomicity under concurrent emission.
- Cardinality bounds on `nullified(Σ)`.
- Whether L1b should be tightened to `#E = 2` at the source.
- Whether the unit-depth retraction discipline should be substrate-level.
- Cross-layer coordination on type-address `K` allocation.

No additional out-of-scope items identified.

VERDICT: REVISE
