# Review of ASN-0116

This ASN is in strong shape: the composite decomposition (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n) is exhibited explicitly with per-step precondition discharge, the gapped/filled bridge correctly handles the fact that ASN-0082's I3 family specifies the vacated arrangement rather than the filled one, the forward-merge impossibility argument in IP1 is careful and correct, the IP6 wp correctly identifies containment (not emptiness) as the weakest form, and the worked example genuinely exercises the wp's discriminating case plus all three boundaries (front, append, empty ×2 sub-cases). Three issues remain.

## REVISE

### Issue 1: Categorical "not a superset" claim contradicts IP4's own case analysis
**ASN-0116, "Invariants the operation must preserve" (paragraph immediately preceding IP4)**: "the suffix witnesses are *relabelled* by `v ↦ shift(v, n)` — so the post-insert V-position set is *not* a superset of the prior one."
**Problem**: This is stated categorically, and IP4 — three paragraphs later — refutes it in two of its own cases. When the suffix part is empty, IP4 establishes `project(e, d, Σ) ⊆ project(e, d, Σ')`: the post-insert set **is** a superset. And even when suffix witnesses are present, IP4 says the reverse inclusion "may or may not hold" and explicitly admits the configuration `project(e, d, Σ) ⊊ project(e, d, Σ')` — again a superset. The summary sentence and the formal claim it introduces assert incompatible things; a reader who trusts the prose sentence will mis-state IP4.
**Required**: Hedge the sentence ("need not be a superset" / "is not in general a superset") or delete it and let IP4's case split carry the point.

### Issue 2: J1★ discharged only for the operated document
**ASN-0116, "INSERT as a valid composite", clause-2 paragraph**: "**J1★ (ExtensionRecordsProvenance)** — every content-subspace range-new address carries a record: the range-new addresses are exactly A_new, and I-PROV records `(shift(a, k), d)` for each."
**Problem**: J1★ quantifies universally over all documents in `E'_doc`, but the justification offered (RAN) is a statement about `d` alone. The instances `d' ≠ d` are never discharged: the claim "the range-new addresses are exactly A_new" is system-wide, yet nothing in the paragraph rules out a range-new address for some other document. Both missing pieces are one-liners already available in the Frame — F-DOC gives `M'(d') = M(d')`, so no address is new to any other document's content-subspace range, and F-ENT gives `E'_doc = E_doc`, so no freshly registered document enters the quantifier — but neither is invoked, so the universal is asserted on the strength of a single instantiation.
**Required**: Add the explicit instantiation for `d' ≠ d` (via F-DOC) and note `E'_doc = E_doc` (via F-ENT) in the J1★ discharge.

### Issue 3: Duplicated restatements (anti-bloat)
**ASN-0116, two locations**:
(a) **Frame clause F-SUB**: the parenthetical "(the block is wholly subspace-S, so the cross-subspace slice of `M'(d)` coincides with that of `M'₀(d)`)" re-derives, nearly verbatim, the bridge's cross-subspace clause already established in the Effect's introductory paragraph ("the union also leaves the *cross-subspace* slice of the gapped arrangement untouched — in every subspace `S' ≠ S`, `M'(d)` and `M'₀(d)` have the same positions and the same values"). Same fact, same justification, stated twice within one section.
(b) **Worked example, IP6-trap paragraph**: the closing "✓ IP6 (the distinction is containment, not emptiness; ℓ is exactly the member the emptiness form over-rejects)" restates the two sentences immediately preceding it ("The *sufficient* emptiness form `Added = ∅` is already violated by ℓ … the *weakest* containment form tolerates ℓ precisely because `ℓ ∈ D(d, Σ)`"), which in turn restate IP6's own "it over-rejects: it refuses the ghost-plus-live-span pre-states above." The same point is made three times across claim and example.
**Problem**: Both are restatements rather than citations — the reader must re-process an argument already closed, which is exactly the accretion pattern this note is flagged for.
**Required**: In F-SUB, cite the bridge's cross-subspace clause instead of re-deriving it. In the worked example, state the containment-vs-emptiness lesson once and close with a bare reference to IP6.

## OUT_OF_SCOPE

### Topic 1: Insertion into the link subspace (S = s_L)
**Why out of scope**: The precondition pins `S = s_C`, and link placement is correctly delegated to K.λ/K.μ⁺_L; the operation that exercises that path is MAKELINK territory per the declared scope, not a gap in this ASN.

### Topic 2: Concurrent insertions and serialization of K.α freshness
**Why out of scope**: The freshness argument presumes the sequential transition discipline of the substrate; what two unserialized authorities may claim is a genuine question, correctly parked in Open Questions rather than answered here.

VERDICT: REVISE
