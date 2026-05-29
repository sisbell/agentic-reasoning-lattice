# Review of ASN-0040

## REVISE

### Issue 1: Circular citation between §B1 and the Bop correctness proof
**ASN-0040, §B1 (Baptismal transitions, "All other namespaces" preamble)**: "By construction, a ∈ S(p₀, d₀) and a satisfies T4 (by B10 preservation, established in the Bop correctness proof)."
**Problem**: This routes the T4-validity of the new element `a` through "the Bop correctness proof." But the Bop correctness proof in turn claims **B1 preservation** and defers it to "§B1." So §B1 cites Bop, and Bop cites §B1 — a mutual deferral that is circular on its face. The fact actually needed (`a` satisfies T4) follows directly and non-circularly from B6 sufficiency (§B6), since `(p₀, d₀)` satisfies B6 and `a ∈ S(p₀, d₀)`.
**Required**: Cite §B6 sufficiency directly for `a satisfies T4`. Do not route this through the Bop proof, whose own B1-preservation clause depends on §B1.

### Issue 2: Triple restatement that B4 / B1 / B10 / B_fin are "structural, not caller-checked"
**ASN-0040, Bop**: the STRUCTURAL line ("an invariant of the operation vocabulary satisfied by construction of Σ, not a caller-checked precondition discharged per call"); the Formal Contract *Structural assumptions on Σ* line ("this is an invariant of the operation vocabulary, not a caller-checked precondition"); the Formal Contract *Preconditions* parenthetical ("they are *state invariants*, not per-call obligations… not discharged by the caller").
**Problem**: The same "not a caller obligation" point is made three times in one operation specification. This is reviser-drift accretion around the operation's structural status — the precise reader must skip past identical qualifications in three slots.
**Required**: State the structural/invariant distinction once (in the Formal Contract) and remove the duplicates.

### Issue 3: Trivial exhaustiveness narration
**ASN-0040, NextAddress justification**: "The case split is exhaustive: children(B, p, d) = B ∩ S(p, d) is a set, so it is either empty or non-empty. No third possibility exists." Also **§B8**: "The two cases are exhaustive: two baptisms either target the same namespace or they do not." Also **§B1**: "The partition is exhaustive on its face…"
**Problem**: Empty/non-empty and same/different are trivially exhaustive; spelling out "no third possibility exists" advances no reasoning. This is exactly the meta-prose the anti-bloat classifier flags. (Contrast B7's three-case exhaustiveness statement, which *is* informative because the trichotomy on lengths/nesting is non-obvious — keep that one.)
**Required**: Delete the trivial exhaustiveness sentences; retain only exhaustiveness claims whose partition is non-obvious.

### Issue 4: B0 stated as an axiom, then re-derived, with significance essay between
**ASN-0040, §The baptismal registry**: B0 is given a full numbered statement plus prose ("This is the state-level reading of T8… B0 forbids any mechanism — not just the allocator… Administrative action, garbage collection, storage failure — none may contract B."), then B0a is introduced, then "B0 (stated above) now follows from B0a."
**Problem**: If B0 is a corollary of B0a, presenting it first as a standalone law with a scenario inventory ("Administrative action, garbage collection, storage failure") and then deriving it is redundant ordering plus essay content in a structural slot. The reader processes B0 as primitive, then must re-file it as derived.
**Required**: Present B0a first; state B0 as the one-line corollary it is. Drop the scenario list or compress to the single load-bearing point (B0 binds all mechanisms, not only the allocator).

### Issue 5: Document-structure narration in the wp section
**ASN-0040, §The high water mark (wp derivations)**: "Throughout these derivations, B4 (Atomic Baptism) guarantees that `children(B, p, d)` is evaluated against the precondition state B… we state this once here and do not repeat it per derivation."
**Problem**: "we state this once here and do not repeat it per derivation" is narration about the document's own organization, not reasoning about baptism. It is the kind of meta-prose that compounds across cycles.
**Required**: State the B4 evaluation-against-precondition fact as a plain assumption for the section; delete the self-referential clause about repetition.

### Issue 6: B4 atomicity stated three ways
**ASN-0040, §Atomicity (B4)**: the formula `s'.B = s.B ∪ {next(s.B, p, d)}` "computed against the state s… committed… in the same step"; then "Equivalently, in the transition relation →… the observation… and the commitment… are not separable. There is no state s_mid…"; then "Each `baptize(p, d) ∈ Σ` is a single edge in the transition graph."
**Problem**: Three paragraphs assert the identical content (one atomic edge, no intermediate state). Two of the three say the same thing in different words.
**Required**: Keep the transition-relation statement ("single edge, no s_mid"); remove the redundant restatements.

## OUT_OF_SCOPE

### Topic 1: Address uniqueness across incomparable execution branches
**Why out of scope**: B8's proof (Case 1) assumes β₁ and β₂ lie on a single transition path (s₁ →* s₂), which holds within one execution. Two baptisms in the *same* namespace on incomparable branches of the reachability relation would, by the determinism remark, produce the same `c_{m+1}`. Whether that constitutes a uniqueness violation is a question about cross-replica / cross-execution identity, which belongs to the replication protocol (BEBE), explicitly deferred. No revision needed here.

VERDICT: REVISE
