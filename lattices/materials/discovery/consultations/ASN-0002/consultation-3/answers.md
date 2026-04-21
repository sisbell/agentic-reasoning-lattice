# Revision Consultation — ASN-0002

**Review:** review-3.md
**Date:** 2026-04-21 12:00

## Summary

3 REVISE items analyzed: 0 internal, 3 consulted (3 theory, 1 evidence)

## Consultation Results

### Issue 1: Premise (iv) cannot support the per-encounter T↔eint exchange that β>1 requires

**Category:** THEORY
**Reason:** The fix requires knowing what the theory commits to regarding the force law governing encounters with internal modes — whether the theory generalizes the potential to couple internal coordinates, or leaves the β>1 per-encounter exchange as a separate postulate. This is a question about the theory's derivational commitments.

**Theory question:** Does the theory commit to a force law that can do work on internal coordinates during an encounter (e.g., part-wise potentials depending on internal configuration), or does it restrict itself to U(r) between COMs and treat β>1 internal-translational exchange as a separate postulated mechanism?

**Theory's Answer:**

# Answer

The corpus restricts its calculational machinery to a central force between centres of gravity and treats the β>1 internal-translational exchange as a separately postulated mechanism (following Clausius), not as a consequence of the force law.

## The committed force law is COM-to-COM

Maxwell states the force law as acting between centres of gravity, with magnitude a function of COM separation only:

> "small bodies or groups of smaller molecules repelling one another with a force whose direction always passes very nearly through the centres of gravity of the molecules, and whose magnitude is represented very nearly by some function of the distance of the centres of gravity" `[1867-maxwell-dynamical-theory-of-gases]`

The specific law used in all the integrations is central and radial:

> "Let us assume that the force between the molecules M₁ and M₂ is repulsive and varies inversely as the nth power of the distance between them" `[1867-maxwell-dynamical-theory-of-gases]`

This force appears in the orbit equation (9) and sets θ as a function of (b, V) alone — no internal-coordinate arguments enter.

## Internal coordinates are explicitly set aside

Maxwell acknowledges that if molecules are composite, work on internal coordinates *should* occur, but declines to model it and instead assumes it away per encounter:

> "If we suppose the molecules to be bodies, or systems of bodies, capable of rotation, internal vibration, or any form of energy other than simple motion of translation, these results will be modified. The value of θ and the final velocities of the molecules will depend on the amount of internal energy in each molecule before the encounter, and on the particular form of that energy at every instant during the mutual action. We have no means of determining such intricate actions in the present state of our knowledge of molecules, so that we must content ourselves with the assumption that the value of θ is, on an average, the same as for pure centres of force, and that the final velocities differ from the initial velocities only by quantities which may in each collision be neglected, although in a great many encounters the energy of translation and the internal energy of the molecules arrive, by repeated small exchanges, at a final ratio, which we shall suppose to be that of 1 to β − 1." `[1867-maxwell-dynamical-theory-of-gases]`

This is the decisive passage. Three commitments are made:

1. θ is taken as the pure-centres-of-force value (i.e., computed from U(r) between COMs).
2. Per-collision exchanges with internal DOFs are neglected.
3. The β ratio is reached "by repeated small exchanges" over many encounters — left as an assumption.

## β is imported, not derived

The 1-to-(β−1) ratio is attributed to Clausius and assumed rather than produced by the collision dynamics:

> "If we assume with Clausius that the ratio of the mean energy of internal motion to that of agitation tends continually towards a definite value (β − 1), we may conclude that, except in very violent disturbances, this ratio is always preserved" `[1867-maxwell-dynamical-theory-of-gases]`

Correspondingly, β enters the energy budget (eq. 67–68) and the specific-heat ratio γ = (2+3β)/(3β) (eq. 113) as a parameter to be fixed from experiment ("can be determined if we know either of the specific heats of the gas, or the ratio between them"), not from the force law.

## Summary

On your dichotomy, the corpus takes the second branch. The committed dynamical law is U(r) between COMs (with n=5 for the viscosity-consistent case); the internal-translational equilibrium is a separate postulate — an averaged, many-encounter ratio imported from Clausius — with the per-encounter mechanism that would underwrite it explicitly declared beyond the paper's reach ("We have no means of determining such intricate actions in the present state of our knowledge of molecules") `[1867-maxwell-dynamical-theory-of-gases]`.

### Issue 2: Motion-primacy elasticity evidence lacks corpus citation

**Category:** BOTH
**Reason:** The elasticity claims are empirical observations invoked to reject a rival constitution; they must be grounded in corpus measurements with identifiable substances, regimes, and precision. If no such measurements exist in the corpus, Theory is also needed to determine whether the remaining grounds for P.motion_primacy suffice.

**Evidence question:** Does the corpus contain measurements of the ratio of form-elasticity to volume-elasticity, for fluids (showing vanishing form-elasticity with considerable volume-elasticity) and for solids (showing form-elasticity smaller than a statical-theory prediction), with identifiable substances and measurement regimes?

**Evidence's Answer:**

No. The corpus contains only one document, `[1819-dulong-petit]`, which reports specific heats and atomic weights for 13 solid elements determined by a cooling-rate method. It contains no measurements of form-elasticity (shear modulus), volume-elasticity (bulk modulus), or their ratio — for fluids, solids, or any other material. Elasticity is not mentioned anywhere in the document.

The question cannot be answered from this corpus.

**Theory question:** If the elasticity evidence is absent or weaker than stated, what grounds remain in the theory for P.motion_primacy, and does the postulate survive on those grounds alone or require demotion?

**Theory's Answer:**

## What the elasticity evidence does in Maxwell's argument

Maxwell's move against statical theories rests on a structural result: if molecules are held at rest in positions of equilibrium, "the forces called into play by a small change of form must always bear a fixed proportion to those excited by a small change of volume" [1867-maxwell-dynamical-theory-of-gases]. He then pushes this against the empirical evidence on two fronts — fluids (form-elasticity "evanescent", volume-elasticity "considerable") and solids (form-to-volume ratio "smaller in proportion... than the theory gives").

Maxwell's own footnote already complicates the solid-body leg: "In glass, according to Dr. Everett's second series of experiments (1866), the ratio of the elasticity of form to that of volume is greater than that given by the theory. In brass and steel it is less."

## What grounds remain if the elasticity evidence is set aside

Four lines in the corpus stand independently of the solid-elasticity appeal.

**1. The fluid case alone is decisive for the target domain.** "In fluids the elasticity of form is evanescent, while that of volume is considerable. Hence such theories will not apply to fluids." Since this paper's subject is gases, the motion hypothesis is already selected for the medium under study by this statement alone.

**2. Explanatory reach.** "We are able, however, to explain a great variety of phenomena by the dynamical theory which have not been hitherto explained otherwise... besides accounting for the relations of pressure, density, and temperature in a single gas, it affords a mechanical explanation of the known chemical relation between the density of a gas and its equivalent weight... It also explains the diffusion of one gas through another, the internal friction of a gas, and the conduction of heat through gases."

**3. Viscosity experiments.** The result that viscosity is independent of density and proportional to absolute temperature "is confirmed by the experiments of Mr. Graham on the Transpiration of Gases, and by my own experiments on the Viscosity or Internal Friction of Air and other Gases." Maxwell notes this is a direct consequence of the dynamical theory — "The result, that the viscosity is independent of the density, follows from the Dynamical Theory of Gases, whatever be the law of force between the molecules" — and moreover that the temperature scaling "requires us to abandon" the hard-sphere variant in favor of inverse-fifth-power repulsion. The statical picture offers no corresponding account.

**4. Equivalent volumes.** "This result of the dynamical theory affords the explanation of the 'law of equivalent volumes' in gases", and the underlying equality of mean *vis viva* holds "whatever theory we adopt as to the nature of the action between the individual molecules."

## The coincidence remark cuts against the elasticity argument alone

Maxwell explicitly concedes that one of the elasticity predictions does not distinguish the two pictures: "The same result and the same ratio of the elasticities would be obtained if we supposed the molecules to be at rest, and to act on one another with forces depending on the distance, as in the statical molecular theory of elasticity. The coincidence of the properties of a medium in which the molecules are held in equilibrium by attractions and repulsions, and those of a medium in which the molecules move in straight lines without acting on each other at all, deserves notice from those who speculate on theories of physics." So even on Maxwell's own reading, the elasticity *ratio* does not by itself pick out the dynamical picture.

## Assessment

Within the corpus, P.motion_primacy would not require demotion if the solid-elasticity evidence were weakened or removed. The load-bearing supports that remain are the fluid case, the dynamical theory's explanatory coverage of phenomena the statical picture cannot address (diffusion, viscosity's density-independence, heat conduction), and the direct experimental confirmation on viscosity. What would require qualification — by Maxwell's own footnote and his coincidence remark — is any narrower claim that *the elasticity-ratio result alone* grounds motion primacy; the corpus already signals that it does not.

A stricter reading: the corpus supports motion primacy *for fluids/gases* on evidential grounds independent of solid-body elasticity. It is silent on whether the same supports extend to solids, where Maxwell's dynamical picture posits oscillation about fixed positions and where, absent the elasticity argument, the corpus offers no separate positive evidence against a statical account.

### Issue 3: P.equipartition derivation treats species sub-populations as temperature-bearing bodies without licensing it

**Category:** THEORY
**Reason:** The fix requires knowing whether the theory licenses treating a species sub-population within a mixed body as a sub-body with its own temperature, or whether equipartition must be re-derived through distributional apparatus (detailed balance on a factorisable joint) that lies outside this note's scope.

**Theory question:** Does the theory commit to sub-populations within a mixed body having a temperature in the sense of P.temp_functional — and if so, on what grounds (e.g., factorisability of the equilibrium joint distribution) — or does the theory's derivation of cross-species mean-vis-viva equality go exclusively through the distributional/detailed-balance route without invoking sub-population temperatures?

**Theory's Answer:**

# Answer

The corpus commits to sub-populations within a mixed body having a temperature, and it does so through *both* the distributional/detailed-balance route *and* a parallel dynamical route that invokes sub-population temperatures explicitly. The two routes are independent and yield the same cross-species equality of mean *vis viva*.

## 1. The theory explicitly assigns a temperature to each sub-population

Maxwell defines temperature between species operationally, via a zero-flux condition on *vis viva*:

> "When the flow of *vis viva* from the one kind of molecules to the other is zero, the temperature is said to be the same. Hence equal volumes of different gases at equal pressures and temperatures contain equal numbers of molecules." [1867-maxwell-dynamical-theory-of-gases]

And, following the derivation of equation (97),

> "Now the state into which two bodies come by exchange of invisible agitation is called equilibrium of heat or equality of temperature. Hence when two gases are at the same temperature, $Q_1 = Q_2$." [1867-maxwell-dynamical-theory-of-gases]

Here $Q_i = \tfrac{M_i}{M_1+M_2}(\overline{\xi_i^2}+\overline{\eta_i^2}+\overline{\zeta_i^2})$ (eq. 95) is a per-species quantity; the "two gases" of the last sentence are the two sub-populations in contact within a mixture. So the notion of temperature is applied to each species independently — functionally defined by whether flow of invisible agitation into/out of it vanishes.

## 2. Route A — distributional/detailed-balance

In the "Final Distribution of Velocity among the Molecules of Two Systems" section, Maxwell counts encounters using a *factorised* joint count:

> "the number of encounters of the given kind between these two sets of molecules will be $f_1(a)f_2(b)\,dV^2 F\,de$" [1867-maxwell-dynamical-theory-of-gases]

Detailed balance then forces

$$f_1(a)f_2(b) = f_1(a')f_2(b'), \quad M_1 a^2 + M_2 b^2 = M_1 a'^2 + M_2 b'^2,$$

whose solution is $f_i \propto \exp(-v^2/\alpha_i^2)$ with $M_1\alpha_1^2 = M_2\alpha_2^2$ (eqs. 22–25). The conclusion (eq. 34) is

> "$M_1\overline{v_1^2} = M_2\overline{v_2^2}$, or the mean *vis viva* of a molecule will be the same in each system. This is a very important result in the theory of gases, and it is independent of the nature of the action between the molecules..." [1867-maxwell-dynamical-theory-of-gases]

In this derivation the word "temperature" is *not* used; factorisability of the joint pair distribution (encoded in the encounter count and in the product ansatz $f_1 f_2$) plus energy conservation carries the whole argument.

## 3. Route B — dynamical, sub-population-temperature-based

In the "Equilibrium of Temperature between two Gases — Law of Equivalent Volumes" section, Maxwell starts from the coupled ODE for the species-resolved agitations (eq. 94) and derives

$$Q_2 - Q_1 = Ce^{-nt} \quad (97),$$

then *defines* equal temperature by $Q_1 = Q_2$, obtaining $M_1/\rho_1 = M_2/\rho_2$ (eq. 99) — equivalent to the mean *vis viva* equality of eq. 34. This route explicitly traffics in sub-population temperatures: each species has its own $\beta_i(\overline{\xi_i^2}+\overline{\eta_i^2}+\overline{\zeta_i^2})$ evolving in time, and "same temperature" names the fixed point.

## 4. Grounds and relation between the two routes

The corpus therefore does *not* take one route to the exclusion of the other. The grounds for sub-population temperature are:

- **Factorisation of the joint distribution at equilibrium.** This is first assumed at the encounter-counting step (the product $f_1(a)f_2(b)$), then recovered as the unique form consistent with detailed balance plus energy conservation. It is what makes $\alpha_1, \alpha_2$ species-specific *moduli* — each species gets its own Maxwellian with its own modulus, which is what licenses a per-species "temperature."
- **Zero net flux of *vis viva* between species.** This is the functional / dynamical criterion (the $Q_1 = Q_2$ fixed point of eq. 97) and is what Maxwell explicitly calls "equality of temperature."

## 5. Caveats about what the corpus does *not* do

- The corpus nowhere considers a single species in a *non-equilibrium* internal state (e.g. anisotropic or non-Maxwellian) and asks whether it still has a temperature in the functional sense. Within a mixture at equilibrium, each species is Maxwellian by construction (eqs. 24–26), so the question of whether "sub-population temperature" presupposes Maxwellian form is not separated out by Maxwell.
- The statement that the result is "independent of the nature of the action between the molecules" (eq. 34) applies to the distributional route; Route B likewise does not depend on a specific force law, though the *rate* of approach to $Q_1=Q_2$ (the constant $n$ in eq. 97) does.
- Whether "P.temp_functional" in the question matches Maxwell's zero-*vis viva*-flux criterion exactly is outside what the corpus states; the corpus offers the zero-flux / $Q_1 = Q_2$ criterion as its definition, and that is the most natural candidate for a functional temperature here.

## Short answer

Yes — the theory commits each sub-population in a mixed body to having a temperature, grounded (i) on the factorised equilibrium joint distribution with its own per-species modulus $\alpha_i$ and (ii) on the zero-*vis viva*-flux definition $Q_1 = Q_2$. Cross-species mean *vis viva* equality is derived *twice*: once through the distributional/detailed-balance route without naming temperature (eq. 34), and once through a sub-population-temperature route (eqs. 94–99). The two routes agree, and the corpus presents them as mutually reinforcing rather than alternatives. [1867-maxwell-dynamical-theory-of-gases]
