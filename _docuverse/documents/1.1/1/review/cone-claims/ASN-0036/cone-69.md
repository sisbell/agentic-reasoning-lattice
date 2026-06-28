**Dependency structure.** S0 is the root axiom; S1 is proved directly from S0 in one step; S3 is proved by transition induction using AX-1 (base), S1 (inherited case), and AX-2 (new/redirected case). No circularity.

**AX-1 and AX-2.** Both are correctly declared as protocol design posits with no Depends entries. AX-1's domain guard on d is unconstrained, consistent with the convention that d ranges over whatever the signature in ASN-0034 provides. AX-2's well-definedness argument for the `Σ.M(d)(v)` application is sound: the conjunct `v ∈ dom(Σ.M(d))` in the second disjunct fires before the application, discharging the domain obligation under strict partial-function semantics.

**S1's proof.** Single step from S0's first conjunct. Correct and complete.

**S3's inductive proof.**

*Base case.* AX-1 yields dom(Σ₀.M(d)) = ∅; S3's quantifier range is empty; invariant holds vacuously. ✓

*Inductive step.* The case split — inherited vs. new-or-redirected — is a classical dichotomy on a fixed v ∈ dom(Σ'.M(d)) and is exhaustive. In the inherited case, J0 applies because v ∈ dom(Σ.M(d)) is given, yielding a ∈ dom(Σ.C), and S1 carries it to dom(Σ'.C). In the new-or-redirected case, the condition on v matches AX-2's range predicate exactly (with v ∈ dom(Σ'.M(d)) already in hand), and AX-2 directly delivers a ∈ dom(Σ'.C). Both cases close. The domain guard on Σ.M(d)(v) in case 2 is handled correctly: the proof writes case 2 as "v ∉ dom(Σ.M(d)), or else v ∈ dom(Σ.M(d)) but Σ'.M(d)(v) ≠ Σ.M(d)(v)," matching AX-2's guarded form. ✓

**Dependency declarations vs. proof use.** S1 cites S0; proof uses S0 only. S3 cites S1, AX-1, AX-2; proof uses exactly these three. No over- or under-declaration.

**Frame conditions and scope.** S3's quantifier ranges over dom(M(d)), not dom(C), so orphaned content makes no appearance in the invariant. S1's monotonicity holds unconditionally on dom(C), which covers the orphaned-content remark correctly. The claim that S1 alone cannot close S3's inductive step — because it is silent on freshly installed mappings — is sound; AX-2 is the non-redundant second ingredient.

**Terminology.** "Arrangement," "V-position," "I-address," and "store" are used consistently throughout. No drift detected.

VERDICT: CONVERGED