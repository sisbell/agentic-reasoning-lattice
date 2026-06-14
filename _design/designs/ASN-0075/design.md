# Design Digest — ASN-0075: SHOWDELETIONS

## What this is

SHOWDELETIONS is a read-only, two-document query that reports the content each document deleted while the other still holds it. It is the first operation that makes the provenance relation `R` *load-bearing* — the note's central result is that this capability cannot be built from the four foundation state components `(C, L, E, M)` alone.

## Design commitments

The load-bearing decisions this note locks in:

- **Deletion is a three-way classification, not a set-difference.** Every (content-address, document) pair is exactly one of CURRENT / DELETED / NEVER_INCLUDED. **Forced** (D-DISCR, with proof): a naive `ran(M(d_B)) \ ran(M(d_A))` conflates content `d_A` once held and deleted with content `d_B` merely acquired — it is provably wrong. The DELETED vs. NEVER_INCLUDED distinction *must* consult provenance.
- **The system must carry durable state beyond `(C, L, E, M)`.** **Forced** (D-NEED): `R` suffices, and reusing the provenance relation rather than introducing a fresh component is the cheapest mechanism that meets the contract. This is the constraint of the whole note: any conforming substrate must persist a provenance record that *survives removal from arrangements*.
- **Provenance is monotone and permanent** (`R ⊆ R'`, P2). Deletion never retracts provenance; that permanence is exactly what keeps DELETED detectable forever. Inherited from ASN-0047, but this note depends on it absolutely — it forbids ever garbage-collecting `R`.
- **Classification is at I-address-set granularity.** **Forced** by the predicate definitions: only `a ∈ ran(M(d))` is read, never V-position multiplicity. Per-occurrence removal is invisible while any occurrence of `a` survives — explicitly scoped out as a Vstream concern.
- **The contract is purely observational and state-functional.** **Forced** (D-OBS, D-STORE, D-RECONS): writes nothing, persists no artifact, depends only on current state not on history. Deterministic and repeatable per state.
- **Output is existing I-addresses, not copies or values.** **Forced** (D-IDENT, D-ORIG): identity preserved by reference, origin derivable from the address. Not merely conventional — it is what lets the report feed an identity-preserving restoration.
- **Two directional halves are meaningful; the A/B labelling is convention.** That a document *lost* content (vs. its partner) is real directional information; *which* half is named "A" is purely operand-order convention (D-SYM). The content-level guarantee is the symmetric union.
- **Meaning is licensed only at a composite boundary.** Computing the answer needs only finiteness, but *trusting* it (three-state exhaustion, D-EXH; the witness lemma, D-WIT) requires the boundary where `R` and `M` are mutually coupled (P4★).

## What must be built

- **An arrangement-range membership test** (CURRENT): given `(a, d)`, decide whether `a` is referenced anywhere in `d`'s current arrangement — the *set* of distinct content-addresses, multiplicity discarded.
- **A per-document provenance projection** (the `R` read-path): for a fixed `d`, obtain `{a : (a,d) ∈ R}` — the content `d` ever held. This, not point membership, is what the operation actually consumes.
- **The provenance relation `R` as durable, monotone, queryable state.** Forced by D-NEED. Its *maintenance* belongs to the placement operations (ASN-0047); this note forces its *existence and a document-forward read path*.
- **The witness-filtered assembly:** the two report halves — content DELETED from one document and CURRENT in the partner — the partner's still-live copy being the recoverability witness.

## Implementation approaches

**The provenance relation `R` — the one piece this note forces into existence.**
Model `R` as an *append-only journal of provenance facts* (one record per "content `a` placed into document `d`"), recovered by replay on load, with an in-memory index built over it. This is exactly the substrate's own proven shape — the `links.jsonl` journal with a replayed registry — and it matches udanax-green's spanfilade, whose DOCISPAN entries are verified append-only and untouched by deletion. The journal gives monotonicity (P2) and durability by construction; the index is a *hint* — the log is authoritative, the index is recomputable on a miss or reload. You cannot derive `R` away (D-DISCR forbids it), so storing it is the simplest thing that honors the spec.

Two real choices here. **Granularity:** singleton addresses vs. contiguous content-address *spans*. Spans are far more compact (content is allocated in runs), mirror DOCISPAN's I-span entries, and set up span-coalesced output later; singletons are simpler but cost O(content). I'd store spans and pay a little interval logic at query time. **Access path:** SHOWDELETIONS needs the *document-forward* projection `d → {a}`. Udanax-green's spanfilade is indexed address-forward (`a → {docs}`) and, per the evidence, exposes *no* document-scoped enumeration of its DOCISPAN entries — a documented gap. Build the index the way this operation reads it: keyed by document. If address-forward lookup is also needed (link resolution), maintain both as two hints over the one journal rather than inverting at query time.

**Current arrangement range `ran(M(d))`.**
`M` comes from the foundation (ASN-0036); the operation needs its deduplicated content-subspace *range* — distinct content-addresses, multiplicity discarded (verified irrelevant: green's deletion and comparison both collapse to I-space set membership). Recompute it by a POOM-style V→I arrangement traversal per query, or maintain a per-document range-set as a cached hint over `M`. For a read-mostly query, cache the range-set and keep `M` authoritative; recompute the hint on a miss.

**The computation — set algebra, not a `dom(C)` scan.**
The spec's comprehension scans all of `dom(C)`, but the answer is three set operations over per-document content-address sets:

```
DeletedFromAWithB = ( Rproj(d_A) ∩ ran(M(d_B)) ) \ ran(M(d_A))
DeletedFromBWithA = ( Rproj(d_B) ∩ ran(M(d_A)) ) \ ran(M(d_B))
```

The `∩ ran(M(partner))` is the witness condition; the `\ ran(M(self))` is "absent now"; anchoring on `Rproj(self)` supplies the provenance that excludes never-included content (and, since `R ⊆ dom(C)×E_doc` by P7, keeps the result content-only by construction). This is precisely the set-difference udanax-green never composed — it shipped only the *intersection* (compare-versions / SHOWRELATIONOF2VERSIONS, verified) and left the difference to client-side arithmetic with no list-level subtract primitive. We compose it directly. The common case (two related versions with small divergence) touches only the documents' own sets, not the corpus; the pathological case stays bounded and correct by finiteness.

Represent the per-document sets as *ordered* sets keyed by tumbler order (T1). Ordered representation buys three things at once: D-ORD's output ordering for free, sorted-merge intersection/difference (linear in the operands), and clean coalescing into spans. A hash representation wins only for isolated point-membership, which this query doesn't dominate. With Rust's persistent `im` structures, an ordered set is the obvious carrier.

**Snapshot and concurrency — lean on D-OBS.**
Because the query writes nothing, it can run against an immutable snapshot with no locking. Persistent (structurally-shared) state makes this free: committing a composite swaps in a new immutable root, and the query reads whatever root is current — so it always reads a boundary. This is the right answer to the concurrency open question: SHOWDELETIONS needs *snapshot isolation over (M, R) together*, nothing stronger. The one hazard to design out is a *torn read* — `M` from after a composite, `R` from before — which surfaces the (in-arrangement-but-no-provenance) state that D-WIT proves impossible at a boundary. Closing it is the standard atomic-commit discipline: a composite must publish its arrangement edit and its provenance-journal append in one root swap.

**Output representation — address-based, because deleted content has no V-position.**
Return the addresses themselves; origin is derivable (S7), and the address prefix structurally names its originating document (verified). Do *not* attempt to return arrangement positions: the evidence is decisive that deleted content has no current V-position and must be expressed in I-address terms — green carries exactly this case as a span-with-origin (a sporgl), not a position spec. The natural enriched encoding is therefore (content-address-span, origin-document), which is also what an identity-preserving restoration will need to consume.

## Guarantees to uphold

| Guarantee | Holds by… |
|---|---|
| **Provenance permanence** (DELETED stays detectable) | construction — append-only `R`; never GC a provenance fact, even when content leaves every arrangement |
| **Discrimination** (DELETED ≠ NEVER_INCLUDED) | active — you must actually consult `R`; the arrangement set-difference shortcut is provably wrong (D-DISCR) |
| **Identity, no copies** | construction — return existing addresses |
| **Origin determinacy** | construction — origin read from the address (S7) |
| **T1 ordering of each half** | construction *if* ordered-set representation; otherwise active sort |
| **Disjoint halves / symmetry** | construction — definitional (contradictory partner-membership; name substitution) |
| **Observationality, no persisted artifact** | construction — read-only query path |
| **Content-subspace restriction** | construction — output ⊆ `dom(C)` and P7 grounds `R` in `dom(C)`, so links cannot enter; the only active care is not commingling link provenance in the index. (This is where green crashes; the spec's subspace algebra removes the hazard outright.) |
| **Consistent-snapshot meaning** | active — publish each composite's `M` edit and `R` append in one atomic root swap; then reads are boundary-consistent by construction |
| **Recoverability of every reported address** | construction — output ⊆ `dom(C)` and the witness is CURRENT, so reported content still exists and there is a live copy to restore from |

## How it fits

- **Leans on ASN-0047** for the provenance relation `R` and its laws (P2 permanence, P4★ bounds, P4a historical fidelity, P7 grounding, the subspace convention, CL-OWN link ownership). The critical dependency: `R` is defined there; SHOWDELETIONS is its first load-bearing consumer.
- **Leans on ASN-0036** for the content store `C`, the arrangement `M(d)`, and `origin` (S7) — supplying `ran(M(d))` and origin derivation.
- **Leans on ASN-0034** for T1, which orders each output half.
- **Leans on the transclusion-multiplicity results (ASN-0058 / ASN-0036)** for the licence to classify at set granularity.
- **Hands to a restoration / undelete operation** (a spec open question and the obvious downstream): SHOWDELETIONS produces the candidate set; an identity-preserving COPY-style operation consumes a subset to reintroduce content from the witness, preserving origin and links — verified as the mechanism (COPY shares addresses; INSERT would allocate fresh and sever identity).
- **Hands to a presentation layer** that renders deletions in a witness-derived reading order (a spec open question).
- Sits in the operations layer as a read-only observational query, above the foundation state and the provenance layer.

## Decisions for the builder

Genuinely open *engineering* choices (distinct from the note's spec-level open questions):

- **`R` granularity:** singleton-address set vs. content-address spans. Prefer spans (compact; enables coalesced output); accept interval logic.
- **`R` access path:** document-forward index (what this query needs) vs. address-forward (what link resolution needs) vs. both as hints over one journal. Build document-forward at minimum; most substrates will want both.
- **`ran(M(d))` materialization:** recompute by arrangement traversal vs. cache a per-document range-set hint. Cache for read-mostly workloads; keep `M` authoritative.
- **Set representation:** ordered (T1 — free ordering, sorted-merge ops, coalescing) vs. hash (point membership). Prefer ordered.
- **Candidate strategy:** literal `dom(C)` scan vs. the `Rproj ∩ ran(M) \ ran(M)` set algebra. Prefer the algebra; it is bounded by the documents' sizes, not the corpus.
- **Output encoding:** bare address set vs. enriched origin-tagged spans. Decide by the consumer; restoration wants the enriched form.
- **Snapshot mechanism:** immutable-root swap (persistent DS) vs. read-lock vs. MVCC. With persistent DS the read is lock-free — the cheapest mechanism meeting the contract.
- **Result caching:** D-OBS makes results memoizable keyed by (state-version, `d_A`, `d_B`); D-STORE forbids persisting them as a document. A volatile cache is permitted — decide if the workload warrants it.
