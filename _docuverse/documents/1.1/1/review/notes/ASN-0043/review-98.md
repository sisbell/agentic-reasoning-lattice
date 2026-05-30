# Review of ASN-0043

I checked the proofs (L0a/T7 discharge, L1c chain + CPP, L9 ghost construction in both cases, FSP hypothesis discharge, L11b sibling extension, PrefixSpanCoverage, the worked example and its four transition steps). The technical content is sound — the FSP factoring is correct, both Case A/B chains discharge h1–h3, and the coverage-disjointness arguments check out. The findings below are accretion items, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Dual-reading meta-commentary in the L9 worked-example verification
**ASN-0043, Worked Example, *L9 (TypeGhostPermission)***: "The L9 lemma applies to this state because its `s_C`-residence precondition is satisfied (...), so this state lies within L9's scope; **the direct enumeration shown here can also be read as discharging L9's conclusion in this state without routing through the lemma.**"
**Problem**: The bolded clause advances no reasoning. The verification has already directly enumerated `g ∉ dom(Σ.C) ∪ dom(Σ.L)` via T7 against each store entry; telling the reader this enumeration "can also be read" as a lemma-free discharge restates what was just shown and offers an alternative interpretive frame instead of a step. It is exactly the skip-past meta-prose the anti-bloat mandate names.
**Required**: Delete the second clause; keep only the statement that the state satisfies L9's `s_C`-residence precondition (or keep only the direct enumeration). One framing, not two.

### Issue 2: L14 re-glosses the L0a disjointness it just cited
**ASN-0043, L14 — DualPrimitive**: "The two domains are disjoint over the `s_C`-resident slice of content (L0a): `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅` — no address holds both a link and `s_C`-resident content (L0a)."
**Problem**: The formula is stated with its `(L0a)` citation, then immediately re-stated in prose with a second `(L0a)` citation. The two halves say the same thing in different words — the "two paragraphs say the same thing" pattern compressed into one sentence. L14's own substance (partition into exactly two stored categories) is carried elsewhere; the disjointness is a cited prerequisite that needs stating once.
**Required**: Drop the trailing "— no address holds both a link and `s_C`-resident content (L0a)" gloss; the formula plus single citation suffices.

## OUT_OF_SCOPE

None beyond the topics the Scope section already excludes.

VERDICT: REVISE
