# Review of ASN-0094

After working through this 22,000+ word specification carefully, including all proofs, walkthroughs, and the appendix on NAT primitives, I find the ASN to be exceptionally rigorous. The proofs are detailed (Sh0–Sh4 each carry full inductive arguments with case enumeration), the worked examples are concrete with specific tumblers and state transitions, the META status of Sh5 is appropriately characterized and downgraded, the cross-ASN references are limited to the foundation ASNs (ASN-0034, ASN-0043, ASN-0086), and the framework is honest about scope limitations (single-process substrate, body-shape uniformity as aspiration rather than commitment).

I have one specific concern worth flagging.

## REVISE

### Issue 1: Inconsistent prose describing RetractionSelfFreshness placement

**Section "Idempotency (Sh4)", *Stratification* subsection:** Two adjacent sentences describe the placement of Lemma — RetractionSelfFreshness inconsistently.

Sentence 1: "Sh4 additionally consumes the *Lemma — RetractionSelfFreshness* (stated immediately below this paragraph, before the induction's base case) at Case C's `K ~ R` sub-case..."

Sentence 2: "Sh4 additionally consumes the *Lemma — RetractionSelfFreshness* — a sub-lemma stated inline within the Sh4 section between Case C and Case D — at Case C's `K ~ R` sub-case..."

The actual textual placement is BEFORE the Base case (Sentence 1 is correct). The "between Case C and Case D" wording in Sentence 2 (and in the Sh-conf section's "Stratified proof order" paragraph, which repeats the same description) is misleading — a reader following the cross-reference will not find the lemma between Cases C and D.

**Problem**: A careful reader trying to verify the proof structure will get conflicting information about where to find the lemma. The "between Case C and Case D" phrasing may be intended in a conceptual sense (the lemma bridges these cases) but reads as a textual position claim.

**Required**: Pick one wording. "Stated before the induction's Base case" matches the actual structure; if "between Case C and Case D" is meant conceptually, rephrase as "consumed between Cases C and D" or similar to avoid the textual-position reading.

## OUT_OF_SCOPE

None — the framework's Open Questions section appropriately catalogs the items that belong to future work (cross-process consistency, ghost-targeting slot semantics, composite shapes, etc.).

VERDICT: REVISE
