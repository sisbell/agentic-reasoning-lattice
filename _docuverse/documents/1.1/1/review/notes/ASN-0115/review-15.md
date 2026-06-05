# Review of ASN-0115

I worked through R0–R11, the supporting definitions, and the four worked instances. The ASN is unusually careful: the R6 no-interior-hole argument is correctly confined to the bindable slice and discharged via T5 + D-SEQ★; the R7 repeatability proof correctly identifies reachability *comparability* (not mere common-ancestor reachability) as load-bearing; the R8 link sub-case is correctly proved vacuous from CL-OWN + CL-UNIQ; and the R11 wp is a genuine non-trivial decomposition. Boundary cases (empty spec-set, empty `act`, depth `> m_S`, terminal overrun, out-of-range subspace) are handled. Foundation definitions are used without reinvention (`act` is genuinely distinct from ASN-0098's `project` and ASN-0058's block `Resolution`).

I found one gap.

## REVISE

### Issue 1: R9 (CoherentMultiOriginAssembly) has no concrete worked instance
**ASN-0115, "What co-delivery reveals: coherent multi-origin assembly" / Claims table R9**: "A spec-set drawing on multiple origins is delivered as one ordered sequence (R5), assembled by resolving each spec against its own document's arrangement independently (R4)… each active position `v` resolves to `a = Σ.M(d)(v)`, and that address determines a home document…"

**Problem**: R9 is one of the three "what co-delivery reveals" revelation claims. Its siblings R8 (transclusion) and R10 (subspace crossing) each receive an explicit worked instance verifying their postconditions against a specific scenario. R9 — the claim whose *entire distinctive content* is that content was **created in distinct documents** and must be assembled coherently with **traceable, non-collapsed origins** — receives none. None of the existing instances exercise two distinct creating documents: R6, R8, R10 are single-document, and R11's fork keeps a single `origin(a)` (the forked version transcludes content whose origin is still the original document). So the one property R9 names ("multiple origins", `origin(a₁) ≠ origin(a₂)`) is never shown concretely. Per the review standard, key postconditions must be verified against at least one specific scenario, and the parallel structure with R8/R10 makes the omission conspicuous.

**Required**: Add a worked instance with two documents `d₁ ≠ d₂` whose content has distinct origins, a spec-set `⟨(d₁, σ₁), (d₂, σ₂)⟩`, showing (a) `deliver` concatenates `d₁`'s items before `d₂`'s in spec-set order (R5/R9 coherence), and (b) each delivered item's resolved address has a determinate, distinct home document — `origin(a₁) ≠ origin(a₂)` via S7 — so provenance is traceable and not collapsed by co-assembly.

## OUT_OF_SCOPE

### Topic 1: inline provenance in the delivered stream
Correctly deferred (Open Question 1); R9 carefully asserts only resolution-traceability, not inline provenance.

### Topic 2: single span straddling the subspace boundary
Correctly excluded by the ordinal-level restriction on `σ` and deferred (Open Question 5).

### Topic 3: behavior on precondition violation / refusal
Whether delivery may fail outright (e.g. an unconsultable document) is correctly distinguished from R6 silent gaps and deferred (Open Question 2).

VERDICT: REVISE
