## What this is

FOLLOWLINK is the link store's single-endset read accessor: given a link address and a slot selector, it returns the recorded endset at that slot — a set of spans over tumbler space, measured by coverage — or a distinguished error if the link or slot does not exist. It is the narrowest read primitive over the link store, and deliberately *only* that: it reads what the link records, not what that record resolves to in any document.

## Design commitments

These are locked in for the whole system; downstream design cannot violate them.

- **The contract is bound at *coverage*, not representation.** Two results that denote the same set of positions are equal answers (F1/F3), regardless of how the spans are decomposed, split, or ordered. This is the deepest commitment: callers may not depend on a span count, a splitting point, or an emission order. You buy implementation freedom by giving up representational determinism — and you must not silently take it back by emitting a stable order callers will come to rely on.
- **FOLLOWLINK reads the *recorded* end, not its *resolution*.** Projecting the recorded endset into a particular document's live arrangement, and dropping addresses absent from that view, is a **separate operation** this note excludes by name. This is a placement decision with teeth: FOLLOWLINK needs no document handle, no arrangement, no content lookup, no lock. The reference implementation bundled resolution in; this spec de-bundles it. Honor the de-bundling — a faithful FOLLOWLINK returns tumbler-space spans, full stop.
- **Pure read, zero mutation (F4).** No state component changes — not content, links, entities, arrangements, or provenance. This forbids read-tracking, access stamping, and any "normalize on read and write back."
- **Empty is a first-class success, distinct from invalid (F7).** `⟨⟩` (a valid slot that presently holds nothing) and `⊥` (no such link or slot) are different return categories and must remain distinguishable, in-process and on the wire. This is the one obligation the reference implementation *failed*, so treat it as forced, not free.
- **The precondition is at its true minimum: link exists ∧ slot exists (F0/F8).** No requirement that any covered address currently holds content. Orphaned and ghost links are answerable; content existence is a separate question this operation never asks.
- **Selector arity is not frozen at three.** Valid selectors are `1..arity(link)`. The from/to/type triple is the floor, not the ceiling; derive bounds from the stored link, don't hard-wire `3`.

What is forced: coverage-exactness, pure-read, empty≠invalid, the minimal precondition, and confinement *at the coverage level*. What is merely conventional (left free by F3/F6): the span decomposition, span ordering, any normal form, and representation-level non-leakage of sibling slots.

## What must be built

Described functionally — what each must do.

- **A by-address link lookup** that maps a link address to its recorded link value, or reports absence.
- **A slot accessor with arity** that indexes the link's endset sequence by selector and knows the link's slot count for bounds-checking.
- **A three-way domain guard** that separates *link absent* and *slot out of range* (both → `⊥`) from *valid slot* (proceed) — and that decides "this end is empty" from the endset itself, never by inferring it from a downstream "nothing found."
- **An endset→span-set emitter** that produces a result whose coverage equals the stored endset's. The stored spans are their own witness, so the cheapest correct emitter copies them.
- **A result-category encoding** that keeps `⟨⟩` (success, empty) and `⊥` (error) distinct end-to-end, including across any serialization boundary.

What must *not* be built for this operation: any arrangement projection, content fetch, reachability/orphan check, document-open or locking gate, or by-content link index. Those belong to other operations.

## Implementation approaches

**Link lookup (by address).**
This repo's working substrate is already the right shape: an append-only `links.jsonl` journal as the authority, recovered by replay on load, with `paths.json` as a registry. Read that as Lampson would: the journal is the durable truth; the in-memory address→link map is a *hint* — recomputable on a miss by replay, never authoritative duplicate state. FOLLOWLINK is a pure reader of that map. Because links are immutable (LP13), the map is *monotone* — entries are only ever added — so it wants no overwrite path and no versioning of its own.
- For a single in-memory binary, keep the whole map resident. Back it with a **persistent (structurally-shared) map** (the `im` crate): a reader holds a consistent snapshot while writers append new versions, giving you lock-free reads that satisfy F4 by construction and snapshot consistency for free. I would pick this by default.
- Move to **on-demand load with an index** only when link volume exceeds memory; the journal stays the source of truth and the index is another recoverable hint.
- Green's granfilade *link orgl*, reached by address, is the proven analogue of the by-address path — and the evidence confirms this path needs **no open-document gate** (the follow path runs without requiring the home document open, Q19). That corroborates the "no lock, no handle" placement; do likewise.

**Slot accessor + selector.**
A link is a finite ordered sequence of endsets, so the selector is a direct positional index and arity is read off the link value. Green's verified design uses the literal integer `1/2/3` *both* as the storage coordinate and the query coordinate — proof that a positional selector is sufficient and cheap. The one thing to *not* copy: Green froze the range with a `==1||==2||==3` whitelist (Q12). Derive bounds from the actual arity instead, so n-set links work unchanged.

**The domain guard — the load-bearing engineering choice (F7).**
Check membership and bounds *first*, at the boundary, and emit `⊥` if either fails. Only then read the slot; if its endset has no spans, return `⟨⟩` as success. This ordering is the whole game. The verified anti-pattern is precisely instructive: Green's follow path treats "retrieval found nothing" as failure and emits a protocol error (`sporgl.c:93` → `putrequestfailed`, Q17), conflating an empty-but-valid end with an invalid request — the exact collapse F7 forbids. The fix is structural: never derive emptiness from a downstream null; derive it from "slot is valid **and** its endset is empty," a decision made in the core against the endset, not at the retrieval layer. The correct pattern already exists in the same codebase — Green's sibling RETRIEVEENDSETS always succeeds and lets an empty end flow out as an empty result (Q17). Model FOLLOWLINK on *that* sibling, not on the followlink path.

**Endset→span-set emitter.**
Emit the stored spans verbatim. F1 holds by construction because coverage is a pure function of the spans you emit and you emit exactly the recorded ones; Green's evidence shows raw endset spans returned by a **pure copy chain**, exponents preserved, no arithmetic (Q13), and multi-region ends kept as **separate spans with coalescing explicitly disabled** (`orglinks.c:412–413`, Q14). That verbatim copy satisfies F2 automatically — *provided the writer stored the disconnected end faithfully in the first place*. So note where F2 really lands: the obligation not to flatten a discontiguous end is the **writer's** (CREATELINK's); FOLLOWLINK's only duty is to not re-introduce over-coverage by merging across a gap. F3 *permits* coalescing adjacent (gap-free) spans or imposing a normal form, but doing so spends work on the read path for no contractual gain. I would emit verbatim and, if a normal form is ever wanted, establish it once at write time so reads stay cheap and stay deterministic-by-permanence (F5).

**Result-category encoding.**
In-process, make success-vs-error a sum/result distinction with the empty span-set living *inside* success — then `⟨⟩ ≠ ⊥` holds by construction and cannot be accidentally collapsed. Across a protocol boundary (the note's open question), carry an explicit status discriminant, not just a payload: an empty list alone is ambiguous with an error that sent nothing. Encode empty-success as an explicit *ok-with-empty* and invalid as an explicit *error*. This is just the remote form of the in-process sum type — and the standing rule "don't overload absence to mean two things."

## Guarantees to uphold

- **Exactness (F1)** and **discontiguity faithfulness (F2):** by construction under verbatim copy of a faithfully-stored end. Active enforcement is needed only if you transform the representation, and the deeper anti-flattening duty for F2 sits on the writer.
- **Representation invariance (F3):** upheld by *under-*promising — guarantee only coverage, and avoid leaking an incidental order callers will latch onto. The risk is over-promising, not under-delivering.
- **Pure read (F4):** by construction if the read path touches only immutable/snapshot state and adds no read-tracking. A persistent link map gives this for free.
- **Temporal determinism (F5):** free, inherited from link permanence (LP13). The only way to break it is to break immutability upstream; FOLLOWLINK enforces nothing itself.
- **Slot confinement (F6):** coverage-level confinement holds by construction since you read only slot `i`. Representation-level non-leakage is *not* a contract guarantee — but it is cheap to provide here (compute the result solely from slot `i`'s spans, never consulting siblings to choose split points), and I would provide it as hardening.
- **Empty≠invalid (F7):** the one guarantee needing *active* design — the variant-typed result plus the boundary-ordered domain guard above.
- **Content independence (F8):** by construction, because the read path never consults content, arrangements, or reachability.
- **Derived invariant:** since the writer enforces a non-empty type slot (L3), `followlink(·, ·, type-slot)` never returns `⟨⟩` — a useful assertion, but one that holds only because the *writer* upholds L3.

## How it fits

FOLLOWLINK sits *above* the raw link store and *below* arrangement/resolution. It leans on the **link store** (ASN-0093) for address→link, on **link permanence** (ASN-0043 L12, ASN-0098 LP13) for F5, on the **endset/span model** (ASN-0043, ASN-0034) for what a slot is, and on **coverage and span-set semantics** (ASN-0098/0043, ASN-0053 — convexity S0, non-empty denotation S2) for the measurement and the empty-collapses. It hands the job of projecting a recorded end against a document's live arrangement, and filtering unreferenced addresses, to a **separate resolution operation** that is explicitly out of scope — that is where shrinkage and document-dependence live, not here. It is the single-slot sibling of **RETRIEVEENDSETS** (all slots), sharing the slot/store machinery. The two access paths of the link store are worth keeping distinct: FOLLOWLINK uses the **by-address** path only; finding links by their endset *content* is a different operation served by the by-content index (Green's spanfilade) — do not consult it here.

## Decisions for the builder

- **Resident map vs on-demand index.** Keep the address→link map fully resident (recovered as a hint from the journal) for a single in-memory binary; switch to an indexed on-demand load only when link volume outgrows memory. Either way, journal is authority, map is a recomputable hint.
- **Verbatim vs normalized emission.** F3 lets you return stored spans as-is or impose a normal form. Pick verbatim on the read path; if you want a normal form, decide *where* it is established (recommended: at write time) — the spec leaves both the form and its placement to you.
- **Result shape and wire discriminant for `⟨⟩` vs `⊥`.** F7 forces *some* explicit-tag scheme; the exact in-process type and the exact wire status encoding are yours to choose.
- **Whether to provide representation-level confinement (beyond F6's coverage guarantee).** Not required by the contract, cheap to provide here; decide whether to commit to it as a hardening property.
- **Selector form and arity discovery.** Positional integer (Green-style, doubling as a storage coordinate) vs symbolic slot name mapped to a position; and whether arity is stored with the link or derived. Do not hard-wire three.
- **Where the bounds check lives.** Validate selector/address at the boundary for fast `⊥` on malformed input — but make the empty-vs-present decision in the core against the actual endset, never inferred from a downstream "nothing found." That split is what keeps F7 intact.
