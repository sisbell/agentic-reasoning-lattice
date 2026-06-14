I reviewed the digest against the note, its claim statements, and the verified Green evidence. This is a strong, unusually careful digest — it grounds every Green claim in the evidence, handles the note-vs-Green mismatches explicitly, and avoids the soundness traps the assignment warns about. I found no material problems, only minor sharpenings.

## Revision list

**1. Section *Implementation approaches → Subspace activation* — reframe "single zero-width placeholder crum, not zero crums" from Green trivia into an actionable caution.** [SHARPENING]
The "not zero crums" correction is accurate and grounded (Q13/Q18), but the digest states the *fact* without the *design reason* a builder needs. Green keeps the placeholder precisely so the first-insert path's precondition (a bottom crum exists) holds — a literally-empty representation can break first-insert (Q13's Bug 0019: `firstinsertionnd` assumes a bottom crum). For a clean-slate builder who won't use POOMs/crums, the load-bearing takeaway is the abstraction, not the crum count: *whatever represents `M(d)=∅` must be insert-extendable from empty*, with Green's placeholder as the worked example of how to guarantee that. Recast the sentence around that.

**2. Section *Implementation approaches → Subspace activation* — "common case cheap, rare case correct" is the wrong Lampson hint.** [SHARPENING]
What this section describes is lazy materialization — "don't pay for what you don't use," defer cost to first use. "Common-case-fast / rare-case-merely-correct" is a different hint (optimize the hot path, fall back to a correct-but-slow path), and first-use of a subspace is neither rare nor a correctness-vs-speed tradeoff. The very next clause ("creation stores no content, and the first content operation pays for what it uses") already states the right principle — just relabel it. Given the digest's Lampson voice, the mislabeled hint is worth fixing.

**3. Section *Implementation approaches → Subspace activation* — flag the `A_L ↔ link+type` fold as one reading, not the mapping.** [SHARPENING]
The reconciliation (note's two sub-allocators `A_C`/`A_L` vs Green's three subspaces, with type `3.x` folded into `A_L`) is sound and is exactly the right move — it correctly avoids claiming the note commits to three subspaces or Green to two. But the note's model plausibly just doesn't represent link *type* as a distinct subspace at this layer (type as content, or a higher-layer concern), so "`A_L` = link + type" is a defensible reconciliation *choice*, not the only one. A half-clause noting that would tighten it. Lowest priority.

## What's solid (no action)

These sections are correct and well-grounded, and I want to be explicit that I checked them hard:

- **Place/content firewall** correctly scopes the claim to the *content* I-address counter (Q16's code exploration shows the *document*-address high-water mark *does* advance). A careless digest would have said "creation doesn't advance the high-water mark" flatly and been wrong; this one didn't.
- **Atomicity vs crash-safety** is handled without contradiction: the spec's "single atomic transition" is a logical guarantee, and the digest correctly identifies the internal find-then-record shape (Q20's crash hazard) and answers Q1 with journal-append-as-commit. This is the strongest part.
- **Forced / derived / merely-conventional** is parsed precisely: the level-separation *requirement* is forced while the *mechanism* (length filter vs truncate-then-increment) is not; the allocation arithmetic is derived, not chosen; only the cached-counter timing is conventional. All "forced" labels check out against the note.
- **No value-based-dedup trap.** The idempotency analysis correctly concludes the operation cannot self-dedup (input is `A` only, value-based identity forbidden) and pushes exactly-once to a session-layer request key — sound, and grounded in the locks.
- **CND.A-act discharge** ("activated allocator reduces to `A`'s presence") is a legitimate design reading directly supported by Q1's "nothing to pre-initialise / no prior initialization entry required."
- Spec-level open questions (Q2–Q6) are cleanly separated from builder decisions, and the BERT/create-open separation (Q17) is accurately stated.

VERDICT: CONVERGED
