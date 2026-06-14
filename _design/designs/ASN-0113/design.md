## What this is

`RETRIEVEDOCVSPANSET(d)` is the **whole-document extent observer**: hand it a document by identity alone and it reports, per content kind, how much there is — a normalized span-set of at most two members, one summarizing the text the document arranges and one summarizing its links. It is a pure read over the document's arrangement `M(d)`; it changes nothing and touches neither the content store nor the link store.

## Design commitments

These are locked in for everything downstream:

- **Identity-only input.** The operation is keyed solely by document identity — no range, no position, no selection. It is the "size profile" probe, distinct from any range-scoped retrieval.
- **The result is span-set-typed, never numeric, never record-valued.** Magnitudes are carried *in span boundaries* (the count is the last component of a width), not designated directly. Consumers read counts off spans. At most two members.
- **Pure query with a minimal read-set (W8).** It reads only the *domain* of `M(d)` — the occupied V-positions — projected by subspace. It does **not** read the I-address values, the content store `C`, or the link store `L`. This is both a purity rule and a correctness rule (see arranged-vs-homed below).
- **Exactly two kinds, intrinsically (W9).** Content lives only in the text subspace (`s_C`) and link subspace (`s_L`); no third subspace can hold document content, so no third member can ever arise. The kind-list is fixed, finite, and ordered.
- **The report is the *arranged* extent, not the *homed* extent (W20).** It counts what `M(d)` currently arranges. A link can be homed at `d` yet absent from `M(d)` (a "reverse orphan" after its position is deleted). The count must reflect the arrangement, which can be a strict subset of what is homed at `d`.
- **Allocation is the gate (W-pre).** An *unallocated* identity is outside the domain and must **fail** — not fabricate `⟨⟩`. An *allocated-but-empty* document returns the defined empty span-set `⟨⟩`. The substrate must distinguish these two states.
- **Single-span-per-subspace exactness is inherited, not established.** A *single* span covers a subspace exactly only because each subspace's occupied positions form a *dense contiguous run* (the contiguity invariant D-CTG★, maintained by the editing operations). This operation **consumes** that invariant; it does not enforce it. If contiguity were relaxed, the single span degrades to a bounding box that overshoots interior gaps.

What is merely conventional: the specific numbering `s_C = 1`, `s_L = 2`. The working depth is **not** conventional: `m_S` is a per-subspace structural value `≥ 2` (S8-depth) that the synthesizer reads off the arrangement, and the general start is the canonical `[S,1,…,1]` of depth `m_S`. Depth 2 — where that prefix collapses to `[S,1]` — is the common/minimal case, not an assumption you may bake in; the note exercises `m_S = 3` precisely to show the synthesizer must handle a genuine interior position. What is forced: the span-set result type, purity, two-kinds-only, arranged semantics, the allocation gate, and reliance on contiguity for exactness.

## What must be built

- **An allocation gate.** A cheap membership test "is `d` an allocated document?" against the document registry, with three-way dispatch: unallocated → fail; allocated and empty in both subspaces → `⟨⟩`; otherwise → emit members.
- **A per-subspace extent aggregator.** For each of the two subspaces, determine from `M(d)`'s key set whether it is occupied and, if so, its count `n_S` (the run length) and its working depth `m_S`. This is the whole computational core, and it needs only the *keys* of `M(d)`, partitioned by first component — never the mapped values.
- **A span synthesizer.** Turn each occupied `(S, n_S, m_S)` into its extent span — start fixed at the canonical `[S,1,…,1]` of depth `m_S`, width the pure displacement encoding `n_S`. (Reuse the span/displacement primitives; do not rebuild them.)
- **An assembler.** Emit the occupied subspaces in subspace order as a span-set, `⟨⟩` if none, keeping each member's subspace identifier intact in its start so kind is self-describing (W14).

## Implementation approaches

The crux is the **per-subspace extent aggregator**, and the right framing is Lampson's: the extent is a *summary of `M(d)`'s domain*. The contiguity invariant collapses that summary to two integers (a count per subspace) plus structural depths — the start is fixed by convention, so you never even need to find a minimum. So the only real question is how cheaply you can get the per-subspace count.

**Option 1 — Compute on read by range scan (the simple thing; my default).** Represent the arrangement as a persistent ordered map keyed by V-position (tumblers are totally ordered, so subspace `S`'s keys are exactly the contiguous key-range under prefix `[S,…]`). Scan each subspace's range, count, read the depth off the first key. Cost is O(occupied positions in `d`), no auxiliary state, always correct, nothing to keep consistent or recover. For a query that is almost certainly not on the hottest path, this is the right starting point — it honors the spec with zero added machinery.

**Option 2 — Order-statistic augmentation (the first optimization).** Keep the same ordered map but augment nodes with subtree counts, so a count over a subspace's key-range is a rank difference in O(log n) without scanning. Pick this when documents grow large *and* this query is measured hot. Cost: the off-the-shelf persistent ordered map doesn't expose rank, so this means a custom size-augmented persistent tree — a real implementation expense to weigh against how often the query actually runs.

**Option 3 — A maintained per-document summary, as a recomputable hint.** Have every arrangement-mutating operation update a per-document summary that the query then reads in O(1). Be precise about *what* is maintained, because two different objects live here. A literal **count-hint** `(n_{s_C}, n_{s_L}, m_{s_C}, m_{s_L})` is `|V_S(d)|` by construction — robust, faithful to the count even if a write-path gap ever opened. That is **not** what udanax-green maintains: `setwispnd` propagates a **bounding-box extent** to the POOM root on every edit, and a bounding box *overshoots interior gaps* (Q11, Q13) — its last component equals the count `n_S` only while the subspace is a dense contiguous run (D-CTG★). So a maintained *extent* imports the very contiguity dependence that W4 rests on and that this operation cannot self-certify; a maintained *count* does not. Either way, the Lampson discipline holds: treat the summary strictly as a **hint** — never journaled as authoritative, **recomputed from the arrangement on load** — so it carries no recovery burden and a drift bug degrades performance, not correctness (Green's query reads the root with no cache layer, so deletions reflect immediately). Pick this only when the query is hot *and* you control every editing path; the cost is coupling, since this note's summary now rides along with every editor.

**Option 4 — Free-ride an existing aggregate.** If the arrangement is itself stored as an enfilade-style structure that already maintains per-node V-extent aggregates for other operations (Green's case — the bounding box serves many callers, so its maintenance cost is amortized), the extent is already computed; just read it. Option 3's caveat applies, and harder: what you free-ride is a *bounding-box extent*, not a count, so its last component is the faithful `n_S` only under D-CTG★ — reading it inherits the same contiguity-trust W4 does, whereas compute-on-read (Options 1/2) counts actual keys and stays faithful even under a write-path gap. This is the best option *if you were going to pay for the aggregate anyway and the write path enforces contiguity*; it is over-engineering to introduce such a structure solely for this query.

My recommendation: ship Option 1, reach for Option 4 if your arrangement representation already carries the aggregate *and* contiguity is enforced on the write path, and only escalate to 2 or 3 under measurement. Mind the faithfulness asymmetry — Options 1/2 count actual keys and remain correct even if a gap opens, while Options 3/4 read an extent that equals the count only under D-CTG★.

**The allocation gate.** Test membership against the document registry — a registration record kept separately from the content journal, the analog of Green's granfilade registration (Green's `findorgl`/`checkforopen` path returns failure, the `?` marker, for an unregistered id, while an existing-but-empty document returns the empty result). The load-bearing requirement: **registration must be a journaled event separate from content writes**, so "no arrangement entries for `d`" (allocated-empty → `⟨⟩`) is distinguishable from "`d` was never allocated" (→ fail). Conflating them by treating "no journal entries" as "doesn't exist" is the tempting wrong move.

**Recovery.** The query itself has no recovery story — it is a pure read. Its inputs ride the standard substrate: an append-only arrangement journal plus a separately-kept document registry, recovered by replay on load (the `links.jsonl` append-only-journal pattern, with registration recorded apart from it). Any extent hint (Option 3) is rebuilt during that replay, never replayed as truth.

**Span synthesis and assembly are by-construction trivial.** The two members are disjoint and emitted in subspace order, so the result is *already normalized* (W13) — do not run a general span-set normalizer; just emit text-then-link. Keep the subspace identifier intact in each start. Note that Green's mixed-document output muddied this — it stripped subspace digits in normalization and the text/link forms became confusing enough that its own knowledge base mislabeled them, and Green used *asymmetric* mechanisms (a root-field read for links, a separate tree traversal for text, an artifact of how it packed digits into one tumbler). With a clean ordered-map representation both subspaces are symmetric range queries, and keeping kind self-describing (start's first component = `S`) is the thing to preserve. This is a place the spec is cleaner than the reference implementation; follow the spec.

## Guarantees to uphold

**Hold by construction (given the operation's inputs are scoped correctly):**
- *Purity and read-set minimality (W8)* — grant this code read-only visibility into `M`'s domain and **no handle** to `C`, `L`, value-dereferencing, or any mutator. Then purity is structural, not a thing to check.
- *At-most-two members, one per occupied subspace (W7)* — iterate the fixed two-element kind-list.
- *Normalized, self-describing output (W13/W14)* — emit in subspace order with identifiers intact; disjointness makes merging impossible.
- *Independence (W15)* — the two counts come from disjoint key-ranges.

**Inherited from invariants enforced elsewhere (the editing operations and the placement discipline):**
- *Exact coverage (W4)* — exact only while contiguity (D-CTG★) holds. This is the one guarantee this operation cannot self-certify. Trust it (it is enforced on the write path) and, in debug builds, assert it cheaply; do not pay to scan for gaps on every read.
- *Content-bearing positions (W17)* — every counted V-position within `ext(d,S)` resolves to real content in `C`/`L` (S3★), one step beyond W4's coverage equality. The reported extent counts content-bearing positions, not abstract addresses; this rests on referential integrity enforced on the write path.
- *Two-kinds-only and disjointness (W9/W11)* — rest not on the *numbering* convention (`s_C=1`, `s_L=2`) but on the subspace-exhaustiveness invariant S3★-aux, a theorem the spec treats as enforced. In Green that invariant was degraded to a *convention only* (its write-admission check `acceptablevsa` was a stub returning TRUE, and `REARRANGE` could cross the boundary), so its disjointness was only as good as the front-end's discipline. The lesson: **enforce subspace confinement at write admission** — the check Green stubbed out — so that this read can trust it. Put the check where the violation can occur (the write), not on every read.

**Require active enforcement here:**
- *The precondition gate (W-pre)* — you must actively fail on an unallocated id rather than returning `⟨⟩`.
- *Faithful, arranged-not-homed count (W20)* — count `M(d)`'s link-subspace positions. The cheap-but-wrong implementation is to count the link store filtered by origin `= d`; that yields *homed* links and gives the wrong answer after any reverse-orphaning. The discipline of reading the arrangement (W8) *is* what makes the count correct.

## How it fits

It sits at the **arrangement-query layer**, a leaf observer: nothing depends on it to keep state correct, and it depends on the foundation beneath it.

- **Leans on:** the arrangement subsystem for `M(d)` (and its domain); the document registry for `d ∈ dom(M)` allocation membership (ASN-0093's registration); the subspace convention assigning text/links to the first component (ASN-0036); the per-subspace shape invariants that guarantee a dense contiguous run and shared depth (D-CTG★/D-MIN★/D-SEQ★, S8-depth, ASN-0047), plus S2/S3★ for functionality and referential integrity; and the span algebra for span validity, displacement, reach, and normal form (ASN-0034/0053). It rebuilds none of these.
- **Hands to:** any caller wanting a document's size profile without its contents — UI/front-end ("5 chars, 2 links"), version-comparison (compare per-kind extents across documents or versions, W14), and allocation/emptiness checks. It is the whole-document sibling of the range-scoped content-region-query family.

## Decisions for the builder

Distinct from the note's spec-level open questions (version-fork permanence, transclusion, a unified overall-extent, extending the kind-list — leave those to the operations that own version and transclusion semantics; keep this operation a pure function of `M(d)` at the queried version):

- **Compute-on-read vs maintained hint.** The note dictates the *answer* (counts), not the structure that yields it. Default to range-scan; escalate to order-statistics or a maintained hint only under measurement, and if you maintain one, make it recomputable and rebuilt on load.
- **Arrangement representation.** Whatever you pick must make "occupied keys under subspace prefix `S`" cheap — a persistent ordered map keyed by V-position is the natural fit; deciding whether to augment it (or free-ride an enfilade aggregate) is yours.
- **Where the allocation bit lives** and how the registry records allocated-empty distinctly from unallocated.
- **How `m_S` is obtained** — read off any occupied position (they share it) or carried explicitly. Minor, but you must choose.
- **Defensive contiguity verification on read vs trust-plus-debug-assert.** Trading safety against per-query cost; trust is the right default if the write path enforces the invariant.
- **Whether to special-case the depth-2 common path** (where the canonical prefix collapses) for speed — a micro-optimization, worth it only if profiling says so.
