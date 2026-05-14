# Review of ASN-0042

## REVISE

### Issue 1: AccountField intro miscites T6 instead of T4(b)
**ASN-0042, AccountField (acct(a)) definition**: "acct(a) is the tumbler whose components are N(a) followed by [0] followed by U(a) — using the foundation's field extraction functions (T6)"
**Problem**: T6 (DecidableContainment) is the *containment-decision* claim that *uses* the field projections N, U, D, E; it does not define them. The projections are defined by T4(b) (UniqueParse). The formal contract slot correctly cites "fields(a) (T4(b))", but the prose intro cites T6, creating an internal inconsistency.
**Required**: Replace "T6" with "T4(b)" in the AccountField prose; keep "decidable by T6" as a separate remark if the decidability angle matters.

### Issue 2: Informal "fields(a)" used as if it were a foundation function
**ASN-0042, AccountPrefix proof and AccountField proof**: "By T4(b), fields(a) decomposes a uniquely into a node field N(a) and a user field U(a)..."
**Problem**: T4(b) defines four separate partial functions N, U, D, E. The foundation contains no "fields(a)" function. The repeated invocation of "fields(a) (T4(b))" makes the proofs read as if they cite a defined operator that doesn't exist.
**Required**: Either replace "fields(a)" with explicit reference to the four projections "N(a), U(a), D(a), E(a) (T4(b))", or introduce "fields(a) ≡ (N(a), U(a), D(a), E(a))" as a local abbreviation with a one-line justification.

### Issue 3: O10 existence proof imprecise in zeros(pfx(π)) = 0 case
**ASN-0042, O10 proof, zeros(pfx(π)) = 0 case**: "Collect the user-field components of all existing sub-delegate prefixes that have entered the user field... each contributing one user-field-position component"
**Problem**: Each sub-delegate prefix has many user-field components, not one. The matching-failure argument requires only that `a'_{#pfx(π)+2} = u` differ from `pfx(π_i)_{#pfx(π)+2}` (the *first* user-field component of pfx(π_i)). The proof also conflates two structurally different sub-delegate forms — `pfx(π).x.…0.Y` (node-extending then account) versus `pfx(π).0.Y` (immediate account fork) — without separating them. The first form fails the prefix check at position #pfx(π)+1 (mismatch 0 vs x); only the second form requires the fresh-u argument.
**Required**: Split into the two cases explicitly; specify "the first user-field component immediately after the user-field separator at position #pfx(π)+1" as the quantity collected; note that "exceeding the maximum" is sufficient but not necessary (any non-collision value works).

### Issue 4: O5 omits explicit π ∈ Π_Σ membership
**ASN-0042, O5 (SubdivisionAuthority)**: "(A Σ, Σ', a, π : Σ → Σ' ∧ a ∈ Σ'.B ∖ Σ.B ∧ allocated_by_{Σ'}(π, a) ⟹ pfx(π) ≼ a ∧ ...)"
**Problem**: The universal quantifier ranges over π with no restriction to Π_Σ. The body invokes pfx(π), which is defined only for principals. O16 quantifies the corresponding existential over π ∈ Π_Σ, but O5's universal does not. A reader cannot tell whether O5 imposes the constraint on every imaginable π or only on principals that exist at Σ.
**Required**: Tighten O5's antecedent to include `π ∈ Π_Σ`, matching O16's existential.

### Issue 5: O7 postcondition (a) proof asserts three-case exhaustion without justification
**ASN-0042, O7 proof, postcondition (a)**: "Three cases exhaust the comparison. Case pfx(π') ≺ pfx(π'')... Case pfx(π') = pfx(π'')... Case pfx(π'') ≺ pfx(π')..."
**Problem**: Exhaustiveness of these three cases depends on the fact that any two prefixes covering the same tumbler are comparable under ≼ — the "covering chain" argument that O2's proof establishes from T5. O7's proof cites neither the chain argument nor O2's lemma. A reviewer must reconstruct why "incomparable" is impossible.
**Required**: Add one sentence citing the covering-chain argument (from O2 or directly from T5) before launching the case split, or cite O2 as a lemma.

### Issue 6: O3 corollary "monotonic refinement" stated without derivation
**ASN-0042, O3, Corollary**: "Since any new effective owner must have a strictly longer prefix than the one it displaces, `#pfx(ω_{Σ'}(a)) ≥ #pfx(ω_Σ(a))` in all transitions."
**Problem**: The proof body only handles the case ω_{Σ'}(a) ≠ ω_Σ(a). The "in all transitions" claim requires the trivial case ω_{Σ'}(a) = ω_Σ(a) — where O13 (PrefixImmutability) gives #pfx(ω_{Σ'}(a)) = #pfx(ω_Σ(a)). Two lines, but currently asserted by inspection.
**Required**: Add a one-line case split: when ω is preserved, O13 gives length equality; when ω changes, the proof body gives strict length increase.

## OUT_OF_SCOPE

None. The ASN's stated scope (abstract structural ownership) is respected throughout. Topics flagged as future work (transfer mechanics, principal authentication, sub-account dense reachability) are correctly listed in Open Questions rather than partially specified.

VERDICT: REVISE
