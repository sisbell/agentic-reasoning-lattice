# ASN-0002: Constitution and the Nature of Heat
*2026-04-21*

What is a body, and what is the heat that resides in it? The theory answers with two commitments that must hold in any valid realization: a body is a collection of discrete constituent units in motion, and the heat of a body is the energy of that motion. Each commitment carries structural consequences that we trace here. We work toward the minimum apparatus the theory requires, and catalog what the theory *does* and *does not* fix.

## The observables we must explain

Two classes of observable are given. A body has a *temperature* — an attribute that can equal, exceed, or fall short of the temperature of another body, and which regulates whether heat flows between them on contact. A body can absorb or release *heat*, measured by its effect on a standard calorimetric reference; the *specific heat* of a substance relates the two, quantifying heat per unit mass per unit temperature change.

These observables must emerge from whatever the theory takes a body to be. The constitutional commitment determines the underlying state; the nature-of-heat commitment determines how that state maps to what we measure.

## The constitutional commitment

Let a body B possess a finite multiset B.mols of constituent units, which we shall call *molecules*. Each molecule m carries

- an inertial mass m.mass ∈ ℝ⁺ (kg),
- a translational velocity m.v ∈ ℝ³ (m/s) of its centre of mass,
- an internal energy m.eint ∈ ℝ⁺₀ (J) of motions of its parts relative to the centre of mass,
- a species label m.species ∈ Species identifying its kind.

These give the abstract state components:

**[Σ.mols]** B.mols is a finite multiset of molecules, with #B.mols ≥ 1.
**[Σ.mass]** Each m ∈ B.mols has m.mass : ℝ⁺ (kg).
**[Σ.v]** Each m ∈ B.mols has m.v : ℝ³ (m/s).
**[Σ.eint]** Each m ∈ B.mols has m.eint : ℝ⁺₀ (J).
**[Σ.species]** Each m ∈ B.mols has m.species ∈ Species.

The species label is primitive in the formalism but not arbitrary: the theory individuates species as equivalence classes of molecules sharing a common mass, a common internal constitution, and common force laws governing their encounters — both with molecules of their own kind and with molecules of any other. Within a species, mass is a kind-level constant: (A m₁, m₂ : m₁.species = m₂.species : m₁.mass = m₂.mass), and we write M_k for the common mass of species k. We abbreviate species_k(B.mols) ≡ {m ∈ B.mols : m.species = k}. What distinguishes one species label from another is the parameter tuple the label stands for; the labels themselves are primitive notation.

What the theory does *not* commit to is the molecule's internal structure. A molecule may be a mere point, a centre of force endowed with inertia, a system of several such centres, or a rigid body of determinate form (in which case the rigidity is itself a substructural assumption, carrying a "molecular theory of the second order" with its own inner binding forces). These are substantively different pictures, and the theory declares that its downstream commitments do not discriminate between them. What matters is the abstraction: an inertial mass, a centre-of-mass velocity, and a scalar "internal energy" compartment.

The scalar representation of internal motion is lossy. A rigid body carries three rotational degrees of freedom; a pair of mutually orbiting force-centres carries additional relative degrees. We absorb all such structure into m.eint by restricting attention to equilibrium states, where (we will postulate) only the aggregate couples observably to translation. Non-equilibrium internal dynamics lie outside the apparatus.

We impose no requirement that molecules be extended or mutually impenetrable. The theory explicitly refuses to inherit from sensible bodies the properties of extension and impenetrability; molecules may overlap, they may be pointlike, and nothing we commit to distinguishes these cases.

## Heat as motion

Define the total energy of a body:

  B.E ≡ (+ m : m ∈ B.mols : ½ · m.mass · (m.v · m.v) + m.eint)     (J)

The core commitment of the theory is

**[P.heat_as_motion]** The heat content of a body coincides with B.E. No separate material stock of heat is posited; the heat of a body is the energy of molecular motion, summed over the body's constituents.

Three structural constraints must hold for this commitment to be tenable.

First, the observed flow of heat from warmer to cooler bodies forces temperature to be a *monotone* functional of whatever measure of motion drives the flow: if heat is motion, imbalance of heat must be imbalance of motion.

Second, heat contents combine additively when bodies are brought into contact. This forces the heat representation to be a sum over constituents — which B.E is, by construction.

Third, different substances at the same temperature do not in general hold equal energy per unit mass. The theory must therefore distinguish the quantity that equalizes at thermal equilibrium from the quantity that merely rides along. We develop this distinction in the next two sections.

## Temperature as a functional of mean translational vis viva

Define the translational vis viva of molecule m, and the body's mean translational vis viva per molecule:

  T(m) ≡ ½ · m.mass · (m.v · m.v)     (J)
  B.T̄  ≡ (1/#B.mols) · (+ m : m ∈ B.mols : T(m))     (J)

**[P.temp_functional]** In the equilibrium regime, the temperature of a body is a strictly monotone function of B.T̄ alone: for bodies B₁, B₂ at equilibrium,
- temp(B₁) = temp(B₂) ⇔ B₁.T̄ = B₂.T̄,
- temp(B₁) < temp(B₂) ⇔ B₁.T̄ < B₂.T̄.

The content of this claim is that the functional depends on B.mass and B.v, not on B.eint. The internal compartment drops out of the temperature functional at equilibrium.

Why the theory commits to this, and why the argument is not a one-step derivation. One might think equilibration selects translational vis viva because only translational motion is exchanged across the boundary between molecules — but the encounter apparatus stated below does not preserve the translational/internal partition per encounter: total energy is conserved, yet energy may flow between a molecule's translational and internal compartments during an encounter. The exchange-across-boundary argument alone does not pin down what equilibrates.

The derivation rests instead on two further modeling commitments. First, encounters are treated as between *centres of force*: under this approximation, the only integral relating initial and final speeds of an encounter pair is M₁a² + M₂b² = M₁a'² + M₂b'² — conservation of translational vis viva at encounter boundaries, with internal energy carried along untouched by the constraint. Second, at equilibrium the one-molecule velocity distribution is stationary under the encounter process (a detailed-balance condition: for any admissible quadruple (a, b, a', b'), f₁(a)f₂(b) = f₁(a')f₂(b')). Together these force the equilibrium distributions to be Maxwellian with equal mean translational vis viva per molecule. The internal compartment is handled separately, by the equilibrium apportionment postulate introduced below, not by the same argument.

That the equilibrium quantity is mean per *molecule* rather than per unit mass or per unit volume follows from the bilateral character of encounters: each encounter is between individual molecules, and stationarity is therefore per-molecule. The result is declared independent of the specific intermolecular force law — the Maxwellian conclusion does not depend on the functional form of the inter-centre force, only on the centres-of-force modeling of the encounter and the stationarity condition. We record P.temp_functional as the commitment whose support rests on the dilute regime (so that encounters factor into discrete pairwise episodes at all) and on the centres-of-force modeling of encounters; outside those conditions the derivation does not run, and the commitment must be regarded as a postulate pending a different argument.

## The internal compartment and the ratio β

A molecule may carry motion additional to the translation of its centre of mass — rotation of a rigid whole, orbital motion of sub-centres, oscillation of bound parts. All such motion is collected into m.eint. At equilibrium the theory postulates a definite apportionment: the mean internal energy per molecule stands in a fixed ratio to the mean translational vis viva, characteristic of the molecular species.

For species k with members species_k(B.mols), write β_k for the ratio of total mean molecular energy to mean translational vis viva:

  (+ m : m ∈ species_k(B.mols) : T(m) + m.eint)
    = β_k · (+ m : m ∈ species_k(B.mols) : T(m))

so the mean internal energy sits at (β_k − 1) times the mean translational vis viva per molecule of that species.

**[P.beta_bounds]** β_k ≥ 1 for every species k.

This is forced by construction: m.eint ≥ 0 (by Σ.eint) and T(m) ≥ 0, so β_k = 1 + Σ eint / Σ T ≥ 1.

**[P.beta_unity_iff_no_internal]** β_k = 1 iff species k carries no internal degree of freedom capable of exchanging energy with translation through encounters.

A pure centre of force, having no internal structure at all, is the clearest case of β = 1. More generally, a molecule may carry internal modes (rotations, oscillations) that are dynamically decoupled from translation by the particular encounter law, in which case those modes cannot be excited by encounters and β = 1 holds regardless. Which realizations of β = 1 actually obtain depends on the force law one assumes for the encounter, which the theory does not prescribe in general; the structural statement P.beta_unity_iff_no_internal is what the theory commits to.

**[P.beta_species_invariant]** β_k depends only on molecular species, not on the state of the body or its temperature, within the regime in which the equilibrium apportionment holds.

Two things require honesty.

First, the apportionment 1 : (β−1) is *postulated*, not derived. The internal dynamics of an encounter, in the presence of internal modes, are beyond what the theory can determine. The postulate (attributed to Clausius) is that many encounters drive the translational–internal ratio to a stable equilibrium value; the value is fixed by constitution, but the mechanism of approach is not specified. Violent disturbances can break the apportionment; the commitment is for the equilibrium regime alone.

Second, β is in principle empirically accessible through observable heat-capacity ratios. The specific relation between β and the ratio of specific heats requires additional apparatus — pressure, volume, and the work done by a body against its external pressure during expansion — that this note does not introduce. We defer the derivation of that relation to a later specification that develops the requisite pressure–volume–temperature machinery. What matters here is structural: β, though underdetermined by direct inspection of the molecule, is pinned by observables the theory can access once it develops that apparatus, so the apportionment is not a hidden parameter in the long run.

## Conservation through encounters

The encounter apparatus we now state applies in the *dilute regime*: molecules spend most of their time beyond each other's sphere of sensible action, so interactions factor into discrete pairwise encounters brief in duration (and in length) compared to free-flight intervals, and the probability that three or more molecules are simultaneously within each other's spheres of action is negligible. This is the regime of a gas. For dense bodies — liquids and solids, where molecules remain continuously within mutual range and there is no free flight to speak of — the encounter decomposition fails, and the theory declines to commit to the form of encounter-level dynamics there; it notes only that an analogous law relating temperature to molecular energy is to be expected for dense bodies, without furnishing its precise form.

An encounter between two molecules is then an interaction episode, bounded in time, during which velocities and internal states change under their mutual force. Outside encounters, molecules move freely: translational velocities are constant, and the internal energy of each molecule is unchanged.

Let (m₁, m₂) be an encounter pair, with primed quantities denoting post-encounter states. The theory imposes:

**[P.enc_momentum]** Each encounter preserves total linear momentum, strictly:
  m₁.mass · m₁.v + m₂.mass · m₂.v = m₁.mass · m₁.v' + m₂.mass · m₂.v'.

**[P.enc_energy]** Each encounter between an isolated pair preserves total energy, strictly:
  T(m₁) + T(m₂) + m₁.eint + m₂.eint = T(m₁') + T(m₂') + m₁.eint' + m₂.eint'.

Both claims follow from the more general principle that molecular interactions are dynamical, governed by some force law, and therefore inherit the conservation principles of any such dynamics.

What the theory does *not* commit to, per encounter, is the partition of total energy between translational and internal. For β = 1 (no internal compartment) the partition is trivial: translational vis viva is strictly conserved per encounter, because there is nowhere else for energy to go. For β > 1 the translational sum T(m₁) + T(m₂) may change per encounter, with the balance flowing into or out of m.eint. Only the *total* (translational plus internal) is strictly conserved per encounter.

Over many encounters, the postulate of equilibrium apportionment fixes the aggregate:

**[P.enc_ratio_equilibration]** In the equilibrium regime the mean ratio of internal to translational vis viva per molecule of a species is (β − 1), maintained as a steady state by the aggregate effect of encounters; per-encounter fluctuations average out.

This claim passes from dynamics to statistics. No individual encounter need preserve the apportionment; the equilibrium ensemble preserves it as a mean.

## Sharing of translational vis viva between species

Consider two species of molecule, k = 1, 2, coexisting in a body or in bodies held in thermal contact. Let M_k and v̄²_k denote species mass and species mean-square speed at equilibrium.

P.temp_functional is a single-body statement: it fixes that each body's temperature is a strictly monotone function of its own B.T̄. To move from there to a cross-species claim, two further commitments are needed. First, the temperature functional must be *species-independent*: the same functional of B.T̄ applies to any body regardless of the species composition, so that equality of temperature across two bodies of different species means equality in a common functional form. Second, the stationarity argument behind P.temp_functional must be run at the cross-species level — for encounters between a species-1 and a species-2 molecule, not merely within-species encounters.

The second step is the detailed-balance argument for cross-species encounters in the dilute regime. Under the centres-of-force modeling of cross-species encounters, the only constraint relating initial pair-speeds (a, b) of a species-1 and a species-2 molecule to their post-encounter speeds (a', b') is M₁a² + M₂b² = M₁a'² + M₂b'². At a stationary equilibrium, f₁(a)f₂(b) = f₁(a')f₂(b') for every pair satisfying that constraint. The only solutions are Maxwellian distributions whose moduli α₁, α₂ satisfy M₁α₁² = M₂α₂², which translates to equality of mean translational vis viva per molecule across species.

**[P.equipartition]** At thermal equilibrium between species 1 and 2, in the dilute regime with cross-species encounters modeled as between centres of force, the mean translational vis viva per molecule is equal across species:
  M₁ · v̄²₁ = M₂ · v̄²₂.

P.equipartition is a *derived* consequence of (i) P.temp_functional, (ii) the species-independence of the temperature functional, and (iii) the modeling commitments under which the detailed-balance argument runs at cross-species level. It is not simply "P.temp_functional restated" — moving from single-body to cross-species adds commitments that the single-body statement alone does not carry.

Two consequences illuminate what temperature measures.

At equal temperature, two species differ in mean-square speed inversely as their masses: a heavier species moves (on average) more slowly. Since mass varies by factors of ten or more across species, so does mean-square speed — yet temperature is equal. Temperature measures energy per unit molecule, as a per-molecule scalar.

At equal temperature, the *total* molecular energy per molecule of species k is β_k · T̄ — so species with different β carry different total energies per molecule at the same temperature. This is what makes specific heat species-dependent even though temperature is universal.

The structural point: what the system equalizes is a per-molecule quantity. Were bodies continuous, the expression M · v̄² would not have the right shape. The equipartition commits the theory to a discrete constitutional unit as the bookkeeping atom of thermal contact.

## Empirical constraint: the atomic-heat regularity

If bodies are discrete at a level whose units are the carriers of heat capacity, and if at ordinary temperatures each unit carries a common per-unit heat capacity, then the specific heat per unit mass of a simple body should vary inversely with its per-unit mass. The product

  (specific heat per unit mass) × (mass per unit carrier)

should be a species-independent constant.

The 1819 Dulong–Petit measurements `[1819-dulong-petit]` record this product for thirteen elemental solids — bismuth, lead, gold, platinum, tin, silver, zinc, tellurium, copper, nickel, iron, cobalt, sulphur — with atomic weight standing for mass per unit carrier. Across a factor of six in atomic weight (13.30 for bismuth, 2.011 for sulphur) and a factor of six in specific heat (0.0288 for bismuth, 0.1880 for sulphur), the product clusters narrowly:

  (A m : m ∈ substances : 0.3675 ≤ m.product ≤ 0.3830),

a total spread of 4.2 % around the mean of 0.3754. The products are dimensionless (relative specific heats and relative atomic weights).

The measurement regime was held structurally uniform across substances: a narrow window of 10° to 5° centigrade above ambient, residual air pressure below 2 mm Hg, a blackened ice-walled surrounding vessel, a silver cylindrical container with axial thermometer. Uniform protocol attributes the residual spread to the bodies themselves, within the probable error of the atomic weights and specific heats individually.

We extract the abstract constraint:

**[P.atomic_heat_regularity]** Within the regime covered by the 1819 corpus — elemental solids near ambient temperature, with the measurement window 5° to 10° centigrade above a 0 °C surrounding — the heat capacity per atom of a simple elemental body is approximately species-independent.

The word "approximately" is load-bearing. The theory does not commit to strict equality; it commits to a regularity whose residual variation it would naturally absorb into species-specific β. For the elemental solids in the 1819 regime, β-variation across species is small enough that the product clusters within 4.2 %.

The regularity is consistent with what the theory says about per-molecule heat capacity in a body: if each atom carries a common mean vis viva at a common temperature, and if β varies only modestly across the species measured, then heat capacity per atom must cluster. But the theory cannot *derive* the regularity from its encounter apparatus, because solids are not dilute — the encounter decomposition on which the detailed-balance argument for P.equipartition depends does not apply. P.atomic_heat_regularity is thus a registered empirical regularity: the theory notes it, and notes its consistency with the per-molecule structure of temperature, but does not pretend to derive it from the dilute-regime apparatus. Whether the equilibrium apportionment extends to dense bodies — and thereby whether the regularity is structural or contingent — is not settled by the theory as developed here.

The regime of the regularity is empirical, not theoretical: the measurements cover a narrow window near ambient, on thirteen elemental solids, with no data at substantially colder or hotter conditions. Whether the regularity extends beyond that window is not determined by the evidence in the corpus. Hydrogen, measured as a gas by different experimenters, gives a product noticeably smaller than the solids; this is flagged as a probable experimental artifact of rapid cooling rather than a commitment of the theory. The corpus leaves unresolved whether the deviation is artifact or substance.

## The primacy of motion

A rival constitution would have molecules at rest, held in equilibrium by central forces, and would derive observable properties from the statics of the configuration. The theory rules this out, fixing the commitment that molecular *motion* is constitutive of heat.

**[P.motion_primacy]** The state variables responsible for heat reside in molecular motion. Heat vanishes iff all molecular motion vanishes.

Two empirical grounds and one conceptual ground force the commitment. Empirically, the elasticity of fluids (which show negligible form-elasticity) is inconsistent with a statical theory in which elastic response arises from inter-particle forces alone — fluidity itself is a phenomenon of motion-mediated deflection. Conceptually, a theory of hard-body collision in which the outcome of an impact depends on the *absolute* motions of the bodies is ruled out by the relativity of motion: the outcome of a local interaction cannot depend on the frame in which it is observed.

P.motion_primacy implies a structural condition on the zero of temperature: whatever temperature value is reached when all molecular motion vanishes, no heat remains at that temperature. The theory does not by itself establish that such a zero is reachable, nor does it commit to an absolute scale; it commits only to the structural identification that motion is what heat is.

## What the theory leaves underdetermined

Several matters are deliberately outside the theory's reach, and the theory says so.

The *internal constitution* of a molecule is underdetermined. A point, a centre of force, a system of centres, and a rigid body are all admissible; different constitutions producing the same β are indistinguishable through any observable we have introduced.

The *per-encounter dynamics* of internal modes are underdetermined. The equilibrium apportionment 1 : (β−1) is postulated from Clausius; the theory has no derivation for it in the present state of knowledge of molecules.

The *off-equilibrium* relation between temperature and the internal compartment is underdetermined. P.temp_functional holds in the equilibrium regime; the apparatus built here does not address states where the molecular velocity distribution has not stabilised.

The *dense regime* is underdetermined. The encounter apparatus on which P.temp_functional and P.equipartition rest presupposes that molecular interactions factor into discrete pairwise episodes with free flight between them — the dilute regime of a gas. For solids and liquids, where molecules remain continuously within each other's spheres of action, the decomposition fails. The theory as stated does not commit to the form of molecular dynamics or the structure of thermal equilibration in dense bodies; P.atomic_heat_regularity is registered there as evidence, not derived from the apparatus.

The *domain of validity of β-invariance* is underdetermined in the strong sense: the theory does not tell us the bounds of the regime in which the equilibrium apportionment 1 : (β − 1) holds, and the 1819 corpus's measurements sit within a narrow empirical window. The theory commits to β-invariance in the regime where the apportionment holds, and remains silent about how far that regime extends.

These gaps are boundaries of the theory's promise, not flaws of the specification. The downstream claims — temperature equality, specific-heat ratios, the atomic-heat regularity — are claims about averages at equilibrium, and they stand without the gaps being filled.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.mols | B.mols : finite multiset of molecules, #B.mols ≥ 1 | introduced |
| Σ.mass | Each m ∈ B.mols has m.mass : ℝ⁺ (kg) | introduced |
| Σ.v | Each m ∈ B.mols has m.v : ℝ³ (m/s) | introduced |
| Σ.eint | Each m ∈ B.mols has m.eint : ℝ⁺₀ (J) | introduced |
| Σ.species | Each m ∈ B.mols has m.species ∈ Species; species is an equivalence class under common mass, internal constitution, and force laws | introduced |
| P.heat_as_motion | Heat content of a body equals B.E = (+ m : m ∈ B.mols : ½ m.mass (m.v·m.v) + m.eint); no separate material stock of heat exists | introduced |
| P.temp_functional | At equilibrium, in the dilute regime with centres-of-force modeling of encounters, temperature is a strictly monotone function of mean translational vis viva per molecule B.T̄ alone, independent of the internal compartment and of the specific form of the intermolecular force law | introduced |
| P.beta_bounds | β_k ≥ 1 for every molecular species k | introduced |
| P.beta_unity_iff_no_internal | β_k = 1 iff species k has no internal degree of freedom that can exchange energy with translation through encounters | introduced |
| P.beta_species_invariant | β_k depends only on molecular species, not on body state or temperature, within the regime in which the equilibrium apportionment holds | introduced |
| P.enc_momentum | Each encounter preserves total linear momentum, strictly per encounter | introduced |
| P.enc_energy | Each encounter between an isolated pair preserves total energy (translational + internal), strictly per encounter | introduced |
| P.enc_ratio_equilibration | At equilibrium the mean ratio of internal to translational vis viva per molecule of a species is (β−1), maintained as a steady state; per-encounter fluctuations average out | introduced |
| P.equipartition | At thermal equilibrium between species 1 and 2, in the dilute regime with centres-of-force modeling of cross-species encounters, M₁·v̄²₁ = M₂·v̄²₂: mean translational vis viva per molecule is equal across species | introduced |
| P.atomic_heat_regularity | Within the regime covered by the 1819 corpus (elemental solids near ambient temperature), heat capacity per atom of a simple elemental body is approximately species-independent | introduced |
| P.motion_primacy | The state variables responsible for heat reside in molecular motion; heat vanishes iff all molecular motion vanishes | introduced |

## Open Questions

- What must the theory guarantee about temperature off equilibrium — is temperature even well-defined when B.mols has not reached its equilibrium velocity distribution?
- Under what abstract conditions on the internal dynamics of a molecule does the equilibrium apportionment 1 : (β−1) hold exactly rather than only in the mean?
- What structural feature of a constitution determines β uniquely, such that two distinct constitutions produce the same β iff they share that feature?
- What must any valid realization commit to regarding the preservation of molecular identity through encounters — must every encounter leave the multiset B.mols unchanged, or may molecules merge, dissociate, or transform?
- In what regime must the atomic-heat regularity hold, and what abstract change in the equilibrium apportionment causes the regularity to fail outside that regime?
- What invariant must any dynamical model of an encounter with internal modes preserve for the translational–internal equilibration to converge on 1 : (β−1) rather than drift?
- What does any valid realization require of the relation between the zero of molecular motion and the zero of the temperature scale?
- What must any valid realization commit to regarding molecular dynamics in the dense regime, where the encounter decomposition fails and there is no free flight between interactions?
- Under what modeling assumptions, besides the centres-of-force abstraction, does the stationarity argument for cross-species encounters yield equality of mean translational vis viva per molecule?
- Under what structural condition on the temperature functional is its *species-independence* guaranteed, so that equality of temperature between two species-distinct bodies entails equality of B.T̄ in a common functional form?
