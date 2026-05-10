# Review of ASN-0042

Based on Dafny verification — 22 modules, 15 clean, 7 divergences

## REVISE

No genuine spec issues. All divergences are proof artifacts or modeling choices.

## QUALITY

### File: DenialAsFork.dfy — SIMPLIFY

`ForkAddressExists` uses `assume {:axiom} false`, making the existence guarantee of O10 unverified:

```dafny
  lemma ForkAddressExists(pi: Principal, s: State)
    ...
  {
    assume {:axiom} false;  // witness construction requires finite-set reasoning over principals
  }
```

The ASN provides a detailed two-case constructive argument (zeros=1: sub-delegates can't reach document-level; zeros=0: choose user-field exceeding all sub-delegate prefixes via T0a). This is the only `assume` in the suite. The argument involves iterating a finite principal set to find a maximum component value — expressible in Dafny with a decreases-on-cardinality induction similar to `MostSpecificExists` in OwnershipExclusivity.dfy. Replace the axiom with a constructive witness or, if the finite-set reasoning remains intractable, factor the two cases into separate lemmas where at least the zeros=1 case (which needs no witness search — any document-level address works) can verify cleanly.

### File: SubdivisionAuthority.dfy — SIMPLIFY

Uses `Principal(id: nat)` with a separate `pfx: map<Principal, Tumbler>`, while the majority of the suite (13 modules) uses `PrefixDetermination.Principal` which embeds the prefix directly. Same inconsistency in AllocationClosure.dfy and PrefixImmutable.dfy. The modules cannot compose across this boundary — you cannot pass a `PrefixDetermination.Principal` where `SubdivisionAuthority.Principal` is expected.

The PrefixImmutable case is defensible (it models the abstract ASN form where Principal and pfx are separate), but SubdivisionAuthority and AllocationClosure have no such justification — they use an `id: nat` field that appears nowhere in the ASN. Align these two modules to `PrefixDetermination.Principal` for composability.

### File: OwnershipExclusivity.dfy — PASS

`MostSpecificExists` induction is well-structured. The three-way case split (longer/equal/shorter) is the natural decomposition. Empty branches are correct — solver handles them. The `assert w in candidates` bridge in the main lemma is load-bearing (establishes `candidates != {}`).

### File: AccountPermanence.dfy — PASS

Four-component decomposition of the trace-level property is well-documented. Each lemma is minimal. The divergence comment accurately describes what is and isn't mechanized.

### File: StructuralProvenance.dfy — PASS

`ZeroAtIndex` and `TwoZerosCount` are clean helpers for the key `CoveringToAccount` lemma. The biconditional structure (`CoveringBiconditional` → `StructuralProvenance`) is elegant and matches the ASN's proof outline.

### File: OwnershipDelegation.dfy — PASS

Three postcondition lemmas cleanly separate O7(a), O7(b), O7(c). `CoveringPrefixesNest` is reused across multiple modules — could be factored into a shared utility, but duplication is minor.

### File: DomainCoverage.dfy — PASS

Inductive step with explicit case split (existing vs. new allocation) is clear and minimal.

### File: IrrevocableDelegation.dfy — PASS

Empty proof body — the solver derives O8 directly from the preconditions. Correct: prefix length comparison is immediate.

### File: OwnershipRefinement.dfy — PASS

Empty proof body. The structural encoding (Principal embeds prefix) makes O3 follow from set inclusion and length comparison. Clean.

### File: NodeLocalOwnership.dfy — PASS

Empty proof body. The solver handles the prefix-to-node-field containment directly.

### File: AccountBoundary.dfy — PASS
### File: AccountPrefix.dfy — PASS
### File: AllocatedAddressValid.dfy — PASS
### File: BootstrapPrincipal.dfy — PASS
### File: AllocationClosure.dfy — SIMPLIFY (Principal type; see SubdivisionAuthority above)
### File: IdentityAxiomatic.dfy — PASS
### File: PrefixDetermination.dfy — PASS
### File: PrefixImmutable.dfy — PASS (abstract modeling justified)
### File: PrefixInjective.dfy — PASS
### File: PrincipalClosure.dfy — PASS
### File: PrincipalPersistence.dfy — PASS
### File: StructuralOwnership.dfy — PASS

## SKIP

### Proof artifacts (7 divergences)

All seven divergences are modeling choices or encoding limitations — none reveals a spec issue:

1. **AccountPermanence** — Trace-level induction not mechanized. The four structural components (base disjointness, prefix consequence, inductive kernel, single-transition composition) are verified. The gap is the induction harness over arbitrary-length state traces, which Dafny handles poorly. The ASN's inductive argument is sound; the Dafny suite verifies its load-bearing steps.

2. **AllocationClosure** — `allocated_by` modeled as an explicit allocator map rather than a primitive relation. Makes the existential witness explicit. Sound encoding of the ASN's primitive relation.

3. **IdentityAxiomatic** — O11 is a meta-property by design. The ASN explicitly states identity is axiomatic. Encoding as a precondition predicate is the correct Dafny representation.

4. **OwnershipRefinement** — O13 (PrefixImmutability) holds by construction because Principal embeds its prefix as a datatype field. The ASN models Principal abstractly with a separate pfx mapping; the Dafny model collapses these. Both are sound — any model satisfying one satisfies the other.

5. **PrefixInjective** — O1b is a tautology under the collapsed Principal model. Same structural argument as (4). Sound.

6. **StructuralProvenance** — O6 proved via covering-set equivalence rather than direct ω modeling. The decomposition (same account field → same covering sets → same ω) faithfully captures the ASN's biconditional proof.

7. **SubdivisionAuthority** — `allocated_by` as explicit allocator map. Same rationale as (2).

### Clean verifications (15 properties)

AccountBoundary, AccountPrefix, AllocatedAddressValid, BootstrapPrincipal, DenialAsFork (postconditions a/b), DomainCoverage, IrrevocableDelegation, NodeLocalOwnership, OwnershipDelegation, OwnershipExclusivity, PrefixDetermination, PrincipalClosure, PrincipalPersistence, StructuralOwnership — all verified without divergence. The ASN properties translate directly.

VERDICT: SIMPLIFY
