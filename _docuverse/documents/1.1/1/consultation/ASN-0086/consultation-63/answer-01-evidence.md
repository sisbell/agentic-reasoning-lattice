## Question 1 [evidence]

> Does ASN-0093 provide a named lemma (e.g., DisjointSubAllocatorChains, CrossDocDisjointness) that delivers `inc(ℓ_prev, 0)` distinctness against `dom(L)` elements homed at d' ≠ d, or is cross-home freshness derivable only as a postcondition of K.λ's contract (via the L1a NUDE-prefix projection plus ChainPrefixExtension)?

## KB Synthesis

The KB does not contain information sufficient to answer this question.

The KB confirms the **behavioral property** you're asking about — cross-document allocation independence — but contains no information about ASN-0093's internal lemma structure, K.λ as a named contract, NUDE-prefix projections, or ChainPrefixExtension.

What the KB *does* establish:

From [SS-ADDRESS-ALLOC] (Finding 0065): link I-address allocation is bounded to `docISA.2.3` as upper bound, making each document's link subspace independent. "The allocation postcondition for MAKELINK is: the new link's I-address is strictly greater than all existing link I-addresses in the same document, and **independent** of link I-addresses in other documents."

From [SS-ADDRESS-SPACE] (Finding 0077): allocation is a family of independent functions partitioned by tumbler range — there is no single `Σ.next` counter, so cross-document distinctness falls out structurally from bounded `findpreviousisagr` searches over disjoint subranges.

From [INV-MONOTONIC] (Finding 0065): per-document monotonicity holds independently across documents.

These establish that cross-home freshness is a **structural consequence of bounded allocation ranges**, but whether ASN-0093 surfaces this as a named lemma versus derives it as a postcondition of K.λ's contract is not answerable from this KB. You would need to read ASN-0093 directly.

---

## Code Exploration

The search is conclusive. Let me report what the code and knowledge base actually contain.

---

## Answer

**ASN-0093 does not exist in this repository.** The document number, all three named lemmas (`DisjointSubAllocatorChains`, `CrossDocDisjointness`, `ChainPrefixExtension`), and all the formal-notation terms in the question (`K.λ`, `L1a`, `NUDE-prefix`, `inc(ℓ_prev, 0)`, `ℓ_prev`, `cross-home freshness`, `sub-allocator`) return **zero matches** across every file in `knowledge-base/`, `findings/`, `docs/`, and `backend/`.

The question's framing — lemma names, K.λ contract, L1a NUDE-prefix projection — belongs to a formal specification system that is not present in this codebase.

### What the code *does* say about related concepts

**Cross-document I-address disjointness** is stated informally in `knowledge-base/kb-formal.md:6790`:

> `create_document produces a document with I-positions disjoint from all existing I-positions.`

That sentence is the entirety of what the knowledge base asserts. It is a **postcondition of `create_document`**, not a named lemma.

**Freshness / non-collision** for intra-document allocation appears at `knowledge-base/kb-formal.md:3166`:

> `fresh I-addresses are disjoint from all previously allocated I-addresses.`

And the mechanism is characterized at `knowledge-base/kb-formal.md:2620` (matching `analyzed/0042.md:37`):

> *"This property (freshness) is guaranteed by sequential execution rather than by an explicit uniqueness check. A formal spec should state the freshness precondition explicitly even though the implementation achieves it structurally."*

The C implementation backing this is monotonic increment in `granf2.c` (`findisatoinsertmolecule` / `inserttextgr`), which walks the granfilade to find the highest allocated address and returns `max + 1`. There is no cross-document allocator registry; each document's granfilade is independent.

### Direct answer to the question

No, ASN-0093 does **not** provide a named lemma — it does not exist here. Cross-home freshness (the claim that a new I-address in document `d` is distinct from all I-addresses in documents `d' ≠ d`) is not established by any named lemma in this codebase. It is not established by a named postcondition either. The knowledge base asserts the **fact** (disjoint I-positions per document) as an observation from golden tests [`knowledge-base/kb-formal.md:6790`], but provides no proof structure — no chain of lemmas, no NUDE-prefix projection, no ChainPrefixExtension. The implementation achieves it structurally through per-document granfilades with no shared counter, but the formal derivation the question asks about does not exist in this repository.

If you want to formalize it, the nearest foothold is [`kb-formal.md:6790`] as the invariant and [`kb-formal.md:2620`] as the mechanism note. A proof would need to be constructed from scratch — it is not already here.
