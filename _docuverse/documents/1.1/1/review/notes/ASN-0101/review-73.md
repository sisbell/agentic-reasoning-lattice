# Review of ASN-0101

I checked the operation specification (D0), the gap-closure argument (D1), the seven preservation claims (D2–D8), the projection characterisation (D9), the wp analysis (D11), the ValidComposite★ extension (D10), and all three worked examples. The mathematics is sound: the reduction argument is complete (including the `m_S = 2` base and the `m_S ≥ 3` minimality induction), the source-correspondence argument in D8 correctly handles the re-mapped `Q ∩ X` positions for every invariant conjunct (S3★, S8★(c) via M12's full precondition set, CL-OWN, CL-UNIQ), the boundary cases are exhaustive, and the content example genuinely exercises interior-of-a-run splitting (the `a_k` are I-adjacent, so the pre-state is a single maximal run that DEL splits). I found one defect.

## REVISE

### Issue 1: Claim labels D10 and D11 are out of order with physical position and dependency
**ASN-0101, section order vs. Claims Introduced table**: The "Weakest precondition for discoverability preservation" section introduces **D11** and physically precedes both "A worked example" and the final "ValidComposite★ extension under DELETE" section, which introduces **D10**.

**Problem**: A reader following the Claims Introduced table (D0…D9, D10, D11) expects D10 before D11, but encounters D11 first and D10 last. The mismatch is reinforced by dependency direction: D10's LP-family-extension paragraph states "D9 and D11 supply the only DEL-specific projection facts," so D10 *depends on* D11 yet carries the lower number. A claim that consumes another should not be numbered ahead of it while also appearing after it in the text.

**Required**: Resolve the inconsistency — either swap the labels (wp → D10, ValidComposite★ → D11) so numeric order matches reading order and dependency, or move the ValidComposite★ section ahead of the wp section. The Claims Introduced table and the in-text cross-references ("D9 and D11 supply…") must then be made consistent with the chosen ordering.

## OUT_OF_SCOPE

None beyond what the Open Questions section already marks (arrangement reconstruction, causal ordering across documents, full reversibility — all correctly deferred to a versioning ASN).

VERDICT: REVISE
