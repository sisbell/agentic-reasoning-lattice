# Review of ASN-0087

## REVISE

### Issue 1: Defensive "genuine vs derived precondition" meta-prose
**ASN-0087, Preconditions**: "We must be careful to state K.λ's *genuine* preconditions, distinguishing them from facts that hold *as consequences* of those preconditions." … "We invoke these as *derived* facts wherever the K.μ⁺_L derivation and the invariant arguments below need them — never as caller obligations."
**Problem**: This is justification of *how* the precondition is presented plus a use-site inventory ("wherever … need them — never as caller obligations"), not advancement of the argument. The substantive content is one line: the precondition is K.λ's; freshness and shape are ASN-0093 lemmas of any A_L(d) emission. The surrounding "we must be careful," "are *not* additional preconditions," "never as caller obligations" is the forward-reference accretion the anti-bloat classifier targets — a reader skips it to reach the precondition block.
**Required**: State the precondition (M-Pre) and mark freshness/shape as derived once, without the meta-framing or the downstream-consumer inventory.

### Issue 2: Redundant freshness derivation
**ASN-0087, Preconditions + "Freshness of the Allocation"**: Preconditions already invokes `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)` citing "[FirstEmissionFreshness, SubsequentEmissionFreshness]" to discharge `ℓ ∉ ran(M(d))`. The later standalone section "Freshness of the Allocation" re-asserts "The address `ℓ` is genuinely new — `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`" and re-cites the same two lemmas.
**Problem**: Two passages in the same document establish the same fact from the same lemmas; the only content unique to the dedicated section is the first-emission/subsequent-emission split. This is the "same thing in different words" pattern.
**Required**: Keep the case-split derivation in one location and have the other site reference it, rather than independently re-invoking the lemmas.

### Issue 3: D-CTG★ asserted by bare phrase, discharge left implicit
**ASN-0087, Invariant Preservation (per-state table)**: "D-CTG★: extension is contiguous — K.μ⁺_L positioning rule."
**Problem**: D-CTG★ is the contiguity conjunct; its actual discharge is the explicit set computation in the D-SEQ★ paragraph (`V_{s_L}^{Σ'}(d) = {[s_L,1,...,1,k] : 1 ≤ k ≤ n_L+1}`). The table gives a one-phrase justification and the D-SEQ★ paragraph never states that it also discharges D-CTG★, so the reader must connect them. Since ASN-0047 derives D-SEQ★ *from* D-CTG★, the direction of discharge should be made explicit to avoid the appearance of circularity.
**Required**: Point the D-CTG★ entry at the D-SEQ★ set computation (which directly exhibits a contiguous initial segment), or add one line in the D-SEQ★ paragraph noting it discharges D-CTG★ directly.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets
Open Question 1 ("what constraints must endsets satisfy when spans reference unallocated I-addresses") is partially answered in-note by the StandardAuthoring discipline and M-FreshExcl; the residual general constraint question is genuinely a future-ASN concern (endset well-formedness theory), not an error here.

VERDICT: REVISE
