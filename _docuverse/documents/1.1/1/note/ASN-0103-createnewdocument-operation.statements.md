# ASN-0103 Claim Statements

*Source: ASN-0103-createnewdocument-operation.md (revised 2026-06-04) — Extracted: 2026-06-05*

## Definition — DocumentChainFrontier

`D_A = {e ∈ E : Document(e) ∧ parent(e) = A ∧ #e = #A + 2}`

The length-restricted document-chain frontier beneath account `A`: collects exactly the entities of `E` carrying the document chain's structural signature beneath `A`. Versions (length `≥ #A + 3`) are excluded. Equal to `E ∩ S(A, 2)`.

---

## CND.def — CreateNewDocument (DEF, definition)

CREATENEWDOCUMENT(A) is a substrate composite Σ →\* Σ' under ValidComposite★ (ASN-0047) realised as a single K.δ firing (case (ii): k=2 off A when D_A=∅, else k=0 off max(D_A)) registering d into E_doc with M(d)=∅; it returns d

---

## CND.pre — CreateNewDocumentPre (PRE, requires)

Preconditions: A ∈ E ∧ Account(A); the invoking principal π owns the account (pfx(π) ≼ A, O1; ASN-0042). The authority to allocate beneath the owned account is a stated modeling assumption — grounded in O5 (ASN-0042) over the registry-carrying state, not discharged here, since O5 quantifies over B and Π_Σ, absent from (C,L,E,M,R). No content argument

---

## CND.A-act — AccountActivated (ASSUME, axiom)

Standing assumption owed by (out-of-scope) account provisioning: A ∈ E ∧ Account(A) ⟹ Activated(A_doc(A)) — an account carries an activated document sub-allocator the instant it exists, with no separate activation step (account-tier analogue of SubAllocatorBundle, ASN-0047; structural per Nelson's baptism/ghost-element intent). Discharges Activated(A_doc(A)) for the ActivatedEmission check on d

---

## CND.alloc — AllocatesDocument (POST, ensures)

Allocates exactly one fresh document address d from A_doc(A)=S(A,2): d = inc(A,2) if D_A=∅ else inc(max(D_A),0), where D_A = {e ∈ E : Document(e) ∧ parent(e)=A ∧ #e=#A+2} is the length-restricted document-chain frontier (versions, length ≥ #A+3, excluded); with Document(d), zeros(d)=2, parent(d)=A, T4-valid(d), d ∉ E

---

## CND.empty — EmptyArrangement (POST, ensures)

M'(d) = ∅: dom(M'(d)) = ∅ and ran(M'(d)) = ∅ — the new document holds no V-positions, no V→I mappings, no content

---

## CND.C-frame — ContentStoreFrame (POST, ensures)

C' = C: the content store is entirely unchanged — no byte added, no value altered. Creation adds a place, not content (ghost element)

---

## CND.L-frame — LinkStoreFrame (POST, ensures)

L' = L: the link store is unchanged

---

## CND.R-frame — ProvenanceFrame (POST, ensures)

R' = R: the provenance relation is unchanged

---

## CND.E — EntitySetGrowth (POST, ensures)

E' = E ∪ {d} with d ∉ E: every existing entity persists (E ⊆ E') and the document population grows by exactly one (|E'\_doc| = |E\_doc| + 1)

---

## CND.doc-frame — DocumentArrangementFrame (POST, ensures)

(A d' ∈ E_doc : M'(d') = M(d')): every existing document's arrangement is wholly untouched

---

## CND.monotone — AllocationMonotonicity (LEMMA, lemma)

d strictly exceeds every document address baptised on A's own document chain — every A_doc(A) emission and every version forked from one (the v\_{#A+1}=0 entities) — including never-populated ones. Document-level entities off that chain (v\_{#A+1}≠0, allocated under a proper sub-account A'=[A,x,…]) are NOT dominated by d, but are distinct from d by divergence at position #A+1, which is all freshness/uniqueness require. Existing addresses remain valid; d is never a reuse. Same-allocator ordering and same-chain distinctness by S0 (StreamOrdering, ASN-0040 — strictly increasing, hence injective over S(A,2), unconditional, no single-authority premise); on-chain version ordering by direct T1 lexicographic dominance at position #A+2 (T9 does not apply across allocators); cross-namespace disjointness by B7 (ASN-0040); permanence T8 (ASN-0034). B8's same-namespace branch is deliberately not invoked, its single-authority precondition being undischarged over this state

---

## CND.subAlloc — SubAllocatorActivation (POST, ensures)

Creation activates A_C(d) and A_L(d) (content and link sub-allocators, anchors [d.0.s_C], [d.0.s_L]) without emission; both subspaces are available but empty at Σ' (SubAllocatorBundle, ASN-0047)

---

## CND.no-sharing — NoSharing (LEMMA, lemma)

The fresh document shares no I-address with any prior document: ran(M'(d)) = ∅; and future content drawn from A_C(d) has origin = d, so by S4 (ASN-0036) it shares no I-address with any other document regardless of value coincidence

---

## CND.own — StructuralOwnership (LEMMA, lemma)

Ownership is structural and derivable over ASN-0047's state (C,L,E,M,R): parent(d)=A and A ≼ d (every A_doc(A) emission has form [A,0,j]), so with pfx(π) ≼ A (CND.pre) and prefix transitivity, owns(π,d) ≡ pfx(π) ≼ d (O1; ASN-0042) — d ∈ odom(π). The subdivision authority O5 (ASN-0042) is NOT discharged here: it quantifies over the registry B and principal set Π_Σ, absent from this state model, so the caller's allocation authority is a stated modeling assumption deferred to the registry-carrying ASN (parallel to the ω deferral). The effective-owner statement ω\_{Σ'}(d) = ω\_Σ(A) is NOT asserted here: ω is defined over ASN-0042's registry B, absent from this state model, and no foundation result couples E to B on the document chain (the needed invariant {e ∈ E : Document(e) ∧ parent(e)=A ∧ #e=#A+2} = Σ.B ∩ S(A,2) is unestablished); the ω-valued claim is deferred to a registry-carrying ASN where the K.δ step is a genuine Bop(A,2) baptism (B6(A,2) holds)

---

## CND.refer — ImmediateReferability (LEMMA, lemma)

d is immediately, permanently, and unambiguously referable: a link may target d at Σ' before any content exists; uniqueness is decentralised (B8, ASN-0040) and identity is immutable for the life of the system

---

## CND.atomicity — Atomicity (LEMMA, lemma)

The single-K.δ decomposition is atomic by the sequential-transition axiom (ASN-0093); no observable intermediate state exists, so all invariants hold throughout. Coupling constraints J0, J1★, J1'★ hold vacuously

---

## CND.inv — InvariantMaintenance (INV, predicate)

Σ' satisfies the full ExtendedReachableStateInvariants (ASN-0047) and the transition invariant P3: P0, P1, M0, S2, S3★, P6, P8, S7d, ActivatedEmission (for d: witness A_doc(A), with d ∈ S(A,2) from Effect One and Activated(A_doc(A)) from the standing assumption CND.A-act), and address permanence (T8, ASN-0034) with distinctness (B7 for cross-namespace, S0 for same-chain injectivity over S(A,2); ASN-0040 — GlobalUniqueness not used, its T10a-conformance premise undischarged, and B8's same-namespace branch not used, its single-authority precondition undischarged over this state) verified directly; the empty-arrangement family (S3★-aux, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, CL-OWN, CL-UNIQ) vacuous for d via dom(M'(d))=∅; the content/link/provenance families (S4, S7a, S7b, C1b, C1c, C-fin, P7, P7a, P4★, P4a, L0, L1, L1a, L1b, L1c, L3, L14, L-fin, NodeLineage) frame-inherited; P3 holds since only M gains the empty entry M'(d)=∅
