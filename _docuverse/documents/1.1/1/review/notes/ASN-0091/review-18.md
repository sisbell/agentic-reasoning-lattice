# Review of ASN-0091

## REVISE

### Issue 1: S2 derivation cites pre-state S2 only at conclusion

**ASN-0091, "S2 derivation at the abstract level"**: "RA-π then assigns Σ'.M(d)(v') = Σ.M(d)(v), a function value determined uniquely by v'."

**Problem**: The phrase "a function value determined uniquely by v'" relies on pre-state S2 (Σ.M(d) being a function). The closing sentence "it relies only on RA-dom, RA-π (bijection), and S2 at Σ" mentions this dependency only after the derivation, not at the step where it is invoked. A reader following the argument step-by-step sees "function value" without attribution.

**Required**: Make pre-state S2 explicit at the point of use — e.g., "Σ.M(d)(v) is uniquely determined by v (pre-state S2)".

### Issue 2: Subspace-preservation derivation appears twice

**ASN-0091, "REARRANGE as Vstream-Only Operation" and "Subspace Frame (REARRANGE_K-specific)"**

**Problem**: The argument that RA-adm + S3★ + L14 forces π to preserve subspaces is given in two places. The first instance (within the abstract-class definition discussion) is woven into the type-correctness argument for π's admissibility; the second (in "Subspace Frame") restates it as part of distinguishing pointwise fixity from subspace preservation. The two presentations differ slightly in framing without cross-reference.

**Required**: Consolidate the derivation in one place and cross-reference from the other, or explicitly note the repetition is for emphasis at each citation site.

### Issue 3: Unclear parenthetical in RE-proj reverse-inclusion

**ASN-0091, "Projection Transports Along π"**: "Then v ∈ dom(Σ.M(d)) (RA-dom carries π's domain to dom(Σ.M(d)))..."

**Problem**: The parenthetical "RA-dom carries π's domain to dom(Σ.M(d))" is unclear. The intended chain is: v' ∈ project(e, d, Σ') ⊆ dom(Σ'.M(d)); RA-dom gives dom(Σ'.M(d)) = dom(Σ.M(d)); π is a bijection of dom(Σ.M(d)) onto itself, so π⁻¹(v') ∈ dom(Σ.M(d)). The current phrasing collapses these steps in a way that obscures what RA-dom contributes.

**Required**: Restate the inclusion chain explicitly: "v ∈ dom(Σ.M(d)) because v' ∈ dom(Σ'.M(d)) = dom(Σ.M(d)) (by RA-dom), and π⁻¹ is a bijection of this set".

### Issue 4: Bijection witness phrasing in "Where Position Lives After Rearrangement"

**ASN-0091, "Where Position Lives After Rearrangement"**: "The bijection π is the entire content of the rearrangement."

**Problem**: When shared I-addresses exist (S5/UnrestrictedSharing), π is not unique — the same transition Σ → Σ' admits multiple valid bijections, as the ASN itself discusses in the opening section and exhibits in the fourth worked example. The phrasing "the bijection π" suggests uniqueness that does not hold.

**Required**: Phrase as "a bijection π" or "any valid bijection π witnessing the transition", with a back-reference to the non-uniqueness discussion in "REARRANGE as Vstream-Only Operation".

VERDICT: REVISE
