# Revision Consultation — ASN-0002

**Review:** review-2.md
**Date:** 2026-04-21 11:44

## Summary

6 REVISE items analyzed: 1 internal, 5 consulted (5 theory, 1 evidence)

## Consultation Results

### Issue 1: Species-independence of temperature functional is a smuggled premise

**Category:** THEORY
**Reason:** Elevating species-independence to a labeled claim requires knowing what standing the theory gives it — postulated outright, or derived from some deeper commitment — and what regime it applies in. Theory is needed.

**Theory question:** Does the theory take species-independence of the temperature functional as a postulate in its own right, or derive it from something else (and if so, from what)? What regime does it claim for the species-independent form?

**Theory's Answer:**

## Derived, not postulated

Maxwell obtains species-independence of the temperature functional (mean vis viva of translation) by two complementary dynamical arguments.

**Path 1 — detailed balance on the final distribution.** In *On the Final Distribution of Velocity among the Molecules of Two Systems acting on one another according to any Law of Force*, Maxwell requires the stationary exchange between velocity pairs $OA, OB$ and $OA', OB'$ to balance, i.e., $f_1(a)f_2(b) = f_1(a')f_2(b')$ (eq. 22), subject only to the kinematic constraint $M_1 a^2 + M_2 b^2 = M_1 a'^2 + M_2 b'^2$ (eq. 23). From this he derives Maxwellian forms with $M_1\alpha^2 = M_2\beta^2$ (eq. 25), hence $M_1\overline{v_1^2} = M_2\overline{v_2^2}$ (eq. 34) [1867-maxwell-dynamical-theory-of-gases]. He flags the generality explicitly: this result "is independent of the nature of the action between the molecules, as are all the other results relating to the final distribution of velocities."

**Path 2 — operational definition plus eq. (94).** In *Equilibrium of Temperature between two Gases — Law of Equivalent Volumes*, Maxwell defines temperature equality by the vanishing of cross-species agitation flux: "the state into which two bodies come by exchange of invisible agitation is called equilibrium of heat or equality of temperature." Equation (94) makes the flux proportional to $Q_2 - Q_1$, where $Q_i = \tfrac{M_i}{M_1+M_2}(\overline{\xi_i^2}+\overline{\eta_i^2}+\overline{\zeta_i^2})$, so equilibrium forces $Q_1 = Q_2$, i.e., equal mean vis viva.

## Regime claimed

The corpus attaches several conditions to the species-independent form:

- **Law-of-force independence**: explicitly asserted — "independent of the nature of the action between the molecules" (eq. 34 discussion).
- **Statistical-equilibrium regime**: "attained only when the molecules have had a great number of encounters."
- **Outside violent disturbances**: the identification of the translational functional as temperature marker piggybacks on Clausius's assumption that the internal-to-translational energy ratio $(\beta-1)$ is preserved — valid "except in very violent disturbances."
- **Quiescent state**: eq. (94) is obtained after dropping translational motion and conductive transport from eq. (93), so the claim is made for the undisturbed, resting mixture.

Maxwell frames the resulting law of equivalent volumes as a *necessary* consequence of the dynamical theory — "it is so, whatever theory we adopt as to the nature of the action between the individual molecules" [1867-maxwell-dynamical-theory-of-gases].

### Issue 3: P.enc_momentum and P.enc_energy rely on a naming-based "follows from"

**Category:** THEORY
**Reason:** Deciding whether to postulate or to step through premises requires knowing which framework the theory commits to at the molecule level (Newtonian mechanics, action-reaction, conservative force law, isolated-pair regime). Theory is needed.

**Theory question:** What does the theory commit to regarding the dynamical framework governing molecular encounters — specifically, does it adopt Newtonian mechanics with action-reaction forces internal to the pair and a conservative force law during an isolated-pair encounter, and are these commitments it takes on as postulates or grounds for further derivation?

**Theory's Answer:**

**Yes to both, with qualifications the corpus makes explicit.**

**Newtonian action-reaction (centre-of-gravity commitment):** Maxwell uses this as ground, not as something he derives. He asserts it universally and then exploits it to reduce the two-body problem:

> "The motion of the centre of gravity will not be altered by the mutual action of the molecules, of whatever nature that action may be. We may therefore take the centre of gravity as the origin of a system of coordinates moving parallel to itself with uniform velocity, and consider the alteration of the motion of each particle with reference to this point as origin." [1867-maxwell-dynamical-theory-of-gases]

The phrase "of whatever nature that action may be" signals that the internal-to-pair equality of action and reaction is taken as given.

**Central conservative force during an isolated encounter:** this is introduced explicitly as a postulate about the model:

> "I propose to consider the molecules of a gas, not as elastic spheres of definite radius, but as small bodies or groups of smaller molecules repelling one another with a force whose direction always passes very nearly through the centres of gravity of the molecules, and whose magnitude is represented very nearly by some function of the distance of the centres of gravity." [1867-maxwell-dynamical-theory-of-gases]

Three commitments are packed in: the force is pairwise, *central* (directed through centres of gravity), and depends only on the separation — hence conservative / derivable from a radial potential.

**These function as grounds for further derivation.** From them Maxwell obtains, by "the equation of central orbits," the deflection angle θ as a function of relative speed and impact parameter:

> "Let us assume that the force between the molecules M₁ and M₂ is repulsive and varies inversely as the nth power of the distance between them, the value of the moving force at distance unity being K, then we find by the equation of central orbits, π/2 − θ = ∫₀^{x'} dx / √(1 − x² − (2/(n−1))(x/α)^{n−1})" [1867-maxwell-dynamical-theory-of-gases]

He likewise derives that each molecule describes a plane curve about the common centre of gravity, that the two orbits are symmetric about the line of apses, and — crucially — that the speed of each molecule relative to the centre of gravity is *unchanged* in magnitude, only rotated:

> "each will be moving with the same velocity relative to the centre of gravity that it had before the mutual action, but the direction of this relative velocity will be turned through an angle 2θ in the plane of the orbit." [1867-maxwell-dynamical-theory-of-gases]

That conservation of relative kinetic energy for the pair is a consequence of the conservative-central-force setup, not an independent axiom.

**The specific force law is downstream, not foundational.** The inverse-fifth-power is introduced as a hypothesis and then selected empirically: the framework (Newtonian / central / conservative) is held fixed while the exponent is tuned to match experiment:

> "The experimental result, that the viscosity is proportional to the absolute temperature, requires us to abandon this hypothesis [hard elastic molecules], which would make it vary as the square root of the absolute temperature, and to adopt the hypothesis of a repulsive force inversely as the fifth power of the distance between the molecules, which is the only law of force which gives the observed result." [1867-maxwell-dynamical-theory-of-gases]

**Where the commitments are weakened, the corpus says so.** When molecules are not pure centres of force, Maxwell concedes that the isolated-pair Newtonian-conservative derivation no longer suffices and is replaced by an on-average assumption:

> "If we suppose the molecules to be bodies, or systems of bodies, capable of rotation, internal vibration, or any form of energy other than simple motion of translation, these results will be modified. The value of θ and the final velocities of the molecules will depend on the amount of internal energy in each molecule before the encounter... we must content ourselves with the assumption that the value of θ is, on an average, the same as for pure centres of force, and that the final velocities differ from the initial velocities only by quantities which may in each collision be neglected" [1867-maxwell-dynamical-theory-of-gases]

Two further simplifying commitments also sit at this level:

> "we shall suppose that the time during which a molecule is beyond the action of other molecules is so great compared with the time during which it is deflected by that action, that we may neglect both the time and the distance described by the molecules during the encounter... We may also neglect those cases in which three or more molecules are within each other's spheres of action at the same instant." [1867-maxwell-dynamical-theory-of-gases]

**Summary.** The theory takes as postulates, for the isolated-pair encounter: (i) Newtonian mechanics in which internal mutual forces leave the pair's centre of gravity moving uniformly (action-reaction), and (ii) a central force depending only on separation (hence conservative). These are the *grounds* from which Maxwell derives the scattering angle, the plane orbit, the preservation of relative speed, and, together with the equilibrium-exchange argument, the distribution of velocities. The particular form of the force law (inverse fifth power) is treated as empirically determined, not foundational; and when molecules have internal structure, the central-conservative derivation is replaced by a parallel statistical assumption.

### Issue 4: The equipartition derivation reaches into the mathematical form of velocity distributions

**Category:** THEORY
**Reason:** The fix turns on whether the theory commits to the Maxwellian form as a load-bearing intermediate or declines to — and if declining, whether P.temp_functional and P.equipartition survive as postulates without the distributional argument. Theory is needed.

**Theory question:** Does the theory commit to the mathematical form of the equilibrium velocity distribution (Maxwellian) as a derivational step, or does it decline to specify the distributional form and instead postulate P.temp_functional and P.equipartition directly?

**Theory's Answer:**

The theory commits to the Maxwellian form as a derivational step. Equipartition and temperature‑as‑kinetic‑functional emerge as consequences of that derivation, not as separate postulates.

**The derivation** ([1867-maxwell-dynamical-theory-of-gases], "On the Final Distribution of Velocity..."): Maxwell imposes detailed balance,

> "When the number of pairs of molecules which change their velocities from OA, OB to OA', OB' is equal to the number which change from OA', OB' to OA, OB, then the final distribution of velocity will be obtained, which will not be altered by subsequent exchanges. This will be the case when $f_1(a)f_2(b) = f_1(a')f_2(b')$" (eq. 22).

Combined with the only kinematic invariant $M_1 a^2 + M_2 b^2 = M_1 a'^2 + M_2 b'^2$ (eq. 23), he extracts the exponential form $f_1(a) = C_1 e^{-a^2/\alpha^2}$, $f_2(b) = C_2 e^{-b^2/\beta^2}$ with $M_1\alpha^2 = M_2\beta^2$ (eqs. 24–25). He argues uniqueness by a cycle‑reversal argument: "This is therefore a possible form of the final distribution of velocities. It is also the only form."

**Equipartition is a consequence, not a postulate**: from the same derivation, "6th. When there are two systems of molecules $M_1\alpha^2 = M_2\beta^2$ ... or the mean *vis viva* of a molecule will be the same in each system. This is a very important result in the theory of gases, and it is independent of the nature of the action between the molecules, as are all the other results relating to the final distribution of velocities."

**Temperature‑as‑functional** is likewise defined after the fact: "When the flow of *vis viva* from the one kind of molecules to the other is zero, the temperature is said to be the same." Temperature is identified with the kinetic invariant whose equality labels the stationary distribution.

**Load‑bearing elsewhere**: the Gaussian fourth moment $\overline{\xi^4} = 3\overline{\xi^2}\cdot\overline{\xi^2}$ (eq. 143) enters the conductivity derivation. The Dec. 17, 1866 addition makes the dependency explicit:

> "unless $\overline{\xi^4} = 3\overline{\xi^2}\cdot\overline{\xi^2}$, we should have obtained a different result. Now this equation is derived from the law of distribution of velocities to which we were led by independent considerations. We may therefore regard this law of temperature, if true, as in some measure a confirmation of the law of distribution of velocities."

**Qualification**: for the inverse‑fifth‑power law ($n=5$), the relative velocity $V$ drops out of the collision integrals, and "In the case in which $n = 5$, $V$ disappears, and we may write the result of integration $\overline{Q}N_2$" — so viscosity and diffusion at $n=5$ can be written in terms of means without invoking the explicit exponential form. Conduction (involving three‑dimensional moments) cannot; there the Maxwellian is required.

So: the distribution is derived, not postulated, and both equipartition and the kinetic temperature are outputs of that derivation.

### Issue 5: "Attributed to Clausius" is an attribution, not a ground

**Category:** BOTH
**Reason:** Restating the postulate as the theory's own commitment requires knowing what alternative the theory rejects and on what grounds; the corpus must also be checked to see whether a Clausius entry grounds the claim evidentially. Both channels needed.

**Theory question:** What alternative to the equilibrium apportionment 1 : (β−1) does the theory reject (ratio depending on state, on history, on initial conditions), and on what grounds does it commit to the apportionment?

**Theory's Answer:**

The corpus acknowledges instantaneous-scale variation in the apportionment but rejects it as the relevant quantity for the theory, committing instead to a single equilibrium ratio 1 : (β−1) that depends only on the nature of the molecules.

**Alternatives acknowledged and set aside**

The corpus grants that β fluctuates at two finer levels:

> "The ratio β will be different for every molecule, and will be different for the same molecule after every encounter with another molecule, but it will have an average value depending on the nature of the molecules, as has been shown by Clausius." [1867-maxwell-dynamical-theory-of-gases]

So state-dependence (per-molecule) and history-dependence (per-encounter) are conceded at the microscopic level, then overruled by appeal to an average. Initial-condition dependence is similarly dissolved by the relaxation argument:

> "the energy of translation and the internal energy of the molecules arrive, by repeated small exchanges, at a final ratio, which we shall suppose to be that of 1 to β − 1." [1867-maxwell-dynamical-theory-of-gases]

The "final ratio" language commits to a terminus that does not retain memory of where the system started.

**Grounds for the commitment**

Four grounds are stated, in descending order of strength:

1. *Citation to Clausius.* The average-value claim is attributed to Clausius ("as has been shown by Clausius"), and the apportionment is framed as adopting his hypothesis: "If we assume with Clausius that the ratio of the mean energy of internal motion to that of agitation tends continually towards a definite value (β − 1), we may conclude that, except in very violent disturbances, this ratio is always preserved" [1867-maxwell-dynamical-theory-of-gases].

2. *Relaxation by many small exchanges.* The "repeated small exchanges" over "a great many encounters" are taken to drive the system to the final ratio, which is the mechanism by which initial conditions and individual-encounter history are washed out.

3. *Confession of ignorance as licensing assumption.* The text is explicit that the commitment is an assumption adopted because the alternative — tracking the full internal dynamics — is not available: "We have no means of determining such intricate actions in the present state of our knowledge of molecules, so that we must content ourselves with the assumption that the value of θ is, on an average, the same as for pure centres of force, and that the final velocities differ from the initial velocities only by quantities which may in each collision be neglected" [1867-maxwell-dynamical-theory-of-gases].

4. *Empirical anchoring via specific heats.* The numerical value of β is tied to measurable quantities: "The value of β can be determined if we know either of the specific heats of the gas, or the ratio between them" [1867-maxwell-dynamical-theory-of-gases]. This is later made operational through γ = (2+3β)/(3β) and the agreement noted between Rankine's computed specific heat of air and Regnault's measurements.

**Scope of the commitment**

The corpus marks a limit: the apportionment "is always preserved" only "except in very violent disturbances." Within that limit, the theory treats β as a constant of the gas, so that the "total heat in the unit of volume of the medium" can be written as ½β(ξ̄²+η̄²+ζ̄²)ρ = (3/2)βp [1867-maxwell-dynamical-theory-of-gases, eqns (68)–(69)] — a step that would not be available under any of the rejected state/history/initial-condition alternatives.

**Evidence question:** Does the corpus contain a Clausius entry (or equivalent) grounding the equilibrium apportionment of translational and internal vis viva, and if so under what citation?

**Evidence's Answer:**

No. The corpus contains only `[1819-dulong-petit]`. There is no Clausius entry, and no source grounding the equilibrium apportionment of translational and internal vis viva (equipartition). That question cannot be answered from the corpus as provided.

### Issue 6: Miscount in the grounds for P.motion_primacy

**Category:** THEORY
**Reason:** To decide between supplying a second empirical ground and correcting the count, we need to know whether the theory actually offers a second empirical observation for motion-primacy beyond fluid elasticity. Theory is needed.

**Theory question:** Beyond the elasticity of fluids, does the theory's grounds for the motion-primacy commitment include a second empirical observation (e.g., latent heat, gas pressure, diffusion, conduction), or is fluid elasticity the sole empirical ground?

**Theory's Answer:**

Beyond fluid elasticity, the corpus supplies a second empirical observation of the same kind, and Maxwell presents them together as the grounds for rejecting statical theories.

Statical theories predict a fixed ratio between form-elasticity and volume-elasticity: "the forces called into play by a small change of form must always bear a fixed proportion to those excited by a small change of volume" [1867-maxwell-dynamical-theory-of-gases]. Maxwell then attacks this prediction in two empirical domains:

1. **Fluids**: "in fluids the elasticity of form is evanescent, while that of volume is considerable. Hence such theories will not apply to fluids."

2. **Solids**: "In solid bodies the elasticity of form appears in many cases to be smaller in proportion to that of volume than the theory gives, so that we are forced to give up the theory of molecules whose displacements are functions of their coordinates when at rest, even in the case of solid bodies." A footnote grounds this in Everett's 1866 experiments on glass.

Only after both observations does Maxwell conclude: "The theory of moving molecules, on the other hand, is not open to these objections."

Of the examples you name, gas pressure, diffusion, and conduction do appear in the corpus, but not as grounds against the statical theory. They enter as phenomena the dynamical theory additionally explains: "We are able, however, to explain a great variety of phenomena by the dynamical theory which have not been hitherto explained otherwise" — listing pressure/density/temperature relations, the Law of Equivalent Volumes, diffusion, internal friction, and conduction of heat [1867-maxwell-dynamical-theory-of-gases]. These are constructive support for the chosen theory, not empirical objections to the alternative. Latent heat is not discussed in the corpus.

So: fluid elasticity is not the sole empirical ground; it is paired with solid-body form-elasticity. Both grounds are of one kind (elasticity-ratio anomalies), and together they carry the eliminative work against statical theories.
