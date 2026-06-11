# Review of ASN-0128

This note is in good shape structurally: the RP projection apparatus is sound and mirrors ASN-0126's bridge correctly, I0a's two-direction proof is complete, I1a's induction covers the K ~ R wrapper case honestly, DR's antichain derivation is genuinely load-bearing and correct, and the wp work (I6, DR) is non-trivial with necessity argued per branch — including the subtle attainability-convention point where the postcondition holds vacuously at a rejected call. The abstract registry example exercises real cases. The remaining issues are below.

## REVISE

### Issue 1: Emit_K under idem=⊥ has no home-validation semantics

**ASN-0128, I5 (IdemFalseAlwaysFresh)**: "Under `idem(K) = ⊥`, no de-duplication test runs: every `Emit_K` call the gate admits invokes `K.λ_sh` and produces a fresh address regardless of `(F, G)` content"

**Problem**: The gate is three clauses — K registered, arity 3, `Sh-conf` — and does not include `d ∈ dom(Σ.M)`. So I5 as written asserts that a gate-passing call with `d ∉ dom(Σ.M)` "invokes `K.λ_sh` and produces a fresh address." It cannot: `a_emit` is total only on `d ∈ dom(Σ.M)` (EmitAddress, ASN-0086), and a deposit homed at an unallocated `d` would violate L1a (LinkScopedAllocation, ASN-0043) — the relation has no such step. I1's home-validation clause repairs exactly this for idem=⊤, but it is explicitly branch-scoped ("On a miss — the only branch that reads `d`") and lives inside a contract whose opening line is "Under `idem(K) = ⊤`." The idem=⊥ surface's behavior on invalid `d` is therefore unspecified. Relatedly, once I1's hit branch admits calls with arbitrary `d`, the exposed surface no longer matches ASN-0086's declared signature (`Σ × dom(Σ.M) × Endset × Endset → …`), and the note never restates the widened signature anywhere.

**Required**: State home validation for idem=⊥ (every admitted call reads `d`; a call with `d ∉ dom(Σ.M)` is rejected — no step, no address, exactly as I1's miss branch), and restate the exposed `Emit_K`'s signature/domain once, covering both idem values.

### Issue 2: The K ~ R exclusion on Emit_K is asserted but never enforced by any contract clause

**ASN-0128, S3 (Retraction)**: "This note therefore exposes `Nullify_Binary` as the **only** retraction entry point — no direct `Emit_K` with `K ~ R` is in the operation set"

**Problem**: This exclusion is load-bearing twice over — the surface-disciplined definition's "equivalently, every retraction is wrapper-routed" holds only if `Emit_K` refuses R-class calls, and I6's disciplined reduction drops C2 on the ground that "`Emit_K` is invoked at `K ≁ R` only." But R is a *registered* type, and I6's uniform preconditions are just the gate: a caller presenting any endset `~`-equal to `[K_R]` with `|F| = |G| = 1` passes every clause of the consolidated contract. Nothing in `Emit_K`'s contract rejects it. The consequence is not hypothetical: a gate-passing `Emit_K` at `K ~ R` with G the address set `{d'.0.s_L}` deposits a retraction whose to-coverage is `subtree(d'.0.s_L)` — every chain slot of `d'` — sterilizing `d'` outright through the exposed surface, directly contradicting S3's "containment is complete." It also breaks S3's attribution claim that the wrapper-routed qualifier "saturates": a direct R-emit with arbitrary from-fill escapes the who-retracts convention.

**Required**: Make the exclusion a clause of the exposed `Emit_K` itself — an explicit `K ≁ R` precondition (one CoverageEqualityDecidable test against the shipped representative) with rejection semantics, listed among I6's uniform preconditions — and cite that clause from the surface-disciplined definition and the disciplined-domain reduction, rather than from S3 prose.

### Issue 3: I0's inseparability rationale is false as stated

**ASN-0128, I0 (SamenessIsCoverageEquality)**: "but under it the active subset could hold coverage-equal tuples that no membership test, no `Observe` pattern, and no retraction separates, since those surfaces all read coverage, never decomposition"

**Problem**: Three of the note's own surfaces contradict this sentence. (i) Retraction separates by address: `Nullify_Binary` targets a tuple's address with single-tuple scope (DR), so one of two coverage-equal active tuples can be retracted while the other stays active — retraction reads the target address, not the stored tuples' coverage. (ii) `Observe_K`'s *patterns* match by coverage, but its *results* are full triples `(a, F, G)` carrying the stored span decompositions — the two tuples are visibly distinct in any returned set. (iii) The enumeration predicates this very note ships read denoted sets: on I0a's separating pair, `targets_of` answers differently for the two decompositions — the exact discrimination I1's hit clause spends a paragraph analyzing as "the loss." The conclusion (coverage as the dedup identity) is adequately grounded by the assertion-as-subtree argument and the Gregory/Nelson evidence; the supporting inseparability claim overreaches and a careful reader trips on it.

**Required**: Scope the claim to what is true — the *matching* surfaces (membership tests, `Observe` patterns, `same_type`) test coverage, so no query can *select* one coverage-equal tuple over another by content — or delete the sentence and rest I0 on the assertion-identity ground alone.

### Issue 4: Meta-prose and cross-section duplication (anti-bloat)

**ASN-0128, multiple sections**:

- The fact that the transition relation is unchanged is stated four times: the commitments bullet ("never a refinement of the relation itself (I1)"), I1's opening sentence, I1's locus paragraph ("The locus keeps ASN-0126 intact: a raw `K.λ_sh` step depositing an I0-duplicate remains a step of the relation"), and RP-c's trailer ("RP-c is trivial because this note adds no precondition to `K.λ_sh`"). One normative statement (I1's) suffices; the rest is the same sentence relocated.
- **RP**: "Transfer then has three clauses; later sections cite them by name." — navigational meta-prose; the clause labels speak for themselves.
- **I0a**: "Both directions of the identity need showing." — proof-obligation narration; the (⊆)/(⊇) markers already say it.
- **DR**: "(I6 needs no such declaration: its POST exhibits the returned address, which a rejected call lacks, so rejection falsifies POST there outright.)" — commentary explaining why a *different* claim doesn't need DR's convention; this is reviser-to-reviewer prose, not part of DR's argument.
- **BH2, Effect**: "the rationale for withholding a general `reach(x, y)` is recorded in What this note doesn't cover" — a deferral pointer to content that appears in full one section later, in a paragraph that has already committed "by design, not omission."
- Rhetorical lead-ins that delay the content: "The ground is one sentence:" (I0), "Neither case is exotic." (BH2), "and it is not optional bookkeeping" (R-C1).

**Problem**: Each instance forces the reader to step over prose that advances no claim; the relation-unchanged repetition is the compounding kind — a fifth restatement next cycle is predictable if not cut now.

**Required**: Trim the listed instances; keep the I1 statement of relation-unchangedness and the BH2 one-line commitment, delete the echoes.

## OUT_OF_SCOPE

### Topic 1: The serializing authority in I4
**Why out of scope**: I4 posits "a serializing authority orders the two calls before either becomes a step" and analyzes both serializations correctly given that assumption. Who serializes, and the atomicity of the dedup-check-plus-step unit, are runtime/topology commitments belonging to a future ASN, not an error in this one.

### Topic 2: Caller-observable rejection semantics
**Why out of scope**: Rejection is uniformly "no step, no address" (I1, S3), which suffices for the contracts here. Whether callers can distinguish *why* a call was rejected (gate failure vs. invalid home vs. P-tgt) is API-surface design for a successor note.

VERDICT: REVISE
