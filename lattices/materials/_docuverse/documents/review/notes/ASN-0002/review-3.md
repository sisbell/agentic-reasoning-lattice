# Review of ASN-0002

## REVISE

### Issue 1: Premise (iv) cannot support the per-encounter T↔eint exchange that β>1 requires

**ASN-0002, "Conservation through encounters"**: "(iv) the inter-molecular force is conservative — central, depending only on the separation of the pair, and derivable from a scalar potential U(r) that vanishes outside the sphere of sensible action."

And later, following P.enc_energy: "For β > 1 the translational sum T(m₁) + T(m₂) may change per encounter, with the balance flowing into or out of m.eint."

**Problem**: A force whose potential is U(r), with r the scalar separation of centres of mass, acts along the COM-connecting line and appears only in the equations of motion of the two COM coordinates. It does not couple to internal degrees of freedom (rotational orientation, bond-vibration coordinates, or relative coordinates of sub-parts). Under (iv) as stated, T(m₁)+T(m₂) and each m.eint are separately conserved through an encounter — T+eint is trivially conserved, but the "balance flowing into or out of m.eint" has no dynamical mechanism in the stated apparatus. The β>1 case is left without a per-encounter mechanism, and P.enc_ratio_equilibration — which presupposes such a mechanism to average to (β−1) — inherits the gap.

**Required**: Either generalize (iv) so the pair interaction can do work on internal coordinates (e.g., a sum of part-wise potentials, so U depends on internal configurations as well as COM separation), or explicitly demote the β>1 case: P.enc_energy stands as derived only for β=1, and for β>1 the per-encounter T↔eint exchange is a separate postulate at the molecule-level dynamics layer. State which route the theory commits to.

### Issue 2: Motion-primacy elasticity evidence lacks corpus citation

**ASN-0002, "The primacy of motion"**: "a statical theory in which elastic response arises from inter-particle forces at rest predicts a fixed ratio between the elasticity of form and the elasticity of volume of any body. That ratio is wrong in two distinct domains. In fluids, form-elasticity is vanishing while volume-elasticity is considerable... In solids, direct measurement of form-elasticity comes in smaller than the statical ratio predicts."

**Problem**: These are empirical claims about measured elasticities, used as two of the three grounds forcing P.motion_primacy. The only corpus citation in the ASN is `[1819-dulong-petit]`. An empirical observation cannot be invoked to reject a rival constitution unless the corpus supplies the observation; the ASN currently leans on unattributed elasticity data. Without citation, the reader cannot check which substances, which regime, and with what precision the claims rest.

**Required**: Cite the corpus source(s) for the form-vs-volume elasticity observations in fluids and in solids, at the scope and precision the corpus supports. If no such source exists in the corpus, remove the elasticity argument and carry P.motion_primacy on what remains (demoting the postulate's strength if the remaining grounds do not suffice).

### Issue 3: P.equipartition derivation treats species sub-populations as temperature-bearing bodies without licensing it

**ASN-0002, "Sharing of translational vis viva between species"**: "Treat the species sub-populations species_1(B.mols) and species_2(B.mols) as aggregates with mean translational vis vivas per molecule T̄_1 and T̄_2 respectively; within the body's equilibrium state, the two sub-populations must share a common temperature (otherwise heat would flow between them, contradicting equilibrium). By P.temp_functional_species_independent the same functional f applies to both sub-populations, and by P.temp_functional's strict monotonicity equal temperature forces T̄_1 = T̄_2."

**Problem**: P.temp_functional defines temperature as a functional of a *body's* B.T̄. A species sub-population within a mixed body is a subset of B.mols, not a body. The step "the two sub-populations must share a common temperature (otherwise heat would flow between them)" presupposes that a sub-population has its own temperature and can exchange heat with another sub-population co-inhabiting the same body — a sub-body premise the apparatus has not committed to. Without that premise the derivation of P.equipartition does not close.

**Required**: Make the sub-body step explicit. Either add a labeled commitment that, at equilibrium, each species sub-population within a mixed body behaves as a sub-body to which P.temp_functional and P.temp_functional_species_independent apply, and justify it (e.g., by noting that at equilibrium each sub-population's velocity distribution is the marginal of a factorisable joint distribution); or re-derive P.equipartition on a route that does not rely on sub-population temperatures (and mark that route as deferred to the distributional apparatus, reducing P.equipartition to a postulate at this level).

VERDICT: REVISE
