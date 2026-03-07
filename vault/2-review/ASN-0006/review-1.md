# Review of ASN-0006

## REVISE

### Issue 1: Self-transclusion makes TC4 and TC7 contradictory
**ASN-0006, Frame conditions**: TC4 states `poom'(source_doc) = poom(source_doc)` and TC7 states that the target's POOM gains new mappings at position p with subsequent positions shifted.
**Problem**: When source = target (a document transcludes from itself), TC4 demands the POOM be unchanged while TC7 demands it be modified. The conjunction is unsatisfiable. The ASN neither excludes self-transclusion by precondition nor reformulates the frame to accommodate it.
**Required**: Either add an explicit precondition `source_doc ≠ target`, or reformulate TC4 and TC7 so that the source-read happens before the target-write (i.e., the I-addresses are extracted from the pre-state POOM, and the post-state POOM reflects only the target modification). The latter is the stronger specification because self-transclusion is a legitimate operation.

### Issue 2: Transclusion independence proof cites TC5 and TC6 beyond their scope
**ASN-0006, Independence of transclusions**: "D's DELETE operates on D's POOM alone (by TC5, operations on D do not modify B's POOM). The I-addresses in A remain in dom.ispace (by I-space permanence — no operation removes addresses from the permanent store)."
**Problem**: TC5 says "**COPY** does not modify the POOM of any document other than the target." TC6 says "**COPY** does not modify ispace." Both are COPY-specific frame conditions. The proof applies them to DELETE and INSERT, which are different operations. The prose in the state definition ("once an address enters dom.ispace, it remains forever") makes the general claim, but it is not formalized. The proof needs two general system axioms: (a) every operation's POOM modification is confined to at most one document, and (b) no operation removes addresses from dom.ispace or mutates ispace content. Neither is stated as a labeled, general property.
**Required**: Introduce and label the two general axioms inline (not by cross-reference). Then cite those axioms — not TC5 and TC6 — in the transclusion independence proof and the INSERT isolation corollary.

### Issue 3: COPY has no stated precondition
**ASN-0006, The COPY operation / Formal summary**: The operation is specified by effects (TC1, TC9), frame (TC4–TC8), and index registration (TC10), but no precondition is stated.
**Problem**: At minimum, COPY requires: the source document exists, the source V-span is within the source POOM's domain, the target document exists, and the insertion position is valid for the target. Without a precondition, the postconditions are vacuously satisfiable (an operation with precondition FALSE satisfies any postcondition). The formal summary lists "Effect" and "Frame" but no "Precondition."
**Required**: State the precondition explicitly. Include at least: source and target documents exist, source V-span resolves to a non-empty set of I-addresses in the source POOM, and insertion position p is within `[0, size(target)]`.

### Issue 4: TC12 is formally identical to TC11
**ASN-0006, Links follow content**: TC11 states `a ∈ endsets(L) ∧ (E p : poom(B).p = a) ⟹ L ∈ discoverable_links(B)`. TC12 states `(E p : poom(B).p = a) ∧ a ∈ endsets(L) ⟹ L ∈ discoverable_links(B)`.
**Problem**: These are the same formula (conjunction commutes). TC12's prose claim — that discoverability holds "regardless of the state of any other document's POOM" — is not captured in the formalization. To say what TC12 intends, the formula would need universal quantification over other documents' POOM states, or an explicit appeal to a general cross-document isolation axiom (which, per Issue 2, is not formalized).
**Required**: Either merge TC12 into TC11 with an added prose remark about deletion-independence, or give TC12 a genuinely distinct formalization that captures the "regardless of other documents' state" claim — which requires the general isolation axiom from Issue 2.

### Issue 5: `discoverable_links` and `endsets` are not defined
**ASN-0006, Links follow content**: TC11 uses `discoverable_links(B)` and `endsets(L)` as primitive terms.
**Problem**: `discoverable_links(B)` is never formally defined. The prose describes the mechanism (convert V-spans to I-spans, query span index), but the predicate itself has no definition. Without one, TC11 is a tautology — it defines discoverability as "whatever TC11 says." Similarly, `endsets(L)` is ambiguous: a link has three endsets (from, to, type). Does `endsets(L)` mean the union of all three? Any one? This matters because a link's "type" endset may reference I-addresses that are categorically different from "from" and "to" endsets.
**Required**: Define `discoverable_links(B)` in terms of the state (ispace, poom, spanindex, links). Clarify whether `endsets(L)` is the union of all three endsets or a specific subset.

### Issue 6: No concrete example
**ASN-0006, throughout**: The ASN introduces 22 properties but verifies none against a specific scenario.
**Problem**: A concrete trace — e.g., document A contains "HELLO" at I-addresses [1.0.1.0.1.1, 1.0.1.0.1.5], document B has "XY" at I-addresses [1.0.2.0.1.1, 1.0.2.0.1.2], COPY A's [0,5) to B at position 1 — would exercise TC1 (B's new mappings reference A's I-addresses), TC7 (B's "Y" shifts from position 1 to position 6), TC9 (contiguous case, k=1), TC10 (span index gains entry for B), and TC13 (home of copied addresses is still A). Without such a trace, the properties are never tested against each other for consistency.
**Required**: Add at least one concrete scenario that traces through the key postconditions (TC1, TC7, TC9, TC10) with specific addresses and positions, and verify them against each other.

## OUT_OF_SCOPE

### Topic 1: Atomicity of multi-span COPY
**Why out of scope**: The ASN correctly identifies this as an open question. Atomicity semantics (all-or-nothing vs. partial observability) require a concurrency model that this ASN does not (and should not) introduce.

### Topic 2: Tiling invariant preservation
**Why out of scope**: The ASN works at the level of `poom : Pos → Addr` (the function), not at the span-representation level. TC22 explicitly declares representation transparency. Tiling is a representation invariant, not a semantic one at this abstraction level. A future ASN on V-space representation could formalize tiling.

### Topic 3: Economic model granularity
**Why out of scope**: TC18 states the principle (compensation follows identity). The granularity question (per-byte vs. per-span vs. per-delivery) is an economic-model concern, not a transclusion-mechanism concern. Correctly deferred to Open Questions.

VERDICT: REVISE
