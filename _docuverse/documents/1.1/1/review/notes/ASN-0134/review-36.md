# Review of ASN-0134

This is strong, careful work. The conflict structure (H0–H3), the strict-implication chain for verdicts (V2) with explicit converse-failure witnesses, the first-emission boundary case in H2, the both-miss interleaving and its G2 analysis, and the §5 partition between model-intrinsic and serialization-borne invariants are all rigorous and correct. The worked traces (§7, §8) check out address-by-address. My findings are narrow.

## REVISE

### Issue 1: G1(i) claims chain-contiguity is step-preserved, contradicting W3 and §5

**ASN-0134, §4 (G1 proof, clause (i))**: "Per-state invariants are preserved by every single step (A6), hence hold at every state of every linearization with no appeal to a global order."

**Problem**: A6's package explicitly *contains* the chain-contiguity members `ChainMembershipForOrigin`/`L-ContiguousPrefix`. But §5 states the opposite of what G1(i) asserts about them: "those members hold at every state of 𝔼 but are **not** model-intrinsic in this section's sense — they are exactly W3's serialization-borne contiguity. *Every other* conjunct of A6 is kept by A0 alone." W3 likewise: dense chain contiguity "is serialization-borne." So "preserved by every single step ... no appeal to a global order" is true for the *model-intrinsic* conjuncts of A6 but **false for contiguity**, which the note itself classifies as needing per-home order. The blanket invocation of A6 in sentence 1 overclaims for precisely the hardest conjunct, and the very next sentence's "allocation invariants (... dense chain contiguity)" then re-establishes contiguity via the per-home frontier argument — so contiguity is covered twice, under two mutually contradictory justifications (step-local vs. per-home-serialized).

A secondary defect: A6 (reachable ⟹ canonical) is invoked in sentence 1 *before* validity is established in sentence 3 ("so the linearization is a valid execution"). Reachability of a linearization's states presupposes its steps are valid →_sh steps, so A6 cannot license per-state invariants until validity is in hand.

**Required**: Order the proof so validity comes first — per-home comparability + H0 + H1 secure frontier-freshness, reordering-invariance + M1 secure the rest — yielding "the linearization is a valid execution," hence reachable. *Then* invoke A6 for the per-state package, and scope sentence 1 to the model-intrinsic conjuncts only, with chain-contiguity carried by the frontier argument exactly as W3/§5 require. As written, G1(i) is internally inconsistent with the note's own §5.

### Issue 2: W0's motivation is mislabeled as its proof

**ASN-0134, §5 (prose after W0)**: "W0 is Nelson's deepest point about permanence, and it is worth quoting his reasoning because it is the proof: the permanence guarantees 'had to be operation-intrinsic, because a guarantee asserted as absolute cannot depend on a reconciliation mechanism the design leaves open.'"

**Problem**: The proof of W0 is already complete inside the claim statement ("Each step's effect either adjoins a fresh key ... or frames the store; no step removes a key or rewrites a value. ... Needs A0, nothing more"). The quoted Nelson sentence is a *design-intent* statement, not a mathematical derivation; asserting "it is the proof" is a category error. The classifier flags exactly this — meta-prose that a precise reader must skip past, here dressed as proof.

**Required**: Cut the "it is worth quoting his reasoning because it is the proof" framing; the proof stands in the claim. Keep the quote only if explicitly marked as motivation.

### Issue 3: Two sections defer to the same downstream open problem (mild)

**ASN-0134, §1 (A5)** "we defer it to Open Question 5" and **§6 (W4)** "closing the reader gap is the open problem A5 flagged."

**Problem**: Both the general-batch discussion (A5) and the run-contiguity discussion (W4) point at the same batch-atomicity / reader-gap open problem via a chain of deferrals — one of the flagged accretion patterns ("multiple paragraphs in different sections defer to the same downstream location"). Mild, but it compounds.

**Required**: State the reader-gap once at its natural home (A5) and let W4 reference it with a bare pointer, not a re-explanation.

## OUT_OF_SCOPE

None. The Open Questions (mechanism realizations for clauses 2/7/8, batch atomicity, durable-verdict relationship, cross-server composition, static sub-allocator partition) correctly scope genuinely future territory, and the §4 K.σ scoping is a defensible exclusion discharged by hypothesis + H3.

VERDICT: REVISE
