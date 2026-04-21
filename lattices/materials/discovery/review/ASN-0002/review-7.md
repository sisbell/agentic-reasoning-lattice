# Review of ASN-0002

## REVISE

### Issue 1: β_k = 1 discharge claim contradicts the case the ASN itself admits earlier
**ASN-0002, §"Conservation through encounters" and claims-table entry for P.enc_ratio_equilibration**: "For β_k = 1 the postulate is discharged by the encounter apparatus (i)–(iv) automatically: with no internal compartment, there is no apportionment to drive and no T ↔ eint exchange mechanism is needed."
**Problem**: §"The internal compartment and the ratio β" explicitly admits a β_k = 1 case in which an exchangeable internal DOF is present — "A species whose internal DOF is coupled to translation through the encounter law but whose equilibrium share happens to be zero would produce β_k = 1 while an exchangeable DOF exists; the present apparatus contains no derivation that forbids such a case." The later unqualified discharge claim, whose justification is "with no internal compartment," does not cover this case: an internal compartment is present, and maintaining its share at zero requires a drive-to-and-stability-at-zero commitment the apparatus (i)–(iv) — whose U(r) couples only to COM coordinates — does not furnish. The claim and its justification disagree on what "β_k = 1" ranges over.
**Required**: Either (a) restrict the automatic-discharge claim to the sub-case where β_k = 1 entails no exchangeable DOF under (i)–(iv), and state that the other admitted β_k = 1 case still needs the postulate, or (b) commit that within apparatus (i)–(iv) the admitted case does not arise (β_k = 1 ≡ no exchangeable DOF, under (i)–(iv)), and confine the broader admission to out-of-apparatus scope. Fix the claims-table entry for P.enc_ratio_equilibration to match.

### Issue 2: "β = 1 regardless" in the decoupled-DOF case overreaches
**ASN-0002, §"The internal compartment and the ratio β"**: "a molecule may carry internal modes (rotations, oscillations) that are dynamically decoupled from translation by the particular encounter law, in which case those modes cannot be excited by encounters and β = 1 holds regardless."
**Problem**: Under (i)–(iv) a decoupled mode's energy is conserved through encounters — neither raised nor lowered. Whatever Σ eint the species begins with persists. β_k = 1 then requires Σ eint = 0 initially, which is a state condition, not a species property; "regardless" overstates what decoupling alone secures. If β_k instead depends on initial Σ eint in this case, that conflicts with P.beta_species_invariant.
**Required**: Drop "regardless" and either specify that decoupled modes yield β = 1 only from a zero-eint initial state (flagging the tension with species-invariance), or collapse the case to "pure centre of force" (no internal compartment by construction), where the β = 1 claim is unambiguous.

### Issue 3: §"Heat as motion" invokes an uncited empirical regularity
**ASN-0002, §"Heat as motion"**: "different substances at the same temperature do not in general hold equal energy per unit mass. The theory must therefore distinguish the quantity that equalizes at thermal equilibrium from the quantity that merely rides along."
**Problem**: This empirical claim is doing structural work — it motivates the per-molecule split between temperature and β and thereby the subsequent architecture — but it is stated without any corpus citation. The connection to the 1819 specific-heat data developed later is not made at the point of use.
**Required**: Cite the corpus evidence (e.g., the 1819 Dulong–Petit table) at the point of invocation, or flag that the empirical basis is developed in §"Empirical constraint: the atomic-heat regularity" so the structural constraint is not floating free.

VERDICT: REVISE
