## What this is

The address-classification layer of the namespace: given a tumbler (a hierarchical address), ASN-0045 names which of four nested levels it denotes — **node, account, document, or element** — or rejects it as not a well-formed address. It is the substrate's "what kind of thing does this address name?" predicate, and it fixes **account** (not *user*) as the canonical name of the zeros=1 level.

## Design commitments

*(forced by the spec vs. merely conventional)*

- **The address space is exactly four nested levels — node, account, document, element — and no more.** *Forced*: the depth ceiling is T4's axiom `zeros(t) ≤ 3`. There is no fifth level; an address with four separators is *invalid*, not "deeper."
- **Level is a pure syntactic function of the address — the count of zero separators — with no external state.** *Forced*: each predicate is defined as `zeros(t) = k`. No registry, lookup, or context decides an address's level; its shape does. You give up context-dependent or re-labelable addresses in exchange for stateless, local, always-consistent classification — the right trade.
- **An address is admissible only if it passes all four `T4-valid` clauses**: bounded zero-count, no adjacent zeros, no leading zero, no trailing zero. *Forced*; ASN-0045 coins `T4-valid` as exactly this conjunction (T4 itself named no such one-place predicate).
- **Classification is total and partitioned, with an explicit invalid complement**: every valid address has *exactly one* level (Partition); every invalid address has *none* (Off-Domain Vacuity). *Forced* — both proven. No overlap, no ambiguity, no faulting on garbage.
- **"Account" is canonical for the zeros=1 level; "user" is a retained alias.** *Conventional* — the one naming choice this note makes, grounded in Nelson and confirmed by udanax-green, where structural/addressing code uniformly says *account* (`ACCOUNT`, `tumbleraccounteq`, `accountfile`, `XACCOUNT`); *user* survives as an integer session-slot index (`userid`, `player[user]`) and in ownership predicates (`isthisusersdocument`), but never as the level name. The level's *existence* is forced; its *name* is the convention. The field-projection symbol `U` is deliberately left unrenamed.

## What must be built

- **A validator** deciding `T4-valid(t)` — the four positional/counting clauses — as a total predicate over any tumbler.
- **A zero-separator count** `zeros(t)` (inherited from T4): the single quantity that decides the level.
- **A classifier** mapping any tumbler to exactly one of {node, account, document, element, invalid}, total and never-faulting.
- **The level vocabulary** as the shared downstream language for "this operation applies to documents / this address names an element," with *account* canonical and *user* an alias confined to the boundary.

## Implementation approaches

This is a place to **not build machinery.** The answer is a pure function of the address, computable in a single scan — cheap because it is a *scan, not a parse*, not because the input is small (the bound is on the zero-*count*, `zeros(t) ≤ 3`, not the length; a Node is *any* zero-free sequence, hence unbounded). Resist parsers-with-ASTs, level registries, and stored/indexed level tags; the whole note is a scan.

- **Fuse validate-and-classify into one streaming pass.** All four `T4-valid` clauses plus the zero-count are decidable in a single left-to-right **O(#t)** scan with O(1) carried state (saw-zero-last?, running zero-count, first/last position), yielding either *Invalid* or the level directly. **Pick this always** over validate-then-classify — there's no reason to walk the address twice.

- **Represent the result as one five-way sum {Node, Account, Document, Element, Invalid}, not four independent booleans.** This is the load-bearing engineering choice. With a single classifying function, *Partition* and *Off-Domain Vacuity* stop being invariants you test and become true *by construction*: a function returns one value, and *Invalid* is disjoint from the four levels. The only thing left to verify is that the scan computes `zeros` and the clauses correctly. Crucially, that core is **name-free**: exactly-one-level falls out of comparing the zero-*count* alone (a count equals one value), needing no level-name lookup or table for correctness or mutual exclusion — the name↔level correspondence (T4c, *account* for zeros=1 and so on) is a separable derived fact used only for *reporting*, and reading exclusivity off it would be circular. The spec's four-predicate form is convenient for *proof*; the sum is the right form for *code*. Four independent predicates would force you to maintain mutual exclusion yourself — strictly worse.

- **Tumbler representation — three options:**
  - *Flat component sequence, classify on demand.* Store the address as its raw component sequence with zeros explicit; recompute level/validity by scan when needed. This is Green's shape — tumblers live as flat integer arrays (its `defaultaccount` literal) and account containment is a prefix scan (`tumbleraccounteq`, "is this document under this account?"). Pick when addresses mostly flow as opaque keys for routing, comparison, and journaling, with only occasional field access.
  - *Parse once into a structured field view.* Parse at the boundary into node/account/document/element fields; the level is the *last populated* field (a Node populates the node field only, an Element all four — populated-count − 1 = zeros), validity becomes "parse succeeded," both O(1) thereafter. Pick when hot paths repeatedly read fields or test containment.
  - *Hybrid (recommended): flat canonical storage form + validate-and-parse once at admission into an immutable, already-classified value.* Storage and journal keys stay flat; everything past the front door carries the structured value with its level attached. Because the address value is immutable, the attached level is a **derived constant, not a stale-able cache** — it can never miss. (Were addresses mutable, you'd demote it to a recomputed *hint*; immutability buys the stronger property for free.)

- **Place the validator as an admission gate; classify on demand.** Enforce `T4-valid` *once*, at the front door — before an address becomes a journal key or registry entry — so the stored substrate carries the standing invariant "every address is valid" and no downstream reader must re-check. This mirrors the repo's own substrate: addresses are the keys into the append-only journal and the `paths.json`-style registry, and a malformed key should never reach them. Classification itself is cheap enough to recompute anywhere; don't index or persist it.

- **Don't reach for `im` here.** An address is a flat sequence held as an immutable value — structural sharing buys it nothing; an inline immutable sequence suffices. Persistent structures earn their keep in the *registries and prefix-indexes keyed by* these addresses, not in the address value itself.

- **Consider letting the verified spec be the implementation.** The definitions are small and executable; the oracle pipeline can emit the classifier directly from the Dafny spec, with Partition / Off-Domain Vacuity machine-checked rather than hand-maintained — worth it precisely because this component is pure and total.

- **On Green's encoding:** Green realizes the same four-level hierarchy and the same account-prefix-containment idea, but its concrete array layout (header words, a double-zero account terminator) is its own encoding, not the spec's single-zero-separator model. Borrow the *structure* (flat arrays, a named ACCOUNT level, prefix containment); don't copy the byte layout.

## Guarantees to uphold

- **Totality / never-faults** — defined on *every* tumbler; malformed input returns *Invalid*, never an exception or a violated precondition. *By construction* iff Invalid is a real return value, not a precondition that can be broken.
- **Exactly one level per valid address (Partition)** — *by construction* with the sum-type classifier (a function is single-valued); reduces to "the scan implements `zeros` and the clauses correctly."
- **Zero levels per invalid address (Off-Domain Vacuity)** — *by construction* with a distinct Invalid tag disjoint from the four levels.
- **Level stability (a derived permanence)** — an address's level never changes; it is a pure function of an immutable address. *By construction.* Downstream may rely on "once an account address, always an account address."
- **Depth ceiling** — nothing is ever classified beyond element. This rests *entirely* on the `zeros ≤ 3` clause and so must be **actively checked** — it is the only thing stopping a four-separator tumbler (zeros=4, e.g. the counter-example `[1,0,1,0,1,0,1,0,1]`) from being read as a new level.

The honest summary: with the right mechanism (one total function returning a sum), every contract here holds by construction *except* the arithmetic of the scan itself — count zeros, check the three positional rules. That is the entire enforcement surface.

## How it fits

- **Leans on ASN-0034 (the tumbler hierarchy).** It consumes `zeros(t)`, T4's validity clauses, and T4c's level↔zero-count correspondence; it does not re-parse addresses, it *names* the levels T4c already pinned. The level-correspondence postconditions additionally lean on T4b/T3 to license T4c at a point, and the ℕ-ordering facts under Partition are inherited, not re-proved here.
- **Hands to storage/registry** as the admission predicate: only `T4-valid` addresses become keys into the journal/registry.
- **Hands to ownership/access control**, which layers *user owns this* on top of the *account* level. Keep these layers clean: ASN-0045 supplies only the pure *level* fact — `Account(t)` is a one-place predicate ("t is account-shaped," zeros=1) on a single address. It says nothing about *containment* ("is document d under account a" — a two-place relation, Green's `tumbleraccounteq`) or about *ownership* ("may this user touch it"). Both containment and ownership sit in layers above this note, and the "structural ≠ ownership" hazard lives at the *containment* layer, not at this note's level predicate. (Green's version path pairs the two explicitly: an account-prefix containment match *and* an ownership check — `tumbleraccounteq` && `isthisusersdocument`.)
- **Hands the level vocabulary** to every addressing operation — resolution, versioning, and anything scoped to "documents" or "elements."
- **Adjacent but not here:** prefix/containment indexing (the granfilade/enfilade idea) is the natural structure for *querying* addresses by level or containment; this note only supplies the per-address label such an index would bucket on. Don't build the index here.

## Decisions for the builder

- **Sum vs. four predicates** — return one classifier yielding a five-way sum (recommended; buys both lemmas), or expose four independent predicates only if some downstream genuinely wants them à la carte, at the cost of maintaining exclusion yourself.
- **What *Invalid* carries** — a bare rejection, or the *reason* (adjacent-zeros / leading-zero / trailing-zero / over-depth). The spec needs only the boolean; an admission gate is far more usable if it reports the failing clause, and the four counter-example rows are the ready-made diagnostic categories.
- **Representation** — flat-on-demand, parse-once, or the hybrid above; driven by how often downstream reads fields versus routes whole addresses.
- **Classify on every access vs. carry a derived level tag** — recompute is fine; it's a cheap O(#t) scan. Tag only if profiling a hot path demands it (and then it's a safe derived constant, given immutability).
- **Naming in the codebase** — commit to *account* for the structural level everywhere; decide whether *user* survives even as an alias in new code or is confined strictly to the ownership layer. Don't let the two vocabularies cross.
- **The degenerate empty tumbler** — confirm the validator's behavior on the zero-length address (the `t₁ ≠ 0` / `t_{#t} ≠ 0` clauses have no element to test). This most likely resolves at the T4/T0 layer, but the classifier must still give it a definite answer (presumably *Invalid*).
