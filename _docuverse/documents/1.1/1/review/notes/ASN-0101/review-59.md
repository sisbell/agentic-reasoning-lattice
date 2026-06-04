# Review of ASN-0101

The formal content is sound. I checked the reduction proof, D1's shift bijection (TS1/TS2 at arbitrary `m_S`), D8's three-group invariant discharge, D9's per-subspace projection split, and D11's wp derivations against all three worked examples; the arithmetic and case analysis hold. The findings below are the anti-bloat patterns this note's `review-mode.anti-bloat` classifier asks me to surface, plus one prose-redundancy item.

## REVISE

### Issue 1: D10 opens with motivational meta-prose (why, not what)
**ASN-0101, D10**: "DEL must take its place as a first-class member of the foundation's elementary transition vocabulary if downstream specifications are to invoke 'DEL in a ValidComposite★ chain' without further apparatus. We record the extension as a named claim."
**Problem**: This sentence explains *why* the extension is needed for downstream consumers rather than stating *what* the claim asserts. It is exactly the "new prose explaining why the claim is needed rather than what it says" pattern flagged for this note. The claim body that follows ("ASN-0047's ValidComposite★ is extended to admit DEL...") already states the content; the opening is throat-clearing the reader must skip past.
**Required**: Delete the motivational opening and lead directly with the claim statement.

### Issue 2: Cross-document example closing paragraph restates the verification just completed
**ASN-0101, cross-document transclusion example, final paragraph**: "In the example, the paragraph's bytes remain in `dom(C')`, the reference from `d'` survives, and the link `ℓ_0` becomes discoverable from `d` with reduced cardinality (1 instead of 2) while remaining discoverable from `d'` at full cardinality — the per-document autonomy established in the D5 section."
**Problem**: Every clause here was established line-by-line in the immediately preceding "Verification of cross-document discoverability" block (D2 byte survival, D5 isolation, the 1-vs-2 cardinality, full-cardinality from `d'`). This is the "two paragraphs say the same thing in different words" pattern — a summary that adds no reasoning over the verification it follows.
**Required**: Remove the paragraph, or compress to a single pointer if a section transition is wanted.

### Issue 3: "Boundaries the abstract specification does not cross" is a one-line essay slot
**ASN-0101, "Boundaries the abstract specification does not cross"**: "DELETE's guarantees concern only the state components named in D0's frame; auxiliary indices, representation choices, and enumeration of orphaned I-addresses are downstream concerns."
**Problem**: A standalone section header carrying a single scope-disclaimer sentence. The substantive "what DELETE does not cover" content (orphan rediscovery) already appears as Open Question 4; this header restates the framing without advancing the argument.
**Required**: Fold the load-bearing part (orphaned-address enumeration is downstream) into the relevant Open Question and drop the section, or merge it into the recoverability note.

## OUT_OF_SCOPE

None. The ASN correctly defers INSERT/COPY/REARRANGE mechanics, versioning, and causal ordering across documents to the Open Questions rather than smuggling them into claims.

VERDICT: REVISE
