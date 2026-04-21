# Revision Consultation — ASN-0002

**Review:** review-5.md
**Date:** 2026-04-21 12:31

## Summary

2 REVISE items analyzed: 0 internal, 2 consulted (2 theory, 0 evidence)

## Consultation Results

### Issue 1: P.temp_functional's formal biconditional contradicts its prose label as a "single-body statement"

**Category:** THEORY
**Reason:** The fix requires knowing whether the theory treats the temperature–vis viva relation as inherently single-body (with species-independence as a separate commitment) or as already cross-species in its primary statement. Theory can clarify the commitment's scope in the source corpus.

**Theory question:** In the dynamical theory of gases as it stands in the corpus, is the relation between temperature and mean translational vis viva per molecule stated (or derived) as a single-body claim that only later gains cross-species reach through an independent step, or is the cross-body/cross-species biconditional part of the same commitment?

**Theory's Answer:**

The cross-species biconditional is part of the same commitment in the corpus. Maxwell does not first state a single-body relation and then extend it; temperature is defined through an inter-species equilibrium condition from the outset.

The definition itself is cross-species:

> "When the flow of *vis viva* from the one kind of molecules to the other is zero, the temperature is said to be the same. Hence equal volumes of different gases at equal pressures and temperatures contain equal numbers of molecules." [1867-maxwell-dynamical-theory-of-gases]

The equipartition result — mean translational *vis viva* per molecule agrees across species in equilibrium — is derived within the same framework, from the stationary final distribution:

> "$M_1\overline{v_1^2} = M_2\overline{v_2^2}$, or the mean *vis viva* of a molecule will be the same in each system. This is a very important result in the theory of gases, and it is independent of the nature of the action between the molecules" [1867-maxwell-dynamical-theory-of-gases]

And the tie-up appears in the "Law of Equivalent Volumes" section:

> "Now the state into which two bodies come by exchange of invisible agitation is called equilibrium of heat or equality of temperature. Hence when two gases are at the same temperature, $Q_1 = Q_2$" [1867-maxwell-dynamical-theory-of-gases]

where $Q_i = \frac{M_i}{M_1+M_2}(\overline{\xi_i^2}+\overline{\eta_i^2}+\overline{\zeta_i^2})$.

So the single-gas statement (e.g., $p = \tfrac{1}{3}\rho V^2$, $\tfrac{3}{2}\beta p$ for total heat per unit volume) is reported, but the species-independent identification of temperature with mean translational *vis viva* per molecule is baked in at the point the word "temperature" is introduced — it is what the zero-flow condition delivers. No independent bridging step from single-species to cross-species is needed or taken.

One qualification the corpus itself flags: "temperature" is tied specifically to *translational* *vis viva* per molecule; total molecular energy carries the species-specific factor $\beta$ for internal motion (equations 67–69, 114). The cross-species commitment attaches to the translational part; $\beta$ varies by species and enters specific heats separately.

### Issue 2: P.beta_unity_iff_no_internal's justification covers only one direction of the iff

**Category:** THEORY
**Reason:** The fix hinges on whether the theory commits to any exchangeable internal DOF carrying a strictly positive share of energy at equilibrium (closing β_k = 1 ⇒ no exchangeable DOF) or whether β_k − 1 is imported species-wise without such a lower bound. This is a theory-commitment question.

**Theory question:** Does the theory commit to the claim that any internal degree of freedom capable of exchanging energy with translation through encounters must carry a strictly positive share of the equilibrium apportionment (so β_k > 1 whenever such a DOF exists), or does it leave open the possibility that an exchangeable DOF carries a zero share at equilibrium?

**Theory's Answer:**

The corpus does **not** commit to that claim. It leaves the matter open, treating the equilibrium apportionment between translation and internal DOFs as a supposition to be fixed empirically, not as a theorem of the theory.

**What the corpus does assert.** For "pure centres of force," β = 1 is a direct consequence: "If the molecules are pure centres of force, there can be no energy of rotation, and the whole energy is reduced to that of translation" [1867-maxwell-dynamical-theory-of-gases]. "In all other cases" the energy is written ½Mv²β, where β is defined as "the ratio of the total energy to the energy of translation."

**Where the claim would have to live, and doesn't.** When Maxwell turns to molecules with rotational or internal motion, he is explicit about what the theory can and cannot derive:

> "We have no means of determining such intricate actions in the present state of our knowledge of molecules, so that we must content ourselves with the assumption that the value of θ is, on an average, the same as for pure centres of force, and that the final velocities differ from the initial velocities only by quantities which may in each collision be neglected, although in a great many encounters the energy of translation and the internal energy of the molecules arrive, by repeated small exchanges, at a final ratio, **which we shall suppose to be that of 1 to β − 1**." [1867-maxwell-dynamical-theory-of-gases]

The phrase "which we shall suppose" marks this as stipulation, not deduction. It is reaffirmed a second time as an assumption borrowed from Clausius:

> "If we assume with Clausius that the ratio of the mean energy of internal motion to that of agitation tends continually towards a definite value (β − 1), we may conclude that, except in very violent disturbances, this ratio is always preserved" [1867-maxwell-dynamical-theory-of-gases].

**How β is pinned down.** Not by the dynamics of encounters in this paper, but by experiment: "The value of β can be determined if we know either of the specific heats of the gas, or the ratio between them" [1867-maxwell-dynamical-theory-of-gases]. Later, β is tied to γ by β = (2/3)·1/(γ − 1) and read off from measured specific-heat ratios.

**On the equilibrium-distribution derivation.** Maxwell's proof that the final distribution is uniquely the Gaussian form (equations 22–26) operates strictly on the translational components ξ, η, ζ of two colliding molecules and uses only the translational energy conservation M₁a² + M₂b² = M₁a′² + M₂b′² [1867-maxwell-dynamical-theory-of-gases, eq. 23]. The argument is not extended to internal DOFs; the cross-system conclusion M₁v̄₁² = M₂v̄₂² concerns translation. So there is no equipartition-style lemma inside the corpus that would force a positive share on any exchangeable internal DOF.

**Inferred, not stated.** One can read the phrasing "1 to β − 1" as tacitly presuming β > 1 whenever internal motion is present — otherwise the ratio is degenerate. But the corpus does not elevate this to a commitment; it is a modelling stipulation, and Maxwell flags the gap explicitly ("We have no means of determining such intricate actions"). A zero-share internal DOF is neither ruled out by a derivation nor endorsed; it simply lies outside what the 1867 theory undertakes to decide.
