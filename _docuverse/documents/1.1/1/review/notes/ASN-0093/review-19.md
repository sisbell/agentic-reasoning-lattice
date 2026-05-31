# Review of ASN-0093

## REVISE

### Issue 1: C1b cites a nonexistent foundation claim (ASN-0036 S7c)

**ASN-0093, Content store invariants (C1b)**: "Every content address has at least two element-field components — the content-side analog of L1b. This is ASN-0036's S7c restated for the substrate."
**Problem**: The provided ASN-0036 claim statements contain S7, S7a, S7b, S7d — there is no **S7c**. ASN-0036 carries no content-side `#E(a) ≥ 2` invariant (S8a's `#t ≥ 2` applies to V-positions, not to `dom(Σ.C)`). C1b is therefore a *new* substrate-level commitment, not a restatement; the citation points at a foundation claim that does not exist. The same false provenance appears in the Properties-Introduced table ("restated from ASN-0036's S7c (content-side analog of L1b)").
**Required**: Drop the S7c citation and label C1b a substrate-level commitment (parallel to how the L0 C-clause is introduced as "added here as a substrate-level commitment"), in both the C1b prose and the Properties table. The invariant itself is fine — it is discharged at K.α by the `#E(a) ≥ 2` precondition — only the provenance is wrong.

### Issue 2: SubAllocatorAxiom.Exists buries its content under proof-discipline meta-prose

**ASN-0093, Address sub-allocators (SubAllocatorAxiom.Exists)**: "The permanence reading ... is established *inductively along with M1*, not as an after-the-fact corollary that requires M1 to be in scope independently. Concretely, the simultaneous induction over transition sequences ... carries M1 as one of its transition-indexed conjuncts; at each step ... the inductive step exhibits (a) M1 at `Σ'` ... and (b) the per-state activation reading ..."
**Problem**: This is `review-mode.anti-bloat` "new prose around an axiom explains why the axiom is needed rather than what it says." The axiom's object-level content is one sentence (chains are active at every `Σ` with `d ∈ dom(M)`). The "permanence reading" is the two-line corollary `d ∈ dom(M) ⇒ d ∈ dom(M')` — i.e. exactly M1, which is proved independently from frame conditions. There is no genuine circularity forcing the activation-permanence into the simultaneous induction (the real entanglement is ChainMembershipForOrigin ↔ freshness, not activation). The ~150-word defensive paragraph makes the reader work past proof-bookkeeping to reach a trivial corollary.
**Required**: Reduce Exists to its object-level statement plus a one-clause corollary ("permanence follows from M1"). Move any genuinely load-bearing induction-ordering remark to the single Simultaneous-induction-framing paragraph that already exists.

### Issue 3: "Earlier-draft note" is relocated revision history

**ASN-0093, Address sub-allocators (SubAllocatorAxiom)**: "*Earlier-draft note.* Two clauses present in earlier drafts — *Disjointness* ... and *FirstEmission's freshness conclusion* — are not axiom content. They are restated as derived lemmas DisjointSubAllocatorChains and FirstEmissionFreshness below, respectively."
**Problem**: Anti-bloat pattern — "a paragraph looks like a prior finding's content relocated rather than removed." This narrates the document's revision history ("earlier drafts") instead of advancing the specification. A reader does not need to know what former drafts contained; the current axiom either has the clauses or it does not. The same retrospective appears redundantly in the Properties table ("Replaces the former SubAllocatorAxiom.Disjoint axiom clause", "Replaces the former freshness conclusion of SubAllocatorAxiom.FirstEmission").
**Required**: Delete the Earlier-draft note. State the two derived lemmas where they belong; drop the "Replaces the former ..." phrasing from the table.

### Issue 4: Use-site inventories attached to definitions and per-chain disciplines

**ASN-0093, Per-chain disciplines / Properties table**: e.g. ChainElementT4Validity — "Consumed at ChainUniformZeroCount, DisjointSubAllocatorChains, StoreT4Validity, FirstEmissionFreshness, and the K.α/K.λ subsequent-emit cross-subspace freshness derivations"; ChainPrefixExtension — "Consumed in (i) the FirstEmissionFreshness lemma below; (ii) the K.α/K.λ subsequent-emit cross-document freshness derivations; (iii) the ChainMembershipForOrigin lemma's contiguous-prefix postcondition below."
**Problem**: Anti-bloat pattern — "a definition's introduction enumerates downstream consumers rather than advancing the definition's meaning." Each discipline's statement (the citation plus the corollary form) is complete on its own; the "Consumed at ..." inventories are bookkeeping that rots as consumers move and forces the reader past it to reach the claim. They recur in both the prose and the Properties table.
**Required**: Remove the "Consumed at / Consumed in" inventories. A discipline needs its statement and its ASN-0040 source; downstream sites cite *up* to it, not the reverse.

### Issue 5: Operation preconditions re-prove the freshness lemmas in full

**ASN-0093, K.α / K.λ preconditions (subsequent-emission and first-emission branches)**: the first-emit branch states "Freshness ... is supplied by FirstEmissionFreshness (which derives the conclusion from L0 + SC-NEQ + ...)", yet the subsequent-emit branch then inlines the entire three-step cross-document derivation, the within-chain derivation, and the dom(L)/dom(C) derivation — and K.λ repeats all of it verbatim with content↔link swapped.
**Problem**: Anti-bloat "two paragraphs in the same document say the same thing in different words." FirstEmissionFreshness (and its stated "one substitution rule" abstracting content/link) already carries the first-emit case; the discharge matrix's K.α/K.λ entries already carry the subsequent-emit case. Re-deriving the full multi-step freshness argument a third time inside each operation's precondition list is redundant with both the lemma and the matrix.
**Required**: In the operation preconditions, state each freshness obligation as a one-line citation to the governing lemma/matrix entry (FirstEmissionFreshness for first-emit; the ChainEnumerationInjectivity + Cross-document disjointness + T7 triad for subsequent-emit). Keep the full derivation in exactly one place.

### Issue 6: "Design rationale for retaining M" is essay content in a state-definition slot

**ASN-0093, State model**: "**Design rationale for retaining `M`.** The substrate could replace `M` with a set `D ⊆ T` ... `M` is retained as a partial function for *downward compatibility* ... Keeping `M` here makes the lift to a higher-layer transition model trivial ..."
**Problem**: Anti-bloat "essay content in structural slots" / prose justifying a design choice rather than specifying state. This paragraph plus the adjacent "Note on `M`'s shape" together argue *why* the substrate keeps `M` rather than specifying what `M` is — the substantive content (M partial, `dom(M)` = registered documents, `M(d)=∅`) is already stated above them.
**Required**: Collapse the rationale to at most one sentence ("`M` is kept as a partial function so higher layers extend it rather than reintroduce a component") or move it to Open Questions / a non-normative remark; do not let it occupy the state-model definition.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal / tombstoning
**Why out of scope**: The Open-Questions treatment of withdrawal paths (a)/(b)/(c) is explicitly deferred and matches the declared out-of-scope set; no flag for missing coverage. (Note: the three-path enumeration is itself somewhat essayistic, but it sits correctly under Open Questions, so it is acceptable placement.)

### Topic 2: Arrangement mutation, entity stratification, provenance
**Why out of scope**: Deferred to higher-layer ASNs by design; arrangement-side invariants (S2/S3/S8a/...) holding vacuously under `M(d)=∅` is the correct substrate-layer treatment, not a gap.

VERDICT: REVISE
