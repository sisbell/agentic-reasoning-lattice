# Channel Assignment — ASN-0126 review-26

**Date:** 2026-06-09 08:32

## Issue 1: The gate-vs-landing (enablement vs active-subset) distinction is restated four-plus times
Reason: Pure editorial trim — remove redundant restatements and reduce P4/P6 to pointers. The distinction and its concrete witness are already fully present in the note; no design intent or implementation evidence is at stake.

## Issue 2: L4/L9 ghost / no-residence-check inheritance stated in full twice
Reason: Deduplication of inherited L4/L9 commitment, keeping the statement in Shape-conformance where it grounds P5. The Nelson "endset addresses do NOT need to resolve" quote is preserved in the surviving paragraph, so no new consultation is needed.

## Issue 3: C0 prose explains why the axiom is needed rather than stating it
Reason: Drop counterfactual justification and meta-commitment paragraph; state C0 plus its one decidability consequence. The decidability payoff is already established one paragraph earlier, so the fix is fully internal.

## Issue 4: Defensive asides reassuring the reader the substrate is not "refusing"
Reason: Remove reassurance clauses that restate facts already carried elsewhere (off-gate availability in Single-source, wp-coincidence in the formal statement). Purely subtractive; derivable from the ASN alone.

## Issue 5: The abutting-span resolution is over-justified
Reason: Keep the set-cardinality rule and P5 note, cut the Gregory implementation trace to a bare citation. The formal content is forced by `Endset = 𝒫_fin(Span)`; the surviving citation retains Gregory's attribution, so no fresh consultation is required.
