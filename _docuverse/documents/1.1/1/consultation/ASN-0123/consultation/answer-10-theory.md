## Question 10 [theory]

> What must the design guarantee about navigating the ancestry chain — that from any version one can reach every ancestor back to the original, and discover descendants forward — even after many successive forks by different owners?

I'll research this carefully. The question sits at the intersection of versions, forking, tumbler addressing, and discovery operations — and there's a subtle tension I want to verify in the source: Nelson's caveat about version numbers being an "accidental extension" that "strictly implies no specific relationship of derivation" (4/29). Let me read the key pages directly.

`★ Insight ─────────────────────────────────────`
The question conflates two distinct fork mechanisms that the design treats differently:
1. **Owner-internal version forks** (CREATENEWVERSION) — ancestry encoded structurally in the tumbler
2. **Cross-owner derivative forks** (versioning-by-inclusion) — ancestry carried by transclusion/shared-Istream, since one owner cannot baptize addresses under another's

"Successive forks by different owners" forces mechanism #2, which changes how the navigation guarantee must be satisfied.
`─────────────────────────────────────────────────`

Let me verify the exact wording on the pages that matter most.
