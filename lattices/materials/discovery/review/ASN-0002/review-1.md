# Review of ASN-0002

## REVISE

### Issue 1: P.equipartition derivation insufficient
**ASN-0002, "Sharing of translational vis viva between species"**: "This is the per-molecule equality applied across species; it is the same content as P.temp_functional, stated for pairs."
**Problem**: P.temp_functional is a single-body statement — temperature is a monotone function of *one body's* B.T̄. P.equipartition is a cross-species claim: when two species coexist at equilibrium, their per-molecule means are equal. That step requires additional commitments — that two bodies at equal temperature have equal B.T̄ (not just that each body's temp is monotone in its own B.T̄), and that this per-molecule criterion applies across species within a mixed body. The "same content" framing hides this.
**Required**: Either walk the cross-species derivation explicitly from P.temp_functional plus a stated assumption that the temperature functional is species-independent, or label P.equipartition as a separate commitment with its own justification.

### Issue 2: γ = (2 + 3β)/(3β) is unjustified and uses out-of-scope apparatus
**ASN-0002, "The internal compartment and the ratio β"**: "β is empirically accessible through the specific-heat ratio γ = c_p/c_v, via γ = (2 + 3β)/(3β)"
**Problem**: This formula is asserted without derivation. It relies on the distinction between c_p and c_v, which presupposes work done against pressure — pressure-volume-temperature apparatus that the ASN's scope declaration explicitly excludes. Stating the formula here smuggles that apparatus in as a fact.
**Required**: Either derive γ(β) from the theory's commitments (which will require importing P-V-T machinery and may belong in a future ASN), or replace the formula with a weaker statement that β is in principle pinned by some observable thermal ratio, deferring the specific relation.

### Issue 3: Encounter commitments need a dilute regime
**ASN-0002, "Conservation through encounters"**: "An encounter between two molecules is an interaction episode, bounded in time… Outside encounters, molecules move freely."
**Problem**: Bounded, non-overlapping encounters with free flight between them is a *dilute* regime assumption. In a dense body, interactions need not factor into discrete pairwise episodes; three-body and persistent interactions are generic. P.enc_momentum, P.enc_energy, and P.enc_ratio_equilibration all rest on this picture, but the regime is not stated. P.atomic_heat_regularity is then applied to solids, which are not dilute — yet the same encounter framework is being invoked to justify β-invariance there.
**Required**: State the dilute regime explicitly as the domain of validity for the encounter apparatus, and say what the theory commits to (or declines to commit to) in the dense regime where encounters do not factor.

### Issue 4: P.temp_functional derivation hand-waves the key step
**ASN-0002, "Temperature as a functional of mean translational vis viva"**: "What is exchanged across that boundary is translational motion — the internal compartment of a molecule does not detach from that molecule and migrate across. If heat flow is what regulates the approach to equilibrium, and if heat is energy of motion, then what equilibrates is the exchange of translational vis viva."
**Problem**: The argument conflates "internal energy does not migrate bodily between molecules" with "internal energy does not participate in equilibration." P.enc_energy allows each encounter to redistribute energy between a molecule's translational and internal compartments; internal energy can therefore change via encounters even though it does not physically cross the boundary as such. The derivation needs to walk through why the mean translational vis viva per molecule — rather than, say, mean total energy per molecule — is the quantity whose equality defines thermal equilibrium.
**Required**: Complete the derivation step, or demote P.temp_functional to a postulate and strike the "why the theory commits to this" paragraph's claim of following-by-argument.

### Issue 5: "Classical regime where internal modes are fully active" is anachronistic
**ASN-0002, "The internal compartment and the ratio β" and later**: "β_k depends only on molecular species… in the classical regime where internal modes are fully active"; "At temperatures low enough that internal modes become dynamically inaccessible, β effectively falls."
**Problem**: The concept of internal modes being "fully active" versus "dynamically inaccessible" depending on temperature is a quantum-mechanical phenomenon (mode freezing). The 1819 corpus has no quantum mechanics; it has no notion that classical internal degrees of freedom could fail to hold energy at low temperature. Importing this concept as a regime qualifier — and using it to explain where P.atomic_heat_regularity holds — reaches beyond the corpus's apparatus.
**Required**: Either define "classical regime" purely within the theory's own vocabulary (e.g., as a regime in which the corpus's measurements were taken, without claiming to know what makes modes inactive outside it), or drop the regime-condition phrasing and note only that β is measured empirically in the regime the corpus covers.

### Issue 6: "Smooth elastic sphere transfers force along the line of centres" asserted, not derived
**ASN-0002, "The internal compartment and the ratio β"**: "A perfectly smooth elastic sphere has none that encounters can excite, since collisions transmit force only along the line of centres and therefore transfer no angular momentum"
**Problem**: This is a specific mechanical claim about collision mechanics used to support P.beta_unity_iff_no_internal. The theory's commitments include inertial mass, velocity, internal energy, and conservation in encounters — they do not include a force law restricting impulse to the line of centres. The claim is imported from classical rigid-body mechanics, not derived from the commitments on the table.
**Required**: Either flag the smooth-sphere argument as an illustrative instance that assumes a specific collision law (not as evidence for the commitment), or state the collision mechanics as an auxiliary postulate when it is needed.

### Issue 7: "Species" is used before being defined
**ASN-0002, throughout section "The internal compartment and the ratio β" onward**: "species_k(B.mols)", "β_k depends only on molecular species"
**Problem**: The Σ.* commitments introduce molecules with mass, velocity, and internal energy, but no species partition. "Species" then appears as a partition of B.mols used throughout β claims and P.equipartition. What distinguishes species — mass? internal constitution? a species label attribute? — is not declared.
**Required**: Introduce species either as a Σ-level attribute on molecules (a species tag) or as an equivalence class on molecules induced by mass and internal constitution, and state which. P.beta_species_invariant presupposes this definition.

## OUT_OF_SCOPE

### Topic 1: Quantitative relation between β and observable specific-heat ratios
**Why out of scope**: Connecting β to experimental γ = c_p/c_v requires P-V-T apparatus (already declared out of scope). A future ASN that introduces gas laws can derive the γ(β) relation there.

### Topic 2: Mechanism by which encounters drive the translational–internal ratio to its equilibrium value
**Why out of scope**: The ASN correctly flags this as postulated, attributed to Clausius, and notes the mechanism is beyond present reach. It is appropriate to leave the convergence mechanism for a future ASN.

VERDICT: REVISE
