# ASN-0024: Operational Fragmentation Bounds

*2026-02-26*

We are concerned with a question that Nelson's specification leaves largely implicit: as editing operations accumulate, how does the internal representation of a document's structure grow? The content itself grows monotonically — every INSERT appends bytes to I-space that are never removed. But the *mapping* from virtual positions to permanent content is another matter entirely. Each edit can split, add, or remove entries in this mapping. We want to know: what bounds hold on this fragmentation, and what structural guarantees must the system provide to any implementation?

The question matters because the mapping *is* the document. A document's V-space is not a copy of content — it is a finite sequence of correspondences between virtual positions and permanent I-addresses. The cost of storing, traversing, and reconstructing a document is proportional not to its content volume but to the number of these correspondences. We therefore need to understand how operations affect that count.

---

## 1. State and Fragmentation

We begin by fixing notation. Let Σ denote the system state. For a document *d* in its current version, we write Σ.M(*d*) for the V→I mapping: a finite sequence of *mapping entries*, each pairing a contiguous V-interval with a contiguous I-interval. We call the number of such entries the *fragmentation count*:

> frag(*d*) = #Σ.M(*d*)

A single mapping entry *e* ∈ Σ.M(*d*) asserts: "V-positions [*e*.v, *e*.v + *e*.w) correspond to I-addresses [*e*.i, *e*.i + *e*.w)." The entry is a pair of boundaries — two tumblers for the V-interval, two for the I-interval. Nelson makes this explicit:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

And critically, the size of this representation is independent of the interval's extent:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

This is our first property.

**F0 (Constant entry cost).** The representation cost of a single mapping entry is bounded by a constant independent of the content volume it spans. Formally, for any entry *e* ∈ Σ.M(*d*): cost(*e*) = *c* for some fixed *c*, regardless of *e*.w.

F0 is architectural, not an optimization. It follows from the span representation: a span is always two tumblers, whether it brackets one byte or one billion. The document's total representation cost is therefore *c* · frag(*d*) — directly proportional to the fragmentation count, independent of content volume.

We write content(*d*) for the total content volume:

> content(*d*) = (+ *e* : *e* ∈ Σ.M(*d*) : *e*.w)

The ratio content(*d*) / frag(*d*) measures the *average span length* — how much content each mapping entry covers. A freshly created document with a single contiguous insertion has frag(*d*) = 1 and arbitrarily large content(*d*). A heavily edited document might have frag(*d*) approaching content(*d*) in the worst case. Understanding what drives this ratio is the purpose of this note.

---

## 2. I-Space Monotonicity

Before analyzing per-operation fragmentation, we must state the foundational asymmetry. I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**F1 (I-space monotonicity).** Let Σ and Σ' be states before and after any operation. Then dom(Σ'.I) ⊇ dom(Σ.I), and for all *a* ∈ dom(Σ.I): Σ'.I(*a*) = Σ.I(*a*).

No operation removes or modifies I-space content. INSERT adds new I-addresses; DELETE removes V→I correspondences but leaves I-space untouched; COPY creates new V→I correspondences pointing to existing I-addresses without affecting I-space. This means that the "permanent" content store grows monotonically, and the only mutable structure is the per-document mapping Σ.M(*d*).

---

## 3. INSERT Fragmentation

Consider INSERT(*d*, *p*, *text*) — inserting content of width *n* at V-position *p* in document *d*. The operation has two effects on the mapping:

**(a) Gap creation.** If *p* falls strictly interior to some existing entry *e* — that is, *e*.v < *p* < *e*.v + *e*.w — then *e* must be split into two entries: a left fragment [*e*.v, *p*) and a right fragment [*p*, *e*.v + *e*.w), with the right fragment shifted to make room for the insertion. This adds one entry (one becomes two).

If *p* falls on an entry boundary (the reach of one entry equals the start of the next, or *p* is at the document's edge), no split occurs.

**(b) New content.** The inserted text occupies freshly allocated I-addresses and maps to V-positions [*p*, *p* + *n*). This requires one new mapping entry — unless the *coalescing condition* (Section 5) is satisfied, in which case an adjacent entry can be extended in place.

In the worst case — interior split plus no coalescing — we get:

**F2 (INSERT fragmentation bound).** For INSERT at position *p* in document *d*:

> frag'(*d*) ≤ frag(*d*) + 2

*Derivation.* The split contributes at most +1 (one entry becomes two). The new content entry contributes at most +1. Total: at most +2. Gregory's implementation confirms this ceiling precisely: the two-blade knife in `makegappm` produces at most two cuts in the V→I tree, and one new leaf is created for the inserted content [insertnd.c:144–146]. The second blade is structurally guaranteed to fall at a subspace boundary, not interior to an existing entry, so only one actual split occurs. ∎

We note that F2 is tight. An INSERT at a position strictly interior to a contiguous span, where the new I-addresses are not adjacent to any existing entry, achieves exactly +2. The bound cannot be lowered without additional assumptions.

---

## 4. DELETE Fragmentation

Consider DELETE(*d*, [*p*, *q*)) — removing content at V-positions [*p*, *q*) from document *d*. This is more subtle than INSERT, because it both creates and destroys entries.

**(a) Boundary splits.** If *p* falls strictly interior to an entry, that entry is split (the portion before *p* survives, the portion from *p* onward is affected). Similarly for *q*. Each interior boundary produces at most one split, contributing at most +1 each.

**(b) Removal.** All entries fully contained within [*p*, *q*) are removed from the mapping. This reduces frag(*d*) by the number of such entries.

The net effect depends on the geometry. We enumerate the cases:

*Case 1: Both boundaries interior to the same entry.* The entry [*a*, *b*) with *a* < *p* < *q* < *b* is cut twice, producing [*a*, *p*), [*p*, *q*), and [*q*, *b*). The middle fragment is then removed. Result: one entry becomes two. Net: +1.

*Case 2: Both boundaries interior to different entries, with zero or more entries between.* The left boundary splits its entry (+1), the right boundary splits its entry (+1), all entries fully between are removed (−*m* for *m* ≥ 0), and the two interior fragments of the split entries are also removed (−2, one from each split entry's interior portion). Net: +2 − *m* − 2 = −*m* ≤ 0.

Wait — we must be more careful. When the left boundary splits entry *e*₁ = [*a*₁, *b*₁) at *p*, we get [*a*₁, *p*) (survives) and [*p*, *b*₁) (falls within the deletion range, so removed). Similarly, when the right boundary splits entry *e*₂ = [*a*₂, *b*₂) at *q*, we get [*a*₂, *q*) (within range, removed) and [*q*, *b*₂) (survives). So the two boundary entries each contribute one surviving fragment and one removed fragment: net change from boundary splits is 2·(+1) − 2·(1) = 0. The *m* fully-interior entries are also removed: net −*m*. Total: −*m* ≤ 0.

*Case 3: One boundary interior, one on a boundary.* One split (+1), the interior fragment is removed (−1), plus removal of any fully-interior entries (−*m*). Net: −*m* ≤ 0.

*Case 4: Both boundaries on entry boundaries.* No splits. Pure removal of covered entries. Net: −*m* ≤ 0.

The worst case is Case 1 — both boundaries interior to the same entry — which gives exactly +1.

**F3 (DELETE fragmentation bound).** For DELETE of span [*p*, *q*) from document *d*:

> frag'(*d*) ≤ frag(*d*) + 1

*Justification.* Case 1 achieves the bound; all other cases yield non-positive net change. Gregory's implementation confirms: when both deletion boundaries are THRUME within the same bottom crum, `slicecbcpm` fires twice (producing three fragments from one), then Phase 2 removes the interior fragment, leaving a net increase of exactly 1 [edit.c:31–76]. ∎

This bound is also tight. Deleting a strict interior subspan of a single contiguous entry always fragments it permanently.

---

## 5. Coalescing: The One Defense

Both F2 and F3 are worst-case bounds. In practice, a crucial optimization prevents fragmentation during the most common editing pattern: sequential appending.

When new content is inserted at a position *p* that coincides with the right boundary of an existing entry *e* — i.e., *p* = *e*.v + *e*.w — and the new content's I-address is the immediate successor of *e*'s I-reach — i.e., the new I-origin equals *e*.i + *e*.w — and the content has the same provenance (same originating document), then no new entry is created. Instead, *e*'s width is extended to absorb the new content.

We define this precisely.

**F4 (Coalescing condition).** Let *e* be an existing entry in Σ.M(*d*) and let (*p*, *i*, *w*, *h*) describe the new content to be inserted at V-position *p* with I-origin *i*, width *w*, and provenance *h*. Coalescing occurs when all three conditions hold simultaneously:

> (i) *p* = *e*.v + *e*.w — the new content abuts *e*'s right V-boundary
> (ii) *i* = *e*.i + *e*.w — the new I-address is I-contiguous with *e*'s reach
> (iii) *h* = *e*.h — the provenance matches

When F4 holds, the operation produces zero new mapping entries: frag(*d*) is unchanged.

Gregory's implementation realizes this in `isanextensionnd` [insertnd.c:301–309], which checks exact tumbler equality of the reach-origin pair across both V and I dimensions, plus homedoc matching. The function fires identically for INSERT and COPY — there is no codepath distinction. For sequential single-character typing, all three conditions are naturally satisfied: the V-position advances by one, the granfilade allocates the next sequential I-address, and the provenance is the same document. One hundred sequential keystrokes produce a single mapping entry of width 100.

**This is the system's sole mechanism for preventing fragmentation.** It is proactive (operates at insertion time), forward-only (extends rightward), and conditional (all three criteria must hold). It is not a compaction pass, not a background optimization, and not retroactive. Once an entry is split, no mechanism reconstitutes it.

---

## 6. COPY Fragmentation

COPY(*source*, *d*, *p*) transcludes content from a source specification into document *d* at V-position *p*. The source content, when resolved against its home document's V→I mapping, may correspond to *g* non-contiguous I-regions. We call *g* the *source fragmentation* of the copy.

**F5 (COPY fragmentation bound).** For COPY of content with source fragmentation *g* into document *d* at position *p*:

> frag'(*d*) ≤ frag(*d*) + *g* + 1

*Derivation.* The gap creation at position *p* can split one existing entry, contributing at most +1 (by the same argument as INSERT's gap creation). The *g* I-regions from the source each become at most one new mapping entry in the target. Coalescing (F4) can reduce this, but in the worst case no coalescing fires. Total: at most *g* + 1. ∎

Two consequences deserve emphasis.

First, F5 is independent of content volume. A COPY that transcludes a million bytes from a single contiguous source region has *g* = 1 and costs at most 2 new mapping entries. A COPY that transcludes ten bytes from ten non-contiguous regions has *g* = 10 and may cost up to 11 entries. Representation cost tracks structural complexity, not size. Nelson states this explicitly:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

Second, the *g* I-regions from the source cannot coalesce with *each other*, since they are by definition non-contiguous in I-space. Coalescing can occur only between a source region and a pre-existing entry in the target that happens to be both V-adjacent and I-adjacent. Gregory confirms this strict 1-to-1 pipeline: the source POOM traversal produces exactly *g* contexts, each becomes exactly one I-span, and each is inserted independently [orglinks.c:425–454, insertnd.c:242–275].

---

## 7. The Absence of Compaction

We now arrive at a property that is not a bound but a structural constraint: the system provides no mechanism for retroactive defragmentation.

**F6 (No retroactive compaction).** No operation merges two existing mapping entries in Σ.M(*d*) into one. Once an entry is split, the fragments persist as separate entries indefinitely.

This is not a prohibition that must be enforced — it is a consequence of the architecture. Merging two entries would require discovering that they are both V-adjacent and I-adjacent with matching provenance, then combining them. No operation inspects existing entries for this condition after their creation. The coalescing mechanism (F4) operates only at insertion time, comparing the *new* content against *existing* entries.

The evidence from Gregory is unambiguous. The rebalancing machinery (`recombinend`) operates on the tree's internal nodes — it redistributes bottom-level entries among their parent containers but never inspects, merges, or splits bottom-level entries themselves [recombine.c:104–131]. The function `levelpull`, which might reduce tree height, is entirely disabled [genf.c:318–342]. A search across the implementation for any compaction, merge, or defragmentation logic finds none.

F6 means that fragmentation is *monotonically non-decreasing* in the absence of DELETE:

> (A Σ, Σ' : Σ' results from INSERT or COPY applied to Σ : frag'(*d*) ≥ frag(*d*))

DELETE can reduce frag(*d*) by removing fully-covered entries (Cases 2–4 in Section 4), but it can never merge the surviving fragments. The total number of "scars" — points where previously contiguous entries were split — only grows.

---

## 8. The Irreversibility of Fragmentation

A deeper consequence of F6 emerges when we consider the interaction of INSERT and DELETE. One might expect that inserting content and then deleting it restores the original state. It does not.

**F7 (Delete-insert irreversibility).** If INSERT(*d*, *p*, *text*) splits an existing entry at interior position *p*, and subsequent DELETE(*d*, [*p*, *p* + |*text*|)) removes the inserted content, the resulting fragmentation count satisfies:

> frag''(*d*) = frag(*d*) + 1

*Derivation.* The INSERT at interior *p* splits one entry into two and adds one for the new content: frag → frag + 2. The DELETE removes the new-content entry (it is exactly bounded by the deletion range) and makes no further splits (both deletion boundaries fall on entry boundaries created by the INSERT). So frag + 2 → frag + 2 − 1 = frag + 1. ∎

The "scar" at position *p* is permanent. The original entry [*a*, *b*) has become [*a*, *p*) and [*p*, *b*), and although these two fragments are V-adjacent (after the deletion shifts the right fragment back), they have a gap in I-space: the I-addresses allocated for the now-deleted content lie between them. No mechanism can bridge that I-gap.

What about repeating this cycle? Gregory's analysis shows the system reaches a *fixed point* after the first cycle. On the second INSERT at the same position *p*, the insertion point falls on the boundary between the two fragments — no split occurs (the boundary is exact, not interior). The new content creates one entry (+1). The subsequent DELETE removes that entry (−1). Net: zero. All cycles beyond the first are structurally neutral.

**F8 (Edit cycle convergence).** For *K* ≥ 1 cycles of INSERT followed by DELETE of the same span at the same interior position *p*:

> frag(*d*) after *K* cycles = frag₀(*d*) + 1

The fragmentation "cost" of exploring an edit is exactly one permanent entry, paid on the first attempt and never again.

---

## 9. Cumulative Bounds

We can now derive aggregate bounds over arbitrary operation sequences.

Let *σ* = *o*₁, *o*₂, ..., *o*ₖ be a sequence of *k* operations applied to document *d* starting from frag₀(*d*). Each operation *o*ⱼ is either INSERT, DELETE, or COPY with source fragmentation *g*ⱼ.

From F2, F3, and F5, applying the bounds cumulatively:

> frag(*d*) ≤ frag₀(*d*) + (+ *j* : *o*ⱼ is INSERT : 2) + (+ *j* : *o*ⱼ is DELETE : 1) + (+ *j* : *o*ⱼ is COPY : *g*ⱼ + 1)

Simplifying for the case where all source fragmentations are 1 (contiguous copies) and starting from frag₀ = 1 (a fresh document with one initial span):

> frag(*d*) ≤ 1 + 2·*k*_ins + *k*_del + 2·*k*_copy

This is **linear in the number of operations**. The fragmentation count cannot grow faster than the number of edits. We state this as:

**F9 (Linear fragmentation bound).** After any sequence of *k* operations (INSERT, DELETE, COPY) applied to a document starting from initial fragmentation frag₀:

> frag(*d*) ≤ frag₀ + 2*k* + (+ *j* : *o*ⱼ is COPY : *g*ⱼ − 1)

where the summation term accounts for high-fragmentation copies contributing more than 2 per operation.

This bound is pessimistic — it does not account for coalescing (which prevents fragmentation during sequential editing) or for DELETE's ability to remove entries (Cases 2–4). The bound captures worst-case adversarial editing. Practical fragmentation is typically far lower, because sequential typing is the dominant editing pattern and F4 coalescing suppresses its fragmentation entirely.

---

## 10. Version Proportionality

Nelson requires that any version be reconstructable efficiently:

> "We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

This demand constrains the relationship between a version's representation and the total edit history.

**F10 (Version representation independence).** The representation size of version *v* of document *d* is proportional to frag(*d*, *v*) — the fragmentation count of that version's mapping — and is independent of the total number of edits ever applied across all versions of *d*.

*Justification.* Each version has its own V→I mapping. By F0, the representation cost is *c* · frag(*d*, *v*). The mapping for version *v* is determined by *v*'s content arrangement alone. Edits to other versions create entries in *those* versions' mappings and append content to I-space, but they do not alter *v*'s mapping. Nelson's separation of I-space (shared, append-only) from V-space (per-version, mutable) is precisely what achieves this independence. ∎

If version retrieval degraded with the total edit count — say, requiring traversal of all *k* edits to reconstruct version *v* — then a heavily-edited document would eventually violate Nelson's "virtually instantaneous" requirement. F10, together with the soft corridor's demand for at most logarithmic slowdown [LM 4/2], ensures that the cost of accessing any version depends on that version's structural complexity, not on the document's editorial history.

---

## 11. Document Isolation

**F11 (Document isolation).** Operations on document *A* do not change frag(*B*) for any document *B* ≠ *A*.

*Justification.* Every editing operation (INSERT, DELETE, COPY, REARRANGE) targets a single document by its identifier. The operation specification describes effects on that document's V-space only:

> "This inserts ⟨text set⟩ in document ⟨doc id⟩ at ⟨doc vsa⟩." [LM 4/66]
> "This removes the given span from the given document." [LM 4/66]

No side effects on other documents' mappings are described or implied. INSERT adds I-space content (shared infrastructure) but does not modify any other document's V→I mapping. COPY reads the source's mapping but writes only to the target's. DELETE operates entirely within one document's V-space. ∎

F11 is reinforced by Nelson's ownership model:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

If Alice's edits to document *A* could fragment Bob's document *B*, Alice would be modifying Bob's property without consent — violating the absolute ownership guarantee.

We note one qualification: system-level indexes (such as the structures supporting FINDDOCSCONTAINING) may record cross-document relationships and grow when transclusions are created. These are system infrastructure, not part of any individual document's structural description. F11 concerns Σ.M(*d*), not global indexes.

---

## 12. Transclusion Volume Independence

We can now state the efficiency guarantee for transclusion as a direct corollary of F0 and F5.

**F12 (Transclusion volume independence).** The fragmentation cost of transcluding content from a source into a target document depends on the number of contiguous I-regions in the source (*g*), not on the total byte volume of the transcluded content.

Transcluding one million contiguous bytes costs the same as transcluding one contiguous byte: a single mapping entry. Nelson describes this as fundamental:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update." [LM 2/36]

This is what makes the system's treatment of large-scale document assembly viable. A compound document built from *k* transclusions of contiguous source regions has frag(*d*) = *k* regardless of whether those regions collectively reference kilobytes or terabytes. The mapping *is* the list of references, and each reference is constant-size.

---

## 13. The Soft Corridor and Time Bounds

We have thus far analyzed space bounds — how many mapping entries exist. Nelson's explicit performance requirement addresses time:

> "An ever-growing network, instantaneously supplying text and graphics to millions of simultaneous users, would be impossible if it slowed down too fast as it grew. (It can't be linear. The system cannot slow down by half as its size doubles.)" [LM 4/2]

The soft corridor requires that operation time degrade at most logarithmically with system size. How does this interact with fragmentation?

If mapping entries are stored in a balanced tree with branching factor *b*, then for frag(*d*) = *n* entries, operations on document *d* require O(log_b(*n*)) tree traversals. By F9, *n* ≤ O(*k*) for *k* operations, so per-operation time is O(log *k*) — well within the soft corridor.

The critical observation is that Nelson specifies the soft corridor as a *time* bound, not a *space* bound. He does not require that representation size grow sub-linearly with operations — only that per-operation time remain logarithmic in the total system size. F9's linear space bound, combined with logarithmic tree access, satisfies this.

Gregory's implementation achieves O(log₆(*n*)) tree height for *n* POOM entries, with height bounded by ⌈log₆(*n*/4)⌉ + 2 [enf.h:26–28, genf.c:263–294]. The asymmetric split strategy (peeling one child rather than halving) does not degrade this bound — the overflow threshold at the root still requires 6× capacity per level, ensuring logarithmic height regardless of subtree imbalance.

---

## 14. What Nelson Does Not Guarantee

We must be precise about what this analysis establishes and what it does not.

Nelson specifies the *semantic effects* of operations and the *performance character* of the system (soft corridor, virtually instantaneous version retrieval, indefinite scaling). He does not specify per-operation space complexity. The bounds F2, F3, F5 are *consequences* of the span-based architecture — they follow from the mathematical structure of contiguous-range mappings. They are not stated requirements in Literary Machines.

Specifically:

**(a) No explicit space complexity.** Nelson's performance discussion [LM 4/2] addresses time degradation curves, not representation size growth. The soft corridor constrains how fast the system may slow down, not how large it may grow.

**(b) No compaction requirement or prohibition.** Nelson neither requires nor forbids defragmentation. F6 (no retroactive compaction) is an observation about what the architecture *implies*, not a stated constraint. An alternative implementation could maintain a compaction pass without violating any of Nelson's explicit requirements — though it would need to preserve all other guarantees (permanent addresses, version retrievability, etc.).

**(c) I-space growth is unbounded by design.** Nelson explicitly embraces unbounded growth in I-space — it is the price of permanent addresses and historical backtrack:

> "Any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The economic counterbalance is storage rental paid by the document owner [LM 4/5], not structural compaction.

---

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| F0 | The representation cost of a single mapping entry is bounded by a constant independent of the content volume it spans | introduced |
| F1 | dom(Σ'.I) ⊇ dom(Σ.I) and content is immutable: I-space only grows | introduced |
| F2 | INSERT increases frag(*d*) by at most 2 | introduced |
| F3 | DELETE increases frag(*d*) by at most 1 | introduced |
| F4 | Coalescing occurs when the new entry is V-adjacent, I-contiguous, and provenance-matching with an existing entry; frag unchanged | introduced |
| F5 | COPY of source with fragmentation *g* increases frag(*d*) by at most *g* + 1 | introduced |
| F6 | No operation retroactively merges two existing mapping entries | introduced |
| F7 | INSERT at interior *p* followed by DELETE of the same content yields frag(*d*) = frag₀(*d*) + 1 | introduced |
| F8 | *K* ≥ 1 insert-delete cycles at the same interior position yield frag₀ + 1, converging after the first cycle | introduced |
| F9 | frag(*d*) ≤ frag₀ + 2*k* + Σ(*g*ⱼ − 1) after *k* operations: linear in operation count | introduced |
| F10 | Version *v*'s representation size depends on frag(*d*, *v*), not on total edit count across versions | introduced |
| F11 | Operations on document *A* do not change frag(*B*) for *B* ≠ *A* | introduced |
| F12 | Transclusion cost depends on number of contiguous source I-regions, not on content volume | introduced |

## Open Questions

- Must an implementation provide a coalescing mechanism equivalent to F4, or is coalescing merely an optimization that well-behaved implementations should offer?
- What fragmentation bounds must hold for REARRANGE, which transposes two regions of a document's V-space?
- If a system-wide content index (supporting FINDDOCSCONTAINING) grows when transclusions are created, what bounds must hold on that index's growth per operation?
- Under what conditions, if any, may an implementation compact a document's V→I mapping without violating permanent address guarantees?
- Must the ratio content(*d*) / frag(*d*) remain above some minimum for the system to satisfy the soft corridor, or is logarithmic tree access sufficient regardless of fragmentation?
- What fragmentation bounds must hold for the link index, given that links reference I-addresses and survive editing of the documents they attach to?
- Does the coalescing condition F4 require exact I-contiguity, or could an alternative weaken this to allow small gaps while preserving correctness?
