# ASN-0071: FINDDOCSCONTAINING Operation
*2026-05-25*

A reader of a document can ask: *what is in this document?* The answer comes from walking the document's arrangement and resolving each V-position to the content at its I-address — the read-direction.

The same reader can ask the inverse: *what documents contain this content?* This is the search-direction. A scholar tracing a quotation, a system computing royalty for transcluded reuse, a writer enumerating who has cited a passage — each needs to enumerate documents whose arrangements reference some specified material.

We specify what such an operation must do. Following Nelson we call it **FINDDOCSCONTAINING**. The question this ASN answers is: what is its result set? What determines membership, what guarantees govern completeness, and what does the operation deliberately not promise about currency in a permanent address space?

We work within the strand model. State `Σ` carries the content store `Σ.C : T ⇀ Val`, document entities `Σ.E_doc ⊆ Σ.E`, and arrangements `Σ.M(d) : T ⇀ T` for each `d ∈ Σ.E_doc` — partial functions from V-positions to I-addresses satisfying functionality (S2), referential integrity (S3), and content immutability (S0). Sharing is unrestricted: distinct `(d, v)` pairs may map to the same I-address (S5). We assume content has been allocated and arranged through the standard transitions of ASN-0047; we specify only the query, not the operations that produce its inputs.

## The query

Content can be named in two registers. By I-address — "the content at addresses `A`" — purely structural. By V-position with source — "the content of document `d` at positions `σ`" — referenced from where the user encountered it.

We accept the latter. A **vspec** is a pair `(d_s, σ)` where `d_s ∈ Σ.E_doc` names a source document and `σ = (u, ℓ)` is a level-uniform V-span (a span over `T` satisfying `Pos(ℓ)`, `actionPoint(ℓ) ≤ #u`, and `#ℓ = #u`, in the sense of ASN-0053). A **vspec-set** is a finite collection `Q = ⟨q₁, q₂, ..., q_k⟩` of vspecs, possibly drawn from multiple source documents.

Why vspecs and not direct I-addresses? Because users name content from where they encounter it. The reader sees document `d` at position `v`; what they want to find is content equivalent to "what `d` puts at `v`". The I-address is structural, typically unknown to the user, and reachable only by consulting `M(d_s)`. The operation accepts the user's name; resolution to I-addresses is its first task.

## Resolution

For a single vspec `(d_s, σ)`, the resolved I-addresses are those that `d_s`'s current arrangement assigns to positions within the span:

  `iaddrs_one(d_s, σ)(Σ) := { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }`

For a vspec-set `Q`:

  `iaddrs(Q)(Σ) := ⋃_{(d_s, σ) ∈ Q} iaddrs_one(d_s, σ)(Σ)`

By S3, every element of `iaddrs(Q)(Σ)` lies in `dom(Σ.C)` — every resolved address is a valid content address.

A vspec may name positions not currently in `dom(Σ.M(d_s))`. The definition handles this silently: the intersection `⟦σ⟧ ∩ dom(Σ.M(d_s))` drops unresolvable positions, and their absence contributes nothing to `iaddrs`. The query reads charitably — as "find documents containing the content at whatever positions of `σ` are currently bound" — rather than insisting on total resolvability.

This is a substantive choice. An alternative specification could reject the entire query as ill-formed if any position is unresolvable. The charitable reading is justified: a position not in the arrangement names no content, so excluding it from the resolution is the natural extension of "find documents containing the content at these positions". The price is reduced diagnostic information — the user cannot distinguish "no documents contain this" from "this query resolved to no I-addresses".

We note a structural property: `iaddrs_one(d_s, σ)(Σ)` depends only on `Σ.M(d_s)`. Each vspec is *source-anchored* — its meaning is fully determined by the pair `(d_s, σ)` given the state. No global context or caller's view is consulted. The resolution of `Q` is the union of independent per-source resolutions; sources can be consulted independently in any order, by any node holding the relevant arrangement.

## The operation

Given resolved I-addresses, FINDDOCSCONTAINING returns the documents whose arrangements currently reference any of them:

  `find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

The definition is brief. Everything FINDDOCSCONTAINING claims is contained in the predicate `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`. The remainder of this ASN unpacks what that predicate guarantees.

## Completeness and soundness

The membership criterion is a biconditional: a document is in the result iff its current arrangement references at least one resolved I-address.

  `d ∈ find(Q)(Σ)  ⟺  d ∈ Σ.E_doc ∧ ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅`

This bundles two distinct guarantees:

  (⟸) **Completeness.** Every `d` satisfying the predicate is in the result.
  (⟹) **Soundness.** Every `d` in the result satisfies the predicate.

An implementation that omits any qualifying document fails completeness. An implementation that includes a document not satisfying the predicate fails soundness. The specification demands both.

A specific failure mode is worth flagging. An implementation that maintains an auxiliary index — "documents containing I-address `a`" — in an append-only fashion, never removing entries when arrangements are contracted, returns a *superset*. Every truly containing document is included (completeness preserved) but some included documents may no longer contain (soundness violated). Such an implementation realizes `find` as a superset oracle:

  `actual_find(Q)(Σ) ⊆ implementation(Q)(Σ)`

The deviation is observable from the abstract specification — a returned `d` for which `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) = ∅` is a soundness failure. We do not adjudicate whether such relaxation is acceptable in practice; we only note that the abstract specification demands exact correspondence, and any deviation must be flagged as a relaxation against the specification rather than treated as conforming.

## Partial overlap suffices

The predicate uses `≠ ∅`. A single shared I-address — one `a ∈ ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)` — is sufficient for `d`'s inclusion:

  `d ∈ find(Q)(Σ)  ⟺  d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) ∧ a ∈ iaddrs(Q)(Σ) ::)`

The result does not require `d` to reference all of `iaddrs(Q)`; it does not require `d`'s reference to be of any particular extent. A document that transcludes a single sentence from a chapter-length query passage qualifies, alongside documents that transclude the whole.

This is the operative reading of Nelson's "any portion": completeness is over the existence of non-empty intersection, not over inclusion of the whole. The asymmetry matters — a query about a large passage may discover documents that each reference only a tiny fragment of it. The result set has no inherent measure of "how much" each returned document contains; to recover an extent measure, the requester must compute `|ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)|` for each returned `d` separately.

## Set semantics

`find(Q)(Σ)` is a set. Each document appears at most once regardless of how many I-addresses it shares with `iaddrs(Q)`:

  for every `d_* ∈ Σ.E_doc`:   `|{ x ∈ find(Q)(Σ) : x = d_* }| ≤ 1`

A document that transcludes ten distinct passages from a queried chapter is reported once, not ten times. The result enumerates documents, not occurrences. To recover occurrence counts, the requester must separately compute the cardinality of `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)` for each returned `d`.

Set semantics must be stated explicitly because the natural implementation — iterating over each queried I-address and collecting source documents — produces duplicates by default. The specification requires deduplication; an implementation that returns a multiset of `(d, a)` pairs satisfies neither the type signature nor the intent.

## Discovery through sharing

The most architecturally significant consequence concerns transclusion. If I-address `a` is referenced by multiple documents — `a ∈ ran(Σ.M(d))` for several `d` — then a query that resolves to `a` discovers all of them:

  `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc  ⟹  d ∈ find(Q)(Σ)`

In particular: `a`'s home document (`origin(a)`, per S7 — if it itself still references `a`) and every transcluding document are discovered by the same query and reported as equally-qualifying members of the result.

The find operation does not distinguish home from transcluding document. Both reference `a`; both satisfy the predicate. The mechanism is structural — the I-address `a` is the same `a` everywhere it appears, because content has permanent identity (S0). Sharing of content corresponds to identity of I-address; identity of I-address is what `find` tests for.

This makes `find` the structural dual of the read-direction. Reading goes from arrangement to content: given `d`, `M(d)` tells which I-addresses `d` references. Finding goes from content to arrangement: given resolved I-addresses, `find` tells which documents reference them. The two operations are duals over the same `M : E_doc → (T ⇀ T)` structure.

The result does not, on its own, distinguish *how* each reported document references the content — native authorship versus transclusion. This distinction is recoverable from the address structure already returned. For each `a ∈ iaddrs(Q)`, `origin(a)` (a function of `a`'s tumbler alone — S7) names `a`'s home document. Comparing `origin(a)` against each `d ∈ find(Q)` recovers the relationship: `d = origin(a)` means `d` authored `a`; `d ≠ origin(a)` means `d` transcludes `a`. The `find` operation does not need to tag its results because tagging is a function the requester can compute from the data.

## Currency: state dependence

`find(Q)(Σ)` is a function of `Σ`. It depends only on the current state — specifically on `Σ.E_doc` and `Σ.M` (and through `M`'s range, on `dom(Σ.C)` via S3):

  `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d))  ⟹  find(Q)(Σ) = find(Q)(Σ')`

History does not enter the definition. The operation does not consult past states, past arrangements, or past transitions. It is a pure function of the present.

This is what Nelson's "containing" (present participle) commits to. The predicate is evaluated at the moment of query, not over the lifetime of the docuverse. A document whose arrangement once referenced `a` but has since been contracted (via K.μ⁻ from ASN-0047) is not in `find(Q)` even if it once was. The operation reports current containment, full stop.

The completeness claim of section 4 must be read in this light. Completeness is over the *currently-containing* set, not over the historically-containing set. An implementation that misses a currently-containing document violates completeness; one that omits a historically-containing-but-no-longer-current document does not. The two semantics are distinct, and the operation commits to the present-tense reading.

## Permanence and currency reconciled

The strand model retains entities permanently (P1: `Σ.E ⊆ Σ'.E`) and content permanently (P0: `dom(Σ.C) ⊆ dom(Σ'.C)`), but arrangements may shrink. So at first inspection, a document whose arrangement contracted away a reference to `a` appears to "lose" that historical containment from `find`'s perspective irrecoverably — a structural tension between permanence (of content and entities) and currency (of containment).

The reconciliation runs through versioning. When a document is to be modified, the design convention is to derive a new version-document — a fresh entity in `E_doc` whose arrangement is initialized from the original via transclusion — and modify the new version, leaving the original arrangement intact. Because P1 preserves the original document in `E_doc` and no transition is applied to `M(d_original)`, the original remains a present document whose present arrangement still references `a`. `find(Q)(Σ)` still discovers the original under its own tumbler address, distinct from the modified version.

But this reconciliation is convention, not a structural guarantee of the strand model. Nothing prevents direct modification of any document via arrangement contraction — and such direct modification erases the historical reference irrecoverably from `find`'s perspective. The operation knows only current arrangements; it has no memory of past ones.

Two consequences follow:

(i) Historical state queries succeed insofar as historical states persist as their own document-entities. If version `V₁` of document family `D` contained passage `a`, and version `V₂` deleted `a`, then a query resolving to `a` reports `V₁` (which still contains `a`) and excludes `V₂` (which does not). Both are documents in `E_doc`, addressed by distinct tumblers. The model treats them as equally first-class — there is no privileged "current" version, only a set of co-existing version-documents each with its own arrangement.

(ii) Recovering "what documents EVER contained this" — the full historical containment relation — requires a separate mechanism. ASN-0047's provenance relation `R` tracks exactly this: `(a, d) ∈ R` records that `d`'s arrangement once contained `a` in the content subspace, and P2 makes `R` permanent. `find(Q)` does not consult `R`. The two operations have different semantics: `find` returns currently-containing documents; an `R`-based query returns ever-containing documents. They coincide exactly when no arrangement contraction has occurred for any document containing the queried I-addresses; they may differ otherwise.

The completeness guarantee of `find` is over *currency*. The completeness guarantee of `R` is over *history*. An operation must commit to one semantic. FINDDOCSCONTAINING, as Nelson specifies it and as we have specified it here, commits to currency.

## Finiteness

  `|find(Q)(Σ)| < ∞`

At any reachable state, `Σ.E_doc` is finite — it grows by one with each K.δ document-creation event, and there have been finitely many transitions from `Σ₀`. `find(Q)(Σ) ⊆ Σ.E_doc` is therefore finite.

This is worth stating because `iaddrs(Q)` may name content that is widely transcluded — a single popular passage could appear in many documents. The result is bounded only by `E_doc` itself. The operation does not promise a small result, only a finite one. Implementations that must materialize the entire result before returning it should be designed expecting that the result can grow with the docuverse.

## What we do not specify

The returned set has presentation and policy properties we have left unspecified. These are not entailed by the abstract operation, and an implementation may add them without conflicting with the specification, provided the unfiltered semantics remain available.

(i) *Order.* `find(Q)(Σ)` is a set. Some implementations may return its elements in a deterministic order (such as ascending tumbler order on document ISA, naturally arising from a sorted index); others may not. Order is a presentation choice. Two implementations both meeting the specification may return the same elements in different orders, and neither violates the specification by virtue of order alone.

(ii) *Replica freshness.* We have specified `find` as a function of "the" state `Σ`. In a distributed deployment, different nodes may hold different views, and "the current state" is replica-dependent. We have not addressed replication consistency. The specification holds within a single-state perspective; extending it to distributed deployments requires additional commitments about consistency model that lie outside the scope of `find`'s definition.

(iii) *Access-control filtering.* The `find` we specified returns ALL containing documents — public, private, and inaccessible-to-requester alike. Nelson's broader design intent (LM 2/59) is that private documents not visible to the requester should not appear in the result. Whether and how to enforce this is a separable concern: implement `find` as specified, then post-filter against the requester's visibility set. The unfiltered `find` is the abstract basis; filtering is a policy layer overlaid on it.

These omissions are deliberate. They distinguish what FINDDOCSCONTAINING fundamentally is from what specific deployments may add around it. Each is properly the subject of a separate specification.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| F-iaddrs | `iaddrs : VSpecSet × Σ → P(dom(C))` with `iaddrs(Q)(Σ) = ⋃_{(d_s, σ) ∈ Q} { Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s)) }` | introduced |
| F-find | `find : VSpecSet × Σ → P(E_doc)` with `find(Q)(Σ) = { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }` | introduced |
| F-COMP | Completeness: every `d ∈ Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` is in `find(Q)(Σ)` | introduced |
| F-SOUND | Soundness: every `d ∈ find(Q)(Σ)` is in `Σ.E_doc` with `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅` | introduced |
| F-PART | Partial overlap suffices: `d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) ∧ a ∈ iaddrs(Q)(Σ) ::)` | introduced |
| F-DIST | `find(Q)(Σ)` is a set; each `d ∈ E_doc` appears at most once | introduced |
| F-SHARE | Cross-document discovery: `a ∈ iaddrs(Q)(Σ) ∧ a ∈ ran(Σ.M(d)) ∧ d ∈ Σ.E_doc ⟹ d ∈ find(Q)(Σ)` | introduced |
| F-CUR | State dependence: `(Σ.E_doc = Σ'.E_doc) ∧ (A d ∈ Σ.E_doc : Σ.M(d) = Σ'.M(d)) ⟹ find(Q)(Σ) = find(Q)(Σ')` | introduced |
| F-FILT | Silent resolution filtering: positions in `⟦σ⟧ \ dom(Σ.M(d_s))` contribute no I-addresses to `iaddrs(Q)(Σ)` | introduced |
| F-LOC | Source locality: `(A Σ, Σ' : Σ.M(d_s) = Σ'.M(d_s) ⟹ iaddrs_one(d_s, σ)(Σ) = iaddrs_one(d_s, σ)(Σ'))` | introduced |
| F-FIN | `|find(Q)(Σ)| < ∞` at every reachable state | introduced |

## Open Questions

What relationship between FINDDOCSCONTAINING's current-state result and the historical containment relation `R` must the system guarantee?

Under what conditions must the system reject unresolvable vspec positions rather than silently filter them?

What completeness must FINDDOCSCONTAINING guarantee when the docuverse state is distributed across replicas with possibly divergent views?

What abstract operation must filter FINDDOCSCONTAINING's result by requester visibility?

What completeness must visibility-filtering preserve over the visible subset of documents accessible to the requester?

What invariant must connect FINDDOCSCONTAINING's result immediately before and after a transition that contracts an arrangement?
