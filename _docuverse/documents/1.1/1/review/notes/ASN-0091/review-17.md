# Review of ASN-0091

## REVISE

### Issue 1: "by π's injectivity" in S2 derivation requires bijectivity, not injectivity
**ASN-0091, "REARRANGE as Vstream-Only Operation" section, S2 derivation paragraph**: "By π's injectivity, each `v' ∈ dom(Σ'.M(d)) = dom(Σ.M(d))` (RA-dom) is the image of a unique `v = π⁻¹(v') ∈ dom(Σ.M(d))`"
**Problem**: The conclusion "is the image of a unique v" splits into two claims — existence (v' is some π(v)) and uniqueness (v is the only such). Existence requires surjectivity; uniqueness requires injectivity. Citing only "injectivity" is logically insufficient for the existence half. The text also uses `π⁻¹`, which is only defined if π is a bijection.
**Required**: Replace "by π's injectivity" with "since π is a bijection" (or "by π's bijectivity"). The premise is supplied by RA-π already.

### Issue 2: "The set is preserved (RE-proj)" in Run Decomposition section is imprecise
**ASN-0091, "Run Decomposition Is Not Invariant" section, paragraph immediately following the symmetric coalescence example**: "if a pre-state contiguous V-interval `[v, v + n)` is in `project(e, d, Σ)`, the post-state image `π([v, v + n))` may consist of multiple disjoint V-intervals. The set is preserved (RE-proj), but its geometry — its decomposition into contiguous V-runs — is not."
**Problem**: RE-proj asserts `project(e, d, Σ') = π(project(e, d, Σ))` — the set transports *via π*. The V-positions actually change (unless π = id, which REARRANGE_K rules out). Saying "the set is preserved" reads as "literally the same set of V-positions," which is false. What is preserved is cardinality (π is a bijection) and the I-address content under M(d) (by RA-π); the V-positions themselves are permuted.
**Required**: Reword to something like "The projection transports faithfully via π (RE-proj) — preserving cardinality and the underlying I-addresses it identifies — but its V-geometry … is not."

### Issue 3: P4a transition-history derivation repeated verbatim in three places
**ASN-0091, RA-adm discussion (main text) + 3-cut worked example admissibility + 4-cut worked example admissibility**: The same multi-sentence argument — that SequentialTransitionAxiom makes the prior trace `Σ_0, ..., Σ_n` append-only and so any pre-existing P4a witness `Σ_k` remains valid at Σ' — appears three times with substantially identical wording.
**Problem**: The repetition adds significant length without adding rigor; the derivation is the same in each instance. It also forces a reader checking admissibility in the second and third worked examples to re-verify text they've already read.
**Required**: Factor the derivation into a single explanation in the main text (alongside "P4a is the one foundation invariant excluded from this class") with worked examples citing it back rather than rederiving.

### Issue 4: Foundation invariants S8a, S8-fin, S8-depth not enumerated in the "trivially preserved" list
**ASN-0091, "REARRANGE as Vstream-Only Operation" section**: "All remaining state-component-only foundation invariants … are trivially preserved across REARRANGE … In particular, P0, P1, P2, P3, P6, P7, P7a, P8, NodeLineage, L0–L14, L12, L-fin, C0–C2, and C-fin hold at Σ' iff they hold at Σ."
**Problem**: The ASN-0036 invariants S8a, S8-fin, and S8-depth depend on `dom(M(d))`, which is modified-but-domain-preserved by REARRANGE. They are *not* state-component-only (they range over `dom(M(d))`), but they *are* preserved — by RA-dom plus the state-independence of `subspace(v)`, `#v`, and `zeros(v)`. The enumeration omits them entirely. The worked examples then verify them explicitly, but a reader checking the abstract argument has no pointer to where they're discharged.
**Required**: Either (i) add a short clause noting that S8a, S8-fin, S8-depth are preserved because they range over `dom(M(d))` (preserved by RA-dom) and depend only on state-independent structural projections of V-positions, or (ii) for REARRANGE_K specifically, point to R-SP (ASN-0084) which already discharges them.

### Issue 5: Claim table omits the ★ (multi-step composed) forms
**ASN-0091, "Claims Introduced" table**: The table lists single-step RE-* claims but not the ★-form composed claims (RE-C★, RE-dom★, RE-cov★, RE-disc★, RE-proj★, RE-trans★, etc.) that the "Composition Across Multi-Step REARRANGE Sequences" section derives.
**Problem**: The ★ forms are first-class derived claims with stated conditions (some require restrictions like "no step targets `d'`"). A future ASN composing multi-step rearrangement reasoning would need to cite these by name; omitting them from the table makes the citation surface implicit.
**Required**: Either add a separate section in the table for the ★ forms, or note in the table that each RE-* extends to its ★ form under the conditions stated in the composition section.

## OUT_OF_SCOPE

### Topic 1: Cross-document transclusion fragmentation guarantees
**Why out of scope**: Already noted in Open Questions. A formal account of "jointly refer to the same span" across fragmented V-intervals would require new machinery (a notion of transclusion-relationship-with-fragments) this ASN does not introduce.

### Topic 2: Link-subspace rearrangement semantics
**Why out of scope**: REARRANGE_K's CS3 fixes cut subspace at s_C. A link-subspace rearrangement would be a distinct operation with its own admissibility (CL-OWN, CL-UNIQ would interact differently). Open Question noted.

### Topic 3: Observational equivalence of rearrangements at the discoverability level
**Why out of scope**: Open Question. Requires defining an equivalence relation on rearrangement transitions that distinguishes arrangement-equality from link-observable-equality.

### Topic 4: Upper bound on run-decomposition cardinality increase per REARRANGE invocation
**Why out of scope**: Open Question. The structural argument shows the increase is bounded only by the cut sequence's potential to break runs; a tight bound would require constraints not visible at this layer.

### Topic 5: Combinatorial completeness of cut-sequence REARRANGE as a generating set for arrangement bijections
**Why out of scope**: Open Question. Asks whether REARRANGE_K can realize every admissible bijection via finite composition — a meta-question about expressive completeness.

VERDICT: REVISE
