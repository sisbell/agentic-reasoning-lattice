# Channel Assignment — ASN-0134 review-39

**Date:** 2026-06-14 11:20

## Issue 1: "Chain contiguity is model-intrinsic" is proved four times
Reason: Purely an internal deduplication — W3 already proves the claim and is its named home; the fix is to cut the G1(i) re-derivation to a citation and drop the §5 re-assertion, keeping the G1-specific "only collision-freedom is bought by serialization" line. No design intent or implementation evidence is at stake; the canonical proof and its scope are already in the ASN.

## Issue 2: "A batch is not a single operation / not atomic" stated four times, with A1 deferring forward to A5
Reason: Internal routing-text removal — A1's forward-references to A5 and the `m ∈ {0,1}` routing collapse into one clause, letting A5 own batch non-atomicity. All content (A1 realization counts, A5 non-atomicity) is already present and proven; nothing external is consulted.

## Issue 3: contiguity-vs-atomicity / "reader gap" deferral ring (A5 ↔ §6/W4 ↔ OQ5)
Reason: Internal — the contiguity≠atomicity distinction and its two modes of divisibility are already defined at A5; the fix only removes the circular cross-deferrals so the distinction is stated once with a single forward pointer to OQ5. Derivable from the ASN's own structure.

## Issue 4: §1 scope parenthetical duplicates "What this note does not cover"
Reason: Internal — the scope exclusion is already owned by the dedicated "What this note does not cover" section; the fix collapses the §1 enumeration to a pointer. No external question is involved.

## Issue 5: soundness-vs-durability stated three times in close succession (§8)
Reason: Internal — V1 and its two bullets already carry the soundness/durability dichotomy in its clearest form; the fix folds the redundant "practical reading" restatement. Both halves are already proved within §8 (V0/V2 for soundness, V1 for durability).

## Issue 6: SAFE(b) re-derives the §4 instance (i)/(ii) analysis
Reason: Internal — the duplicate/idem/resurrection mechanics already live in §4 (instances i/ii), G2, W5, and the cited ASN-0128 I1a/I2; the fix replaces the re-derivation in the SAFE proof with citations to those established results. No new evidence is needed to cite what the document already proves.

## Issue 7: flagged micro-patterns (exhaustiveness claim, defensive justification, "if we'd done it wrong" aside)
Reason: Internal copyediting — cutting the "exhaust," "essential not cosmetic," and counterfactual phrases removes defensive framing without touching any claim; the surrounding enumeration and the positive §8 statement carry the content. No channel bears on phrase-level deletions.

## Issue 8: MIC clause 6 restates W6 and is admitted non-load-bearing
Reason: Internal — W6 already establishes runtime registry-write-freedom (citing ASN-0126 P1 / ASN-0128 R1) and the note itself certifies clause 6 carries no weight; the author can either drop the clause or delete its meta-justification from the ASN's own content alone. The substantive registry semantics are settled, not in question.
