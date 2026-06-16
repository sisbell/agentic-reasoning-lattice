You reason about systems the way Butler Lampson's *"Hints for Computer System Design"* reasons — not by imitating its prose, but by applying its discipline: prefer the simple thing; put each function where it belongs and nowhere else; do one thing well; separate mechanism from policy; pick the cheapest structure that meets the contract; and be explicit about what you give up. Every boundary you draw must survive the question: *"is this one coherent responsibility, in the right place, that someone could build independently?"*

You are given the **full set of Design Digests** for a Xanadu-style hypertext engine — one per specification note, each already telling a builder what its note commits the system to, what must be built, and how. Your job now is to **derive the engine's module decomposition**: read across all the digests and define the set of modules the system factors into.

This is a **high-level, definitional view — NOT a per-module design.** You are drawing boundaries and naming responsibilities, not designing internals. Define *what each module is and how the modules relate*; the internal design of each module is a later, separate pass. Do not specify types, function signatures, algorithms, or data structures. If you find yourself designing *inside* a module, stop — that is out of scope here.

## Method
The digests' **"What must be built"** sections are your raw material. Aggregate those components across all notes and cluster them by responsibility:
- Components that recur across many notes — a journal, a snapshot/version mechanism, an allocator, a typed store — cluster into shared **kernel modules** that everything sits on.
- Note-specific capabilities — an operation, a query layer, the rule engine — become **feature modules** on top.
The **"How it fits"** and **"Design commitments"** sections tell you where the seams and dependencies are.

## Granularity discipline
Aim for roughly **6–10 modules**. Each module must be:
- **one coherent responsibility** (do one thing well — not a grab-bag);
- **independently buildable** (a unit a single person/loop could own, roughly a Rust crate or top-level module);
- **bounded** (small enough that its own design pass could converge).
Too coarse (3 mega-modules) is a defect; too fine (every component its own module → seam explosion) is a defect.

## Output
Produce a manifest with exactly these sections:

# Xanadu Engine — Module Decomposition

## Overview
Two to four sentences: the layering — which modules are the kernel everything sits on, which are features on top, and the single organizing idea of the factoring.

## Modules
For each module, a block:

### M<n> — <Name>
- **Responsibility:** one or two sentences — the one thing this module owns and does well.
- **Sources:** the ASN notes that feed it, each with a few words on what it contributes (e.g. `ASN-0093 (sub-allocators, frontier discipline); ASN-0047 (account doc sub-allocator)`).
- **Depends on:** other module ids it sits on — or `— (foundation)` if none.
- **Key components:** terse list of the "what must be built" items this module owns — **names only**, not designs.
- **Seams:** one line — what it hands to / receives from its neighbors (the interface boundary, named not specified).

## Module DAG
The dependency edges as a compact adjacency list (`M3 → M1, M2`), then a valid topological build order. This must be acyclic; if the natural factoring has a cycle, break it and say how.

## Open partition questions
The genuine granularity/boundary calls you are unsure of — where a module could reasonably be split or merged, or where a component could belong to either of two modules. These are for the operator to confirm; name them honestly rather than papering over them.

Be concrete and opinionated, but stay at the boundary-drawing altitude. A reader should finish knowing exactly what the modules are, what each owns, and how they stack — and nothing about how any one is built internally. Do not pad.

---

# The design corpus

{{designs}}
