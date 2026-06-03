# Review of ASN-0070

## REVISE

### Issue 1: Worked example states `coverage` as an exact finite set, contradicting its own definition and Configuration 1

**ASN-0070, A Worked Example, Configurations 2, 3, and 5**:
- Config 2: "Modify the endset to `L(ℓ).e₁ = {(a₀, δ(1, m_a))}`, so `coverage = {a₀}`."
- Config 3: "`L(ℓ).e₁ = {(b, δ(1, m_a))}` ... every block's intersection with `{b}` is empty."
- Config 5: "`coverage(L(ℓ).e₁) = {a₀} ∪ {ℓ₀} = {a₀, ℓ₀}`."

**Problem**: By the note's own definition `coverage(e) = ⋃_{σ∈e} ⟦σ⟧` with `⟦σ⟧` the T12 half-open interval, the coverage of `{(a₀, δ(1, m_a))}` is `{t : a₀ ≤ t < a₀ ⊕ δ(1, m_a)} = {t : a₀ ≼ t}` (PrefixSpanCoverage / L13, ASN-0043) — the entire subtree of `a₀`, not the singleton `{a₀}`. Configuration 1 treats this correctly ("contains the three depth-`m_a` addresses ... together with deeper-depth tumblers ... only the three depth-`m_a` members ... are ever met by an intersection"), but Configs 2, 3, and 5 write `coverage` as the exact finite set. The conclusions survive only because block I-extents are depth-`m_a` and the intersection happens to pick the right elements — but the asserted coverage equalities are false, and Config 3's stated hypothesis (`b ∉ ran(M(d))`) is the wrong precondition (the load-bearing fact is that no element-level member of `subtree(b)` lies in `ran(M(d))`).

**Required**: State coverage in Configs 2, 3, 5 as the half-open interval / subtree (or explicitly as "the depth-`m_a` slice of coverage is …"), matching the careful treatment already used in Config 1, and adjust the Config 3 reasoning to intersect against the actual coverage rather than `{b}`.

### Issue 2: Open Question 4 poses a question the body has already decided

**ASN-0070, Open Questions**: "Where must responsibility for canonicalisation lie — must a downstream consumer mandate canonical form, or may any finite representation be admissible with callers deriving canonical form independently?"

**Problem**: The Canonical Form section already answers this: "We do not commit the operation's postcondition to canonical form ... An implementation may return any representationally equivalent form. The canonical form is the derivation that callers apply when representational identity matters." The implementation-evidence parenthetical reinforces the same decision ("Implementations seeking representational identity must canonicalise downstream"). Listing the resolved point as an open question leaves the note self-contradictory about whether the question is settled.

**Required**: Remove Open Question 4, or reframe it to name the genuinely open residue (e.g., *which* downstream consumer bears the cost) rather than restating the decided either/or.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics of `follow` against a concurrently-modified document
**Why out of scope**: Open Question 2 raises this correctly as future territory; `follow` is specified as a pure query against a fixed state, and concurrency control belongs to a transition/scheduling ASN, not this one.

### Topic 2: Cross-home and transclusion-lineage relationships between resolutions
**Why out of scope**: Open Questions 1 and 3 concern relationships across documents with shared lineage — these require version/transclusion machinery this query note does not (and should not) define.

VERDICT: REVISE
