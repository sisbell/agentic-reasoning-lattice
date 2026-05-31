# Review of ASN-0043

This note carries the `review-mode.anti-bloat` classifier. The mathematical content is mature — the L1c chain, the FSP/FSE conformance machinery, PrefixSpanCoverage, and the six-step worked example all check out under scrutiny (I verified the Case A/Case B chains in L9, the coverage-union argument in Step 6, and the FSE freshness/length-preservation argument). My findings are accretion of meta-prose around forward references, which the classifier asks me to surface at source.

## REVISE

### Issue 1: L0b's body is mostly use-site inventory and "why the theorem is needed" prose, not the claim
**ASN-0043, L0b — LinkAddressValidity**: "This is the T4-validity postcondition established by L1c's chain, and it is the *single* licensing fact this ASN uses for the field projections on link addresses: with every link address T4-valid and element-level (L1, `zeros(a) = 3`), T4b's `E`, `N`, `U`, `D` projections ... are well-defined on all of `dom(Σ.L)`, so `subspace_I(a)` ... and `home(a)` exist for every `a ∈ dom(Σ.L)`. T4-validity is load-bearing here, and `zeros(a) = 3` alone (L1) would not suffice ..."
**Problem**: The actual claim of L0b is one line (`(A a ∈ dom(Σ.L) :: T4-valid(a))`, established by L1c). The remainder is exactly two flagged patterns: a use-site inventory ("the *single* licensing fact this ASN uses for the field projections") and defensive justification explaining why the theorem is needed ("T4-validity is load-bearing here, and `zeros(a) = 3` alone would not suffice"). This is "new prose around [a result that] explains why it is needed rather than what it says." The reader must skip past the inventory to reach the derivation.
**Required**: Reduce L0b to its claim plus the L1c citation. Drop the "single licensing fact" inventory and the "load-bearing / would not suffice" justification — the projections' well-definedness is already discharged where they are used.

### Issue 2: Properties table entries enumerate downstream consumers
**ASN-0043, Properties Introduced table**:
- L1d: "... ; consumed by FSP's L0 bullet, L9, L14, L14a, and the worked example"
- FSE: "... discharges FSP's h1–h3"
- FSP: "... leaves `coverage(ℓ.type)` unconstrained"
**Problem**: "A definition's introduction enumerates downstream consumers rather than advancing the definition's meaning." The L1d entry's consumer list and the FSE entry's "discharges FSP's h1–h3" tell the reader where the lemma is *used*, not what it *says* — and these consumer lists rot as the ASN evolves. The table column should state the property, not index its call sites.
**Required**: Strip the use-site clauses from the L1d and FSE rows (and trim the FSP row to its preservation statement). Consumer relationships belong in the dependency graph, not the statement column.

### Issue 3: Multiple sections defer sideways/forward to L0b for the same fact
**ASN-0043, Definition — home / L0 / L1d(b) / L0a**: home: "The definition presupposes its stated domain condition ... which L0b (below) discharges for every link address." L0: "The projection `subspace_I(a) = E(a)₁` is well-defined on every `a ∈ dom(Σ.L)` by L0b." L1d(b): "T4-validity holds on each side — for `a ∈ dom(Σ.L)` by L0b ...". 
**Problem**: "Multiple paragraphs in different sections defer to the same downstream location." Four separate sites (home, L0, L0a's content-side discussion, L1d) each re-announce that projection well-definedness on `dom(Σ.L)` comes from L0b. The `home` deferral is additionally a forward pointer ("L0b (below)") while L0b itself derives from L1c, producing a home→L0b→L1c chain the reader must thread. One statement of "T4b projections are well-defined on `dom(Σ.L)` by L0b" suffices; the repeated deferrals are accretion.
**Required**: State the projection-well-definedness fact once (at L0b), and let the other sites use `subspace_I`/`home` without re-citing the licensing chain each time.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace invariant
The note's own Open Questions ask whether a content-side invariant should fix a global `s_C` so disjointness extends past the `s_C`-resident slice. L14/L14a are honestly scoped to the slice; extending them is a content-model (ASN-0036) question, not a defect here.

VERDICT: REVISE
