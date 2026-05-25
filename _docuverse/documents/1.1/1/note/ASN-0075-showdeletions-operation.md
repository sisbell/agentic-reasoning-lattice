# ASN-0075: SHOWDELETIONS Operation

*2026-05-25*

Nelson lists "show deletions" among the operations the system must provide (LM 4/79). The intuition is direct: given two documents that share content history, identify the content that was present in one but is absent from the other. We approach this abstractly. We do not specify how documents come to share history, nor how content is removed from an arrangement — those mechanics belong elsewhere. We specify only what the operation must produce, what guarantees it must offer over its output, and what state it consults.

The central difficulty is that two situations are observationally indistinguishable without further information: content `a` may be absent from document `d`'s arrangement because `d` once contained `a` and removed it (it was *deleted*), or because `d` was never an arrangement that contained `a` (it was *never included*). A "show deletions" operation must distinguish these. We will show that the provenance relation `R` introduced in the transition model supplies exactly the information required, and that any conforming implementation must therefore maintain such a relation — without it, deletion is not detectable as a kind separate from prior absence.

## Foundation Recap

We take from the foundation:

- **Content store** `Σ.C : T ⇀ Val` (ASN-0036, S0): a partial function from tumblers to content values, append-only with immutable values across transitions.
- **Arrangement** `Σ.M(d) : T ⇀ T` (ASN-0036, S2, S3, S8a, S8-depth): a per-document partial function from V-positions to I-addresses.
- **Entity set** `Σ.E ⊆ T` and its document partition `Σ.E_doc` (ASN-0047).
- **Provenance relation** `Σ.R ⊆ T × E_doc` (ASN-0047): `(a, d) ∈ R` iff document `d` has, at some point in the system's history, contained I-address `a` in its content-subspace arrangement.
- **Provenance permanence** `R ⊆ R'` across transitions (P2, ASN-0047): once `(a, d) ∈ R`, it remains so.
- **Provenance bounds** `Contains_C(Σ) ⊆ R` (P4★, ASN-0047): if `a` is currently in `d`'s content-subspace arrangement, then `(a, d) ∈ R`.
- **Historical fidelity** (P4a, ASN-0047): if `(a, d) ∈ R`, some prior reachable state had `a` in `d`'s content-subspace arrangement.
- **Provenance grounding** `R ⊆ dom(C) × E_doc` (P7, ASN-0047): every provenance pair references content that exists.
- **Origin function** `origin(a)` (ASN-0036, S7): every `a ∈ dom(C)` has a uniquely determined originating document, invariant across states.
- **Subspace projection** `subspace_I(a)` (ASN-0036, S7c): identifies the content (`s_C`) or link (`s_L`) subspace of an I-address.
- **Subspace convention** `s_C = 1, s_L = 2` (ASN-0047, SubspaceConventionAxiom).
- **Link subspace ownership** (CL-OWN, ASN-0047): link-subspace V-positions of `d` map only to link I-addresses with `origin = d`.

We restrict attention to the content subspace throughout. The justification appears in §D-SUBSP.

## The Three States of Content

We classify each pair `(a, d)` with `a ∈ dom(C)`, `subspace_I(a) = s_C`, and `d ∈ E_doc` into one of three states:

```
CURRENT(a, d)         ≡  a ∈ ran(M(d))
DELETED(a, d)         ≡  (a, d) ∈ R  ∧  a ∉ ran(M(d))
NEVER_INCLUDED(a, d)  ≡  (a, d) ∉ R
```

We must show these are exhaustive and mutually exclusive — otherwise the operation's outputs would have undefined classifications.

**Lemma D-EXH (Three-State Exhaustion).** For every `(a, d)` with `a ∈ dom(C)`, `subspace_I(a) = s_C`, and `d ∈ E_doc`, exactly one of `CURRENT(a, d)`, `DELETED(a, d)`, `NEVER_INCLUDED(a, d)` holds.

*Proof.* The three predicates correspond to three of the four cases of the cross-product `(a ∈ ran(M(d))) × ((a, d) ∈ R)`:

| `a ∈ ran(M(d))` | `(a, d) ∈ R` | Predicate |
|---|---|---|
| Yes | Yes | CURRENT |
| Yes | No | impossible |
| No  | Yes | DELETED |
| No  | No  | NEVER_INCLUDED |

The "impossible" row is excluded by P4★: if `a ∈ ran(M(d))` and `subspace_I(a) = s_C`, then `(a, d) ∈ Contains_C(Σ) ⊆ R`, contradicting `(a, d) ∉ R`. The remaining three rows are mutually exclusive and exhaustive. ∎

## Why the Provenance Relation Is Load-Bearing

We now show that the state components `(C, M)` alone are insufficient to support SHOWDELETIONS — any conforming implementation must maintain state information equivalent to `R`.

**Lemma D-DISCR (Discrimination Requires Provenance).** No function computable from `(Σ.C, Σ.M)` alone can distinguish `DELETED(a, d)` from `NEVER_INCLUDED(a, d)` for arbitrary `(a, d)`.

*Argument.* We exhibit two reachable states `Σ_k` and `Σ'_k` for which `(Σ.C, Σ.M)` agree but `DELETED` and `NEVER_INCLUDED` disagree.

Consider two transition histories. In the first, document `d` is created, content `a` is inserted into its arrangement, then `a` is removed. The final state `Σ_k` has `a ∈ dom(C)`, `a ∉ ran(M_k(d))`, and `(a, d) ∈ R_k` (because `a` was once in `d`'s arrangement, and P2 preserves this). So `DELETED(a, d)` holds at `Σ_k`.

In the second, document `d` is created and `a` is inserted into the arrangement of *some other document `d'`*, never into `d`. The final state `Σ'_k` has `a ∈ dom(C)`, `a ∉ ran(M'_k(d))`, and `(a, d) ∉ R'_k`. So `NEVER_INCLUDED(a, d)` holds at `Σ'_k`.

By choice of operations, `Σ.C_k = Σ.C'_k` (both contain `a`) and `Σ.M_k(d) = Σ.M'_k(d) = ∅`. Any function `f(C, M)` returns the same value at both states. But the classifications differ — so `f` cannot be a discriminating predicate. ∎

This is the abstract justification for the provenance relation: without `R` (or any informationally equivalent component), the system cannot tell "this content was lost" from "this content was never here." The "show deletions" operation requires the former interpretation; therefore any system supporting it must maintain `R`.

## The SHOWDELETIONS Operation

Let `d_A, d_B ∈ E_doc`. The operation takes two documents and observes the state. We define the asymmetric output sets:

```
DeletedFromAWithB(d_A, d_B)
   =  {a ∈ dom(C) :
         subspace_I(a) = s_C
       ∧ DELETED(a, d_A)
       ∧ CURRENT(a, d_B)}

DeletedFromBWithA(d_A, d_B)
   =  {a ∈ dom(C) :
         subspace_I(a) = s_C
       ∧ DELETED(a, d_B)
       ∧ CURRENT(a, d_A)}
```

Each asymmetric set captures content deleted from one document and still arranged in the other. The presence of the "witness" document (where the content remains current) is what makes the deletion observable as recoverable: every `a` in `DeletedFromAWithB` is reachable through `d_B`'s current view, and the reverse holds symmetrically.

**Definition (SHOWDELETIONS).** The operation is the ordered pair:

```
SHOWDELETIONS(d_A, d_B)
   =  (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))
```

The two halves are necessarily disjoint: by D-EXH, no `a` can simultaneously satisfy `DELETED(a, d_A)` and `CURRENT(a, d_A)`, so an address `a` in `DeletedFromAWithB` cannot be in `DeletedFromBWithA` (the former requires `CURRENT(a, d_B)`, the latter `DELETED(a, d_B)`).

The operation's precondition is `d_A ∈ E_doc ∧ d_B ∈ E_doc`. Its postcondition characterises the result set-theoretically. We capture this in wp form. Let `q` abbreviate the predicate:

```
Result = (DeletedFromAWithB(Σ, d_A, d_B), DeletedFromBWithA(Σ, d_A, d_B))
```

Then `wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc)`. The operation always terminates with `q` true when its precondition holds.

## Distinguishing Deletions from Additions

A naive set-difference of current ranges — `ran(M(d_A)) \ ran(M(d_B))` — would conflate two distinct phenomena: content `d_A` had that `d_B` deleted, and content `d_A` acquired (e.g., through insertion or transclusion) that `d_B` never received. The "show deletions" name and intent target only the former.

Our definition forces the disambiguation by requiring `(a, d_A) ∈ R` for content reported as deleted-from-A. This says: `a` must have been in `d_A`'s arrangement at some point. Content that was only ever in `d_B`'s arrangement satisfies `NEVER_INCLUDED(a, d_A)` rather than `DELETED(a, d_A)`, and is correctly excluded from the deletion report.

The same set-theoretic difference computed without `R` would mislabel additions as deletions. The provenance-aware definition above is therefore not optional — it is what makes the operation deliver on its name.

## Restriction to the Content Subspace

The condition `subspace_I(a) = s_C` is essential.

**Claim D-SUBSP.** SHOWDELETIONS operates only over the content subspace (`s_C`).

*Justification.* Content-subspace addresses can be shared between documents because the system permits one document's content arrangement to map V-positions to I-addresses allocated by another document — content identity transcends document boundaries within the content subspace.

The link subspace differs structurally. By CL-OWN (ASN-0047), if `subspace(v) = s_L` and `M(d)(v) = a`, then `origin(a) = d`: a document's link-subspace V-positions reference only its own link addresses. There is no inheritance of link content across documents in the way that there is for content. So "cross-document deletion of link material" is not a well-formed comparison — each document's link-subspace material is its own, and no comparison document holds it as witness.

Restricting SHOWDELETIONS to the content subspace is therefore not an implementation simplification but a structural necessity. The link subspace requires a separate (and per-document, not cross-document) analysis.

## Identity Preservation

**Claim D-IDENT.** For every `a` in either output set, the returned reference is precisely the I-address `a` — not a copy with new identity.

*Justification.* The output sets are defined as subsets of `dom(C)`. Each element is an existing I-address. We return addresses, not values.

The architectural significance is foundational. An operation that recovers content using these references dereferences existing entries in `C`; it does not allocate new ones. Three guarantees that depend on persistent I-address identity therefore survive recovery:

- *Link survival.* By foundation invariants on link endsets, links attach to I-addresses. If `a` is in `dom(L)`'s endsets, the link continues to resolve to the same `a` regardless of which arrangements currently expose `a`.
- *Transclusion integrity.* If another document's arrangement maps a V-position to `a`, that mapping continues to reference the same content; no aliasing or shadow copy is introduced.
- *Origin attribution.* `origin(a)` continues to identify the original allocator of `a`; the chain of provenance is not severed by recovery.

If SHOWDELETIONS returned new identities — fresh I-addresses with the same byte values — all three guarantees would collapse. The recovered content would be unaddressable by existing links, would not match existing transclusions, and would have spurious new origin. Returning addresses is therefore not a presentation choice; it is a correctness requirement.

## Origin Traceability

**Claim D-ORIG.** For every `a` in either output set, `origin(a)` is determined and identifies a unique document — the originating allocator of `a`.

*Justification.* By S7 (ASN-0036), `origin(a)` is defined for every `a ∈ dom(C)` and is invariant across all states in which `a ∈ dom(C)`. The output sets are subsets of `dom(C)`, so `origin` is well-defined on every output element.

The user-facing meaning: any returned address self-identifies its home document. When `d_A` and `d_B` were derived from a common ancestor `d_C`, content inherited from `d_C` and later deleted from `d_A` carries `origin(a) = d_C`. Content originally allocated by some other document and transcluded into `d_A` before deletion carries that other document's address as origin. The output need carry no extra "origin annotation" beyond the address itself — origin is derived structurally from the address.

This matters operationally because it scopes recovery rights and accounting. The originating document is recoverable from the address; recovery operations can verify permissions against `origin`; royalty or attribution mechanisms have the data they need.

## Order Preservation

**Claim D-ORD.** If the output is presented as an ordered sequence, the order is consistent with the witness document's V-position ordering of the referenced addresses.

For `DeletedFromAWithB(d_A, d_B)`, define `vpos_B(a)` as the unique (by S2) V-position satisfying `M(d_B)(vpos_B(a)) = a` for `a ∈ ran(M(d_B))`. The output is ordered such that for any `a, a'` with `vpos_B(a) < vpos_B(a')` under T1 (ASN-0034), `a` precedes `a'` in the presentation. Symmetrically for `DeletedFromBWithA` using `vpos_A`.

*Justification.* Deleted content has no V-position in the document from which it was deleted: V-position information is local to a current arrangement and is not preserved by `R`. So the deleted document's "original ordering" of the content is not observable in the current state — it was a property of an arrangement no longer present. The only observable V-ordering is the witness document's. Choosing the witness order for presentation is the only choice that uses observable data.

We note explicitly what is *not* claimed: the order in which `a` appeared in `d_A` before deletion is *not* recoverable. A user who needs to act on the content reads it in the witness's order — which is convenient, because that is also the order in which it appears when accessed through the witness.

## Symmetry

**Claim D-SYM.** Argument swap maps each output half into the other:

```
SHOWDELETIONS(d_A, d_B)  =  (X, Y)
SHOWDELETIONS(d_B, d_A)  =  (Y, X)
```

where `X = DeletedFromAWithB(d_A, d_B)` and `Y = DeletedFromBWithA(d_A, d_B)`.

*Justification.* By name-substitution in the definitions: `DeletedFromAWithB(d_B, d_A)` reads as "addresses with `DELETED(a, d_B) ∧ CURRENT(a, d_A)`," which is exactly `DeletedFromBWithA(d_A, d_B)`. Likewise the other half.

The content-level guarantee — the union of both halves as a set of I-addresses — is therefore symmetric in the operands. The presentation labelling (which half is "from A" vs. "from B") swaps accordingly. This matches the design intent that correspondence between documents is a structural fact about shared content and not an asymmetric query over arguments.

## Actionability

**Claim D-ACT.** The output is in a form usable as input to any operation that consumes I-addresses to produce arrangement extensions.

*Justification.* Each output element is an I-address in `dom(C)`. Any operation whose input type accepts I-addresses (or spans thereof) can consume the output directly. The output is *not* wrapped in V-position structure — wrapping it that way would require either fictitious positions (deleted content has no V-position in the queried document) or borrowed positions from the witness (which would have to be coordinated with the recovery target's address space, an entanglement the abstract output cannot impose). The output is *not* wrapped in content values — wrapping it that way would require copying values into new identities, breaking D-IDENT.

The natural compact form is therefore a set of I-spans, each tagged with the originating document so that contiguous runs sharing the same origin can be grouped. Formally, drawing on the span and bundle algebras:

A *deletion witness run* is a triple `(i_start, ℓ, origin)` such that, using the OrdinalShift of ASN-0034:

- every address in `{i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)}` belongs to the deletion set;
- every such address satisfies `origin(a) = origin`;
- no contiguous extension to the left or right is also in the deletion set with the same origin.

By construction (and using the canonical-decomposition results of ASN-0058, M11–M12, applied to the witness's arrangement restricted to the deletion set), the deletion set decomposes uniquely into a finite collection of maximal witness runs. The collection can be enumerated, transmitted, and consumed without information loss.

We emphasise: this presentation is a *form*, not a *fundamental commitment*. The abstract specification fixes only the set of I-addresses. The run-grouping presentation is a useful packaging that preserves identity (every position is its original I-address) and origin (every address shares the named origin), making the output efficient to transmit while remaining compositional.

## Observational Frame

**Claim D-OBS.** SHOWDELETIONS does not modify any state component.

Formally, for state `Σ = (C, L, E, M, R)` and the state `Σ'` obtaining after the operation:

```
Σ'.C  =  Σ.C
Σ'.L  =  Σ.L
Σ'.E  =  Σ.E
Σ'.R  =  Σ.R
(A d ∈ E_doc ::  Σ'.M(d) = Σ.M(d))
```

The operation reads `M(d_A)`, `M(d_B)`, and `R`; it computes the output sets; it returns them. No transition relation is invoked.

Consequences: SHOWDELETIONS is repeatable on the same state (yields identical results); it commutes with other observational queries; and a later invocation after intervening state changes correctly reflects the new state.

## Output Need Not Be Stored

**Claim D-STORE.** The output is not required to be stored as a document or otherwise integrated into the persistent content store.

*Justification (negative claim).* SHOWDELETIONS is observational (D-OBS); its result is delivered to the caller. The caller may inspect, transform, retain, or discard the result. The system does not, of its own accord, create a new document or other persistent artefact to hold the result.

If a user wishes to capture a particular SHOWDELETIONS result for sharing or future reference, they have separate mechanisms for doing so: they may compose a new document whose arrangement transcludes the recovered I-spans (using D-IDENT's identity preservation), or they may establish correspondence assertions between the two compared documents. These captures are user actions, not built-in obligations of SHOWDELETIONS.

The justification for keeping the operation observational rather than constructive: SHOWDELETIONS is a function of state (D-RECONS below). Functions can be recomputed from their inputs whenever needed. Storing the result would buy persistence at the cost of staleness — any subsequent state change makes a stored result potentially out of date. The system is more flexible with observation than with creation.

## State-Functional Independence

**Claim D-RECONS.** The output depends only on the current state `Σ`. It does not depend on the particular sequence of transitions by which `Σ` was reached.

*Justification.* Each predicate `CURRENT`, `DELETED`, `NEVER_INCLUDED` is defined in terms of components of `Σ` only (`M`, `R`, `dom(C)`, `subspace_I`). The output sets are characterised entirely by these projections. Two distinct transition histories yielding the same `Σ` therefore yield identical SHOWDELETIONS outputs.

This is what makes the operation an honest function of state. The user need not know how the system arrived at its current configuration; consulting the current configuration suffices. P4a (historical fidelity, ASN-0047) ensures that whenever the operation reports `DELETED(a, d)`, there really was a past state where `a` was in `d`'s arrangement — but the *route* to that past state is irrelevant to the report itself.

## Edge Cases

*Documents with no shared content.* If for every `a ∈ dom(C)`, `¬((a, d_A) ∈ R ∧ a ∈ ran(M(d_B)))` and `¬((a, d_B) ∈ R ∧ a ∈ ran(M(d_A)))`, then no address satisfies either asymmetric definition. Both output halves are empty. The operation succeeds and reports no deletions — correctly so, because the documents have no shared content history through which one could witness deletions in the other.

*Both arrangements empty.* If `dom(M(d_A)) = dom(M(d_B)) = ∅`, then `ran(M(d_A)) = ran(M(d_B)) = ∅`, so `CURRENT` fails for every `a` on both sides. Both halves are empty.

*Same document compared against itself.* If `d_A = d_B`, then for each `a`, `DELETED(a, d_A) ∧ CURRENT(a, d_A)` is contradictory (by D-EXH). Both halves are empty. The operation is well-defined and trivially yields the empty pair.

*Asymmetric population.* If `d_A` has rich history (large `R`-projection) but its current arrangement is empty, while `d_B`'s arrangement currently holds many of the addresses `d_A` historically held, then `DeletedFromAWithB` may be large and `DeletedFromBWithA` may be empty. The asymmetry of the two halves directly mirrors the asymmetry of the editing histories.

## Composability with Restoration

While we do not specify any restoration operation here, we note that the output's form makes restoration *possible*. The output is a set of I-addresses in `dom(C)`, each carrying determinate origin (D-ORIG) and preserving identity (D-IDENT). A restoration operation consuming a subset of these addresses can extend a target document's arrangement to include them at fresh V-positions, with `origin` and link-resolvability preserved because no new identities are introduced.

The user-facing meaning: a "show deletions" query feeds naturally into a "bring back this part" follow-up, with no loss of identity in the round trip. That is what makes the operation more than diagnostic.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CURRENT | `CURRENT(a, d) ≡ a ∈ ran(M(d))` | introduced |
| DELETED | `DELETED(a, d) ≡ (a, d) ∈ R ∧ a ∉ ran(M(d))` | introduced |
| NEVER_INCLUDED | `NEVER_INCLUDED(a, d) ≡ (a, d) ∉ R` | introduced |
| D-EXH | For every `(a, d)` with `a ∈ dom(C)`, `subspace_I(a) = s_C`, `d ∈ E_doc`, exactly one of CURRENT, DELETED, NEVER_INCLUDED holds | introduced |
| D-DISCR | No function of `(C, M)` alone can distinguish DELETED from NEVER_INCLUDED; any system supporting SHOWDELETIONS must maintain a state component informationally equivalent to R | introduced |
| DeletedFromAWithB | `{a ∈ dom(C) : subspace_I(a) = s_C ∧ DELETED(a, d_A) ∧ CURRENT(a, d_B)}` | introduced |
| DeletedFromBWithA | Symmetric counterpart of DeletedFromAWithB | introduced |
| SHOWDELETIONS | Observational operation `SHOWDELETIONS(d_A, d_B) = (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))` | introduced |
| D-SUBSP | The operation restricts to the content subspace `s_C`; cross-document deletion comparison is structurally meaningful only there | introduced |
| D-IDENT | Output references are I-addresses themselves; no copies, no new identities | introduced |
| D-ORIG | Every output element `a` has determinate `origin(a)` | introduced |
| D-ORD | Output presentation, when ordered, is consistent with the witness document's V-position ordering | introduced |
| D-SYM | `SHOWDELETIONS(d_B, d_A)` is the component-swapped pair of `SHOWDELETIONS(d_A, d_B)` | introduced |
| D-ACT | Output is in a form consumable by I-address-based operations; deletion witness runs `(i_start, ℓ, origin)` are the natural compact form | introduced |
| D-OBS | SHOWDELETIONS modifies no state component; it is purely observational | introduced |
| D-STORE | The output is not required to be stored as a document; it is a query result | introduced |
| D-RECONS | The output depends only on the current state, not on transition history | introduced |
| DeletionWitnessRun | Triple `(i_start, ℓ, origin)` denoting a maximal contiguous I-address run in the deletion set sharing one originating document | introduced |

## Open Questions

What abstract characterisation of "shared content history" between two documents, expressed solely in terms of R, predicts when SHOWDELETIONS will yield non-empty results?

When deleted content has been removed from every document that ever contained it, through what state component does the system still retain the option to expose it for query or recovery?

What invariants must hold over the evolution of R to ensure that DELETED is monotone — once classified DELETED, always classified DELETED unless content is re-introduced into the document's arrangement?

How should SHOWDELETIONS report content that was deleted from both compared documents but remains current in a third document not in the pair?

If the system supports concurrent state transitions, what consistency model must SHOWDELETIONS observe to deliver coherent joint snapshots of M and R?

How does SHOWDELETIONS generalise to families of more than two documents, and what witness-structure replaces the binary asymmetric pair?

Under what conditions on the witness arrangement does the deletion set admit a finite presentation as a union of contiguous I-address spans, and when must it enumerate addresses singly?

What guarantees must the witness's V-order satisfy to ensure that presentation-ordered output of SHOWDELETIONS corresponds to a user-meaningful reading sequence rather than a structural accident?

Should the system distinguish content "deleted with a witness in a prior arrangement of the same document" from "deleted with a witness in a sibling document," and what additional structure would that distinction require?
