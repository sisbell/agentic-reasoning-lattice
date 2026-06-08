# Review of ASN-0113

The mathematics is sound. I checked the extent-span construction (W2/W3), exact coverage (W4) including the non-vacuous depth-3 application of T5, subspace confinement (W10), disjointness (W11), the partition (W16), the faithful-count premises for content vs. links (W20), and the weakest-precondition characterization (W19) — all hold. The note is even self-aware about which worked instances exercise which proof steps (the m_S=2 collapse vs. the depth-3 prefix-confinement case), which is good rigor.

The findings are confined to the redundancy this note's anti-bloat classifier targets: the result-type thesis is established three separate times.

## REVISE

### Issue 1: The "result is a two-kind span-set" thesis is stated twice with the same citation

**ASN-0113, "The substrate we measure" intro vs. "What the caller must be handed"**: The intro already discharges the result type — "Nelson fixes the shape exactly. RETRIEVEDOCVSPANSET 'returns a span-set indicating both the number of characters of text and the number of links'… First, the result is a *span-set*… Second, the spans report *two distinct kinds*." The later section re-opens the identical point with the identical quote: "Nelson fixes it: a *span-set*… whose two members indicate 'the number of characters of text and the number of links' (4/68)."
**Problem**: Two paragraphs in different sections say the same thing (result is a two-member span-set, one per kind) with the same Nelson 4/68 citation. This is the "two paragraphs say the same thing in different words" pattern. The intro motivates; the W0 section should *fix the type* and move on, not re-motivate.
**Required**: Strip the re-motivation from "What the caller must be handed" down to the W0 commitment itself (type = normalized span-set ≤ 2 members; `⟨⟩` for doubly-empty), letting the intro carry the Nelson framing.

### Issue 2: "The count is read off the boundary" is pre-stated, then restated

**ASN-0113, "What the caller must be handed" vs. "The count is read off the boundary"**: The former pre-states the mechanism — "each member span's *extent* encodes the count of its subspace, because the positions in a subspace form a dense run (D-SEQ★) whose cardinality is exactly the width of the covering span. The number is read off the boundary, not stored as a tally." The single-subspace section then derives the same point with overlapping citations — "Because the run is dense, `n_S` is recoverable from the span alone… This is how a span-set 'indicates the number' (4/68) without designating a number directly (4/24)."
**Problem**: The count-from-boundary reconciliation appears in both places with the same 4/68 / 4/24 citations. The proper home is the single-subspace derivation (after W2/W3 supply `δ(n_S, m_S)`); pre-stating it in the type section is essay content pre-empting the derivation.
**Required**: Remove the pre-statement from "What the caller must be handed"; keep the derivation at its natural site once the width tumbler exists.

### Issue 3: "Permanence of the report" largely re-derives W8

**ASN-0113, "Permanence of the report"**: "Permanence is therefore *inherited, not primitive* — it descends from the stability of the state, not from any property the operation contributes."
**Problem**: W18's substantive increment over W8 is exactly one clause ("changes only when `M(d)` changes"). The surrounding paragraphs restate pure-query/state-dependence (already W8) in essayistic form. The meta-commentary about permanence being "inherited, not primitive" adds no claim beyond W8 + the one clause.
**Required**: Compress to the increment: W18 = W8 plus "the report changes iff a transition reshapes `M(d)`." Drop the inherited-vs-primitive exposition.

## OUT_OF_SCOPE

### Topic: Derivability from a single overall extent; permanence across forks/transclusion
**Why out of scope**: The open questions correctly defer these (single overall extent is ASN-0112; fork/transclusion permanence is future territory). The note does not smuggle claims about them into the body — it states them as open questions, which is the right disposition. No action needed.

VERDICT: REVISE
