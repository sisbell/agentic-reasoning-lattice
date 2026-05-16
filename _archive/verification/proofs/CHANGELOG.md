# Proof Modules — Changelog

## 2026-03-16: TumblerOwnership — ASN-0042 proof promotion, 232 total verified

Promoted 22 ASN-0042 property proofs from 22 modeling files into 6 consolidated modules in TumblerOwnership/:
- **TumblerOwnership.dfy** — shared definitions: Principal, State, Covers, IsEffectiveOwner, StrictPrefix, PrincipalPersistence, AddressPermanence, DelegationPrecondition, Acct, CoveringPrefixesOrdered, O1 (Owns), O9 (NodeLocalOwnership), O11 (ValidSession), O12
- **OwnershipProvenance.dfy** (7): O0, O1a (AccountBoundary), O1b (PrefixInjective), O6 (StructuralProvenance), AccountPrefix — plus ZeroAtIndex, TwoZerosCount, CoveringToAccount, AccountToCovering, CoveringBiconditional helpers
- **OwnershipExclusivity.dfy** (4): O2 — EqualLengthCoveringEqual, EffectiveOwnerUnique, MostSpecificExists (recursive set induction), OwnershipExclusivity (witness construction)
- **OwnershipPermanence.dfy** (6): O3 (OwnershipRefinement), O8 (IrrevocableDelegation), O13 (structural), AccountPermanence — plus BootstrapDomainsDisjoint, EffectiveOwnerExtends, DelegatorWithinDomain helpers
- **OwnershipDelegation.dfy** (9): O4 (DomainCoverage), O5 (SubdivisionAuthority), O7 (OwnershipDelegation), O14 (BootstrapPrincipal), O15 (PrincipalClosure), O16 (AllocationClosure), O17 (AllocatedAddressValid) — plus Delegate function, DomainCoveragePreserved
- **OwnershipFork.dfy** (2): O10 (DenialAsFork) — Fork, OwnershipPreserved, ForkOwnership, ForkAddressExists ({:axiom})

Deduplicated: Covers (was in 10+ files), IsEffectiveOwner (10+ files), StrictPrefix (4 files), PrincipalPersistence (5 files), CoveringPrefixesNest/Ordered (3 files), DelegationValid/Precondition (2 files) — all extracted into TumblerOwnership.dfy.

Rewrites (semantically equivalent, Dafny-verified):
- **SubdivisionAuthority, AllocationClosure**: Principal(id: nat) + pfx map rewritten to Principal(prefix: Tumbler) with direct field access. Removes map indirection; same logical constraint.
- **BootstrapDomainsDisjoint**: restructured from `ensures false` (contradictory preconditions) to positive `ensures IsPrefix(...) || IsPrefix(...)` (contrapositive). Avoids warn-contradictory-assumptions.
- **ForkAddressExists**: `assume {:axiom} false` in body upgraded to bodyless `lemma {:axiom}` (Dafny 4 idiom).
- **PrefixImmutable (O13)**: dropped as explicit predicate — structural with embedded prefix model. Documented in comments.

Renames: AccountField → Acct, AccountPrefix (lemma) → AccountPrefixLemma, CoveringPrefixesNest → CoveringPrefixesOrdered, DelegationValid → DelegationPrecondition.

## 2026-03-16: TumblerBaptism — ASN-0040 proof promotion, 199 total verified

Promoted 18 ASN-0040 property proofs into TumblerBaptism/ directory:
- **TumblerBaptism.dfy** — shared definitions: StreamElement, InStream, Children, ValidBaptism, Next, BaptismState, Baptize, StreamMatchesInc
- **BaptismBranching.dfy** (5): S0, S1, B5, B5a, B7 — structure of the fork
- **BaptismRegistry.dfy** (12): B0, B0a, B₀, B1, B2, B4, B6, B8, B9, B10, RegistryGrowth, OnlyRegistryModified — the set B and how it grows
- **BaptismGhost.dfy** (1): B3 — cross-cutting property bridging baptism and content model, isolated pending future bridge specification

StreamElement extracted from 10 duplicated definitions per Dafny review recommendation. InStream, Children, ValidBaptism also deduplicated.

## 2026-03-16: Remove NodeOntology — ASN-0035 deprecated

Removed NodeOntology/ directory (NodeOntology.dfy, NodeIdentity.dfy, NodeAllocation.dfy). ASN-0035 (Node Ontology) deprecated — its properties are fully covered by ASN-0034 (tumbler algebra), ASN-0040 (baptism), and ASN-0042 (ownership). Level-specific predicates (NodeAddress, AccountAddress, etc.) added to TumblerHierarchy.dfy. 159 total verified.

## 2026-03-15: TwoSpace — ASN-0036 proof promotion, 199 total verified

Promoted 15 ASN-0036 property proofs into TwoSpace/ directory:
- **TwoSpace.dfy** — shared definitions: Val, TwoSpaceState, ContentImmutability, ReferentialIntegrity, AllPositive, Origin
- **TwoSpaceContent.dfy** (7): S0, S1, S4, S6, S7a, S7b, S7
- **TwoSpaceArrangement.dfy** (7): S2, S3, S5, S8-fin, S8a, S8-depth, S8
- **TwoSpaceSeparation.dfy** (1): S9 — the capstone theorem

Grouping principle: content store invariants vs arrangement invariants vs the separation theorem.

Deduplicated: ContentImmutability (was in 3 files), ReferentialIntegrity (2 files), AllPositive (2 files), Val type (5 files) — all extracted into TwoSpace.dfy.

## 2026-03-14: NodeOntology — ASN-0035 proof promotion, 165 total verified

Promoted 19 ASN-0035 property proofs into NodeOntology/ directory:
- **NodeOntology.dfy** — shared definitions: NodeAddress, Root, Parent, IsChildOf, Children, NodeState, Actor, AuthGrant, authorized, ZeroCount helpers
- **NodeIdentity.dfy** (12): Σ.nodes, N0, N1, N2, N3, N5, N6, N7, N9, N10, N13, N14, N16
- **NodeAllocation.dfy** (5): N4, N8, N11, N12. N15 (AllocationAuthority) and DC1 (AuthorityPermanence) deferred to Account Ontology — they introduce Actor/authorized concepts that belong in the account layer.

Grouping principle: NodeIdentity = what nodes ARE, NodeAllocation = how they're CREATED.

ZeroCountAllPositive lemma extracted from duplication (was in AlwaysValidStates and UniformNodeType) into NodeOntology.dfy shared definitions.

NodeAllocation imports NodeIdentity for predicate definitions used in BAPTIZE preservation proofs.

## 2026-03-13: TumblerAlgebra — extract shared definitions, rename for clarity

Extracted definitions duplicated across ASN-0034 modeling files into TumblerAlgebra.dfy:
- **LastNonzero** (+ LastNonzeroRec, LastNonzeroAt): last nonzero component position. From AllocatorDiscipline.dfy (was `LastSig`/`LastSigRec`/`LastSigIs`).
- **FindZero**: first zero in sequence from a given position. From SubspaceDisjoint.dfy.
- **AllocationInc** (+ AllocationIncMonotone): hierarchical increment TA5 and its monotonicity lemma. From AllocatorDiscipline.dfy / HierarchicalIncrement.dfy (was `Inc`/`IncStrictlyGreater`).
- **LessEq**: less-than-or-equal ordering. From ContiguousSubtrees.dfy.
- **SubtractResultAt**: characterize each component of TumblerSubtract result. From SubtractionStrictOrder.dfy (was `SubComponent`).

Renames reflect intent: `LastSig` → `LastNonzero` (self-documenting), `Inc` → `AllocationInc` (distinguishes allocation protocol from displacement arithmetic), `SubComponent` → `SubtractResultAt` (avoids ambiguity with "sub-component").

Added type aliases `Address = Tumbler` and `Displacement = Tumbler` for role clarity. Applied to `ActionPoint(w: Displacement)`, `TumblerAdd(a: Address, w: Displacement): Address`, `AllocationInc(t: Address, ...): Address`. Ordering and subtraction signatures stay as `Tumbler` (role-agnostic).

Planned rename for Allocation module: `AllocationPermanence` → `AddressPermanence`. ASN-0034 labels T8 "Allocation permanence" but T8's statement is about the address persisting, not the allocation act. The old ASN-0001 proofs used `AddressPermanence` which is more precise.

## 2026-03-13: Consolidated proof modules — 5 modules, 125 verified

Promoted 29 ASN-0034 property proofs from modeling into 5 consolidated modules:
- **Order.dfy** (6): T0a/b, T1, T2, T3, TA6
- **Hierarchy.dfy** (5): T4, T5, T6, T7, PrefixOrderingExtension
- **Addition.dfy** (7): TA0, TA1, TA-strict, TA1-strict, TA1-weak, T12, TA7a
- **Subtraction.dfy** (5): TA2, TA3-strict, TA3-weak, TA4, ReverseInverse
- **Allocation.dfy** (6): T8, T10a, T10b, T10c, T10d, T11

Not promoted: T9 ForwardAllocation (lemma of T10a, stays in modeling). TA5 HierarchicalIncrement absorbed into TumblerAlgebra (AllocationInc + AllocationIncMonotone).

Deduplicated: LessEq, FindZero, LastNonzero/AllocationInc, SubtractResultAt from TumblerAlgebra. Subtraction helper lemmas prefixed Strict/Weak to disambiguate. PartitionMonotonicity uses Hierarchy.PrefixOrderingExtension instead of inlined copy. NonNesting defined once in Allocation.

Renames applied: `AllocationPermanence` → `AddressPermanence` (address binding is what persists). `LessEqual` → `LessEq` (from TumblerAlgebra). `SubComponent` → `SubtractResultAt` (from TumblerAlgebra). `LastSig`/`Inc` → `LastNonzero`/`AllocationInc` (from TumblerAlgebra).

Allocation imports Hierarchy for ValidAddress/ZeroCount (IncrementPreservesValidity) and PrefixOrderingExtension (CrossPartitionMonotonicity). All other modules depend only on TumblerAlgebra.

## 2026-03-13: ASN-0034 restart — clean slate

ASN-0034 (Tumbler Algebra) converged, replacing ASN-0001 as the foundation. Removed all deprecated modules: AddressAllocation (ASN-0001 property proofs), Foundation (Two-Space state model), DocumentOntology (ASN-0029 types), TwoSpace (ASN-0026 properties). These will be regenerated fresh against ASN-0034 as each downstream ASN is redrafted.

Retained: TumblerAlgebra/TumblerAlgebra.dfy (shared definitions). ASN-0034 property proofs will be generated into TumblerAlgebra/ alongside the definitions module.
