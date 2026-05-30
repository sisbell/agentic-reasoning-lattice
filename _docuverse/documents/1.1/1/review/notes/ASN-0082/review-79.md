# Review of ASN-0082

## REVISE

### Issue 1: Scoping axioms duplicated and re-cited at every use site

**ASN-0082, "Scoping axioms" + "Contraction formal contract"**: The dedicated paragraph
> "*Subspace axiom: S = 1.* The contraction operation is defined only on the text subspace. *Depth axiom: #p = 2.* V-positions in the text subspace have depth 2..."

restates the same two constraints that the formal contract immediately re-asserts as preconditions: "`S = 1` (subspace scoping axiom)" and "`#p = 2` (depth scoping axiom)". The parenthetical tags "(subspace scoping axiom)" / "(depth scoping axiom)" are then carried into nearly every downstream lemma statement (D-SHIFT, D-BJ, D-SEP, D-DP, S8-depth-post, D-CTG-post, D-MIN-post, D-SEQ-post …).

**Problem**: This is the "two paragraphs say the same thing" pattern plus use-site-inventory noise. The constraints belong in one place (the formal contract preconditions). The repeated parentheticals do not advance any proof — they are bookkeeping the reader must skip.

**Required**: Drop the standalone "Scoping axioms" paragraph; keep `S = 1` and `#p = 2` as ordinary preconditions in the contract. Remove the "(scoping axiom)" tags from individual lemma statements.

### Issue 2: D-BJ part (c) is proof-by-restatement

**ASN-0082, D-BJ (ShiftBijectivity)**: 
> "*Proof of (c).* Q₃ is defined as {σ(v) : v ∈ R}, so surjectivity holds by construction. ∎"

**Problem**: Surjectivity onto a set defined as the image is vacuous — it carries zero content. The bijection's real obligation is injectivity, discharged in (b). Listing (c) as a proof obligation and "discharging" it by quoting the definition of Q₃ is exactly the checkmark-grade non-proof the standards forbid.

**Required**: Either delete (c) and retitle the lemma "order-preserving injection R → Q₃," or, if "bijection" is wanted for downstream phrasing, state once that Q₃ is *defined* as the image so σ : R → Q₃ is bijective, without dressing it as a separate proof.

### Issue 3: Triplicated frame-note prose in the cross-subspace worked example

**ASN-0082, "Cross-subspace preservation" verification (contraction)**: three consecutive verification lines repeat the same sentence in different clothing:
> "...Non-text V_2(d') ... preserved verbatim by D-CS — the foundation imposes no D-CTG obligation on V_2."
> "...Non-text V_2(d') preserved by D-CS — the foundation imposes no D-MIN obligation on V_2..."
> "...Non-text V_2(d') preserved by D-CS — the foundation imposes no D-SEQ obligation on V_2..."

**Problem**: One claim — "D-CS carries V_2 verbatim; D-CTG/D-MIN/D-SEQ do not apply to V_2" — is stated three times. The per-invariant ✓ for V_1 is the substance; the V_2 clause is identical noise on each line.

**Required**: Verify D-CTG-post/D-MIN-post/D-SEQ-post for V_1 only, and state the V_2 exemption once (it is already covered by the D-CS line in the same verification block).

### Issue 4: The S ≠ 1 "active" insertion case is asserted but never exercised

**ASN-0082, end of insertion section**: 
> "When the link subspace is itself the active (shifted-into) region, a shifted image may land in a former tombstone slot — permitted, because link sparsity, not gap structure, is the invariant."

**Problem**: I3 is stated for any `S ≥ 1`, and this is the one non-trivial, surprising consequence (a shift target coinciding with a tombstoned slot), yet every worked example uses `S = 1` active. Standard 6 requires a concrete check of the non-obvious postcondition; the case actually claimed to differ from the text-subspace case is the one left unverified.

**Required**: Add a short worked example with `S = 2` as the shifted region (e.g. M(d) with a sparse V_2 containing a tombstone gap), tracing I3, I3-V, I3-CS to confirm a shifted image landing in a former tombstone slot raises no S2/S3 conflict — or, if that scenario belongs to a future link-insertion ASN, move the assertion there rather than leaving it unbacked here.

## OUT_OF_SCOPE

### Topic 1: Contraction at ordinal depth > 1

**Why out of scope**: The `#p = 2` restriction and the TA4 zero-prefix vs. S8a-positivity collision are already named in the Open Questions. Generalizing D-SEP/D-DP and the projection round-trip to deeper ordinals is genuinely new territory, correctly deferred.

VERDICT: REVISE
