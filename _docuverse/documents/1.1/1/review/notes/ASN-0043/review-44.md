# Review of ASN-0043

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage placement
PrefixSpanCoverage is a general result about tumbler spans and prefix sets — it characterizes the coverage of a unit-depth span as exactly the set of prefix extensions. This is span algebra, not link ontology; it happens to be needed here for L10 and L13 but will likely be needed by future ASNs (content queries, span operations) independently of links.
**Why out of scope**: The lemma is correct and properly proven in this ASN. Whether it migrates to a span algebra or tumbler algebra ASN is a project-structuring decision, not a correctness issue.

### Topic 2: Self-referencing and compound link well-formedness
The ontology permits a link whose endset references its own address (L4 imposes no restriction, L13 confirms link addresses are valid span targets). It also permits arbitrary chains of link-to-link references. Whether recursive or self-referencing structures require additional well-formedness constraints — acyclicity, bounded depth, or structural typing — is an open design question.
**Why out of scope**: The ontology correctly defines what links ARE; constraints on what compound structures are USEFUL belong in a future ASN on link operations or compound link semantics.

### Topic 3: Endset coverage equivalence for queries
Two endsets with different span decompositions can have identical coverage. The ASN correctly notes this (`coverage` is a lossy projection) but defers the question of when coverage-equivalent endsets should be treated as interchangeable for query purposes.
**Why out of scope**: This is query semantics, not ontology.

---

This ASN is unusually thorough. Every claim is backed by explicit argument. The L9 witness construction verifies all 17 invariants individually. The L11b witness does the same. PrefixSpanCoverage is proven by complete case analysis on depth (same, greater, shorter), with both inclusion and exclusion directions handled. The worked example covers the base state, two extensions (for non-injectivity and reflexive addressing), and two state transitions (for non-vacuous verification of L12/L12a). Boundary cases are addressed: empty endsets appear in the L9 witness, ghost types are demonstrated, and the depth-1 degeneracy motivating L1b is explicitly worked through.

The logical dependency structure is clean and non-circular: L1c (axiom) feeds L11a via GlobalUniqueness; L0 + L1 + S7b + T7 yield disjointness; L12 yields L12a; S3 + L0 jointly satisfy L14a (stated independently for forward compatibility). No property references a non-foundation ASN.

VERDICT: CONVERGED
