# Review of ASN-0114

The technical content here is sound. I checked every claim and every derivation, and they hold:

- **F0/wp** — the definedness precondition is genuinely weakest: in-domain yields a span-set witness (the recorded endset is its own witness), out-of-domain yields `⊥` which is not a span-set, so the postcondition fails exactly off the stated condition.
- **F1, F2, F3, F5, F6, F8** — derivations are explicit and correct. F2's `|R| ≥ 2` argument (≥1 via first collapse, ≠1 via S0 convexity contradiction) is airtight; F5's composition of single-step L12 into the `→*` closure via LP13 is correct.
- **F7** — the empty/invalid distinction is handled with real care: the relation-vs-value framing is resolved precisely (both `⟨⟩` and `⊥` are the determinate collapse cases), the slot-3 guarantee is discharged from the two collapses + L3, and the `wp(·, R = ⟨⟩)` derivation is a genuinely non-trivial backward chain.
- The **worked instance** correctly discharges F2 (disconnected `coverage(e₁)` over T, witness `a₃ < a₅ < a₇`) and F7, and grounds them in `F`/LP-Fin against the implementation evidence.
- All cross-references are to foundation ASNs; no out-of-scope claims; no implementation-mechanics drift.

What remains are prose-level redundancies that the anti-bloat mode asks me to surface at source.

## REVISE

### Issue 1: Redundant rationale in the exactness section
**ASN-0114, "What the result must be: exact coverage, no more and no less"**: "Because the endset *is* the connection — the from-set is precisely what the link is 'from' — there is no wider or narrower region for a faithful answer to report (Q9). The endset is definitional, not a summary of some other region, so exactness is forced, not merely desirable."
**Problem**: These two consecutive sentences make the same argument — the endset defines the region, therefore exactness is mandatory. The second sentence ("definitional, not a summary … forced, not merely desirable") is a paraphrase of the first ("there is no wider or narrower region for a faithful answer"); "forced" is already established by "no wider or narrower region," and "not merely desirable" is rhetorical emphasis carrying no new content. This is the "two sentences say the same thing in different words" pattern.
**Required**: Keep one. The first already grounds exactness in the endset-is-the-connection point and cites Q9; delete the second.

### Issue 2: Content-free preview clause in the problem statement
**ASN-0114, "The problem"**: "We shall find that each of these questions has a sharp answer, and that the sharp answers are exactly the invariants an implementation must satisfy."
**Problem**: This is a pure announcement that reasoning will occur — it states that answers exist and that they are invariants, without supplying either. The four rhetorical questions preceding it do map onto F1/F6/F1–F2/F7 and earn their place as scene-setting; this closing clause adds nothing a reader following the claims must retain.
**Required**: Delete the sentence; the rhetorical questions stand on their own. (The "What relationship / What discloses / Which admissible / what boundary" preview is fine — it is the announcement clause specifically that is empty.)

## OUT_OF_SCOPE

None. The "recorded end versus its resolution" section discusses resolution-against-a-document only to *disclaim* it (stating what FOLLOWLINK does not do, and tying the disclaimer back to F1/F5/L12), rather than defining claims about it — so it is correctly within bounds, not an out-of-scope claim. The Open Questions (normal form, resolution shrinkage, serialization of `⟨⟩`/`⊥`, higher-slot distinction, multi-document reporting) are all genuine future territory, not gaps in this note.

VERDICT: REVISE
