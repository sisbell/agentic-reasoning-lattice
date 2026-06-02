# Review of ASN-0047

## REVISE

### Issue 1: Content-subspace scoping rationale stated three times
**ASN-0047, P4★ / Scoped coupling constraints / J1★ derivation**: The argument "the unscoped `Contains(Σ) ⊆ R` cannot hold once any link-subspace mapping exists, because P7 grounds R in dom(C) and links live in dom(L)" appears in full three times:
- P4★: "The unscoped bound cannot hold once any link-subspace mapping exists: `Contains(Σ)` would then include `(ℓ, d)` ... yet provenance entries satisfy P7 ... `(ℓ, d) ∉ R`."
- Scoped coupling constraints: "Provenance coupling must be scoped ... for the same reason the unscoped bound `Contains(Σ) ⊆ R` fails against P7 (see P4★ above)..."
- J1★ derivation: "...where the unscoped bound `Contains(Σ) ⊆ R` is unsatisfiable once link-subspace mappings exist."

**Problem**: Two of the three are pure restatements of the first — the anti-bloat "two paragraphs in different sections say the same thing" pattern. The reasoning does not advance at the second and third sites.
**Required**: Keep the derivation at P4★ (its canonical home) and reduce the other two to a bare citation ("scoped per P4★"), removing the re-derived P7/L14 mechanics.

### Issue 2: Forward-reference accretion — repeated deferrals to one downstream location
**ASN-0047, K.μ⁻ definition and K.μ⁻ amendment**: Both defer to the same proof — "this equivalence is proved in *K.μ⁻ admissible contraction shape* below" (definition) and "is determined by the constructive precondition directly (see *K.μ⁻ admissible contraction shape* below)" (amendment). Likewise the "*Necessity and sufficiency of the precondition*" proof is forward-pointed from both the K.μ~ precondition list and ValidComposite★ clause (1).

**Problem**: This is the flagged "multiple paragraphs in different sections defer to the same downstream location" pattern; each duplicate pointer is navigational overhead that compounds across cycles.
**Required**: Retain a single forward pointer per target (the earliest use site) and drop the redundant restatements of what the downstream section will establish.

### Issue 3: K.δ case (ii) k=0 fork — `d_op ∈ E_doc` is a loose precondition
**ASN-0047, J4 Definition (Fork), precondition**: "The *precondition* is d_src ∈ E_doc ∧ d_op ∈ E_doc ∧ V_{s_C}(d_op) ≠ ∅, together with the per-sub-case activation condition ... the k = 0 sub-case fires when `A_v(d_src)` already has a frontier (a prior version exists, supplying prev_version)."

**Problem**: The binding that distinguishes a fork from an independent sibling-document creation — that the k=0 operand sits on `A_v(d_src)`'s frontier, not `A_doc(parent(d_src))`'s — is stated only in prose ("the discriminating fact is which allocator's frontier the k = 0 operand sits on"). The *formal* precondition conjunct for `d_op` is merely `d_op ∈ E_doc`, which any document satisfies. A reader checking the precondition mechanically cannot tell a fork from a sibling allocation from the listed conjuncts alone.
**Required**: Promote the discriminator into the formal precondition, e.g. `d_op ∈ dom(A_v(d_src))` (d_op is an emission of d_src's version sub-allocator), so the fork's defining structural fact is checkable from the precondition rather than recovered from narrative.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
The ASN's K.μ⁻ contracts the link subspace by suffix removal only; interior-link withdrawal with survivor renumbering is correctly deferred (already an Open Question and acknowledged at *D-CTG★/D-MIN★ Modeling choice*). This belongs to a future ASN, not a revision here.

### Topic 2: S8★(s_L) omission of maximal-run uniqueness
The link-subspace span decomposition drops ASN-0036 S8 condition (c) via the trivial length-1 decomposition. No downstream result in this ASN consumes link-subspace run uniqueness, so this is a deliberate scope boundary, not an error.

VERDICT: REVISE
