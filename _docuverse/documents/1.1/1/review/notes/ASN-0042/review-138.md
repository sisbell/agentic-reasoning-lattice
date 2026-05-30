# Review of ASN-0042

## REVISE

### Issue 1: Revision-history meta-prose in O14's header
**ASN-0042, O14 (BootstrapPrincipal)**: "The initial principal set satisfies the following labeled conjuncts (cited individually by label throughout this ASN; the formerly bundled "first clause" is split into O14.1 and O14.2):"
**Problem**: Two clauses of pure accretion. "cited individually by label throughout this ASN" is a use-site inventory that does not advance the axiom's meaning; "the formerly bundled 'first clause' is split into O14.1 and O14.2" narrates the note's own revision history — content that belongs in a changelog, not the axiom. The precise reader must skip past both to reach the conjuncts.
**Required**: Reduce to "The initial principal set satisfies the following labeled conjuncts:" — delete the parenthetical entirely.

### Issue 2: Forward use-site pointer in the State Axioms notation
**ASN-0042, State Axioms, Notation**: "We say 'allocated address' and 'address in `Σ.B`' interchangeably; from the ownership model's perspective, every address requiring an effective owner is one that the system has baptized. The monotonicity the proofs below invoke is baptismal-registry monotonicity `Σ.B ⊆ Σ'.B` (B0 of ASN-0040)."
**Problem**: "The monotonicity the proofs below invoke is…" is a forward inventory of downstream consumers — it names where a fact will be used rather than establishing it. The intervening essay sentence ("from the ownership model's perspective…") restates the preceding sentence without adding content. This is exactly the forward-reference accretion the anti-bloat classifier targets.
**Required**: Keep the definitional identity (`Σ.B` is ASN-0040's `s.B`); state B0 monotonicity as a cited fact without the "the proofs below invoke" framing; drop the restated "from the ownership model's perspective" sentence.

### Issue 3: Duplicated argument in O8's proof
**ASN-0042, O8 proof, "The parent cannot be the longest match"**: the paragraph concludes "Hence `ω_{Σ'}(a) ≠ π`," immediately followed by "To see this last step precisely: suppose for contradiction that `ω_{Σ'}(a) = π`…" which re-derives the identical conclusion formally.
**Problem**: Two paragraphs establish the same step — an informal summary and then its rigorous restatement. Under the standard "no proof by handwave," the informal version is not load-bearing once the contradiction proof is present; it is redundant prose the reader must reconcile against the formal version.
**Required**: Keep the contradiction argument; delete the preceding summary paragraph (or demote it to a one-line lead-in), so the step is established once.

### Issue 4: O7(b) cites a postcondition whose stated domain excludes the address in question
**ASN-0042, O7 proof, Postcondition (b)**: "Let `a ∈ Σ''.B ∖ Σ'.B` … By postcondition (a), no principal in `Π_{Σ'}` covering an address of `odom(π')` has a prefix longer than `pfx(π')`, so `#pfx(π''') ≤ #pfx(π')`".
**Problem**: Postcondition (a) is stated only for `a ∈ odom(π') ∩ Σ'.B`, but the address here is `a ∈ Σ''.B ∖ Σ'.B` — outside (a)'s declared domain. The fact actually needed (every `π'' ∈ Π_Σ` with `pfx(π') ≼ a` has `#pfx(π'') < #pfx(π')`) was established inside (a)'s three-case body for *any* such `a`, independent of `Σ'.B` membership, but the citation points at the narrower stated postcondition.
**Required**: Either cite the structural sub-fact from (a)'s proof body directly, or generalize (a)'s statement to all `a` with `pfx(π') ≼ a` (not only `Σ'.B` addresses), so the appeal in (b) lands on a claim whose domain contains the address.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer reconciling provenance (O6) with effective ownership (O2)
**Why out of scope**: Nelson's "someone who has bought the document rights" implies transfer, but the ASN correctly defers this — the system as specified has no transfer mechanism, and the divergence between inalienable provenance and effective owner is genuinely new territory (already listed under Open Questions), not an error in this note's refinement regime.

META: 

VERDICT: REVISE
