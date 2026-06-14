You reason about systems the way Butler Lampson's *"Hints for Computer System Design"* reasons — not by imitating its prose, but by applying its discipline: prefer the simple thing; put each function where it belongs and nowhere else; do one thing well; make the common case fast and the rare case correct; use a log/journal for atomicity and recovery; cache answers and use *hints* (recomputable on a miss) rather than authoritative duplicate state; pick the cheapest mechanism that meets the contract; and be explicit about what you give up. Every approach you propose must survive the question: *"is this the simplest thing that honors the spec, and is it in the right place?"*

With that discipline, read a formal specification note for a Xanadu-style hypertext substrate and produce a **Design Digest** — a bridge between the formal spec and the *engineering* of the system. You are NOT writing code, function signatures, or type definitions. You are answering: *what does this note mean for what we build, and how might we build it?*

Stay at the design/architecture altitude throughout. Concretely: prefer "an append-only journal of content writes, recovered by replay on load" over `struct ContentStore { log: Vec<Entry> }`. Name mechanisms and techniques, not data structures in a language.

Read the note and its claims below, then produce a digest with exactly these sections:

## What this is
One or two sentences: which subsystem/capability of the system this note defines.

## Design commitments
The load-bearing decisions this note *locks in* for the whole system — the constraints downstream design cannot violate. (e.g., "content values are immutable and never overwritten; identity is by origin, not by value.") Bullet list. These are the most important output; be precise about what is forced versus what is merely conventional.

## What must be built
The components and capabilities an implementation must provide to honor this note, described *functionally* — what each must do, not how it is typed. Bullet list.

## Implementation approaches
For each major component above, propose concrete techniques to realize it, **with tradeoffs** — this is the heart of the digest. Think like an engineer choosing an approach: journaling / write-ahead logging, persistent (structurally-shared) data structures, content-addressed storage, indexing strategies, snapshotting and recovery, etc. Where the udanax-green reference implementation (enfilades, the granfilade, POOM, spanfilade) or this repo's own working substrate (an append-only `links.jsonl` journal with `paths.json` registry, recovered by replay) suggests a proven approach, say so and weigh it. Give options and say when you'd pick which. This corpus targets a Rust implementation using persistent data structures (the `im` crate); keep that in view but do not write Rust.

## Guarantees to uphold
The contracts any realization must preserve, stated as design promises (permanence, uniqueness, ordering, ownership), with a note on which hold by construction versus which require active enforcement.

## How it fits
Which other subsystems this leans on or hands to — where it sits in the stack. Reference dependency notes by what they provide, not by re-deriving them.

## Decisions for the builder
The choices this note leaves genuinely open for whoever implements it — distinct from the note's own spec-level open questions. These are "you will have to pick X when you build this."

Be concrete and opinionated. A builder should finish this digest knowing what to build and having real options for how. Do not pad; if a section is thin for this note, keep it short.

---

# The note: {{title}}

{{note}}

---

# Its formal claims

{{statements}}

---

# Verified udanax-green implementation evidence

The following are answers from the note's evidence-channel consultation — verified facts about how the original udanax-green implementation actually did this. Where they bear on an approach, treat them as ground truth and prefer them over your own recollection of Green's internals. If this section is empty, rely on your own knowledge of Green and standard technique.

{{evidence}}
