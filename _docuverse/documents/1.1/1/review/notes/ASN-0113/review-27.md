# Review of ASN-0113

## REVISE

### Issue 1: W5's general non-canonical-anchor construction is dead content the operation never exercises

**ASN-0113, "The extent of a single subspace" (W5)**: "The *general* statement — that *any* contiguous `V_S(d)`, canonically anchored or not, admits some single exact span — is strictly stronger than the operation requires; D-MIN★ excludes a non-canonical anchor, so this is not a live case for the operation. We record it only to support the open question on relaxing D-CTG★ below, and confine it to that hypothetical. The sketch: for a contiguous run with arbitrary minimum `a = min(V_S(d))`..."

**Problem**: This is a full paragraph proving something the in-spec operation never encounters (D-MIN★ pins the anchor to `[S,1,…,1]`, so W4 already disposes of every live case). It is wrapped in defensive prose announcing its own irrelevance — "strictly stronger than the operation requires," "not a live case," "confine it to that hypothetical," and closing with "the W4 span always serves and the general construction is never exercised in-spec." To follow W5's operative content (forward in-spec = immediate from W4; converse via order-convexity) a reader must skip past this entire excursion. The substance belongs, if anywhere, to the D-CTG★-relaxation open question, not to a claim about this operation.

**Required**: Remove the general non-canonical-anchor sketch. State the forward direction in-spec (immediate from W4 under D-MIN★) and keep the converse with its concrete counterexample; if the general case must be acknowledged, a one-line pointer to the open question suffices.

### Issue 2: W5 defers twice to the same open question and bookends a duplicated dependency claim

**ASN-0113, "The extent of a single subspace" (W5)**: opening — "**Exactness is contingent on contiguity.** The single covering span is exact *only because* `V_S(d)` is a contiguous run (D-CTG★)." Closing — "the converse just established records that this exactness genuinely *depends* on D-CTG★ rather than holding unconditionally. Whether relaxing that invariant would oblige the operation to fragment is taken up in the open questions below." Plus the mid-section "We record it only to support the open question on relaxing D-CTG★ below."

**Problem**: The "exactness depends on D-CTG★" point is asserted at the open and re-asserted at the close in different words, and the section defers to the same downstream open question twice. These are the compounding forward-reference / duplication patterns the anti-bloat pass exists to catch.

**Required**: Make the dependency claim once (it is the converse's conclusion) and defer to the open question at most once.

### Issue 3: W5's claims-table status cell carries scoping caveats instead of a status

**ASN-0113, Claims Introduced table, W5 row**: "...forward direction in-spec is immediate from W4 under D-MIN★ (canonical anchor); the general non-canonical-anchor construction exceeds what the operation requires and is confined to the D-CTG★-relaxation hypothetical; converse by order-convexity..."

**Problem**: The status column should summarize the claim, not relitigate scope. This cell reproduces the same hedging that bloats the body.

**Required**: Reduce to a one-clause statement of the claim once Issue 1 is resolved.

### Issue 4: Label numbering skips W19

**ASN-0113, claims**: the sequence runs W0–W18 then jumps to W20, with no W19 introduced or referenced anywhere.

**Problem**: A reader or tool scanning the labels sees an unexplained gap. If W19 was retired in a prior cycle, nothing records that.

**Required**: Either reuse W19 for the cardinality-wp claim (currently W20) or note the retirement, so the label space has no silent hole.

## OUT_OF_SCOPE

(none — the version-fork, transclusion, overall-extent-consistency, and subspace-extension questions are correctly held as open questions, not smuggled in as claims.)

VERDICT: REVISE
