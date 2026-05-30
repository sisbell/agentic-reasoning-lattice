# Review of ASN-0043

## REVISE

### Issue 1: CPP closing sentence duplicates the `s = h(a)` postcondition it precedes
**ASN-0043, L1c (CPP lemma closing paragraph and "Postcondition: `s = h(a)`")**: CPP closes with "The single `k₁ = 2` step seats the field-separating zero at position `#s + 1`, which is what the `s = h(a)` postcondition below records"; the postcondition then states "The third zero of `a` first appears at position `#s + 1` — the one seated by `k₁ = 2` ... Hence `s = h(a)`."
**Problem**: The same fact (third zero at position `#s + 1`, seated by `k₁ = 2`) is asserted in two adjacent paragraphs, with the earlier one forward-referencing the later ("which is what the ... postcondition below records"). The reader has to read the claim, see it deferred, then read it again. This is reviser drift accreted into the lemma's closing slot.
**Required**: Delete the preview from CPP's closing; let the postcondition state it once. Move the genuinely separate "no further `kⱼ = 2` is admissible" remark to wherever the chain's zero-count structure is actually used, or drop it if redundant with L1c's chain clause `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2`.

### Issue 2: Forward-pointing meta-prose justifying lemma ordering in L1c
**ASN-0043, L1c (paragraph preceding CPP)**: "This length premise is exactly what the following local lemma requires."
**Problem**: The sentence advances no reasoning; it only announces that the next lemma will use the premise just stated. This is the "prose justifies document ordering / forward pointer" pattern.
**Required**: Delete the sentence. CPP's own precondition (`p ≤ #t₀`, steps beyond `p`) already states what it requires.

### Issue 3: Non-load-bearing AllocatedSet apparatus in L11b freshness argument
**ASN-0043, L11b ("Construction of fresh `a'`")**: "...extending `dom(Σ.L)` ... beyond the existing initial segment of occupied siblings. This is precisely the shape that AllocatedSet's domain-embedding clause (ASN-0034) admits ... The least-`i` choice therefore preserves the initial-segment structure of the sibling stream in `Σ'`."
**Problem**: The freshness requirement discharged is `a' ∉ dom(Σ.L)`, which the very next clause supplies ("by choice"). No invariant in L0–L14 or L-fin requires the realized link-allocation domain to be an initial segment, and FSP's hypotheses (h1–h3) do not consult contiguity. The "least-`i`" device and the AllocatedSet initial-segment justification are therefore gratuitous — accreted reasoning that does not bear on existence of a conforming extension.
**Required**: Replace with: by L-fin `dom(Σ.L)` is finite and the sibling stream is infinite (T10a.7), so some `a⁽ⁱ⁾ ∉ dom(Σ.L)` exists; take it. Drop the initial-segment paragraph.

### Issue 4: Duplicated "remaining items" inventory
**ASN-0043, after FSP proof and in L11b conformance**: After FSP — "The remaining items — non-state-local invariants ... (L2, L4, L7, L8, L10, L13) — are proven once over all conforming states and require no per-state re-verification." In L11b — "the non-state-local items (L2, L4, L7, L8, L10, L13) and transition corollaries (L12a from L12) hold by their own proofs."
**Problem**: The same use-site inventory of the same six labels appears twice in different words. This is the "two paragraphs say the same thing" / "use-site inventory" pattern.
**Required**: State the non-state-local set once (e.g., at FSP) and have L11b/L9 simply cite it rather than re-enumerate.

### Issue 5: Downstream-consumer meta-prose embedded in FSP statement
**ASN-0043, FSP lemma statement (final sentence)**: "FSP places no constraint on the endset *targets* of `ℓ` — in particular `coverage(ℓ.type)` is left free, which is exactly the freedom L9 exploits."
**Problem**: The clause "which is exactly the freedom L9 exploits" names a downstream consumer rather than advancing the lemma's meaning — the definition-enumerates-consumers pattern. The factual half ("places no constraint on targets") is fine; the consumer annotation is noise.
**Required**: Trim to "FSP places no constraint on the endset targets of `ℓ`; in particular `coverage(ℓ.type)` is unconstrained." Let L9 state that it relies on this when it does.

### Issue 6: Redundant "Consequence — identification within a state" subsection
**ASN-0043, L11a**: "Within any single state `Σ.L` is a partial function, so an address names at most one link; the substantive content of L11a is that this within-state identification extends across allocation events."
**Problem**: That `Σ.L` is a partial function (one link per address within a state) is immediate from the `Σ.L : T ⇀ Link` definition and is not what L11a claims; L11a's claim (distinct events → distinct addresses) is already fully stated above. The subsection restates the trivial half and re-announces "the substantive content of L11a is..." — essayistic framing that does not extend the proof.
**Required**: Delete the subsection, or reduce to a one-clause note that within-state single-valuedness comes from the partial-function typing while L11a is the cross-event strengthening.

## OUT_OF_SCOPE

### Topic 1: Lifting L0a/L14a from the `s_C`-resident slice to all of `dom(Σ.C)`
**Why out of scope**: This depends on ASN-0036 absorbing a global content-subspace constant; the ASN correctly records it as an Open Question rather than asserting global disjointness. New territory for an ASN-0036 revision, not an error here.

### Topic 2: Whether conforming systems must implement subtype-aware query
**Why out of scope**: L10 characterizes only the structural affordance; query-interface obligations are a separate operations/interface concern, properly deferred.

VERDICT: REVISE
