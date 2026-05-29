# Review of ASN-0040

## REVISE

### Issue 1: The necessity of condition (i) misses the real structural reason — stream aliasing

**ASN-0040, §B6 necessity, sub-case (b)**: "At d = 1 the stream happens to remain fully T4-valid — by S2, a pure-trailing-zero parent p at d = 1 generates the same stream as the B6-valid namespace obtained by dropping p's trailing zero and incrementing the depth (e.g. ([1, 0], 1) and ([1], 2) share the stream [1, 0, n]). The d = 1 stream therefore supplies no T4 obstruction, but none is needed: (i) excludes p directly because p is not a valid parent address."

**Problem**: The proof correctly observes (via S2) that `S([1,0],1) = S([1],2)`, then draws the weak, tautological conclusion that "(i) excludes p directly." The substantive consequence is left unstated: if (i) were dropped, `([1,0],1)` and `([1],2)` would be **two distinct B6-valid pairs producing identical streams**. That directly falsifies B7 (Namespace Disjointness), since B7 asserts `S(p,d) ∩ S(p',d') = ∅` for distinct pairs — and it collapses B8 Case 2, whose entire argument is "different namespaces → B7 → distinct addresses." So condition (i) is genuinely *load-bearing for B7 and B8*, not merely a parent-level hygiene rule. The proof cites S2 — the exact lever for the aliasing argument — and then declines to use it for the conclusion it actually supports.

**Required**: State the real necessity: without (i), S2 makes the trailing-zero pair `(p,1)` alias the B6-valid pair `(p',2)`, breaking B7 disjointness and B8 uniqueness. Either derive this explicitly in sub-case (b), or add it to B7's/B8's preconditions discussion so the dependency on (i) is visible where it bites.

### Issue 2: The necessity claim for (i) is of a different kind than for (ii)/(iii), and the framing conflates them

**ASN-0040, §B6 statement**: "Conditions (ii) and (iii) are necessary and sufficient for T4 preservation of the sibling stream, given (i). … Condition (i) … is necessary because a parent violating T4 is excluded at the parent level — including the d = 1 trailing-zero case, where the resulting stream would itself be T4-valid yet the parent still fails T4."

**Problem**: The header promises necessity/sufficiency *for stream T4-preservation*. But sub-case (b) shows that for d = 1 trailing-zero parents the stream **is** T4-valid — so (i) is demonstrably *not* necessary for stream T4-preservation. The proof patches this by switching to "parent-level" necessity ("Condition (i) is necessary for the system"), a different and partly circular notion: (i) literally states "p satisfies T4," so "(i) is necessary because p must satisfy T4" proves nothing. The two notions of necessity are run together under one heading, and the honest statement — (i) is necessary for stream-T4 in sub-cases (a) and the d=2 part of (b), but for **non-aliasing** (Issue 1) in the d=1 case — never appears.

**Required**: Separate the two claims explicitly: (ii) and (iii) are necessary/sufficient for *stream* T4-preservation; (i) is independently required so that (a) defective prefixes/counts do not propagate (sub-case a, d=2 of b) and (b) trailing-zero parents do not alias an existing B6 namespace (Issue 1). Drop the circular "necessary because p must be valid" phrasing.

### Issue 3: Reviser-drift duplication and overstated cross-reference

**ASN-0040, §B6 statement vs. sub-case (b)**: The d = 1 trailing-zero observation ("the resulting stream would itself be T4-valid yet the parent still fails T4") is stated in full in the B6 statement paragraph and then restated in full in necessity sub-case (b). Two paragraphs assert the same point in different words — the accretion pattern this review mode targets. Collapse to one site (the proof), leaving at most a one-clause pointer in the statement.

**ASN-0040, Properties Introduced, B0 row**: "irrevocability (extends T8)". B0 governs `s.B`; T8 governs `allocated(s)`. The relationship between these two sets is explicitly an **open question** ("Under what activation discipline does `allocated(s) ⊆ s.B` hold"). Calling B0 an extension of T8 prejudges that open relationship. Restate as "analogous to T8 for the registry component" or drop the parenthetical.

## OUT_OF_SCOPE

None. The aliasing concern (Issue 1) is internal to baptism's own B7/B8 and is in scope.

VERDICT: REVISE
