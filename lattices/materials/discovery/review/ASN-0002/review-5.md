# Review of ASN-0002

## REVISE

### Issue 1: P.temp_functional's formal biconditional contradicts its prose label as a "single-body statement"
**ASN-0002, §"Temperature as a functional of mean translational vis viva"**: "[P.temp_functional] ... the temperature of a body is a strictly monotone function of B.T̄ alone: for bodies B₁, B₂ at equilibrium, temp(B₁) = temp(B₂) ⇔ B₁.T̄ = B₂.T̄, temp(B₁) < temp(B₂) ⇔ B₁.T̄ < B₂.T̄."

**ASN-0002, §"Sharing of translational vis viva between species"**: "P.temp_functional is a single-body statement: it fixes that each body's temperature is a strictly monotone function of its own B.T̄." And then: "[P.temp_functional_species_independent] ... Equivalently: for any two bodies B₁, B₂ at equilibrium, temp(B₁) = temp(B₂) ⇔ B₁.T̄ = B₂.T̄, whether B₁ and B₂ share species or not."

**Problem**: The biconditional in P.temp_functional quantifies universally over pairs of bodies (B₁, B₂) with no restriction on shared species composition. Read literally, that already forces temp(B₁) = temp(B₂) whenever B₁.T̄ = B₂.T̄ across species-distinct bodies — i.e., it already encodes species-independence. But the later section labels P.temp_functional a "single-body statement" and introduces P.temp_functional_species_independent with the same biconditional (explicitly adding "whether B₁ and B₂ share species or not") as a separate commitment. The formal statement of P.temp_functional does not match the prose reading, and P.temp_functional_species_independent duplicates what P.temp_functional already entails.

**Required**: Either (a) restrict the biconditional in P.temp_functional to bodies of a common species composition, so that cross-composition coverage is genuinely added by P.temp_functional_species_independent, or (b) reformulate P.temp_functional as a single-body claim without a two-body biconditional (e.g., "for any body B, temp(B) = f_B(B.T̄) for some body-specific strictly monotone f_B"). Keep the formal statement, the prose explanation, and the derivation chain of P.equipartition consistent with whichever choice is made.

### Issue 2: P.beta_unity_iff_no_internal's justification covers only one direction of the iff
**ASN-0002, §"The internal compartment and the ratio β"**: "[P.beta_unity_iff_no_internal] β_k = 1 iff species k carries no internal degree of freedom capable of exchanging energy with translation through encounters. A pure centre of force, having no internal structure at all, is the clearest case of β = 1. More generally, a molecule may carry internal modes (rotations, oscillations) that are dynamically decoupled from translation by the particular encounter law, in which case those modes cannot be excited by encounters and β = 1 holds regardless."

**Problem**: The argument given grounds only the backward direction: if a species has no exchangeable internal DOF (either no internal structure or dynamically decoupled modes), then m.eint cannot be excited by encounters and β_k = 1. The forward direction — β_k = 1 ⇒ no exchangeable internal DOF — is not argued. Under the ASN's own apparatus this direction is not automatic: a species with a DOF coupled to translation via the encounter law could in principle carry a species-characteristic apportionment ratio of zero (the ASN treats β_k − 1 as a species-imported value following Clausius, not as derivationally required to be strictly positive when an exchangeable DOF is present), which would produce β_k = 1 while an exchangeable DOF exists. The "iff" is therefore half-argued.

**Required**: Either (a) weaken to an implication ("no exchangeable internal DOF ⇒ β_k = 1") and note that the converse is not grounded in the present apparatus; (b) supply an argument that any DOF capable of exchanging energy with translation must carry a strictly positive share at equilibrium, closing the forward direction; or (c) relabel P.beta_unity_iff_no_internal as a postulated structural commitment (using the same honest postulate framing used for P.beta_species_invariant) and drop the examples' presentation as derivational justification for an iff.

VERDICT: REVISE
