# Review of ASN-0047

## REVISE

### Issue 1: P7a "derivation" box is a forward pointer that duplicates the Class (b) argument
**ASN-0047, *Cross-layer invariants*, P7a**: "*Derivation.* P7a is a composite-boundary property, not an elementary invariant: between a K.α event and its coupled K.μ⁺/K.ρ it transiently fails. It is discharged at composite boundaries in the *Class (b)* proof below (see the P7a row...), where J0 supplies the witnessing `v ∈ dom(M'(d))`... and J1★ then supplies `(a, d) ∈ R'`. ∎"
**Problem**: The box labeled *Derivation* contains no derivation — it previews the J0→S3★+L14→J1★ chain and then defers. That identical chain is then stated in full a third time in the Class (b) P7a paragraph ("J0 supplies `d ∈ E'_doc`... Suppose for contradiction `subspace(v) = s_L`... J1★ supplies `(a, d) ∈ R'`"). This is forward-reference accretion: the same argument appears in the definition box, the verification-matrix row, and the per-property paragraph. (The git log entry "add P7a derivation note" suggests recent accretion.)
**Required**: Keep one substantive statement of the chain (Class (b)) and reduce the Cross-layer P7a box to a one-line pointer ("composite-boundary property, discharged in Class (b)"). Do not state the witness chain twice.

### Issue 2: Defensive anti-circularity prose in K.μ⁻ admissible-contraction-shape reverse direction
**ASN-0047, *K.μ⁻ admissible contraction shape*, reverse direction**: "The post-state invariants are hypothesised on a *candidate* contraction `M_cand(d)`, **not** on the constructive form being shown equivalent." ... "Those three are themselves discharged from the genuine hypothesis `dom(M_cand(d)) ⊂ dom(M(d))` with value-preservation on survivors — **not** from any restriction conclusion."
**Problem**: The repeated "not on X" / "not from Y" guarding restates the same non-circularity point twice and reads as a defense against a prior reviewer concern rather than advancing the proof. The actual derivation (S8-fin from finite-subset, S8a/S8-depth from survivor shape, then D-SEQ★, then the φ_S bijection) stands on its own; the disclaimers are meta-prose.
**Required**: State the hypothesis once (candidate `M_cand` with the listed properties) and derive. Drop the "not …" disclaimers.

### Issue 3: SubAllocatorBundle glossary row is an essay / use-site inventory in a structural slot
**ASN-0047, *Properties Introduced* table, SubAllocatorBundle row**: a multi-sentence paragraph re-enumerating the inherited ASN-0093 lemmas (FirstEmission, FirstEmissionFreshness, DisjointSubAllocatorChains, ChainDiscipline, ChainElementT4Validity, ChainEnumerationInjectivity) and restating "the one obligation discharged *beyond* them."
**Problem**: A glossary row should state the property. This row reproduces the inheritance accounting that already lives verbatim in the SubAllocatorBundle definition box — a use-site inventory duplicated into a structural slot.
**Required**: Compress to the property statement plus a pointer to the definition box; the lemma inventory belongs in one place only.

## OUT_OF_SCOPE

### Topic 1: Empty-from/to endsets and one-sided/type-only link semantics
**Why out of scope**: The ASN's K.λ admits `e₁`/`e₂` empty (only `e₃ ≠ ∅` required), and the distinguishability of one-sided vs. type-only markers is already listed as an Open Question. This is future link-semantics territory, not an error in the transition model.

### Topic 2: Renumbering-aware interior link-arrangement contraction (interior DELETEVSPAN)
**Why out of scope**: K.μ⁻ models suffix-removal contraction only; interior compaction/renumbering is correctly deferred to a future ASN and flagged in the Open Questions. Operation-level DELETEVSPAN mechanics are scoped out.

The technical content I checked — the K.δ case-(ii) discharge tree, the K.μ~ full-clearance decomposition (admissibility (i)–(v), Steps A/B, K.μ~-FIX/RANGE), the J0/J1★/J1'★ couplings, S3★/S3★-aux, D-CTG★/D-MIN★/D-SEQ★ derivation (both m=2 and m≥3), the fork φ-bijection (order + multiplicity, incl. the duplicate-I-address and depth-rebasing worked cases), and the Class (a)/(b) induction split — is internally consistent, with boundary cases (empty arrangement, full clearance, fresh document, orphan link) covered. No correctness defect found. The remaining items are accreted meta-prose.

VERDICT: REVISE
