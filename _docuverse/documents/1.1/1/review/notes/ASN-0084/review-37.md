# Review of ASN-0084

## REVISE

### Issue 1: "The bijection π" phrasing claims uniqueness it does not establish
**ASN-0084, R-PPERM and R-SPERM**: "The bijection π : dom(M(d)) → dom(M'(d)) satisfying M'(d)(π(v)) = M(d)(v) is..."
**Problem**: When M(d) has duplicate I-addresses (permitted by S5 — UnrestrictedSharing — and exhibited in Worked Example 2 where origin-distinguished but sharing-compatible patterns appear), multiple bijections satisfy M'(d)(π(v)) = M(d)(v): any reassignment that preserves multiplicity within an I-address equivalence class is a valid witness. The lemma constructs one such bijection — the cut-point-induced one — but the definite article "The" suggests uniqueness that is not proved.
**Required**: Rephrase as "The cut-point-induced bijection π..." or "A canonical bijection π..." and add a sentence noting the construction picks one element from an equivalence class of valid bijections when M(d) has duplicates.

### Issue 2: R-WP's proof references content defined later in the ASN
**ASN-0084, R-WP proof**: "R-BLK constructs B' from B via Phases 1–3 under R-PRE; we verify both S8 clauses (a) and (b) on the construction" and "by R-COMM, valid because v_j and v_j + k lie in the same region after Phase 1".
**Problem**: R-WP appears in the "Sufficient Precondition" section, but its S8 discharge relies on R-BLK (Phases 1–3) and R-COMM, both defined two sections later. A reader walking the ASN top-to-bottom encounters the proof's load-bearing claims as forward references with no preview.
**Required**: Either reorder the sections so R-COMM and R-BLK precede R-WP, or prefix R-WP with an explicit forward-reference note stating what R-BLK constructs and what R-COMM provides.

### Issue 3: Necessity analysis missing — sufficiency is the only direction shown
**ASN-0084, R-WP**: "The lemma establishes sufficiency only (one direction, ⇐) ... Necessity — that R-PRE etc. is *required* for Q to hold under REARRANGE_C — is not claimed here ... is beyond the scope of this ASN."
**Problem**: With sufficiency alone, the reader cannot judge whether R-PRE is over-strong. Is R-PRE(iv) (full coverage of the affected range) necessary? Is R-PRE(v) (w_α, w_β ≥ 1) necessary? Without at least one concrete necessity result, the strength of R-PRE is unverified. The depth requirement of the review standard expects "Find a non-trivial case" for wp analysis; the ASN computes wp's sufficient antecedent for a non-trivial Q but skips necessity entirely.
**Required**: Add at least one necessity sketch — exhibit a concrete pre-state where dropping one conjunct of R-PRE (e.g., the coverage clause R-PRE(iv)) causes Q to fail on a specific invariant (e.g., S8(b) misalignment after Phase 1 cannot split a gapped run cleanly).

### Issue 4: Subspace confinement consequence omits compound-shift case
**ASN-0084, "Consequences of R-PRE — Subspace confinement"**: "The shifted positions `c₀ + j`, `c₁ + j`, `c₂ + j` named in R-P1, R-P2, R-S1, R-S2, R-S3 retain subspace S by case analysis on j..."
**Problem**: R-P2's LHS is `c₀ + w_β + j`, R-S2's is `c₀ + w_β + j`, R-S3's is `c₀ + w_β + w_μ + j`. These are *compound* shifts, not the single shifts `c_i + j` enumerated. The extension via Extended Associativity ((c₀ + w_β) + j with each step preserving subspace) is straightforward but not stated; the reader must reconstruct it.
**Required**: Add: "Compound shifts c_i + (w_β + j), c_i + (w_β + w_μ + j) reduce via Extended Associativity to iterated single shifts (c_i + w_β) + j or ((c_i + w_β) + w_μ) + j, each preserving subspace by OrdShiftHom (b)."

### Issue 5: Worked Example 1 has shallower R-BLK trace than Examples 2 and 3
**ASN-0084, Worked Example: 3-Cut Pivot**: Phase 1 is described in detail; Phases 2 and 3 are compressed to "The rearrangement then inserts the single-element D run between ([1,1], A, 1) and ([1,2], B, 2)."
**Problem**: Worked Examples 2 and 3 each give explicit Phase 1 (Split), Phase 2 (Classify), Phase 3 (Reassemble) traces with per-run displacement. Example 1's compressed form is inconsistent and forces the reader to mentally re-execute the algorithm.
**Required**: Expand Example 1 with explicit Phase 2 classification (([1,1], A, 1) → exterior left; ([1,2], B, 2) → α; ([1,4], D, 1) → β; ([1,5], E, 1) → exterior right) and Phase 3 reassembly with Δ_α = +1, Δ_β = −2, mirroring Examples 2 and 3.

### Issue 6: REARRANGE_C operation parameterization could be clearer
**ASN-0084, "Operation — REARRANGE_C"**: "REARRANGE_C(Σ, d) is the state transition Σ → Σ' parameterized by a cut sequence C and a target document d..."
**Problem**: The operation is named REARRANGE_C (subscripted by C), and `REARRANGE_C(Σ, d)` takes Σ and d as arguments. But the precondition R-PRE(C) takes C explicitly, suggesting C is also a runtime parameter. The notational distinction between operation-symbol parameterization and operation-application arguments is left implicit.
**Required**: Clarify whether C is a static parameterization of an operation family or a runtime input; if the latter, write `REARRANGE(Σ, d, C)` for consistency with how R-PRE(C) is invoked.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: Listed as open question 1. The structural extension to higher cut counts is genuinely new territory and warrants its own ASN.

### Topic 2: Higher-depth text subspaces (m_1 > 2)
**Why out of scope**: The ASN explicitly restricts to m_1 = 2 throughout, and multi-component ordinal arithmetic for displacement analysis would require its own lift via NAT-sub on tumblers rather than singletons.

### Topic 3: REARRANGE_C composition
**Why out of scope**: Listed as open question 2. Whether sequences of REARRANGE_C compose to a single REARRANGE_C requires a separate algebraic analysis.

### Topic 4: Maximal partition characterization of M'(d)
**Why out of scope**: R-BLK acknowledges B' may not be canonical, and the closing remark explicitly identifies which pre-state pairs become mergeable post-state as outside scope. Worked Example 2 exhibits the phenomenon (B and H merging into a width-3 run); a full characterization would require its own structural analysis.

### Topic 5: Link-subspace REARRANGE
**Why out of scope**: The ASN explicitly confines REARRANGE to text subspace (S = 1, depth 2). Bridge semantics for links — endset preservation, tombstoning behaviour — is deferred to a separate operation.

### Topic 6: Cross-subspace constraints on cut placement
**Why out of scope**: CS3 forces cuts into a single subspace by construction; multi-subspace cut sequences are a different operation class.

VERDICT: REVISE
