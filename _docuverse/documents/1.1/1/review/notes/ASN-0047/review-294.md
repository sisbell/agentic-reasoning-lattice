# Review of ASN-0047

This is a large, carefully-constructed transition model. The core mathematics — the K.δ/K.μ family discharge, the J0/J1★/J1'★ couplings, the per-subspace D-SEQ★ derivation (the `u_M` infinite-family argument in particular), and the worked examples — is rigorous and the boundary cases I probed (empty arrangement under K.μ⁻, full clearance under K.μ~, interior replacement, k=0 vs k=1 fork content-source) are correctly handled. My findings are confined to precision and accreted meta-prose, the latter per this note's `review-mode.anti-bloat` directive.

## REVISE

### Issue 1: Editorial meta-prose justifying why clause (v) is recorded
**ASN-0047, *Decomposition of K.μ~* (admissibility clauses)**: "Clause (v) is *not* an independent design choice in the manner of (iv); it is *forced by the chosen full-clearance realisation*. … We record this forced property as admissibility clause (v) precisely so the admissible and realisable classes coincide (Step (A)). Clauses (iv) and (v) together are what make the realisable π … coincide with the admissible π."

**Problem**: This is reviser-drift meta-prose — it explains the *editorial decision* to record clause (v) and how it serves Step (A), rather than advancing the argument. The mathematical content (LRP forces `π(v) = v` on `dom_L`) is already stated in the preceding sentence; the bookkeeping commentary about *why the clause exists* is the kind of prose a precise reader must skip past. (By contrast, clause (iv)'s cross-subspace transposition counterexample is genuine content and should stay.)

**Required**: State clause (v) as "(v) link-subspace fixing: `(A v ∈ dom_L(M(d)) :: π(v) = v)` (forced by LRP under the full-clearance realisation)" and delete the paragraph explaining why it is recorded for class-coincidence. The coincidence is established by Step (A) itself.

### Issue 2: The same fact (π fixes `dom_L` pointwise) is derived twice via the same argument
**ASN-0047, *Decomposition of K.μ~*, Step (A) Case `s_L`** and ***Link-subspace fixity and realisation* step (4)**: Step (A) Case `s_L` concludes "Pointwise link fixity (clause (v), `π(v) = v`) for these sources holds by LRP together with CL-UNIQ injectivity at the pre-state." Step (4) then re-derives the identical conclusion: "CL-UNIQ at Σ … forces `π(v) = v`."

**Problem**: Two paragraphs in the same section establish `π(v) = v` on `dom_L` by the same LRP + CL-UNIQ route. This is the "two paragraphs say the same thing in different words" pattern. The second derivation adds only the post-state CL-UNIQ corollary, which is one line.

**Required**: Keep one derivation of pointwise fixity (Step (4), which also yields post-state CL-UNIQ) and have Step (A) Case `s_L` cite it rather than re-deriving, or vice versa.

### Issue 3: Induction variable does not cover the per-state obligation
**ASN-0047, *Extended reachable-state invariants*, proof opening**: "The proof proceeds by induction on the number of valid composite transitions from Σ₀."

**Problem**: The per-state (Class a) invariants are claimed to hold at *every elementary-transition target, including the intermediate states reached partway through a composite*. Induction on the *number of composite transitions* gives the hypothesis only at composite endpoints `Σ_n`; it does not, by itself, reach the intermediate states of composite `n+1`. The actual work that covers intermediate states is the per-elementary matrix ("preserved step-by-step by each elementary transition") — i.e. the real induction for Class (a) is over elementary steps, not composites. The stated induction variable mismatches the stated obligation.

**Required**: State that Class (a) per-state invariants are proved by induction over *elementary* transitions (every elementary-target state, intermediate ones included), with the matrix as the inductive step; reserve composite-count induction for the Class (b) boundary properties where it is appropriate.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior contraction of the link subspace
**Why out of scope**: K.μ⁻ models only suffix removal, so interior withdrawal of a link V-position requires a compact-and-renumber operation the elementary transition does not provide. This is correctly identified in the Open Questions and belongs to a future ASN modeling the implementation's `DELETEVSPAN`; it is not an error in the present elementary set.

VERDICT: REVISE
