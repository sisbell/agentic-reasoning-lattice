# Review of ASN-0098

## REVISE

### Issue 1: F is defined informally
**ASN-0098, Boundary and Width Behaviour**: "The set of *substrate-emittable addresses* is the union of all such chain elements across all T4-valid document tumblers and both subspaces; we denote it `F`."
**Problem**: F is used quantitatively in the tightness predicate `(A t ∈ F : s ≤ t < s ⊕ ℓ : t ∈ dom(Σ_e.C) ∪ dom(Σ_e.L))` as a set, but never defined via set-builder notation. The text description leaves the membership predicate underspecified — does F include addresses from K.α and K.λ only, or also future ASN allocators? Are anchors `b_C(d)` excluded?
**Required**: Give F a formal definition such as `F = {a ∈ T : (E d ∈ T, s ∈ {s_C, s_L}, k ≥ 1 :: d satisfies T4 ∧ zeros(d) = 2 ∧ a = [d, 0, s, k])}`. This makes the universal quantifier in the tightness predicate fully precise and makes the exclusion of anchors (which have `#E = 1` while F-elements have `#E = 2`) explicit.

### Issue 2: Inductive extensions hand-waved
**ASN-0098, Boundary and Width Behaviour, descendant case**: "This argument extends inductively to descendants of `d'` (further version chains), whose chain elements diverge at position `#d_0 + 1` for exactly the same reason."
**Also**: "Tightness is therefore preserved against every ancestor at every depth in the version sub-allocator tree from which `d_0` descends."
**Problem**: The inductive step is asserted but not shown. What is the induction over (lineage depth? chain index? component position?), what is the inductive hypothesis, and how does it discharge the chain element's value at position `#d_0 + 1` for arbitrary descendants? "For exactly the same reason" is the same pattern as "by similar reasoning" — a hand-wave for what is in fact a multi-case argument.
**Required**: State the induction explicitly. Base case: direct descendant `d' = inc(d_0, 1)`. Inductive step: descendant `d'' = d'.z_1.z_2...z_q` extends `d'` by non-zero components without introducing new zeros at positions `≤ #d'`, so chain elements of `A_C(d'')` agree with `d'` on positions `1..#d'`; in particular, position `#d_0 + 1` (which is `≤ #d'`) contains `x_1 ≥ 1`. T1 case (i) at position `#d_0 + 1` then yields the strict inequality.

### Issue 3: LP20 stated as inclusion when equality is the natural content
**ASN-0098, LP20**: "`{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))`"
**Problem**: The architecturally substantive claim is the equality `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))`, which follows directly from the projection definition: `v ∈ project(e, d, Σ) ⟺ v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) ∈ coverage(e)`, so the image is `ran(Σ.M(d)) ∩ coverage(e)`. The stated inclusion is a strict weakening, obtained by composing the equality with S3★'s `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)`. The equality is what holders can rely on; the inclusion loses the range characterization.
**Required**: State the equality `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))` and derive the inclusion as a corollary via S3★.

### Issue 4: LP18 proof does not establish `a ∈ dom(Σ'.L)`
**ASN-0098, LP18 — Resurrection**: "By the definition of `project`, `v ∈ project(a, i, d, Σ')` since `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) = a* ∈ coverage(Σ'.L(a).eᵢ)`."
**Problem**: The expression `coverage(Σ'.L(a).eᵢ)` and `project(a, i, d, Σ')` both require `a ∈ dom(Σ'.L)` for the slot accessor to be well-defined. The proof writes these terms without first discharging this precondition. The premise `a ∈ dom(Σ.L)` (orphaned link at Σ) does not directly imply `a ∈ dom(Σ'.L)` — that requires Store Monotonicity★ or LP13.
**Required**: Add the missing step. Cite Store Monotonicity★ (or LP13) to establish `a ∈ dom(Σ'.L)`, then proceed with the slot accessor being well-defined.

### Issue 5: Citation ambiguity for ChainEnumerationInjectivity
**ASN-0098, Boundary and Width Behaviour, achievability**: "chain elements with index `> m` lie at or above `inc(t_m^C(d_0), 0)` by ChainEnumerationInjectivity (T10a.7, ASN-0093)"
**Problem**: T10a.7 (EnumerationInjectivity) is a foundation lemma in ASN-0034; ChainEnumerationInjectivity is a distinct lemma in ASN-0093 specialised to T10a-discipline-satisfying chains. The combined citation `(T10a.7, ASN-0093)` is ambiguous — which lemma is being invoked, and from where?
**Required**: Cite as `ChainEnumerationInjectivity (ASN-0093)` if the chain-specific lemma is intended (most likely, given the chain context), or as `T10a.7 (EnumerationInjectivity, ASN-0034)` if the foundation lemma is intended. Do not combine.

### Issue 6: Order-preservation under K.μ⁺_L's first-arrangement constraint not addressed
**ASN-0098, LP9**: "The argument is identical for both extension operations because each shares the same structural form on `Σ.M(d)`."
**Problem**: K.μ⁺_L (ASN-0047) has an additional constraint `ℓ ∉ ran(M(d))` (first-arrangement) that K.μ⁺ lacks, plus the fixed depth `m_L = 2` (LinkVPositionDepthAxiom). These constraints affect the achievable shape of `dom(Σ'.M(d)) ∖ dom(Σ.M(d))` and the per-subspace dependence of D-CTG★/D-MIN★. The proof treats the two operations as structurally identical without addressing whether these K.μ⁺_L-specific constraints interact with the projection growth characterisation.
**Required**: Either explicitly check that the K.μ⁺_L constraints (first-arrangement, fixed depth, link-subspace placement) leave LP9's argument structurally unchanged, or split LP9 into a K.μ⁺ case and a K.μ⁺_L case with the appropriate per-case discharge.

## OUT_OF_SCOPE

### Topic 1: Reverse discovery (V-position → links containing it)
**Why out of scope**: The Open Questions section explicitly lists this as future work. The current ASN defines forward projection only; reverse navigation requires additional indexing semantics that belong in a future ASN.

### Topic 2: Contiguity-preservation of projections under K.μ~
**Why out of scope**: The Open Questions section identifies this. K.μ~ can scatter contiguous projections; whether/when contiguity must be preserved is a separate property requiring its own treatment.

### Topic 3: Cross-document projection identity under "same operations"
**Why out of scope**: The Open Questions section identifies the operation-comparability problem. Whether two documents undergoing structurally parallel edits yield identical projections requires formalising "same operation" across per-document state, which is a separate undertaking.

VERDICT: REVISE
