# Review of ASN-0067

## REVISE

### Issue 1: Variable name collision — "m" used for both V-position depth and content reference count
**ASN-0067, ContentReferenceSequence definition**: "A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₘ⟩ of content references with m ≥ 1."
**Problem**: Throughout the ASN, `m` denotes the common V-position depth in a document's text subspace (from S8-depth). The ContentReferenceSequence definition reuses `m` for the number of references. These two quantities are unrelated. A reader tracing the composite resolution — `resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₘ)` — encounters `m` meaning "count of references" immediately after sections where `m` means "tumbler depth."
**Required**: Use a distinct variable for the content reference count (e.g., `p` or `|R|`). The depth meaning of `m` is established by the foundation and should not be shadowed.

### Issue 2: Wrong citation for S8a preservation in C3
**ASN-0067, Invariant Preservation (C3)**: "Shift preserves zeros(v) = 0 and positivity (TS4, ASN-0034)."
**Problem**: TS4 (ShiftStrictIncrease) states `shift(v, n) > v`. It says nothing about preserving `zeros(v) = 0` or component-wise positivity. The correct justification is the OrdinalShift definition (ASN-0034): `shift(v, n)` changes only the last component of `v` (adding `n` to it); all other components are unchanged. Since `v` has all positive components (`zeros(v) = 0`), `shift(v, n)` also has all positive components. The same misattribution applies to the shifted post-block argument in the same paragraph.
**Required**: Replace the TS4 citation with the OrdinalShift definition and the component-preservation argument. Two sentences suffice.

### Issue 3: Elementary decomposition does not handle B_post = ∅
**ASN-0067, Elementary Decomposition**: "the COPY composite decomposes into four elementary steps: Σ = Σ₀ →^{K.μ⁻} Σ₁ →^{K.μ⁺} Σ₂ →^{K.μ⁺} Σ₃ →^{K.ρ} Σ₄ = Σ'"
**Problem**: Two boundary cases break this decomposition.

**(a) Append (v = v₀ + N, N > 0).** All blocks satisfy `v_β + n_β ≤ v`, so B_post = ∅. Step 1 (K.μ⁻) requires `dom(M'(d)) ⊂ dom(M(d))` — strict contraction. With nothing to remove, the precondition fails. Step 2 (K.μ⁺ for shifted B_post) similarly has nothing to add, failing its strict-extension precondition.

**(b) Empty text subspace (N = 0).** B = ∅, so B_post = ∅. Same failure as (a).

The high-level COPY definition (Phase 2, steps i–v) is correct in both cases — `B' = B_pre ∪ {γ₁, ..., γₖ}` when B_post = ∅. But the proof that this constitutes a valid composite has a gap: the four-step elementary decomposition is the mechanism by which the ASN establishes ValidComposite, and it silently assumes B_post ≠ ∅.

In the same paragraph, the claim "D-CTG is a design constraint on reachable states, not a precondition of any elementary transition" is imprecise. Steps 1–2 alone form a valid composite (J0, J1, J1' all satisfied — K.μ~ preserves `ran(M(d))` so J1 is vacuous, and `R' = R` so J1' is vacuous). The resulting intermediate state Σ₂ is therefore reachable by a valid composite, yet it violates D-CTG (the gap at `[v, v + w)`). D-CTG is not an invariant of all reachable states — only of states reached by "complete" operations designed to preserve it.

**Required**: Make the decomposition conditional. When B_post = ∅, the composite is K.μ⁺ (placement) followed by K.ρ (provenance) — no reordering step. State each case, verify elementary preconditions for each, and verify coupling constraints for each. Also amend the D-CTG remark to acknowledge that intermediate reachable states can violate it; what COPY preserves is D-CTG at its own endpoint.

### Issue 4: "Injectivity" where "functionality" is meant
**ASN-0067, Resolution definition**: "it inherits the properties on which M11 and M12 depend: injectivity per V-position (S2)"
**Problem**: S2 (ArrangementFunctionality) says M(d) is a *function* — each V-position maps to exactly one I-address. That is functionality, not injectivity. Injectivity would mean distinct V-positions map to distinct I-addresses, which S5 (UnrestrictedSharing) explicitly denies. The restriction `f = M(d_s)|⟦σ⟧` inherits functionality (restricting a function yields a function), and that is the property M11/M12 need. Calling it "injectivity" could mislead a reader into believing M(d) is injective.
**Required**: Replace "injectivity per V-position" with "functionality per V-position" or simply "S2 (each V-position maps to exactly one I-address)."

### Issue 5: No concrete worked example
**ASN-0067, throughout**: The ASN presents symbolic scenarios (the self-transclusion table, the multi-source composition discussion) but no fully concrete example with specific tumbler values.
**Problem**: A worked example with specific tumblers would mechanically verify the construction. For instance: document `d` has block decomposition `{([1,1], a₀, 3), ([1,4], b₀, 2)}` (5 text positions). COPY from source document `d_s` with resolve producing `⟨(c₀, 2)⟩` at target position `[1,3]`. The example would show: the split of the first block at c = 2, the classification into B_pre and B_post, the shift by w = 2, the placed block, the composed B', and explicit verification of C0, C2, C4, C6 against the result. This grounds the abstract construction in concrete arithmetic.
**Required**: Add one fully worked example with specific tumbler addresses, block decompositions, and postcondition checks.

## OUT_OF_SCOPE

### Topic 1: Concurrency model
**Why out of scope**: The ASN correctly identifies (C13 observation) that ValidComposite provides sequential correctness only. Defining visibility guarantees for concurrent COPY operations on the same document is new territory requiring a concurrency model not yet in the foundation.

### Topic 2: D-CTG enforcement in ASN-0047
**Why out of scope**: The elementary decomposition reveals that D-CTG is not preserved by all valid composites (a standalone K.μ~ can create V-position gaps). Whether ASN-0047 should promote D-CTG to a reachable-state invariant — perhaps by restricting which composites are valid — is a framework question for ASN-0047, not an error in ASN-0067.

VERDICT: REVISE
