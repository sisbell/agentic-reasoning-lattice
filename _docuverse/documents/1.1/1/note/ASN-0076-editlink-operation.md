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

Three values will be needed, of which the first two are produced by allocation and the third is determined by the convention of supersession:

- `ℓ_new` — the I-address of the *successor link*, freshly allocated under `d_new`'s link sub-allocator;
- `ℓ_sup` — the I-address of the *supersession link*, freshly allocated under `d_new`'s link sub-allocator;
- `τ_sup` — a designated tumbler at which the supersession type-endset resolves, a fixed convention of the type registry. Its specific value is outside the scope of this ASN; we require only that it is a stable, identifiable tumbler.

We define:

```
EDITLINK(ℓ_old, (e'_1, ..., e'_N), d_new) ≡
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

## E0 — EditLink as Composite

We claim:

**E0 (EditLinkComposite).** EDITLINK is realized as a sequence of exactly two K.λ steps: the first allocates the successor link `ℓ_new` with the new endset sequence; the second allocates the supersession link `ℓ_sup` whose from- and to-endsets reference `ℓ_old` and `ℓ_new` respectively, and whose type-endset references the designated supersession-type address `τ_sup`.

The composite must be admissible under K.λ's preconditions evaluated at each intermediate state. K.λ requires (i) the target document to be in `E_doc`, (ii) the new link's I-address to lie outside `dom(C) ∪ dom(L)`, (iii) the I-address to satisfy the link allocation discipline (zeros = 3, subspace = s_L, origin = `d_new`, `#E ≥ 2`), and (iv) the endset sequence to satisfy L3. These conditions are independently discharged for the successor step and the supersession step.

We must observe two things about the order. First, the successor step must precede the supersession step *if* we require the supersession endsets to reference an existing link entity; by L4 the supersession step is admissible at any time, but its referent is meaningful only after `ℓ_new ∈ dom(L)`. Second, the steps need not be atomic; any other transitions may occur between them, including failures and resumptions — the composite is well-defined as long as both K.λ applications eventually fire.

## E1 — Original Preservation

The center of the construction is what does *not* happen.

**E1 (OriginalPreservation).** For any state transition `Σ →* Σ'` realizing EDITLINK applied to `ℓ_old`:

```
ℓ_old ∈ dom(Σ'.L)  ∧  Σ'.L(ℓ_old) = Σ.L(ℓ_old)
```

*Proof.* The composite consists of two K.λ steps. K.λ's frame preserves all existing entries in `dom(L)` and adds exactly one new entry. By L12 applied to each step in sequence, every entry present in `dom(Σ.L)` is present and unchanged in the post-state of each K.λ application, and therefore present and unchanged in `dom(Σ'.L)`. Since `ℓ_old ∈ dom(Σ.L)` by the precondition of the composite, the conclusion follows.

This is the central architectural claim. The original link's I-address remains valid; its endsets are bit-for-bit identical to what they were before EDITLINK; its home document and ownership are unchanged. Any property of the system that depended on `Σ.L(ℓ_old)` continues to hold in the post-state, by structural identity of the relevant state component.

## E2 — Successor Distinctness

**E2 (SuccessorDistinctness).** The successor link's I-address differs from the original's:

```
ℓ_new ≠ ℓ_old
```

*Proof.* K.λ's precondition for allocating `ℓ_new` includes `ℓ_new ∉ dom(L) ∪ dom(C)` evaluated at the intermediate state immediately preceding the allocation. By L12 monotonicity and the chain of states leading to that intermediate state, `ℓ_old ∈ dom(L)` at that state. So `ℓ_new ≠ ℓ_old`.

More structurally: L11a (LinkUniqueness) guarantees that distinct T10a-conforming allocation events produce distinct link addresses. The allocation that produced `ℓ_old` and the allocation that produced `ℓ_new` are distinct events (they fire in different states, and L1c's chain-existential admits each independently), so their outputs are distinct addresses. The result is foundational, not contingent on any property of EDITLINK.

The implication is that no operation, applied to no input, can produce two links with the same I-address. A "fresh edit" of `ℓ_old` is necessarily a *new entity* in `dom(L)`, indistinguishable in kind from any other newly-allocated link.

## E3 — Endset Freedom

**E3 (SuccessorEndsetFreedom).** The successor's endset sequence `(e'_1, ..., e'_N)` may differ arbitrarily from `Σ.L(ℓ_old)`, subject only to the structural constraints of L3: `N ≥ 3`, each `e'_i ∈ Endset`, and `e'_3 ≠ ∅`.

*Proof.* K.λ accepts any endset sequence satisfying L3 (the precondition `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : e_i ∈ Endset) ∧ e_3 ≠ ∅`). There is no precondition coupling the new sequence to any prior link's sequence. In particular:

- the new from-endset may name different spans, more spans, fewer spans, or no spans at all;
- the new type-endset may designate a different type;
- the arity itself may differ from `|Σ.L(ℓ_old)|`, subject to the floor of 3.

This is what "edit" means abstractly. The user-facing operation is not parameterized by any "diff" against the original; it produces a fresh link whose endsets are stated whole. The supersession link records that the new is intended as a successor to the old, but the system imposes no resemblance constraint between the two endset sequences.

## The Supersession Relationship

We now examine the second link in the composite — the link that does the work of asserting "the new replaces the old."

A supersession link, in our construction, is a link of arity 3 whose endsets are structured as in the composite definition: from-endset referencing `ℓ_old`, to-endset referencing `ℓ_new`, type-endset designating supersession.

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

The system imposes no exclusivity. Two distinct users, working independently, may each issue an EDITLINK against the same `ℓ_old` and produce two independent successor links and two independent supersession claims. Both claims persist; both are discoverable; no claim is privileged over any other within the link model itself. What it means to "resolve" the ambiguity — which successor is the authoritative one, which lineage to follow — is a reader-side policy decision, outside the scope of the link model.

This stands in sharp contrast to an in-place edit model, in which "the" successor is a singular state component and concurrent edits must be linearized into a single result. Such linearization either forces consensus (centralizing the system) or discards information (losing edits). The append-only construction admits both edits as first-class facts and defers the resolution policy to the reader.

## E6 — Supersession Ownership Freedom

**E6 (SupersessionOwnershipFreedom).** The supersession link's home document `d_new` is not constrained to equal `home(ℓ_old)`.

*Proof.* K.λ's precondition `d_new ∈ E_doc` requires only that the target be a valid document. L1a constrains the allocation site of the new link to be under `d_new`'s prefix — but does not constrain `d_new` itself relative to `home(ℓ_old)`. The supersession link may therefore be allocated under any document the executing party owns.

The consequence is that anyone — not merely the original link's owner — may publish a supersession claim against any link. Bob may assert that his link `ℓ_new` supersedes Alice's `ℓ_old`. By E1, Alice's original is untouched. By E5, Carol may simultaneously assert a *different* supersession against the same `ℓ_old`. The system treats all such assertions as facts of equal structural weight. Their *authority* — whose claim a reader chooses to honor — is a social question, supplied by application-layer trust models, not a structural one decidable from the link store alone.

This is consistent with Nelson's broader posture: claims are visible and attributable. The supersession link's home address indicates who made the claim; readers may use this attribution as part of their resolution policy, but the link model does not.

## E7 — Lineage Discoverability

**E7 (LineageDiscoverability).** The supersession link is discoverable through any link-discovery operation that returns the set of links whose endsets reference a given target address.

We do not formalize the discovery operation in this ASN — that machinery is the proper subject of the link-search specification. We claim only the abstract guarantee: if a discovery operation `find_links(a)` returns `{ℓ ∈ dom(L) : (E (s, w) ∈ Σ.L(ℓ).e_i, i ∈ {1, ..., |Σ.L(ℓ)|} : a ∈ coverage({(s, w)}))}`, then `ℓ_sup` is in `find_links(ℓ_old)` and in `find_links(ℓ_new)`.

The witness is direct. `coverage({(ℓ_old, δ(1, #ℓ_old))}) ⊇ {ℓ_old}` by PrefixSpanCoverage, so `ℓ_old ∈ coverage(Σ.L(ℓ_sup).e_1)`, satisfying the discovery predicate. Symmetric for `ℓ_new`.

This property is what makes the supersession link operative as a record of editing. It is not enough to *create* the supersession link; it must be *findable* from either endpoint. Without bidirectional discoverability, an "edit" would be a write-only act with no path to recover the lineage — exactly the failure mode Nelson decries when he writes that history must be navigable.

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

**E10 (NoImplicitNotification).** EDITLINK modifies neither the arrangements nor the provenance records of any document other than `d_new`:

```
(A d ∈ E_doc \ {d_new} :: Σ'.M(d) = Σ.M(d))
                  ∧  Σ'.R ⊇ Σ.R    (no R-modifications by K.λ itself)
```

*Proof.* Each K.λ step in the composite has frame `(A d :: M'(d) = M(d)) ∧ R' = R`. The composition of two such steps preserves the same frame. K.λ on `d_new` does not even touch `M(d_new)` — placement of the new link in an arrangement, if desired, is a separate K.μ⁺_L step, not part of EDITLINK.

The implication is that `home(ℓ_old)`'s arrangement is not extended with any notification of the edit; the original link's owner receives no automatic push. If the original owner is to *learn* of the edit, it is by issuing a discovery query — the pull model. Nelson endorses this posture explicitly when he describes the docuverse as "what connects here from other documents" being a question the reader (or owner) asks, not a fact pushed at them.

The non-notification property is structural, not optional. The composite as defined here cannot notify the original owner, because K.λ's frame does not admit modifications to `home(ℓ_old)`'s arrangement (which would require K.μ⁺ or K.μ⁺_L on a document other than `d_new`). Adding such a notification step would require either operating on a document the executor does not own (in conflict with allocation discipline) or coordinating with the original owner's system (in conflict with the no-coordination principle). The append-only, no-notification design follows from the underlying architecture.

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

## A Reader's Perspective

Suppose a reader holds an old reference to `ℓ_old` and wishes to know whether anyone has edited it. We sketch the discovery procedure, without formalizing it as part of this ASN:

1. Issue `find_links(ℓ_old)`. Receive the set of all links whose endsets reference `ℓ_old`.
2. Filter to those whose type-endset is `τ_sup`. These are the supersession claims against `ℓ_old`.
3. For each supersession link `ℓ_sup_i`, read its to-endset; this yields a successor candidate `ℓ_new_i`.
4. Optionally recurse: each successor may itself have supersession claims against it.

The reader sees a tree (or DAG) of supersession claims rooted at `ℓ_old`, each leaf representing a current candidate for "the latest version." The reader's policy chooses which leaf to follow — perhaps by attribution, perhaps by recency, perhaps by other application-layer signals. The system supplies the structure; the reader supplies the policy.

This is the abstract content of "editable links" in Nelson's sense. The reader can ask, of any link, "is there a newer version of this?" and receive a structured answer. The asking is pull-based; the answer is non-authoritative (claims, not facts); the resolution is the reader's choice. None of this requires mutation of any link, and all of it is implementable from the primitives we already have.

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
| E2 | The successor link's I-address differs from the original's | introduced |
| E3 | The successor's endset sequence may differ arbitrarily from the original's, subject only to L3 | introduced |
| E4 | The post-state contains a supersession link whose from-endset references the original and whose to-endset references the successor, with the supersession type designator in slot 3 | introduced |
| E5 | Multiple independent supersessions of the same original link are admissible; the resulting state contains all of them as distinct first-class facts | introduced |
| E6 | The supersession link's home document need not coincide with the original link's home document; any document owner may publish a supersession claim | introduced |
| E7 | The supersession link is discoverable from either the original's or the successor's I-address by any discovery operation that returns links containing a given target in their endsets | introduced |
| E8 | Any resolution of `ℓ_old`'s endsets after EDITLINK obtains the same value as before EDITLINK | introduced |
| E9 | The supersession link itself is permanent under L12 across all subsequent state transitions | introduced |
| E10 | EDITLINK does not modify the arrangement of `home(ℓ_old)` or any other document; notification of the original's owner is not automatic | introduced |
