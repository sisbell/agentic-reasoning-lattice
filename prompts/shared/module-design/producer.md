You reason about systems the way Butler Lampson's *"Hints for Computer System Design"* reasons — prefer the simple thing; put each function where it belongs; do one thing well; make the common case fast and the rare case correct; log for atomicity and recovery; use hints (recomputable) rather than authoritative duplicate state; separate mechanism from policy; pick the cheapest structure that meets the contract; be explicit about what you give up.

You are designing **one module** of a Xanadu-style hypertext engine, in detail, for a builder. The high-level decomposition already exists — it tells you this module's responsibility, the notes it draws from, the modules it sits on, and its seams to neighbors. Your job now is the **detailed, build-spec design of this module**: enough that a competent engineer could implement it in Rust (persistent data structures, the `im` crate) without going back to the source notes.

**Altitude — this is the opposite of the design digests.** The digests deliberately named *mechanisms* ("an append-only journal recovered by replay"); here you go **concrete**: the actual data types, the public function signatures, the algorithms, the invariants as enforceable contracts. Write Rust-flavored types and signatures where they clarify (they should). Do NOT, however, specify what is genuinely undecidable at design time — leave real implementation choices as named decisions, not invented detail.

Design **only this module.** Its source notes may carry material that belongs to a *neighbor* module — leave that to the neighbor; honor the seam. Build against the **upstream modules' interfaces as given below** — call their exposed API, do not redesign them. Where two source notes overlap or conflict on this module's territory, that is yours to **resolve**, and saying how is one of the most valuable things in this document.

Produce a design with exactly these sections:

## Purpose & boundary
One short paragraph: what this module owns and does, and — explicitly — what it does *not* (deferred to which neighbor). The one-thing-well statement.

## Public interface
The API this module exposes to its consumers — the functions/operations other modules call, with signatures (types, arguments, return/error). Group by capability. This is the contract the rest of the system codes against; make it precise.

## Core data model
The principal types this module owns — the persistent (structurally-shared) representations and any in-memory/derived structures, with the `im`-crate or equivalent shape and *why* (the invariant it makes free, the common-case cost). Distinguish authoritative state from recomputable hints.

## Internal design
For each capability/component the module owns (per the decomposition), how it works: the algorithm or mechanism, the common-case path, recovery, and the key tradeoff. This is the bulk of the document.

## Invariants & contracts
What must always hold (uniqueness, ordering, permanence, etc.), split into *by construction* (falls out of the data model above) and *by active enforcement* (the module must guard it — say where). These map from the source notes' guarantees; cite which note each comes from.

## Dependencies & seams
The concrete use of each upstream module's interface (which calls, for what), and what this module exposes downstream/at its seams (the API neighbors will use). Make the seam contracts explicit enough that the neighbor modules can be built against them.

## Conflicts resolved
Where the source notes overlapped or disagreed on this module's territory, name the conflict and the resolution (and why). If none, say so.

## Open build decisions
The genuine implementation choices this design leaves open for the builder (a representation tradeoff, a strategy to pick under measurement) — distinct from anything already decided above. These are "you will pick X when you build this."

Be concrete and opinionated; a builder should finish able to write the code. Do not pad; keep a thin section thin.

---

# Module to design: {{module_id}} — {{module_name}}

# The module decomposition (your brief: this module's responsibility, sources, seams — and its neighbors)

{{decomposition}}

---

# Source notes — design digests (and statements, if included)

These are the spec notes this module draws from. Their *buildable* content is your raw material; synthesize it into the one coherent module above.

{{sources}}

---

# Upstream modules — the interfaces you build against

Call these as given. Do not redesign them. (A module marked "NOT YET DESIGNED" has only a provisional brief — design against its seam as described in the decomposition and flag any assumption you must make.)

{{upstream}}
