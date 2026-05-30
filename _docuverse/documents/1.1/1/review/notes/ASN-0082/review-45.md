# Review of ASN-0082

## REVISE

### Issue 1: Core arithmetic derivations rest on ASN-0034 lemmas absent from the foundation

**ASN-0082, "Ordinal Extraction" (PositiveOffsetExceeds), I3-S, D-S, D-SEP**: The proofs repeatedly cite `NAT-sub` (left-/right-telescoping, right-inverse), `NAT-addbound` (left-/right-dominance), `NAT-cancel` (mirror form), and `NAT-addassoc`, all attributed to "ASN-0034."

**Problem**: None of these appear in the ASN-0034 foundation vocabulary. The only NAT axioms supplied are NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder. Critically, NAT-addcompat gives order-compatibility only for the *left-fixed* summand (`n ≥ p ⟹ m + n ≥ m + p`) and NAT-closure gives only the *left* identity (`0 + n = n`). The recurring dominance step `p₂ + c > c` (PositiveOffsetExceeds in the form `a + b > b`) is the left-summand form, which is *not* derivable from the extracted foundation — which is precisely why the author reaches for NAT-addbound/NAT-cancel. The ASN even acknowledges "the foundation offers no commutativity-of-`+` axiom," then derives the commutativity instance `n + ℓₘ = ℓₘ + n` (I3-S) and `c + c' = c' + c` (D-S) from these *also-absent* lemmas. Every span-width-preservation result (I3-S, D-S) and the gap-closure lemma D-SEP therefore rest on uncited content.

**Required**: Either restate these as available foundation axioms (confirming they exist in ASN-0034) or rebuild PositiveOffsetExceeds, I3-S(a), D-S(a), and D-SEP using only NAT-addcompat/closure/discrete/order/wellorder. If the left-summand dominance is genuinely underivable, that is a foundation gap to resolve before this ASN can stand.

### Issue 2: ASN-0036 citations to S7c and S9 reference nonexistent foundation claims

**ASN-0082, I3-S7, S7-post, I3-C**: "satisfies S7a …, S7b …, S7c (ElementFieldDepth), S7d …"; and "S9 (TwoStreamSeparation, ASN-0036) guarantees existing content is preserved."

**Problem**: The ASN-0036 foundation extract contains S7a, S7b, S7d, and the derived S7, but no S7c. S7's own dependency list in the foundation names "S7a, S7b, S7d together with S0, S4" — pointedly omitting S7c — strongly indicating S7c does not exist. Likewise there is no S9 (TwoStreamSeparation) in ASN-0036. I3-C's justification and the allocation-preservation lemmas thus cite phantom foundation content.

**Required**: Remove the S7c conjunct (or justify the element-field-depth property from an existing claim), and replace the S9 citation in I3-C with the actual content-preservation source (S0 already supplies `dom(C) ⊆ dom(C')` with value preservation).

### Issue 3: Ordinal toolkit cited as foundation but not present in the extract

**ASN-0082, "Ordinal Extraction"**: `ord(v)`, `vpos(S, o)`, `w_ord`, and `OrdAddHom` are each marked "(cited, ASN-0036)."

**Problem**: The provided ASN-0036 foundation includes OrdShiftHom but none of ord/vpos/w_ord/OrdAddHom. The entire contraction construction (σ(v) = vpos(S, ord(v) ⊖ w_ord), D-SEP's `ord(r) ⊖ w_ord = ord(p)`, D-BJ) depends on these definitions and on OrdAddHom(a). If they are not foundation-stable, the contraction proof is unfounded; if they are, the extract is inconsistent.

**Required**: Confirm these are present in the current ASN-0036 and correct the foundation reference, or define them within this ASN. As written they cannot be verified self-containedly.

### Issue 4: I3-V redundancy explained at length instead of resolved

**ASN-0082, I3 narrative**: "I3-V is *not* an independent constraint, however — it is a corollary of I3-CS restricted to v ∈ dom(M(d))… I3-V is retained in the postcondition list for readability: the explicit vacating clause names which pre-state positions are emptied, complementing I3-CS's negative closure…"

**Problem**: This is defensive meta-prose justifying the retention of a clause the ASN itself proves redundant. The reader must work past a paragraph arguing why a non-load-bearing postcondition is kept. Either I3-V carries content (then state it as a derived lemma with a one-line proof) or it does not (then drop it). The "retained for readability / maps cleanly to operational implementations" rationale is the bloat pattern flagged for this note.

**Required**: Demote I3-V to a one-line corollary of I3-CS, or remove it. Delete the justification paragraph.

### Issue 5: Duplicated wp "recipe" prose and parallel deferrals across the two halves

**ASN-0082, I3-S2 wp analysis and S2-post wp analysis**: Both close with near-identical framing ("This is the same recipe as I3-VP/S8a-post …") and both end with an identically structured paragraph ("The remaining post-state lemmas … admit wp derivations of the same form … we have not worked them in detail because the obligations they surface are subsumed …").

**Problem**: Two sections say the same methodological thing in different words, and the same "not worked in detail" deferral appears twice. Combined with the repeated deferrals to "a future INSERT ASN" (Scope paragraph, I3-C discussion, gap-region paragraph), this is the cross-cycle accretion the anti-bloat classifier targets: multiple paragraphs deferring to the same downstream location and restating one recipe.

**Required**: State the wp recipe once, reference it from the second occurrence, and consolidate the future-INSERT-ASN deferrals into a single Scope sentence.

## OUT_OF_SCOPE

### Topic 1: Deeper-than-2 contraction (ordinal depth > 1)
The TA4 obstruction at `#p > 2` is correctly identified as requiring new analysis; restricting contraction to `#p = 2` is a legitimate scoping choice, and the generalization belongs in a future ASN (as the Open Questions note).

### Topic 2: Content placement filling the insertion gap
Allocating the n new I-addresses at `[p, shift(p, n))` and re-establishing D-CTG/D-MIN/D-SEQ for the full INSERT post-state is properly deferred; the shift sub-operation specified here is a coherent unit.

VERDICT: REVISE
