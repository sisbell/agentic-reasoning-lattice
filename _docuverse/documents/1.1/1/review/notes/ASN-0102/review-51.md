# Review of ASN-0102

## REVISE

### Issue 1: COPY is not self-sufficient "in exactly the sense" of J2/J3

**ASN-0102, Definition of COPY (Amendment to ValidComposite★)**: "It is *self-sufficient* in exactly the sense ASN-0047 attributes to `K.μ⁻` (J2) and `K.μ~` (J3): around its own step it records its own provenance and discharges the step-local content of the couplings J0/J1★/J1'★ and the boundary property P4★, needing no support from neighbouring steps."

**Problem**: J2 (ContractionIsolation) and J3 (ReorderingIsolation), as stated in the foundation claims, assert `C' = C ∧ L' = L ∧ E' = E ∧ R' = R`. Their self-sufficiency is *full state-isolation*, and in particular `R' = R` — K.μ⁻ and K.μ~ record **no** provenance. COPY's own definition writes `Σ'.R = Σ.R ∪ {(a_j+i, d)}`, so `R' ≠ R` in general. The clause's own gloss ("records its own provenance") names precisely the way COPY differs from J2/J3, yet the lead-in claims the sense is *exactly* theirs. The two transitions COPY is likened to are the two that change the least; COPY changes M *and* R.

**Required**: Drop "in exactly the sense ... J2 ... J3," or restate the analogy precisely: COPY is *coupling-self-sufficient* (it needs no neighbouring step to discharge J0/J1★/J1'★/P4★ for its own effect), which is weaker than J2/J3's state-isolation. The cited precedent for "records its own provenance, needs no neighbour" is not J2/J3 but the composite J4 (Fork), which bundles K.μ⁺ + K.ρ.

### Issue 2: Duplicated standalone/embedded framing and boundary-lift scaffolding (anti-bloat)

**ASN-0102, Amendment paragraph and X14 "Boundary lift (invoked uniformly below)"**: The Amendment states COPY "may stand as a length-1 (standalone) composite or appear as one step within a longer valid composite," then forward-defers ("The coupling obligations are discharged in X14"). X14 then re-erects the same distinction in full: "In the *standalone* reading COPY is a length-1 composite ... In the *embedded* reading COPY carries `Σ_i → Σ_{i+1}` ...".

**Problem**: The standalone-vs-embedded composite reading is set up twice, in two sections, with the first instance serving only as a forward pointer to the second — matching the flagged patterns "two paragraphs in different sections say the same thing" and "multiple paragraphs defer to the same downstream location." The Amendment paragraph carries no object-level content COPY's definition needs; it is rationale for why COPY is freely composable plus a deferral to X14. A reader must hold the same framing twice and skip the first to reach the discharge.

**Required**: State the composability fact once (COPY is an elementary transition added to ValidComposite★'s atomic vocabulary), and place the standalone/embedded boundary-lift only at X14 where the couplings are actually discharged. Remove the pre-deferral and the "both authorities place COPY inside larger units of work" justification from the Amendment.

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content after later displacement
The Open Questions ask what ties origin to continued discoverability after a *subsequent* operation displaces copied content again. This is downstream-operation interaction (and belongs with the link-projection / re-arrangement machinery), not a guarantee COPY itself must establish — correctly left open.

### Topic 2: Re-transclusion provenance (a referencing document becoming a source)
The chained-reference containment question is genuine but concerns the composition of COPY with a *further* COPY whose source is `d`; the per-operation contract here (X10, X14) is sufficient for one hop, and the multi-hop containment account is future territory.

VERDICT: REVISE
