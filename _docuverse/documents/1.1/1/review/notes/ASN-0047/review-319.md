# Review of ASN-0047

I read the ASN against its foundations and verified the worked examples on concrete tumblers (the fork k=1/k=0 allocations, origin/parent projections, the interior-replacement range arithmetic, and the D-SEQ★ derivation cases all check out). The transition model is correct and self-consistent. My findings are confined to the forward-reference/meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface; they are presentation defects, not correctness defects, but each is a concrete REVISE per the note's "flag at source" instruction.

## REVISE

### Issue 1: Freshness-discharge content stated once, then restated per sub-case
**ASN-0047, FrontierEquivalence *Freshness discharge (scope note)* and K.δ case (ii)**: The scope note is introduced explicitly to "state once how that guard encodes the current frontier index at k = 0 versus the at-most-once-per-`(t, k')` occurrence at k ∈ {1, 2}." K.δ case (ii) then *re-cites* it ("per FrontierEquivalence's *Freshness discharge* scope note") **and** re-states its content per sub-case: at k=0, "the case-level `e ∉ E` *is* the k = 0 frontier check"; at k ∈ {1, 2}, "it reads whether the spawn `(t, k')` has already been performed."

**Problem**: This is exactly the "states once" claim being undercut by relocated restatement — the note's whole purpose is defeated when the same case-split reappears at the use site. Matches the anti-bloat pattern "a paragraph looks like a prior finding's content relocated rather than removed" and "multiple paragraphs say the same thing in different words." The two worked examples re-cite the note a third and fourth time.

**Required**: Either keep the per-sub-case encoding in the scope note and have K.δ carry only a bare pointer, or inline it in K.δ and delete the scope note. One location, not two.

### Issue 2: Rationale and use-site prose lodged in structural slots
**ASN-0047, J0 / Properties table J0 row / S3★**: Three instances of meta-prose in slots that should carry the claim only.
- J0: "The motivation is Nelson's design intent (LM: content enters the docuverse only by placement in a document), which justifies imposing J0 rather than establishing it as ground truth of the transition vocabulary." — prose explaining *why the constraint is imposed* rather than what it constrains.
- Properties table, J0 row: "**Imposed (not derived)** — a clause-(2) validity constraint of ValidComposite★, motivated by Nelson's design intent, not an axiom of the elementary transition system." — the same rationale restated in the index table.
- S3★ definition: "...yields the subspace-position correspondence `subspace(v) = subspace_I(a)` ... **(used in the *Notation*)**." — a definition's body enumerating a downstream use-site.

**Problem**: These match the listed patterns "new prose around an axiom explains why the axiom is needed rather than what it says," "a definition's introduction enumerates downstream consumers," and rationale duplicated across two slots. The logical-status distinction ("imposed, not derived") is load-bearing and should stay; the Nelson-motivation gloss and the "(used in the Notation)" pointer are not.

**Required**: Keep the "imposed, not derived" status flag at one location; drop the duplicated Nelson-motivation sentence from the J0 prose (or the table row, not both) and the "(used in the Notation)" use-site note.

## OUT_OF_SCOPE

None. The ASN stays within state/operation/invariant territory; implementation citations (Gregory's `docreatenewversion`, etc.) serve as evidence in the foundations' established style and do not constitute drift.

VERDICT: REVISE
