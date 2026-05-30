# Review of ASN-0084

## REVISE

### Issue 1: Post-state S8 derivation stated four times
**ASN-0084, R-SP and surrounding sections**: The claim "post-state S8 comes from foundation S8, not from B'" is restated at least four times:
- R-SP intro: "Post-state S8 itself is not discharged by B' — it follows from foundation S8, as shown below."
- R-SP body: "Post-state S8 is met by foundation S8 (ASN-0036) directly: ..."
- R-SP proof, S8 clause: "Existence and uniqueness of the maximal decomposition of M'(d) hold by foundation S8, whose preconditions are preserved ..."
- R-SP *Remark*: "Post-state S8 is supplied by the foundation, not by B': once the rearrangement preserves dom(M(d)), S2, and S3, foundation S8 gives the unique maximal partition of M'(d) directly."

Plus the *Canonical decomposition* paragraph and the R-BLK closing paragraph each say it again.
**Problem**: Six restatements of one fact. The reader must repeatedly re-confirm that the same point is being made, not a new one. This is the "two paragraphs say the same thing in different words" pattern, compounded across the section.
**Required**: State once (in the R-SP S8 clause, where the preconditions are actually checked) that foundation S8 supplies the maximal partition because dom, S2, S3 are preserved. Delete the intro sentence, the standalone "Post-state S8 is met..." paragraph, and the closing Remark's repetition.

### Issue 2: Identical sentence duplicated across R-PPERM and R-SPERM
**ASN-0084, R-PPERM and R-SPERM**: Both lemmas contain verbatim: "The non-S branch records, in the piecewise definition itself, that π is the identity on positions with subspace(v) ≠ S — exactly the (NS-π) clause of R-NS, which the proof below cites once at the non-S case."
**Problem**: Same explanatory sentence in two slots; it advances neither formula. The piecewise definitions already show `π(v) = v` on the non-S row.
**Required**: Remove both sentences. The non-S row of each formula is self-explanatory; the proof's "by R-NS(NS-π)" citation suffices.

### Issue 3: Same future-ASN deferral repeated in multiple sections
**ASN-0084, Canonical decomposition / R-BLK / R-SP Remark / Open Questions**: The deferral of "exhaustive-merge / canonical reduction to the maximal partition" appears in *Canonical decomposition* ("operationalizing canonical reduction ... is deferred to a future ASN"), in R-BLK's closing paragraph ("recovering it from B' by exhaustive merging ... is deferred to a future ASN, as noted under Canonical decomposition above"), in the R-SP *Remark*, and again as Open Question 6.
**Problem**: Multiple paragraphs in different sections deferring to the same downstream location — the flagged "see X below / deferred to Y" accretion pattern.
**Required**: State the deferral once (Open Questions is the natural home) and remove the in-line repetitions; R-BLK need only assert "B' is valid but not necessarily maximal."

### Issue 4: w_μ ≥ 1 attributed to CS2, contradicting the ASN's own derivation
**ASN-0084, closing remark of the swap section**: "the 4-cut swap transposes two regions separated by at least one middle position (CS2 forces w_μ ≥ 1)."
**Problem**: The *Width positivity* consequence derives w_μ ≥ 1 from the witness "c₁ ∈ [c₁, c₂) ∩ V_S(d)," and c₁ ∈ V_S(d) is supplied by **R-PRE(iv)**, not CS2. CS2 only gives the strict ordering c₁ < c₂, which alone does not force a V-position to exist between them. The parenthetical contradicts the ASN's stated derivation.
**Required**: Change to "(R-PRE(iv) together with CS2–CS4 forces w_μ ≥ 1)" or cite the Width-positivity consequence directly.

### Issue 5: R-NS (NS-inv) is a downstream-consumer inventory
**ASN-0084, R-NS (NS-inv)**: The "*Catalogue (non-S-applicable invariants)*" and "*Out of scope for (NS-inv)*" passages enumerate S8a, S8-fin, S8-depth, S2, D-CTG, D-MIN, D-SEQ, S3, S8-uniq, S8-cons with a per-invariant note on which transport mechanism applies and which are handled elsewhere.
**Problem**: This is a use-site inventory — it catalogues which invariants consume (NS-π)/(a)/(b) and which are "discharged at the global dom-preservation step in R-SP," rather than advancing the lemma. R-SP already performs the per-clause invariant audit; the catalogue duplicates that bookkeeping.
**Required**: Reduce (NS-inv) to its actual content: "any ASN-0036 invariant evaluated only on non-S positions is preserved, since dom is unchanged and M'(d) = M(d) pointwise on non-S positions." Drop the per-invariant catalogue and the "Out of scope" routing list; let R-SP own the audit.

### Issue 6: REARRANGE_K *Partiality* paragraph is defensive non-content
**ASN-0084, Operation — REARRANGE_K, *Partiality***: "on inputs that violate R-PRE(K), REARRANGE_K is undefined, and this ASN makes no commitment about the resulting state — neither that the operation aborts, nor that it produces some particular Σ', nor that any postcondition is satisfied. Out-of-contract behaviour is the caller's obligation to avoid via R-PRE(K), not the specification's to characterize."
**Problem**: Once "REARRANGE_K is a partial operation defined exactly where R-PRE(K) holds" is stated, the enumeration of three things the spec does *not* promise, plus the "caller's obligation" essay, adds nothing. This is defensive meta-prose in a structural slot.
**Required**: Keep "REARRANGE_K is partial, defined exactly where R-PRE(K) holds against Σ.M(d)." Delete the rest.

### Issue 7: "S7 ≡ S7a ∧ S7b ∧ S7d" mischaracterizes a theorem
**ASN-0084, R-SP, Q statement and proof**: "S7 (StructuralAttribution, ≡ S7a ∧ S7b ∧ S7d)" and "S7 reduces to the conjunction S7a ∧ S7b ∧ S7d on Σ.C."
**Problem**: In ASN-0036, S7 is a *theorem* whose postconditions concern origin(a) (well-definedness, distinct origins for distinct documents, invariance), derived *from* S7a/S7b/S7d plus T4. It is not equivalent to the conjunction of those axioms. The substance (S7's postconditions survive because C' = C, so origin is recomputed identically) is correct, but the "≡" is wrong.
**Required**: State that S7's postconditions are preserved because origin(a) depends only on Σ.C and C' = C; drop the "≡ S7a ∧ S7b ∧ S7d" equivalence.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: Correctly deferred in Open Questions; the depth-2/text-subspace and {3,4}-cut restrictions are explicit scope choices, not gaps in this ASN.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Whether two REARRANGE_K compose to one is new territory; this ASN specifies a single operation and its invariant preservation.

VERDICT: REVISE
