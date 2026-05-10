# Review of ASN-0047

## REVISE

### Issue 1: Temporal decomposition omits S3 as a cross-layer invariant

**ASN-0047, Temporal decomposition**: "Four invariants bind the layers together, making the temporal contracts precise. P6 is intra-existential… P7 and P7a bridge the existential and historical layers… P4… bridges the presentational and historical layers — it is the load-bearing constraint that necessitates J1's coupling."

**Problem**: The enumeration claims four binding invariants but omits S3 (referential integrity, ASN-0036: `ran(M(d)) ⊆ dom(C)`), which is the only invariant directly binding the presentational layer (M) to the existential layer (C). The section creates a false impression that the presentational layer is bound only to the historical layer (via P4), with no direct constraint tying what a document displays to what content exists. S3 provides exactly that constraint.

The omission is internally inconsistent: the same section says "Cross-layer coupling occurs only in constructive directions: K.α (existential) couples with K.μ⁺ (presentational) via J0" — acknowledging the existential–presentational coupling — but never names S3 as the invariant that makes J0 necessary, despite naming P4 as the invariant that makes J1 necessary. The parallel structure demands S3 be enumerated.

The reachable-state theorem and the arrangement invariants lemma both correctly list S3, so the property is maintained — the gap is only in the temporal decomposition narrative, which is the ASN's declared "central structural insight."

**Required**: Add S3 as a fifth binding invariant in the temporal decomposition. The enumeration should read: P6 (intra-existential, C↔E), S3 (presentational→existential, M→C), P7 (historical→existential, R→C), P7a (existential→historical, C→R), P4 (presentational→historical, M→R). Note S3's role as the load-bearing constraint for J0, symmetric to P4's role for J1.

## OUT_OF_SCOPE

### Topic 1: Span-level operation constraints

The elementary transitions operate at individual V→I mapping granularity. Whether composite operations (INSERT, DELETE, COPY) must preserve correspondence run structure (S8, ASN-0036) beyond the degenerate singleton decomposition is not addressed and belongs in a future ASN specifying named operations.

**Why out of scope**: The ASN explicitly excludes named operations and their specifications. Span structure preservation is a property of those higher-level operations, not of the elementary transition model.

### Topic 2: Provenance query semantics

R accumulates historical containment pairs, and the ASN proves that R is monotonic, grounded, and covers all content. How the system answers queries against R (e.g., "which documents have ever contained content from origin X?") is not specified.

**Why out of scope**: The ASN defines R's structure and invariants. Query resolution is an interface concern, not a state transition property.

VERDICT: REVISE
