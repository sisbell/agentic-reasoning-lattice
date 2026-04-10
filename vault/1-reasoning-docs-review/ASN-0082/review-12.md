# Review of ASN-0082

## REVISE

### Issue 1: Local axioms VD and VP reinvent foundation properties from ASN-0036
**ASN-0082, Local Axioms**: VD ("All V-positions within a given subspace of a document share the same tumbler depth") and VP ("subspace(v) = v₁ ≥ 1")
**Problem**: ASN-0036 already establishes both results. S8-depth states `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)` — identical to VD. S8a states `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)` — which subsumes VP and is strictly stronger. VP extracts only the `v₁ ≥ 1` conjunct while dropping `zeros(v) = 0` and `v > 0`, creating a weaker local axiom whose preservation (I3-VP) does not establish full S8a preservation. VB (BootstrapDiscipline) exists solely to derive VD from T10a.1, but S8-depth already provides the result — VB introduces allocator-discipline machinery unused by any other proof in this ASN.
**Required**: Cite S8-depth and S8a from ASN-0036 as the operative invariants. Remove VB and VD. I3-VD should verify S8-depth preservation; I3-VP should verify full S8a preservation (including `zeros(v) = 0`). The proof for the zero-count condition is straightforward: shifted positions inherit all components from v at positions `< m` (positive by S8a on M(d)) and have `vₘ + n > 0` at position m.

### Issue 2: Statement registry misattributes foundation definitions as locally introduced
**ASN-0082, Statement Registry**: M(d) listed as "introduced (local)", subspace(v) listed as "introduced (local)"
**Problem**: ASN-0036 defines `Σ.M(d) : T ⇀ T` (the arrangement function) and `subspace(v) = v₁` (the subspace identifier). These are foundation definitions, not local introductions. The registry marks both as "introduced (local)" when they should be "cited (ASN-0036)."
**Required**: Change both entries from "introduced (local)" to "cited (ASN-0036)."

### Issue 3: Missing content-store frame condition; S3 and S9 preservation unverified
**ASN-0082, Post-Insertion Shift / Structural preservation**: The seven clauses constrain M'(d) but say nothing about C.
**Problem**: The shift operates on arrangements without modifying the content store C, but this is never stated. Without this frame condition, referential integrity (S3: every I-address in ran(M(d)) is in dom(C)) cannot be verified for the post-state. S9 (TwoStreamSeparation, ASN-0036) establishes that arrangement changes preserve content — but the ASN neither cites S9 nor states the content-store frame. The structural preservation section claims to "enable composition with subsequent operations," yet an operation depending on S3 cannot confirm it from the stated postconditions.
**Required**: Add a content-store frame condition (e.g., `I3-C: dom(C') = dom(C) ∧ (A a : C'(a) = C(a))`). Then verify S3 preservation: for every v ∈ dom(M'(d)), M'(d)(v) ∈ dom(C) — which follows from C unchanged (I3-C) and the fact that every M'(d) value equals some M(d)(u) ∈ dom(C) by S3 on the pre-state. Cite S9 as the foundation guarantee that arrangement-only modifications preserve content.

### Issue 4: I3-CS and I3-CX labeled "frame" in registry but function as domain closure postconditions
**ASN-0082, Statement Registry**: I3-CS and I3-CX listed with Type = "frame"
**Problem**: Frame conditions describe what doesn't change. I3-CS and I3-CX constrain what positions are *permitted* in dom(M'(d)) — they close the domain from above. The body text correctly describes them as "domain closure clauses," but the registry labels them "frame." This distinction matters for composition: the INSERT ASN will add gap positions to dom(M'(d)), which extends (not violates) I3-L/I3-X but does violate I3-CS's upper bound. Calling them "frame" suggests they persist through composition; they don't.
**Required**: Change registry Type for I3-CS and I3-CX from "frame" to "postcondition" (matching their function as domain closure constraints on the shift step).

## OUT_OF_SCOPE

### Topic 1: Correspondence run (S8) preservation under shift
**Why out of scope**: I3 preserves individual mappings; the lift to S8's finite correspondence-run decomposition (showing that (shift(v, n), a, k) is a valid run whenever (v, a, k) was) is a natural derived result but belongs in a future ASN connecting the shift to the POOM structure.

### Topic 2: D-CTG / D-SEQ for intermediate post-shift state
**Why out of scope**: The gap [p, shift(p, n)) violates D-CTG (V-contiguity). Restoration requires gap-filling, which the ASN explicitly defers to the INSERT ASN. The forward reference notes that VD and VP must be re-derived; it should also mention D-CTG and D-SEQ, but this is a completeness note for the forward reference, not an error in this ASN.

VERDICT: REVISE
