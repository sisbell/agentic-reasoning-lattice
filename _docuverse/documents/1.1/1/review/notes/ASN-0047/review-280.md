# Review of ASN-0047

## REVISE

### Issue 1: "Four components" undercount and missing L-permanence statement in the Permanence section

**ASN-0047, Permanence**: "We classify each component by the transitions it admits. Four components, three distinct permanence contracts."

**Problem**: The extended state is `Σ = (C, L, E, M, R)` — five components. The Permanence section then gives labeled permanence properties for C (P0), E (P1, P8), R (P2), and M (the arrangement-modes paragraph), but gives **no permanence statement for L at all**. The link store's immutability (L12) is only introduced later (Link allocation / Destruction confinement). Under the most charitable reading the "four" counts the permanent components {C, L, E, R} against three contract types — but even then L is the one permanent component lacking the P0/P1/P2-style property statement that the section establishes for every other permanent component. The parallel "P0 subsumes S0/S1 … and L12 extends ASN-0043's link immutability" is asserted in *Destruction confinement*, not here where the reader first meets the permanence taxonomy.

**Required**: State L's permanence (L12, or a P0-parallel) in the Permanence section alongside P0/P1/P2, and correct or disambiguate the "Four components" count so it matches the five-component state.

### Issue 2: K.μ~-FIX entry in *Properties Introduced* cites D-SEQ, not D-SEQ★

**ASN-0047, Properties Introduced table, K.μ~-FIX row**: "from D-SEQ + bijection cardinality (n'_S = n_S) + subspace preservation + length preservation (admissibility (iii)) fixing per-subspace depth"

**Problem**: The body derivation of K.μ~-FIX consumes the per-subspace **D-SEQ★** ("D-SEQ★ at the pre- and post-states gives `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`…"), not the foundation-level per-document D-SEQ. The extended state supersedes D-SEQ with D-SEQ★, so the unstarred citation in the summary table names the wrong (foundation) form.

**Required**: Change "D-SEQ" to "D-SEQ★" in the K.μ~-FIX table row.

### Issue 3: Nelson/Gregory exegesis and a worked scenario embedded inside the K.μ~ admissibility-clause definitions

**ASN-0047, Decomposition of K.μ~ (admissibility clauses (iii) and (v))**: e.g. "We are careful to claim no more than this. Clause (v) does not establish a global non-rearrangeability guarantee … A withdraw-and-re-add composite re-seats a link without violating any invariant: K.μ⁻ removes a link's V-position … two subsequent K.μ⁺_L steps re-append the two links in the opposite order … What is permanent is the link's *I-address* … Gregory's implementation places each link by append-at-end (`findnextlinkvsa`) … Nelson's 'permanent order of arrival' (LM 4/12) is therefore carried by the I-address subspace ordinal …" and, in clause (iii), "REARRANGE transposes contiguous regions within a document's flat, dense V-stream (Nelson 4/67) … the V-stream has no internal depth levels for content to be moved into."

**Problem**: The admissibility clauses (i)–(v) are a structural enumeration defining which π the operation admits. Embedded inside them is a ~150-word essay (link permanence, a fully worked withdraw-and-re-add re-seating walk-through, Gregory's `findnextlinkvsa`, Nelson LM 4/12 / 4/67 exegesis) that does not advance the clause definition — a reader tracing "what does clause (v) require?" must skip past it. This is essay content in a structural slot, the exact pattern the anti-bloat classifier flags.

**Required**: Reduce each clause to its definition plus a one-line independence note. Move the link-permanence / order-of-arrival discussion and the withdraw-and-re-add scenario to a dedicated prose paragraph (or fold the re-seating walkthrough into the existing link worked example, where Step 5 already exercises orphaning).

### Issue 4: Default-value convention for `M(d) = ∅` restated across three adjacent passages

**ASN-0047, The state model**: the `M(d) = ∅` off-domain convention appears in the Bridging lemma parenthetical ("`M(d) = ∅` when `d ∉ dom(M) = E_doc`"), again in the standalone *Notational convention (default value)* box ("the expression `M(d)` abbreviates the empty partial function `∅` … `M(d) = ∅` does not signal allocation status"), and a third time in the (†) discharge ("the default-value convention (`M(d) = ∅` for every `d ∉ E_doc`)").

**Problem**: Three statements within one section assert the same convention. The discriminating content (E_doc-membership, not `M(d) = ∅`, is the allocation test) is duplicated rather than stated once.

**Required**: State the default-value convention once (the *Notational convention* box) and have the Bridging lemma and (†) reference it rather than re-stating it.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link contraction
The Open Question on interior link withdrawal (compact-and-renumber `DELETEVSPAN` vs. the suffix-only K.μ⁻) is correctly deferred — modeling the implementation's interior-deletion renumbering is a future ASN, not a gap in this one's suffix-only contraction.

### Topic 2: Concurrency / serialization of link allocation
The Open Question on concurrent same-document allocation is appropriately a question, not a claim; concurrency is out of scope per the Scope section.

VERDICT: REVISE
