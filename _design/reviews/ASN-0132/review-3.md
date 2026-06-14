This is a strong digest. It reads the note's commitments accurately (the forced/conventional split is right throughout), it makes correct and disciplined use of every evidence answer — Green's off-by-one dedup, the dead-coded home filter, count-costs-like-enumeration, multi-session disabling, the deeply-orphaned empty-request zero — and it proposes approaches that honor rather than violate the note's locks (dedup keyed by **address** not value; index and cache as Lampson **hints**, not truth; epoch invalidation reconciled with CN-SNAP). All eleven claims and all six open questions are covered, and it stays at design altitude. The load-bearing analysis — that identity-uniqueness needs *active* enforcement, that the query channel (not the operation) is what loses orphans, that q\* maintenance is +1−k and the naïve rule drifts low — is genuinely correct and the most useful part.

I found no material problem. The items below are refinements.

**Revision list**

1. **`[SHARPENING]` "How it fits": "Deliberately does not use discoverability (ASN-0098)" slightly overstates.** The note's prose leans on ASN-0098's **LP17** (an orphaned link persists in `dom(Σ.L)` with value unchanged) and **LP18** (resurrection) to justify CN-ORPHAN — LP17 is the reason an orphan is still countable. Narrow the claim to what is true: the count excludes the `discoverable_from` *relation* specifically (the formal CN-ORPHAN dependency is FL-REACH, ASN-0121), while orphan-persistence and resurrection facts are inherited from ASN-0098. Don't say ASN-0098 is unused.

2. **`[SHARPENING]` Approach 7 (Persistence/recovery): the journaling-of-`Σ.L` discussion is scope-creep.** Durability of link creations/retractions belongs to ASN-0086's emit/nullify operations, not to this read-only count. Trim to the conclusion the count actually owns: it writes nothing; the in-memory `Σ.L`, the `nullified` set, the per-slot indexes, and any count cache are all **rebuildable hints**; nothing about the count survives a restart — recompute. Keep that; drop the generic append-log/replay framing for `Σ.L` itself.

3. **`[SHARPENING]` Approach 4: a "running cardinality" for `q*` reads like the stored counter CN-SNAP forbids.** Add one clause making it the same hint as approach 5's cache — maintained outside `Σ`, rebuildable from `Σ.L`, never authoritative. The maintenance rule (+1 per created addressable link incl. retractors, −k for newly-nullified targets) is correct; just label the aggregate a hint so it can't be mistaken for state.

4. **`[SHARPENING]` CN-STAB / "What must be built": name the reverse-orphan case the note dwells on.** A link whose *own* home-arrangement entry is removed (reverse-orphaned) still answers a *home-bounded* count, because `home(a)` is a projection of the permanent address and is unmoved by arrangement edits (dedicated evidence, Q17). The digest covers the principle (home = membership on the address projection) but never surfaces the case; one sentence makes it concrete.

Each Green-level claim in the digest is grounded in the evidence answers; nothing is fabricated, no altitude slips into types/signatures, and the recommended defaults (scan-first, set-by-address dedup, global epoch, single-store scope) are defensible.

VERDICT: CONVERGED
