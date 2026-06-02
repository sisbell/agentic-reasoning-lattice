# Review of ASN-0047

I checked the elementary transitions and their frames, the coupling constraints (J0/J1★/J1'★), the K.μ~ decomposition and its admissibility/necessity arguments, the FrontierEquivalence lemma, the D-SEQ★ derivation (both depth cases), the K.μ⁻ shape-equivalence proof, and the Class (a)/Class (b) verification. The core reasoning holds: the matrix is complete over invariant × transition, base case Σ₀ is discharged conjunct-by-conjunct, and the load-bearing lemmas (FrontierEquivalence, K.μ~-FIX, link-subspace fixity, the necessity/sufficiency of the K.μ~ precondition) are proved rather than asserted. The findings below are accretion the anti-bloat classifier flags, not defects in the claims.

## REVISE

### Issue 1: Use-site inventory in the layer-separation note advances no reasoning
**ASN-0047, *Amendments to existing transitions*, "Modeling choice (layer separation)"**: "The downstream results built on the link-subspace shape (D-SEQ★, the K.μ⁻ contraction, CL-UNIQ, and worked-example Step 5) rest on the discharged invariant."
**Problem**: This is a downstream-consumer inventory — it enumerates where the invariant is later used rather than advancing what D-CTG★/D-MIN★ mean or why they hold. It is exactly the "definition's introduction enumerates downstream consumers" pattern the classifier names. The first two sentences of the paragraph (M(d) vs. dom(L); L12 discharges link permanence) are the load-bearing content; the inventory sentence and the trailing "Modeling interior link withdrawal requires a renumbering-aware contraction…" pointer to Open Questions are scaffolding.
**Required**: Delete the use-site inventory sentence. Keep the substantive point (the strengthening constrains only `M(d)`, and link permanence is discharged on `dom(L)` by L12); leave the interior-withdrawal limitation to the Open Questions entry that already states it, without a forward pointer here.

### Issue 2: ValidComposite★ is restated in full before its definition, then defined again
**ASN-0047, *Coupling and isolation* (P4★ region)**: "Validity of a composite transition `Σ →* Σ'` is defined as **ValidComposite★** in *Scoped coupling constraints*: a finite sequence of atomic transitions whose every step satisfies its elementary precondition (clause 1) and whose net effect between Σ and Σ' satisfies the coupling constraints J0, J1★, and J1'★ (clause 2)."
**Problem**: This reproduces both clauses of ValidComposite★ — which is then stated in full, in its own definition box, in *Scoped coupling constraints*. The P4a definition box and J2/J3 also defer to ValidComposite★. This is the "two paragraphs say the same thing in different words" / "multiple paragraphs defer to the same downstream location" pattern, a symptom of P4★ being introduced before the definition it depends on.
**Required**: Replace the inline restatement with a bare forward pointer ("ValidComposite★, defined in *Scoped coupling constraints*"). The single authoritative two-clause statement should live only at the definition site.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal (renumbering-aware link contraction)
**Why out of scope**: K.μ⁻ models link-subspace contraction by suffix removal only; interior withdrawal with survivor renumbering is genuinely new operational territory. It is correctly deferred to the Open Questions list, and L12 already discharges link *permanence* on `dom(L)` independently of the arrangement, so this is not a gap in what the ASN claims.

VERDICT: REVISE
