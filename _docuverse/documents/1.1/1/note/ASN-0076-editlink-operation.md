# ASN-0076: EDITLINK Operation

*2026-05-25*

Nelson lists "editable links" among the desired features of the docuverse (LM 4/79). The current specification establishes through L12 (LinkImmutability, ASN-0043) that once a link enters `dom(Σ.L)`, its value is permanently fixed across every state transition. The two commitments appear to contradict each other: how can links be edited if their endsets cannot change?

We will resolve the tension by observing that "editing" need not — and, we will argue, *must* not — mean "in-place mutation." A document, in this architecture, is not edited by overwriting; the original persists in storage, a new version is created alongside it, and the lineage between them is recorded as part of the docuverse. We will show that link editing must follow exactly the same pattern, and that the existing primitives are sufficient to express it as a composite. No new primitive is required, no existing invariant is weakened, and every guarantee the original link enjoyed continues to hold unaffected.

The consultation evidence supports this reading directly. Nelson is explicit that FEBE supplies `MAKELINK` but no `EDITLINK` or `MODIFYLINK`; the seventeen commands of XU.87.1 admit no link-modification operation. Gregory's analysis of udanax-green confirms the same absence at the implementation level: link orgls carry no "supersedes" field, the spanfilade is append-only with no `deletespanf`, link I-addresses are monotonic and never reused, and the granfilade retains every link orgl forever once allocated. Both authorities arrive independently at the same architectural commitment: there is no operation that mutates an existing link.

What there *is*, however, is the means to express edit semantics as a composite of two link-allocation events. We formalize this composite as EDITLINK and demonstrate that the resulting structure realizes every property a user would expect of an "edit" — the new endsets are reachable, the supersession relationship is discoverable, the history is traceable — while leaving the original link entirely undisturbed.

## Foundation Recap

We take from the foundation:

- **Link store** `Σ.L : T ⇀ Link` (ASN-0043): a partial function mapping tumbler addresses to link values, each of arity ≥ 3 (L3).
- **Link addresses** are element-level tumblers in the link subspace `s_L` (L0, L1).
- **Link Permanence** (L12): `(A Σ → Σ' :: (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))` — once created, a link's address persists and its value is permanently fixed.
- **Link uniqueness** (L11a): distinct T10a-conforming allocation events produce distinct link addresses.
- **Link allocation discipline** (L1a, L1c): every link is allocated under its home document's tumbler prefix via T10a-conforming increments.
- **N-endset structure** (L3): every link has `|Σ.L(a)| ≥ 3` endsets; the third (type) endset is non-empty.
- **Endset generality** (L4): endset spans may reference any tumbler — including link I-addresses themselves.
- **Reflexive addressing** (L13): for any `b ∈ dom(Σ.L)`, the unit-depth span `(b, δ(1, #b))` is the canonical reference to the link at `b`.
- **Set semantics of endsets** (L5) and **slot distinction** (L6): endsets are unordered; slots are addressable.
- **Standard triple convention**: arity-3 links have slot 1 as from-endset, slot 2 as to-endset, slot 3 as type-endset.
- **K.λ — LinkAllocation** (ASN-0047): the elementary transition that adds a fresh link to `dom(L)` under a specified home document with specified endsets. The frame of K.λ preserves `C`, `E`, `M`, and `R`.
- **PrefixSpanCoverage** (ASN-0043): for any tumbler `x` with `#x ≥ 1`, `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}` — the unit-depth span at `x` denotes exactly the prefix-closure of `x`.

We will need nothing else.

## The Composite

We name an existing link `ℓ_old ∈ dom(Σ.L)` whose semantic content is to be revised, and we name an endset sequence `(e'_1, ..., e'_N)` with `N ≥ 3` and `e'_3 ≠ ∅` — the new endsets, satisfying L3's structural constraints. We name a document `d_new ∈ E_doc` under which the new links will be allocated; `d_new` is owned by whichever party initiates the edit, and need not coincide with `home(ℓ_old)`.

Three values will be needed, of which the first two are produced by allocation and the third is supplied as an external input:

- `ℓ_new` — the I-address of the *successor link*, freshly allocated under `d_new`'s link sub-allocator;
- `ℓ_sup` — the I-address of the *supersession link*, freshly allocated under `d_new`'s link sub-allocator;
- `τ_sup` — a tumbler supplied by the caller as the address designating the supersession relationship. EDITLINK requires only that `τ_sup ∈ T ∧ #τ_sup ≥ 1`, so that the unit-depth span `(τ_sup, δ(1, #τ_sup))` is well-formed under T12. Whether `τ_sup` lies in `dom(C)`, `dom(L)`, or neither — whether it is element-level, document-level, or in some dedicated subspace — is not constrained by the link model. EDITLINK simply records the caller's chosen address. Foundation evidence supports this open-endedness: L4 (EndsetGenerality, ASN-0043) explicitly permits endset spans to reference any addresses, and L9 (TypeGhostPermission, ASN-0043) explicitly permits type-endset addresses that lie outside `dom(C) ∪ dom(L)`. The semantics of distinguishing "supersession-type addresses" from other type addresses — and any registry convention that pins `τ_sup` to a particular tumbler — are deferred to a future ASN on type-endset conventions.

**Precondition (composite, evaluated at the pre-state `Σ`):**

```
ℓ_old ∈ dom(Σ.L)
d_new ∈ E_doc
N ≥ 3
(A i : 1 ≤ i ≤ N : e'_i ∈ Endset)
e'_3 ≠ ∅
τ_sup ∈ T ∧ #τ_sup ≥ 1
```

We define:

```
EDITLINK(ℓ_old, (e'_1, ..., e'_N), d_new, τ_sup) ≡
    K.λ(d_new, ℓ_new, (e'_1, ..., e'_N));
    K.λ(d_new, ℓ_sup, (E_from, E_to, E_type))
```

where the supersession endsets are:

```
E_from = { (ℓ_old, δ(1, #ℓ_old)) }
E_to   = { (ℓ_new, δ(1, #ℓ_new)) }
E_type = { (τ_sup, δ(1, #τ_sup))  }
```

By L13 and PrefixSpanCoverage, `coverage(E_from) = {t : ℓ_old ≼ t}` (the singleton `{ℓ_old}` plus its extensions, of which there are none until subsequent allocations may add them), and similarly for `E_to` and `E_type`. The supersession link has arity 3, satisfies L3 (`e_3 ≠ ∅`), and references the two link entities via canonical unit-depth spans.

The composite is *not* a primitive of the transition vocabulary `Σ` introduced in ASN-0047. It does not extend that vocabulary. It is a named pattern of two existing primitive applications, no different in kind from any other sequence of transitions a user might issue.

**EDITLINK as a valid composite.** We verify against ValidComposite★ (ASN-0047). The composite applies K.λ twice. (i) Elementary preconditions of K.λ are satisfied at each intermediate state, as discharged in E0 below. (ii) J0 (AllocationRequiresPlacement) is vacuously satisfied: K.λ's frame preserves `C`, so `dom(Σ'.C) = dom(Σ.C)` across the composite and the antecedent `a ∈ dom(C') \ dom(C)` is empty. (iii) J1★ (ExtensionRecordsProvenanceContentSubspace) and J1'★ (ProvenanceRequiresExtensionContentSubspace) are vacuously satisfied: K.λ's frame preserves all arrangements `M(d)`, so the range differences `ran(M'(d)) \ ran(M(d))` are empty, and the antecedent of each coupling is empty. Therefore EDITLINK satisfies ValidComposite★.

## E0 — EditLink as Composite

We claim:

**E0 (EditLinkComposite).** EDITLINK is realized as a sequence of exactly two K.λ steps: the first allocates the successor link `ℓ_new` with the new endset sequence; the second allocates the supersession link `ℓ_sup` whose from- and to-endsets reference `ℓ_old` and `ℓ_new` respectively, and whose type-endset references the designated supersession-type address `τ_sup`.

The composite must be admissible under K.λ's preconditions evaluated at each intermediate state. K.λ requires (i) the target document to be in `E_doc`; (ii) the new link's I-address to lie outside `dom(C) ∪ dom(L)`; (iii) the I-address to satisfy the link allocation discipline `zeros(·) = 3 ∧ E(·)_1 = s_L ∧ #E(·) ≥ 2 ∧ origin(·) = d_new`; and (iv) the endset sequence to satisfy L3 — arity at least 3, each endset in `Endset` (equivalently: each constituent span satisfies T12), and the third endset non-empty.

We discharge each precondition at each step explicitly.

**Successor step** — `K.λ(d_new, ℓ_new, (e'_1, ..., e'_N))` fires from the pre-state `Σ`. The K.λ rule determines `ℓ_new` from `d_new`'s allocator state by case analysis:

*Sub-case (a) — first emission.* When `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} = ∅`, K.λ's first-emission rule fixes `ℓ_new = [d_new.0.s_L.1]`. SubAllocatorAxiom.FirstEmission (ASN-0047) certifies that this tumbler satisfies `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)` at the state of allocation, with `origin(ℓ_new) = d_new` and `#E(ℓ_new) = 2`.

*Sub-case (b) — subsequent emission.* When `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new} ≠ ∅`, K.λ's subsequent-emission rule fixes `ℓ_new = inc(max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_new}, 0)`. By SubAllocatorAxiom.T10aConformance, `A_L(d_new)` is a T10a-conforming allocator and `inc(·, 0)` extends its enumeration; by L11a (LinkUniqueness, ASN-0043) the output is distinct from every prior link allocation, so `ℓ_new ∉ dom(Σ.L)`. By SubAllocatorAxiom.Disjointness, `dom(A_L(d_new))` is disjoint from every content sub-allocator's domain; combined with L14 (StoreDisjointness, ASN-0047), `ℓ_new ∉ dom(Σ.C)`.

In both sub-cases, SubAllocatorAxiom.Namespace certifies that `ℓ_new` is T4-valid with `zeros(ℓ_new) = 3`; SubAllocatorAxiom.Subspace gives `E(ℓ_new)_1 = s_L`. The origin equality `origin(ℓ_new) = d_new` follows from the allocator rule (`ℓ_new` is emitted by `A_L(d_new)`, whose outputs all carry origin `d_new`). The depth bound `#E(ℓ_new) ≥ 2` holds directly in (a) (the first emission has `#E = 2`) and is inherited in (b) from TA5(c) — `inc(·, 0)` preserves length — applied to a prior emission that itself satisfied `#E ≥ 2`. The endset sequence `(e'_1, ..., e'_N)` satisfies L3 by the precondition of the composite. Clauses (i)–(iv) of K.λ are therefore discharged at the successor step.

After the successor step, the intermediate state `Σ_1` has `dom(Σ_1.L) = dom(Σ.L) ∪ {ℓ_new}` with `Σ_1.L(ℓ_new) = (e'_1, ..., e'_N)`; all other state components are unchanged by K.λ's frame.

**Supersession step** — `K.λ(d_new, ℓ_sup, (E_from, E_to, E_type))` fires from `Σ_1`. Since `ℓ_new ∈ dom(Σ_1.L)` with `origin(ℓ_new) = d_new`, the set `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d_new}` is non-empty; K.λ's subsequent-emission rule applies unconditionally. Since `inc(·, 0)` strictly increases its argument by TA5(a), `ℓ_new` is the maximum of `A_L(d_new)`'s outputs in `dom(Σ_1.L)`, so the rule fixes `ℓ_sup = inc(ℓ_new, 0)`. By the same argument structure as sub-case (b) of the successor step, now applied at `Σ_1`: T10aConformance + L11a give `ℓ_sup ∉ dom(Σ_1.L)`; Disjointness + L14 give `ℓ_sup ∉ dom(Σ_1.C)`. Namespace gives `zeros(ℓ_sup) = 3`; Subspace gives `E(ℓ_sup)_1 = s_L`. The origin equality follows from the allocator rule. The depth bound `#E(ℓ_sup) ≥ 2` follows from TA5(c) inherited from `#E(ℓ_new) ≥ 2`. Clauses (i)–(iii) of K.λ are thereby discharged at the supersession step; clause (iv) — L3 for the supersession endset sequence — requires further work.

L3 requires arity at least 3 (satisfied by arity 3), every endset in `Endset`, and the third endset non-empty. The third endset `E_type` is a singleton, hence non-empty. Membership of each of `E_from`, `E_to`, `E_type` in `Endset = 𝒫_fin(Span)` requires each constituent span to satisfy T12. The three spans share the form `(x, δ(1, #x))` for `x ∈ {ℓ_old, ℓ_new, τ_sup}`. T12 (SpanWellDefinedness, ASN-0034) requires (a) `Pos(ℓ)` and (b) `actionPoint(ℓ) ≤ #s`. By OrdinalDisplacement (ASN-0034) at `(n, m) = (1, #x)`: `Pos(δ(1, #x))` holds (since `n = 1 ≥ 1` and `m = #x ≥ 1`) and `actionPoint(δ(1, #x)) = #x`. So T12(b) reads `#x ≤ #x`, saturating with equality. The three lengths are positive in each case:

- *For `E_from`:* `#ℓ_old ≥ 1` by T0 (every tumbler in T has length ≥ 1, ASN-0034); concretely `#ℓ_old ≥ 6` since `ℓ_old` is element-level with `#E ≥ 2` (L1, L1b).
- *For `E_to`:* `#ℓ_new ≥ 1` by T0; concretely `#ℓ_new ≥ 6` for the same reason.
- *For `E_type`:* `#τ_sup ≥ 1` by the precondition of the composite.

Each of the three supersession spans therefore lies in `Span`, each singleton endset lies in `Endset`, and L3 holds for `(E_from, E_to, E_type)`. Clause (iv) of K.λ is discharged at the supersession step.

We must observe two things about the order. First, the successor step must precede the supersession step *if* we require the supersession endsets to reference an existing link entity; by L4 the supersession step is admissible at any time, but its referent is meaningful only after `ℓ_new ∈ dom(L)`. Second, by SequentialTransitionAxiom (ASN-0047) each K.λ step is atomic, but the two steps need not be adjacent in the transition sequence; arbitrary other transitions may intervene between them.

**Invariant inheritance.** EDITLINK is a ValidComposite★ (discharged in §The Composite), so by ExtendedReachableStateInvariants (ASN-0047) every per-state invariant of the extended reachable state continues to hold at the post-state — in particular L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, CL-OWN, CL-UNIQ, and the S-invariants S0–S3★, S7a–d, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, P6, P7, P8, NodeLineage. The composite-boundary properties P4★, P4a, P7a hold at the post-state because EDITLINK satisfies J0, J1★, and J1'★ (discharged in §The Composite). EDITLINK therefore preserves the full invariant suite of ASN-0047's extended reachable state without introducing any new invariants of its own.

## E1 — Original Preservation

The center of the construction is what does *not* happen.

**E1 (OriginalPreservation).** For any state transition `Σ →* Σ'` realizing EDITLINK applied to `ℓ_old`:

```
ℓ_old ∈ dom(Σ'.L)  ∧  Σ'.L(ℓ_old) = Σ.L(ℓ_old)
```

*Proof.* The composite consists of two K.λ steps. K.λ's frame preserves all existing entries in `dom(L)` and adds exactly one new entry. By L12 applied to each step in sequence, every entry present in `dom(Σ.L)` is present and unchanged in the post-state of each K.λ application, and therefore present and unchanged in `dom(Σ'.L)`. Since `ℓ_old ∈ dom(Σ.L)` by the precondition of the composite, the conclusion follows.

This is the central architectural claim. The original link's I-address remains valid; its endsets are bit-for-bit identical to what they were before EDITLINK; its home document and ownership are unchanged. Any property of the system that depended on `Σ.L(ℓ_old)` continues to hold in the post-state, by structural identity of the relevant state component.

## E2 — Successor Distinctness

**E2 (SuccessorDistinctness).** The successor link's I-address differs from the original's, and the supersession link's I-address differs from both:

```
ℓ_new ≠ ℓ_old  ∧  ℓ_sup ≠ ℓ_old  ∧  ℓ_sup ≠ ℓ_new
```

*Proof.* K.λ's precondition for allocating `ℓ_new` includes `ℓ_new ∉ dom(L) ∪ dom(C)` evaluated at the intermediate state immediately preceding the allocation. By L12a (LinkStoreMonotonicity, ASN-0043), `dom(L) ⊆ dom(L_i)` at every intermediate state `L_i` along the chain leading to the K.λ step, so `ℓ_old ∈ dom(L_i)` whenever `ℓ_old ∈ dom(Σ.L)`. So `ℓ_new ≠ ℓ_old`. The same argument applied to the second K.λ step (which sees both `ℓ_old` and `ℓ_new` in its pre-state link store) yields `ℓ_sup ≠ ℓ_old` and `ℓ_sup ≠ ℓ_new`.

More structurally: L11a (LinkUniqueness, ASN-0043) guarantees that distinct T10a-conforming allocation events produce distinct link addresses. The allocation events producing `ℓ_old`, `ℓ_new`, and `ℓ_sup` are pairwise distinct (they fire at distinct states, and L1c's chain-existential admits each independently), so their outputs are pairwise distinct addresses. The result is foundational, not contingent on any property of EDITLINK.

The implication is that no operation, applied to no input, can produce two links with the same I-address. A "fresh edit" of `ℓ_old` is necessarily a *new entity* in `dom(L)`, indistinguishable in kind from any other newly-allocated link, and the supersession claim is itself a third distinct entity.

## E3 — Endset Freedom

**E3 (SuccessorEndsetFreedom).** The successor's endset sequence `(e'_1, ..., e'_N)` may differ arbitrarily from `Σ.L(ℓ_old)`, subject only to the structural constraints of L3: `N ≥ 3`, each `e'_i ∈ Endset`, and `e'_3 ≠ ∅`.

*Proof.* K.λ accepts any endset sequence satisfying L3 (the precondition `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : e_i ∈ Endset) ∧ e_3 ≠ ∅`). There is no precondition coupling the new sequence to any prior link's sequence. In particular:

- the new from-endset may name different spans, more spans, fewer spans, or no spans at all;
- the new type-endset may designate a different type;
- the arity itself may differ from `|Σ.L(ℓ_old)|`, subject to the floor of 3.

This is what "edit" means abstractly. The user-facing operation is not parameterized by any "diff" against the original; it produces a fresh link whose endsets are stated whole. The supersession link records that the new is intended as a successor to the old, but the system imposes no resemblance constraint between the two endset sequences.

## The Supersession Relationship

We now examine the second link in the composite — the link that we will call a *supersession link* by convention, while keeping the conventional designation carefully separated from the structural witness the link model can actually establish.

What we will call a supersession link, in our construction, has the structural form of a link of arity 3 whose endsets reference `ℓ_old`, `ℓ_new`, and `τ_sup` via canonical unit-depth spans, as specified in the composite definition. The link model alone cannot *identify* such a link as a supersession: it admits arity-3 links whose first endset references one link, whose second endset references another link, and whose third endset references some third address for any number of reasons, with no syntactic mark distinguishing those whose author meant to assert supersession from those whose author did not. Identification depends on the external convention that designates `τ_sup` as the supersession-type address — a convention this ASN cannot fix and defers to a future ASN on type-endset conventions (see Open Questions). The claim that follows is therefore structural: it establishes that the spans are present in the endsets and recoverable by any discovery operation, not that the link is identifiable as a supersession without an external designation of `τ_sup`.

**E4 (SupersessionLink).** Following EDITLINK, the state `Σ'` contains a link `ℓ_sup ∈ dom(Σ'.L)` with:

```
(ℓ_old, δ(1, #ℓ_old)) ∈ Σ'.L(ℓ_sup).e₁
(ℓ_new, δ(1, #ℓ_new)) ∈ Σ'.L(ℓ_sup).e₂
(τ_sup,  δ(1, #τ_sup))  ∈ Σ'.L(ℓ_sup).e₃
```

By L13, the spans `(ℓ_old, δ(1, #ℓ_old))` and `(ℓ_new, δ(1, #ℓ_new))` are well-formed references to the link entities at those addresses. By L4, endset spans may target any tumblers — including link I-addresses. By PrefixSpanCoverage, the canonical unit-depth span at `x` has coverage `{t : x ≼ t}`, which contains `x` itself and any addresses that may later be allocated as extensions of `x`. The supersession link therefore stands in a permanent structural relationship to the two link entities it relates.

We observe that the supersession link is not privileged by the link model. It is a link like any other — same allocation discipline, same immutability, same discoverability. What makes it a *supersession* link is the convention of `τ_sup` in its type-endset; readers and writers of the system agree, by convention external to the link store, that this type address designates the supersession relationship.

## E5 — Divergent Successors

The asymmetry between immutable link entities and mutable supersession assertions reveals a property absent from in-place edit models.

**E5 (DivergentSuccessors).** For any state `Σ` satisfying all invariants and any natural number `k`, there exists a sequence of transitions `Σ →* Σ_k` such that `Σ_k` contains `k` distinct supersession links each naming `ℓ_old` in its from-endset, with `k` distinct successor links in their respective to-endsets.

*Proof.* By induction on `k`. The base `k = 0` is trivial. For the inductive step, given `Σ_{k-1}` with `k-1` such supersessions, apply EDITLINK to produce a fresh successor `ℓ_new,k` (distinct from all prior successors by L11a) and a fresh supersession link `ℓ_sup,k` (likewise distinct). By L12, all `k-1` prior supersessions persist; the new one is added; the resulting state `Σ_k` has the required structure.

The system imposes no exclusivity. Two independent EDITLINK composites against the same `ℓ_old`, occurring in either order in the transition sequence, yield a state containing both supersession claims as distinct facts; no transition ordering produces a conflict. Both claims persist; both are discoverable; no claim is privileged over any other within the link model itself. What it means to "resolve" the ambiguity — which successor is the authoritative one, which lineage to follow — is a reader-side policy decision, outside the scope of the link model.

This stands in sharp contrast to an in-place edit model, in which "the" successor is a singular state component and successive edits must be reconciled into a single result. Such reconciliation either forces consensus (centralizing the system) or discards information (losing edits). The append-only construction admits both edits as first-class facts and defers the resolution policy to the reader.

## E6 — Supersession Ownership Freedom

**E6 (SupersessionOwnershipFreedom).** The supersession link's home document `d_new` is not constrained to equal `home(ℓ_old)`.

*Proof.* K.λ's precondition `d_new ∈ E_doc` requires only that the target be a valid document. L1a constrains the allocation site of the new link to be under `d_new`'s prefix — but does not constrain `d_new` itself relative to `home(ℓ_old)`. The supersession link may therefore be allocated under any document the executing party owns.

The consequence is that anyone — not merely the original link's owner — may publish a supersession claim against any link. Bob may assert that his link `ℓ_new` supersedes Alice's `ℓ_old`. By E1, Alice's original is untouched. By E5, Carol may simultaneously assert a *different* supersession against the same `ℓ_old`. The system treats all such assertions as facts of equal structural weight. Their *authority* — whose claim a reader chooses to honor — is a social question, supplied by application-layer trust models, not a structural one decidable from the link store alone.

This is consistent with Nelson's broader posture: claims are visible and attributable. The supersession link's home address indicates who made the claim; readers may use this attribution as part of their resolution policy, but the link model does not.

## E7 — Lineage Discoverability

**E7 (LineageDiscoverability).** The supersession link's endsets structurally contain `ℓ_old` and `ℓ_new` as discoverable referents. Formally, define for each `a ∈ T` the *covering set*

```
covers(Σ, a) ≡ {ℓ ∈ dom(Σ.L) : (E i, (s, w) : 1 ≤ i ≤ |Σ.L(ℓ)| ∧ (s, w) ∈ Σ.L(ℓ).e_i : a ∈ coverage({(s, w)}))}
```

— the set of links whose endsets reference `a` through at least one span. Then in the post-state `Σ'`:

```
ℓ_sup ∈ covers(Σ', ℓ_old)  ∧  ℓ_sup ∈ covers(Σ', ℓ_new)
```

*Proof.* By the construction of `Σ.L(ℓ_sup).e_1 = E_from = {(ℓ_old, δ(1, #ℓ_old))}` and PrefixSpanCoverage (ASN-0043), `coverage({(ℓ_old, δ(1, #ℓ_old))}) ⊇ {ℓ_old}`, so `ℓ_old ∈ coverage(Σ'.L(ℓ_sup).e_1)`. Hence `ℓ_sup ∈ covers(Σ', ℓ_old)`. Symmetrically for `ℓ_new` via `Σ'.L(ℓ_sup).e_2 = E_to`.

The claim is structural: it concerns the relationship between `Σ'.L(ℓ_sup)`'s endsets and the addresses `ℓ_old`, `ℓ_new`, evaluated in the post-state link store. Any discovery operation that returns `covers(Σ, ·)` — or any superset of it that respects endset coverage — will surface `ℓ_sup` when queried with `ℓ_old` or `ℓ_new`. The formalization of such operations is the proper subject of the link-search specification; E7 establishes only that the structural witness is present.

This property is what makes the supersession link operative as a record of editing. It is not enough to *create* the supersession link; the structural relationship must be present in the link store so that any conforming discovery operation can recover the lineage. Without this structural witness, an "edit" would be a write-only act with no path to recover the lineage — exactly the failure mode Nelson decries when he writes that history must be navigable.

## E8 — Original Resolution Unaffected

**E8 (OriginalResolutionUnaffected).** Any operation that resolves an endset reference to `ℓ_old` and reads `Σ.L(ℓ_old)` obtains the same value before and after EDITLINK.

*Proof.* By E1, `Σ'.L(ℓ_old) = Σ.L(ℓ_old)`. Resolution operations on `ℓ_old` consult `Σ'.L(ℓ_old)` and obtain the unchanged value. No state component intermediating this lookup is altered by EDITLINK (the frame of K.λ preserves `C`, `M`, `E`, `R`; and EDITLINK only extends `L`, never modifies).

This is the formal counterpart of Nelson's permanence guarantee. A reader who held a reference to `ℓ_old` before EDITLINK still holds a valid reference after; the link's endsets are still readable; the link's content is identically what it was. The supersession claim is *additive* — it adds information about a relationship, without subtracting any information from the original. A reader is free to ignore the supersession entirely and continue to follow `ℓ_old` as if no edit had occurred.

## E9 — Lineage Permanence

The same argument that protects the original protects the supersession assertion.

**E9 (LineagePermanence).** Once created, the supersession link persists across all subsequent state transitions:

```
ℓ_sup ∈ dom(Σ.L)  ⟹  (A Σ → Σ' :: ℓ_sup ∈ dom(Σ'.L) ∧ Σ'.L(ℓ_sup) = Σ.L(ℓ_sup))
```

*Proof.* The supersession link is a link, and L12 applies uniformly to all entries in `dom(L)`.

The implication is that *the historical record of editing is itself immutable*. A user who later wishes to "retract" the supersession cannot do so by mutating `ℓ_sup`. They can, however, allocate a *counter-claim* — a new link asserting that the supersession is not in force, or that a different supersession should take precedence. The counter-claim is, structurally, just another link; it is itself permanent; and it joins the supersession in the discoverable web of assertions about `ℓ_old`. The system accumulates the full history of claims and counter-claims, leaving the resolution policy to the reader.

## E10 — No Implicit Notification

The transition frame of K.λ tells us what EDITLINK does *not* do.

**E10 (NoImplicitNotification).** EDITLINK modifies neither any arrangement nor the provenance record of any document:

```
(A d ∈ E_doc :: Σ'.M(d) = Σ.M(d))  ∧  Σ'.R = Σ.R
```

*Proof.* Each K.λ step in the composite has frame `(A d :: M'(d) = M(d)) ∧ R' = R`. The composition of two such steps preserves the same frame. In particular, K.λ on `d_new` does not even touch `M(d_new)` — placement of the new link in an arrangement, if desired, is a separate K.μ⁺_L step, not part of EDITLINK.

The implication is that `home(ℓ_old)`'s arrangement is not extended with any notification of the edit; the original link's owner receives no automatic push. If the original owner is to *learn* of the edit, it is by issuing a discovery query — the pull model. Nelson endorses this posture explicitly when he describes the docuverse as "what connects here from other documents" being a question the reader (or owner) asks, not a fact pushed at them.

The non-notification property is structural, not optional. The composite as defined here cannot notify the original owner, because K.λ's frame does not admit modifications to `home(ℓ_old)`'s arrangement (which would require K.μ⁺ or K.μ⁺_L on a document other than `d_new`). Adding such a notification step would require either operating on a document the executor does not own (in conflict with allocation discipline) or coordinating with the original owner's system (in conflict with the no-coordination principle). The append-only, no-notification design follows from the underlying architecture.

## A Worked Example

We make the construction concrete by tracing EDITLINK through specific tumbler values.

Suppose Alice owns document `d_alice = [3.0.5.0.7]` — node 3, account 5, document 7 — and has allocated a single link `ℓ_old = [3.0.5.0.7.0.2.1]` as the first emission of `A_L(d_alice)`. This address is well-formed under the link allocation discipline: `zeros(ℓ_old) = 3` (positions 2, 4, 6), `subspace_I(ℓ_old) = E(ℓ_old)_1 = 2 = s_L`, `origin(ℓ_old) = d_alice`, `#E(ℓ_old) = 2 ≥ 2`. Suppose `Σ.L(ℓ_old) = (F_old, G_old, Θ_old)` for some triple of endsets — the specific endsets Alice gave the link at creation.

Bob owns document `d_bob = [4.0.2.0.3]` and wishes to publish a successor with revised endsets `(e'_1, e'_2, e'_3)`. At the pre-state `Σ`, no links have been emitted by `A_L(d_bob)` yet; the set `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d_bob}` is empty. Bob supplies `τ_sup = [1.0.1.0.2.0.2.5]` as the address designating supersession — its specific value matters only insofar as `τ_sup ∈ T ∧ #τ_sup = 8 ≥ 1`, the requirements of the composite's preconditions.

The composite `EDITLINK(ℓ_old, (e'_1, e'_2, e'_3), d_bob, τ_sup)` unfolds as follows.

*Step 1.* `K.λ(d_bob, ℓ_new, (e'_1, e'_2, e'_3))` fires from `Σ`. The first-emission predicate of K.λ holds, so `ℓ_new = [d_bob.0.s_L.1] = [4.0.2.0.3.0.2.1]`. The preconditions are discharged: `d_bob ∈ E_doc`; `ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)` by SubAllocatorAxiom.Disjointness combined with L11a; `zeros(ℓ_new) = 3 ∧ E(ℓ_new)_1 = s_L`; `#E(ℓ_new) = 2`; `origin(ℓ_new) = d_bob`; the endset sequence has arity 3 with non-empty third slot. The effect: `dom(L_1) = dom(Σ.L) ∪ {ℓ_new}`, with `L_1(ℓ_new) = (e'_1, e'_2, e'_3)`.

*Step 2.* `K.λ(d_bob, ℓ_sup, (E_from, E_to, E_type))` fires from the intermediate state. Now `{ℓ' ∈ dom(L_1) : origin(ℓ') = d_bob} = {ℓ_new}`, so the subsequent-emission rule applies: `ℓ_sup = inc(ℓ_new, 0)`. Since `ℓ_new = [4.0.2.0.3.0.2.1]` is T4-valid, TA5-SigValid gives `sig(ℓ_new) = #ℓ_new = 8`, and TA5 specifies that `inc(·, 0)` increments the component at position `sig`, so `ℓ_sup = [4.0.2.0.3.0.2.2]`. The endsets resolve to:

```
E_from  = { ([3.0.5.0.7.0.2.1], [0, 0, 0, 0, 0, 0, 0, 1]) }
E_to    = { ([4.0.2.0.3.0.2.1], [0, 0, 0, 0, 0, 0, 0, 1]) }
E_type  = { ([1.0.1.0.2.0.2.5], [0, 0, 0, 0, 0, 0, 0, 1]) }
```

Each displacement is `δ(1, 8)` — length 8 (matching the target tumbler), all zeros except for `1` at the last position. The effect: `dom(L_2) = dom(L_1) ∪ {ℓ_sup}`, with `L_2(ℓ_sup) = (E_from, E_to, E_type)`. The post-state is `Σ' = (Σ.C, L_2, Σ.E, Σ.M, Σ.R)`.

We check the claims against this state.

**E0.** K.λ's preconditions were discharged for both steps in the trace above. Step 1 invoked the first-emission rule (no prior outputs of `A_L(d_bob)`); SubAllocatorAxiom.FirstEmission furnished `ℓ_new ∉ dom(Σ.C) ∪ dom(Σ.L)` and `#E(ℓ_new) = 2`; .Namespace and .Subspace furnished `zeros(ℓ_new) = 3 ∧ E(ℓ_new)_1 = 2 = s_L`; the allocator rule fixed `origin(ℓ_new) = d_bob`; the supplied `(e'_1, e'_2, e'_3)` satisfied L3. Step 2 invoked the subsequent-emission rule with `ℓ_new` as the maximum prior output of `A_L(d_bob)`; .T10aConformance + L11a + .Disjointness + L14 (StoreDisjointness) gave `ℓ_sup ∉ dom(L_1) ∪ dom(C_1)`; .Namespace + .Subspace + TA5(c) (inheriting `#E ≥ 2` from `ℓ_new`) discharged the namespace clauses. T12 held for the three supersession spans at `actionPoint(δ(1, 8)) = 8 ≤ 8 = #x`, with `Pos(δ(1, 8))` by OrdinalDisplacement (n = 1, m = 8); L3 thus held for `(E_from, E_to, E_type)`. ✓

**E1.** `ℓ_old = [3.0.5.0.7.0.2.1] ∈ dom(Σ'.L)` because L12 preserves it across both K.λ steps; `Σ'.L(ℓ_old) = (F_old, G_old, Θ_old) = Σ.L(ℓ_old)`. Alice's link is untouched. ✓

**E2.** Pairwise distinctness:
- `ℓ_new ≠ ℓ_old`: `[4.0.2.0.3.0.2.1] ≠ [3.0.5.0.7.0.2.1]`, differing at component 1 (`4 ≠ 3`).
- `ℓ_sup ≠ ℓ_old`: `[4.0.2.0.3.0.2.2] ≠ [3.0.5.0.7.0.2.1]`, differing at component 1.
- `ℓ_sup ≠ ℓ_new`: `[4.0.2.0.3.0.2.2] ≠ [4.0.2.0.3.0.2.1]`, differing at component 8 (`2 ≠ 1`). ✓

**E3.** Bob is free to make `(e'_1, e'_2, e'_3)` bear no resemblance whatsoever to `(F_old, G_old, Θ_old)`: any from-endset, any to-endset, any type-endset designator. The composite imposes no coupling between the new sequence and Alice's original; the only constraints are L3's structural ones (`N = 3 ≥ 3`, each `e'_i ∈ Endset`, `e'_3 ≠ ∅`), which the precondition supplies. ✓

**E4.** The post-state contains `ℓ_sup` with the expected endset structure. By PrefixSpanCoverage, `coverage({(ℓ_old, δ(1, 8))}) = {t : ℓ_old ≼ t}`, which includes `ℓ_old` by reflexivity. So `(ℓ_old, δ(1, 8)) ∈ Σ'.L(ℓ_sup).e_1`, witnessing the structural reference to `ℓ_old` in the first endset; symmetrically for `e_2` and `e_3`. (We do not — and cannot, within the link model — claim from this that `ℓ_sup` is *the* supersession of `ℓ_old`; that designation requires the external `τ_sup` convention.) ✓

**E5.** Suppose Carol owns `d_carol = [5.0.1.0.4]` and, from the post-state `Σ'`, independently runs `EDITLINK(ℓ_old, (e''_1, e''_2, e''_3), d_carol, τ_sup)`. By L12, Bob's `ℓ_new = [4.0.2.0.3.0.2.1]` and `ℓ_sup = [4.0.2.0.3.0.2.2]` persist into Carol's pre-state. Carol's `A_L(d_carol)` has emitted no prior links, so the first-emission rule fixes her successor at `ℓ_new,carol = [5.0.1.0.4.0.2.1]`; the subsequent-emission rule then fixes her supersession at `ℓ_sup,carol = [5.0.1.0.4.0.2.2]`. By L11a, all four addresses are pairwise distinct. The resulting state contains two distinct links whose first endsets reference `ℓ_old`. The argument generalizes by induction on the number of independent edits. ✓

**E6.** `home(ℓ_sup) = d_bob = [4.0.2.0.3] ≠ [3.0.5.0.7] = d_alice = home(ℓ_old)`. K.λ's precondition `d_new ∈ E_doc` was satisfied by `d_bob` alone; nothing in the composite required `d_bob = home(ℓ_old)`. Bob's claim is published in his own namespace, attributable to him, without Alice's participation. ✓

**E7.** `ℓ_sup ∈ covers(Σ', ℓ_old)`: take `i = 1`, `(s, w) = (ℓ_old, δ(1, 8))`; `ℓ_old ∈ coverage({(ℓ_old, δ(1, 8))})` by PrefixSpanCoverage and reflexivity. Symmetrically `ℓ_sup ∈ covers(Σ', ℓ_new)`. ✓

**E8.** Any operation that reads `Σ'.L(ℓ_old)` obtains `(F_old, G_old, Θ_old)` — identical to what `Σ.L(ℓ_old)` would have returned. The claim reduces to E1, which gives `Σ'.L(ℓ_old) = Σ.L(ℓ_old)`. ✓

**E9.** Across any future transition `Σ' → Σ''`, L12 applied to `ℓ_sup ∈ dom(Σ'.L)` gives `ℓ_sup ∈ dom(Σ''.L) ∧ Σ''.L(ℓ_sup) = Σ'.L(ℓ_sup) = (E_from, E_to, E_type)`. The supersession assertion persists indefinitely; no transition admitted by the model can retract it. ✓

**E10.** No K.λ step modifies any arrangement or `R`. `Σ'.M(d_alice) = Σ.M(d_alice)`; `Σ'.M(d_bob) = Σ.M(d_bob)`; and for every other `d ∈ E_doc`, `Σ'.M(d) = Σ.M(d)`. `Σ'.R = Σ.R`. In particular, Alice's arrangement is unchanged — she receives no notification of Bob's claim. ✓

The example exhibits the asymmetry recorded in E6: Alice retains full control of `d_alice`; Bob retains full control of `d_bob`; the supersession claim itself lives in `d_bob`, attributable to Bob, discoverable from either endpoint via E7.

## Why Editing Cannot Be Otherwise

We pause to consider the alternative — an in-place EDITLINK that mutates `Σ.L(ℓ_old)` to a new endset sequence — and to show that it is incompatible with the invariants we already have.

Suppose for contradiction that there exists a transition `Σ → Σ'` and a link `ℓ ∈ dom(Σ.L)` such that `Σ'.L(ℓ) ≠ Σ.L(ℓ)`. Then by definition the transition violates L12, since L12 quantifies over all transitions and asserts equality for every entry in `dom(Σ.L)`. So no such transition is legal in the current model.

Could we weaken L12 to permit mutation? We could — but at the cost of everything L12 provides. Consider what L12 guarantees:

- An endset reference to `ℓ` made today resolves to the same value tomorrow.
- A supersession link created against `ℓ` continues to assert the relationship to the value of `ℓ` it was created against.
- A reader who held `ℓ`'s endsets at time `t_1` and revisits at `t_2` obtains the same answer.
- A discovery query that returns `ℓ` as a result is making a claim about `ℓ`'s endsets that remains valid at the time the reader follows the result.

Without L12, none of these holds. Every reader must inspect timestamps, every reference must carry version metadata, every assertion must be qualified by "as of when," every cached result is suspect. The web of permanent references — which is the architectural commitment that makes the docuverse the docuverse — collapses into the same time-conditioned reference web that the design was created to escape.

The dilemma is stark: if links are mutable, references are unreliable; if references are reliable, links are immutable. There is no third path. The composite construction we have defined is the only way to provide user-facing edit semantics without giving up the reliability of references.

## On Identity

We are now in a position to answer a question that has appeared throughout: when a link is "edited," is the result *the same link* or *a different link*?

The address identity is unambiguous: `ℓ_old ≠ ℓ_new` by E2. They are distinct tumblers, the outputs of distinct allocation events, distinct entries in `dom(L)`. Operations that depend on link identity — searching, citing, owning — treat them as separate entities.

The *semantic* relationship is not a property of either link in isolation. It is recorded in a third object, the supersession link `ℓ_sup`, which makes the claim explicit. The claim is in the assertion, not in either of the things asserted about. This is significant: it means the system can accommodate *retractable assertions* without retracting any underlying link. A counter-claim against `ℓ_sup` does not require modifying `ℓ_sup` (it cannot, by L12); it requires only allocating another link asserting the negation.

The architectural slogan: *links are immutable; relationships between links are claims; claims are themselves links.* The whole edifice is built from one primitive (the link) and one structural rule (L12). Edit semantics, supersession, version lineage, counter-claims, retractions — all of these are patterns of link allocation, not new mechanisms.

## Appendix: An Illustrative Reader Procedure

*This section is illustrative, not a verified property of EDITLINK.* It sketches one way a reader might use the structural witnesses E1–E10 establish, but it formalizes no procedure, proves no termination, and verifies no correctness. Several of the concepts it invokes — chains of supersession claims, DAGs of successors, policies for selecting among them, recursion into successors — are explicitly listed in the Open Questions below as deferred to future work. Nothing in this section should be read as a claim of this ASN.

Suppose a reader holds an old reference to `ℓ_old` and wishes to know whether anyone has published a supersession against it. One could imagine a procedure that:

1. Queries `covers(Σ, ℓ_old)` (E7) for the set of links whose endsets reference `ℓ_old`.
2. Filters to those whose type-endset coverage matches a designated supersession address.
3. Reads each candidate's to-endset to obtain a successor address.
4. Optionally recurses on each successor.

What such a procedure should return, whether it terminates, how it should reconcile multiple supersessions of the same source, what policy guides the reader's selection — none of these are settled here. They are sketched only to motivate the design and to indicate that the structural witnesses established by E1–E10 are intended to support such procedures eventually.

## Open Questions

- What invariants must the supersession relation preserve when chains of supersessions form, and under what conditions can such chains contain cycles?
- Must the system guarantee that the supersession-type endset is recognizable to any conforming reader, and if so, by what convention?
- What does it mean abstractly for a supersession claim to be *retracted* or *contradicted*, given that the underlying supersession link is itself permanent?
- Under what guarantees can a reader compute the set of "current" successors of an original link, and how does that computation respond to concurrent additions of further supersession links?
- May a supersession link relate more than two links — for example, asserting that one new link supersedes several old ones jointly, or that one old link splits into several successors?
- What must the system guarantee about the relationship between editing a link and editing the content the link references — should following a link to "edited" content take the reader to the original's endset content or to the successor's?
- How does the abstract identity of an edited link interact with discovery operations that scan link endsets — should both `ℓ_old` and `ℓ_new` be returned when searching for links containing a particular span?

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| E0 | EDITLINK is realized as a composite of two K.λ steps: successor allocation followed by supersession link allocation | introduced |
| E1 | Across EDITLINK, the original link's address persists and its endset value is unchanged | introduced |
| E2 | The successor link's I-address differs from the original's, and the supersession link's I-address differs from both | introduced |
| E3 | The successor's endset sequence may differ arbitrarily from the original's, subject only to L3 | introduced |
| E4 | The post-state contains a link `ℓ_sup` whose first endset references `ℓ_old`, whose second endset references `ℓ_new`, and whose third endset references `τ_sup` via canonical unit-depth spans (a structural witness; semantic identification as a supersession requires an external `τ_sup` convention) | introduced |
| E5 | Multiple independent supersessions of the same original link are admissible; the resulting state contains all of them as distinct first-class facts | introduced |
| E6 | The supersession link's home document need not coincide with the original link's home document; any document owner may publish a supersession claim | introduced |
| E7 | The supersession link's endsets structurally contain `ℓ_old` and `ℓ_new` as covering witnesses, available to any discovery operation that returns links covering a given target | introduced |
| E8 | Any resolution of `ℓ_old`'s endsets after EDITLINK obtains the same value as before EDITLINK | introduced |
| E9 | The supersession link itself is permanent under L12 across all subsequent state transitions | introduced |
| E10 | EDITLINK modifies no arrangement and does not extend `R`; no notification reaches the original owner | introduced |
