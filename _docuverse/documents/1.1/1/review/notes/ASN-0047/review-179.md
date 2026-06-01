# Review of ASN-0047

## REVISE

### Issue 1: Circular citation of K.μ~-FIX in the sufficiency proof

**ASN-0047, *Decomposition of K.μ~*, "Necessity and sufficiency of the precondition" (sufficiency direction)**: "By K.μ~-FIX, `dom(M'(d)) = dom(M(d))`, so `S8a`, `S8-depth`, `S8-fin`, `D-CTG★`, `D-MIN★`, `D-SEQ★` at the post-state inherit unchanged from the pre-state's per-state hypothesis (the V-position domain is fixed)."

**Problem**: K.μ~-FIX is derived *from* D-SEQ★ at the post-state: "D-SEQ★ at the pre- and post-states gives `V_S(d) = {...}` and `V_S(d') = {...}`; since π is a bijection ... `n'_S = n_S` and `V_S(d') = V_S(d)`." The sufficiency proof is establishing admissibility clause (i), which *is* the stipulation of D-SEQ★(Σ') and the other post-state invariants. Using K.μ~-FIX (which presupposes D-SEQ★(Σ')) to inherit D-SEQ★(Σ') is circular: K.μ~-FIX is only valid once admissibility holds, and admissibility is precisely what sufficiency must prove. The necessity direction avoids this (admissibility is assumed there), but sufficiency cannot.

**Required**: For the transposition witness `π_swap`, domain fixity holds *by construction* — `π_swap` is a permutation of `dom(M(d))` fixing all but two elements, so `dom(M'(d)) = π_swap(dom(M(d))) = dom(M(d))` directly from the bijection equation, independent of any post-state invariant. Cite that construction, not K.μ~-FIX, so the post-state invariants inherit from a genuinely prior fact.

### Issue 2: k=1 child-spawn zero-count condition denied rather than discharged

**ASN-0047, *K.δ case (ii) discharge and parent-allocator activation*, k=1 bullet**: "child-spawn admissibility: `k' = 1 ∈ {1, 2}` and no zero-count side condition fires at `k' = 1`."

**Problem**: T10a's axiom imposes a runtime precondition "`zeros(t) ≤ 3` when `k' = 1`" (and `zeros(t) ≤ 2` when `k' = 2`). There *is* a zero-count side condition at `k' = 1`. The claim that "no zero-count side condition fires" contradicts the foundation T10a discipline. The k=2 bullet handles its bound correctly and explicitly ("T10a admits `k' = 2` when `zeros(spawnPt) ≤ 2`, satisfied a fortiori"), so the k=1 treatment breaks the ASN's own per-step discharge convention.

**Required**: Discharge the k=1 condition the same way as k=2: the operand `t ∈ E_doc` has `zeros(t) = 2 ≤ 3`, so T10a's `k' = 1` precondition is satisfied a fortiori — not absent.

### Issue 3: Why-needed justifications that imagine the excluded case

**ASN-0047, K.μ⁺ amendment (ContentSubspaceRestriction)**: "The restriction is necessary — without it, K.μ⁺ could create a link-subspace V-position mapping to dom(C), violating S3★."

**ASN-0047, K.μ⁺_L precondition (`ℓ ∉ ran(M(d))`)**: "This guarantees CL-UNIQ at the post-state: were `ℓ ∈ ran(M(d))` already, there would exist some `v' ∈ dom(M(d))` ... and adding `(v_ℓ, ℓ)` ... would produce two distinct V-positions both mapping to `ℓ`, violating CL-UNIQ."

**Problem**: Both passages argue from a counterfactual that the precondition itself rules out — explaining why the restriction is needed rather than stating what it requires, and reasoning about a state the carrier excludes. This is the reviser-drift pattern the note flags ("a paragraph imagines a case the claim's precondition already excludes" / "explains why the axiom is needed rather than what it says"). The discharge that matters (the precondition holds, so S2/S3★/CL-UNIQ are preserved) stands without the counterfactual.

**Required**: State the precondition and the invariant it discharges; drop the "without it / were it otherwise" counterfactual elaboration.

## OUT_OF_SCOPE

None. The ASN stays within state, transitions, and invariants; named operations and concurrency are correctly deferred to Open Questions and the Scope exclusions.

VERDICT: REVISE
