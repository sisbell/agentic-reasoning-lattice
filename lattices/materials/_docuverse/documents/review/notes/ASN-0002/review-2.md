# Review of ASN-0002

## REVISE

### Issue 1: Species-independence of temperature functional is a smuggled premise
**ASN-0002, "Sharing of translational vis viva between species"**: "To move from there to a cross-species claim, two further commitments are needed. First, the temperature functional must be *species-independent*: the same functional of B.T̄ applies to any body regardless of the species composition..."
**Problem**: Species-independence is used as a premise in the derivation of P.equipartition but is never given a claim label (no P.temp_functional_species_independent or similar). It appears in no row of the Claims Introduced table. A commitment load-bearing enough to derive P.equipartition cannot sit in connective prose; it must be named and accounted for in the postulate/derived ledger.
**Required**: Elevate species-independence of the temperature functional to a labeled P-claim, with status (postulated? derived? from what?) and regime. Add it to the Claims Introduced table. Then have P.equipartition's derivation cite it by label.

### Issue 2: P.temp_functional's stated regime does not match its actual regime
**ASN-0002, "Temperature as a functional of mean translational vis viva"**: "**[P.temp_functional]** In the equilibrium regime, the temperature of a body is a strictly monotone function of B.T̄ alone..."
**Problem**: The prose statement of the commitment names only "equilibrium regime." But the subsequent discussion records that support "rests on the dilute regime… and on the centres-of-force modeling of encounters," and the status-column entry qualifies it accordingly. The main claim statement must carry the same regime qualification as the status row; a reader citing P.temp_functional from the body will promote it beyond what the theory established.
**Required**: Restate P.temp_functional in the body with the same regime qualifications as the table row: "In the equilibrium regime, in the dilute regime, under the centres-of-force modeling of encounters, ..."

### Issue 3: P.enc_momentum and P.enc_energy rely on a naming-based "follows from"
**ASN-0002, "Conservation through encounters"**: "Both claims follow from the more general principle that molecular interactions are dynamical, governed by some force law, and therefore inherit the conservation principles of any such dynamics."
**Problem**: This is proof by naming. "Inherit the conservation principles of any such dynamics" is an appeal to an unstated framework. Conservation of momentum per encounter requires specifically that the inter-molecular forces be internal to the pair (action–reaction) and that no external impulse act during the encounter interval; conservation of energy requires that the force law be conservative and that the encounter be between an isolated pair. None of these premises is stated. The claims themselves are strong enough that the theory must either postulate them outright, or step through the premises (Newtonian mechanics at the molecule level, action–reaction, isolated pair during encounter interval, conservative force law).
**Required**: Either flag P.enc_momentum and P.enc_energy as postulates with their required premises named (Newtonian mechanics at molecule level; force internal to the pair; isolated-pair regime; conservative force), or replace the "follows from" with a stepped argument from those premises.

### Issue 4: The equipartition derivation reaches into the mathematical form of velocity distributions
**ASN-0002, "Sharing of translational vis viva between species"**: "The only solutions are Maxwellian distributions whose moduli α₁, α₂ satisfy M₁α₁² = M₂α₂²..."
**Problem**: The scope list explicitly rules out "the distribution of molecular velocities and its mathematical form." The P.equipartition derivation (and the support argument for P.temp_functional) rests on uniqueness of the Maxwellian as the solution to a functional equation — the *form* of the velocity distribution. The ASN imports an out-of-scope result to carry its derivations.
**Required**: Either demote P.temp_functional and P.equipartition to postulates (stated without the distributional argument), with their status row reading "postulated" and the regime qualifications preserved; or reconstruct the derivation using only the apparatus this ASN commits to. Do not use the Maxwellian as a load-bearing intermediate while claiming the distributional form is outside scope.

### Issue 5: "Attributed to Clausius" is an attribution, not a ground
**ASN-0002, "The internal compartment and the ratio β"**: "The postulate (attributed to Clausius) is that many encounters drive the translational–internal ratio to a stable equilibrium value..."
**Problem**: The apportionment postulate is supported by naming a historical figure rather than by a commitment the theory takes on its own authority. A postulate stands on the theory's own decision to accept it or on an evidential tie to the corpus; attribution to a named person is neither. Additionally, "many encounters" is an unquantified modifier that the review instructions explicitly flag as a hand-wave ("Many in what sense?").
**Required**: Remove the attribution; state the postulate as what the theory adopts, naming what alternative it rejects (e.g., "the theory adopts that equilibration of the internal compartment with translation through the aggregate of encounters yields a species-characteristic ratio; the alternative — that the ratio depends on state or on history — is rejected on the grounds of …"). If Clausius appears in the corpus, cite the corpus entry as evidence rather than naming the person as source. Replace "many encounters" with the regime condition actually at work (equilibrium regime, per P.enc_ratio_equilibration).

### Issue 6: Miscount in the grounds for P.motion_primacy
**ASN-0002, "The primacy of motion"**: "Two empirical grounds and one conceptual ground force the commitment."
**Problem**: Only one empirical ground (the elasticity/fluidity of fluids) and one conceptual ground (relativity of motion) are given. The sentence promises a second empirical ground that is not delivered.
**Required**: Either supply the second empirical ground, or correct the count to "one empirical ground and one conceptual ground."

## OUT_OF_SCOPE

None. The gaps catalogued in "What the theory leaves underdetermined" and the Open Questions are appropriately flagged as boundaries rather than errors.

VERDICT: REVISE
