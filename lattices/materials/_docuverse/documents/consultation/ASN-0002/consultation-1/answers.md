# Revision Consultation — ASN-0002

**Review:** review-1.md
**Date:** 2026-04-21 11:15

## Summary

7 REVISE items analyzed: 0 internal, 7 consulted (7 theory, 1 evidence)

## Consultation Results

### Issue 1: P.equipartition derivation insufficient

**Category:** THEORY
**Reason:** The fix turns on whether the corpus's theory commits P.temp_functional to be species-independent, and whether cross-species equipartition is derived or postulated separately. Theory channel is needed.

**Theory question:** Does the corpus's theory commit temperature to be the same functional of B.T̄ across all species, and does it derive cross-species equality of mean translational vis viva from that, or is cross-species equipartition introduced as its own commitment?

**Theory's Answer:**

The corpus does **not** define temperature as a shared functional of mean translational vis viva across species; cross-species equality of mean translational vis viva is *derived*, not posited.

**Temperature equality is given operationally.** Maxwell defines it by vanishing net flow of vis viva between species:

> "When the flow of *vis viva* from the one kind of molecules to the other is zero, the temperature is said to be the same." [1867-maxwell-dynamical-theory-of-gases]

And again at the derivation point:

> "the state into which two bodies come by exchange of invisible agitation is called equilibrium of heat or equality of temperature."

**Cross-species equipartition of translational vis viva is then derived twice, by independent routes.**

1. *From the stationary-distribution analysis.* Detailed exchange f₁(a)f₂(b) = f₁(a')f₂(b'), together with the sole constraint M₁a² + M₂b² = M₁a'² + M₂b'² (eq. 23), forces Gaussians with M₁α² = M₂β² (eq. 25). The corpus states:

> "M₁v̄₁² = M₂v̄₂², or the mean *vis viva* of a molecule will be the same in each system. This is a very important result in the theory of gases, and it is independent of the nature of the action between the molecules, as are all the other results relating to the final distribution of velocities." [eq. 34]

2. *From the encounter dynamics.* Equation (96) gives ∂(Q₂−Q₁)/∂t = −n(Q₂−Q₁), so Q₂−Q₁ decays exponentially. Combined with the operational definition, equal temperature ↔ Q₁ = Q₂, i.e. M₁(ξ̄₁²+η̄₁²+ζ̄₁²) = M₂(ξ̄₂²+η̄₂²+ζ̄₂²). The corpus states the conclusion as "Hence when two gases are at the same temperature, Q₁ = Q₂" (eq. 98).

**So the commitments are:** (i) temperature equality := zero net vis-viva flow (definitional); (ii) the dynamical/distributional machinery from which exchange equalization follows. Cross-species equipartition of translational vis viva is then a theorem, and the fact that temperature ends up represented by the same functional of M·v̄² across species is a *consequence* of that theorem, not an independent commitment.

**One distinct commitment to flag:** within a single species, the corpus adopts Clausius's ratio between internal and translational modes — "if we assume with Clausius that the ratio of the mean energy of internal motion to that of agitation tends continually towards a definite value (β−1)" (eq. 67). That is introduced as an assumption and concerns intra-molecular, not cross-species, equipartition.

### Issue 2: γ = (2 + 3β)/(3β) is unjustified and uses out-of-scope apparatus

**Category:** THEORY
**Reason:** The fix requires knowing whether the corpus's theory actually derives γ(β), and what apparatus (e.g., pressure-volume machinery) the derivation depends on. Theory channel is needed.

**Theory question:** How does the corpus's theory relate the specific-heat ratio γ to β, what derivation does it use, and what apparatus (pressure, volume, work against expansion) does that derivation require?

**Theory's Answer:**

## The β–γ relation

The corpus defines β as "the ratio of the total energy to the energy of translation" [1867-maxwell-dynamical-theory-of-gases] for a molecule, and γ as the ratio of specific heat at constant pressure to specific heat at constant volume. It relates them by

> "γ = (2+3β)/(3β)" (eq. 113), "whence β = (2/3)·(1/(γ−1))" (eq. 114).

## The derivation

It proceeds in two thermodynamic steps:

**Step 1 — heat added at constant density.** Starting from "The total energy of agitation of unit of mass is βV² = E, or E = (3β/2)(p/ρ)" (eq. 108), the corpus states: "If, now, additional energy in the form of heat be communicated to it without changing its density, ∂E = (3β/2)(∂p/ρ) = (3β/2)(p/ρ)(∂θ/θ)" (eq. 109), giving the constant-volume specific heat "∂E/∂θ = (3β/2)·p/(ρθ)" (eq. 110).

**Step 2 — adiabatic expansion back to the original pressure.** "Now, let the gas expand without communication of heat till the pressure sinks to its former value, and let the final temperature be θ + ∂'θ. The temperature will thus sink by a quantity ∂θ − ∂'θ, such that (∂θ−∂'θ)/θ = 2/(2+3β)·∂p/p" (eq. 111). This yields ∂'θ/θ = 3β/(2+3β)·∂θ/θ and the constant-pressure specific heat "∂E/∂'θ = (2+3β)/2 · p/(ρθ)" (eq. 112). Dividing (112) by (110) gives eq. 113.

## What the apparatus requires

Step 2 relies on the adiabatic relation the corpus derives a page earlier under "Cooling by Expansion": from eq. (93), "the second, third, and fourth [terms] represent the cooling by expansion" — these are p(du/dx)+p(dv/dy)+p(dw/dz), the pressure doing work against a volume-changing motion of the element. Setting conduction and heat exchange to zero gives "2·∂ρ/ρ = 3β·∂V̄²/V̄² = 3β·∂θ/θ" (eq. 105) and hence "∂p/p = (2+3β)/(3β)·∂ρ/ρ" (eq. 107), which is the relation invoked in eq. 111.

So the derivation requires, explicitly, pressure p, density ρ (standing in for volume through MN = ρ), and the work-against-expansion term that appears as p·(du/dx+dv/dy+dw/dz) in eq. 93 [1867-maxwell-dynamical-theory-of-gases]. Heating is done at constant density; expansion is done without communication of heat until p returns to its original value; the corpus does not write "work = p dV" as a separate quantity but routes it through the cooling-by-expansion terms in the energy equation.

### Issue 3: Encounter commitments need a dilute regime

**Category:** THEORY
**Reason:** The fix depends on what the corpus's theory says about the regime of validity for its encounter apparatus, and what (if anything) it commits to in dense matter. Theory channel is needed.

**Theory question:** Does the corpus's theory restrict its encounter-based reasoning (discrete pairwise episodes with free flight between them) to a dilute regime, and what does it say about interactions in dense bodies such as solids?

**Theory's Answer:**

Yes. The corpus confines encounter-based reasoning to a dilute regime in two explicit ways and leaves dense bodies essentially outside its scope.

**The dilute-regime assumption**

The phase distinction is stated qualitatively at the outset: "in gases the greater part of the path of each molecule is supposed to be sensibly rectilinear and beyond the sphere of sensible action of the neighbouring molecules" [1867-maxwell-dynamical-theory-of-gases].

The formal simplification in the two-body calculation makes this quantitative: "we shall suppose that the time during which a molecule is beyond the action of other molecules is so great compared with the time during which it is deflected by that action, that we may neglect both the time and the distance described by the molecules during the encounter, as compared with the time and the distance described while the molecules are free from disturbing force. We may also neglect those cases in which three or more molecules are within each other's spheres of action at the same instant" [1867-maxwell-dynamical-theory-of-gases].

The transfer-of-momentum derivation of pressure relies on the same dilution: "The mechanical action between the parts of the medium on opposite sides of the plane consists partly of the momentum thus transferred, and partly of the direct attractions or repulsions between molecules on opposite sides of the plane. The latter part of the action must be very small in gases, so that we may consider the pressure between the parts of the medium on opposite sides of the plane as entirely due to the constant bombardment kept up between them" [1867-maxwell-dynamical-theory-of-gases].

**Dense bodies: solids and liquids**

The corpus marks these phases as distinct and largely declines to treat them. For solids, molecules "oscillate about their positions of equilibrium, but do not travel from one position to another in the body"; in liquids they "are supposed to be always under the action of the forces due to neighbouring molecules throughout their course" [1867-maxwell-dynamical-theory-of-gases] — i.e. the discrete free-flight/encounter decomposition does not apply because there is no free flight.

On whether an analogous temperature law holds, the corpus is explicit that it cannot be written down: "A law of the same general character is probably to be found connecting the temperatures of liquid and solid bodies with the energy possessed by their molecules, although our ignorance of the nature of the connexions between the molecules renders it difficult to enunciate the precise form of the law" [1867-maxwell-dynamical-theory-of-gases].

The corpus also considered, and rejected, a purely statical alternative for solids: "In solid bodies the elasticity of form appears in many cases to be smaller in proportion to that of volume than the theory gives, so that we are forced to give up the theory of molecules whose displacements are functions of their coordinates when at rest, even in the case of solid bodies" [1867-maxwell-dynamical-theory-of-gases].

**Summary**

The encounter-based apparatus (discrete pairwise episodes, free flight between them, two-body reductions, neglect of triples) is assumed to hold only where free-flight time dominates interaction time — i.e. gases. For liquids and solids, the corpus identifies the relevant qualitative picture (continuous mutual action; oscillation about equilibrium) but declines to extend its reasoning there and registers the precise law as unknown.

### Issue 4: P.temp_functional derivation hand-waves the key step

**Category:** THEORY
**Reason:** The fix requires knowing whether the corpus actually derives that mean *translational* vis viva per molecule is what equilibrates, or whether it is posited. Theory channel is needed.

**Theory question:** Does the corpus's theory derive that the quantity equalized at thermal equilibrium is mean translational vis viva per molecule (rather than mean total energy per molecule), and if so by what argument?

**Theory's Answer:**

Yes. The corpus [1867-maxwell-dynamical-theory-of-gases] derives equalization of **translational** mean vis viva per molecule, and handles internal energy by a separate (weaker) assumption rather than by the same detailed-balance argument.

**The derivation (Final Distribution of Velocity section).**

1. Collision mechanics are treated as between centres of force, so the only relation between initial and final speeds is conservation of translational kinetic energy:

   > "the only relation between $a$, $b$ and $a'$, $b'$ is $M_1 a^2 + M_2 b^2 = M_1 a'^2 + M_2 b'^2$" [eq. 23]

2. The stationarity condition $f_1(a)f_2(b) = f_1(a')f_2(b')$ [eq. 22], combined with constraint (23), yields Maxwellian distributions with moduli satisfying

   > "$M_1\alpha^2 = M_2\beta^2$ ... whence $M_1\overline{v_1^2} = M_2\overline{v_2^2}$, or the mean *vis viva* of a molecule will be the same in each system." [eqs. 25, 33, 34]

   Here $v$ denotes the translational speed (the $\xi,\eta,\zeta$ of the centre of gravity).

3. The explicit "Equilibrium of Temperature between two Gases" section confirms this: equation (94) and the definitions

   > "$\tfrac{M_1}{M_1+M_2}(\overline{\xi_1^2}+\overline{\eta_1^2}+\overline{\zeta_1^2}) = Q_1$" [eq. 95]

   involve only translational components; $Q_1=Q_2$ is taken as the criterion of equal temperature [eq. 98].

**Why not total energy.** Internal motion is handled by a separate assumption borrowed from Clausius — that translational and internal energies reach a fixed ratio through accumulated exchanges:

> "the energy of translation and the internal energy of the molecules arrive, by repeated small exchanges, at a final ratio, which we shall suppose to be that of 1 to $\beta - 1$"

and

> "The ratio $\beta$ will be different for every molecule ... but it will have an average value depending on the nature of the molecules."

Since $\beta$ depends on species, equality of translational vis viva does not in general imply equality of total energy $\beta\cdot\tfrac{1}{2}Mv^2$. The collision-based detailed-balance argument delivers only the translational equality; the total-energy picture then follows by the separate Clausius assumption about the translational/internal ratio.

Maxwell emphasizes the robustness of the translational result specifically:

> "This is a very important result in the theory of gases, and it is independent of the nature of the action between the molecules." [after eq. 34]

### Issue 5: "Classical regime where internal modes are fully active" is anachronistic

**Category:** BOTH
**Reason:** The fix needs both what regime vocabulary the corpus's theory actually uses, and what temperature/substance range the measurements cover — so the revision can restate the regime condition in corpus-native terms. Theory and Evidence channels are needed.

**Theory question:** Does the corpus's theory have any notion that internal molecular modes could be inactive or "frozen out" at some temperatures, or does it treat β as uniformly applicable across the regimes it addresses?

**Theory's Answer:**

The corpus treats β as uniformly applicable. It is a species-level constant set by molecular structure, not modulated by temperature or regime.

From [1867-maxwell-dynamical-theory-of-gases]:

- β is "the ratio of the total energy to the energy of translation… it will have an average value depending on the nature of the molecules, as has been shown by Clausius. The value of β can be determined if we know either of the specific heats of the gas, or the ratio between them."
- "If we assume with Clausius that the ratio of the mean energy of internal motion to that of agitation tends continually towards a definite value (β − 1), we may conclude that, except in very violent disturbances, this ratio is always preserved."

The only variation the corpus acknowledges is (a) fluctuation molecule-to-molecule and collision-to-collision — "β will be different for every molecule, and will be different for the same molecule after every encounter" — and (b) departure under "very violent disturbances." Neither is a temperature-dependent deactivation of modes.

Operationally, Maxwell carries β as a constant through the specific-heat results (eqs. 110, 112, 114) and the ratio γ = (2+3β)/(3β) (eq. 113). He treats γ as a fixed per-gas number (e.g., "γ = 1.409" for air, "γ for carbonic acid is 1.27") and remarks that "γ is nearly the same for air, oxygen, hydrogen, and carbonic oxide" — with no suggestion that γ, and hence the active internal content, should shift with temperature.

So to answer directly: the corpus has no notion of internal modes being inactive or frozen out. Its mechanism for setting the internal/translational ratio is "repeated small exchanges" in collisions driving a definite final ratio, and that ratio is assumed preserved across all the regimes the paper addresses (equilibrium, diffusion, viscosity, conduction, expansion). The question of whether some internal degrees of freedom could fail to participate at some temperatures is not one the corpus entertains; asking it reaches beyond what the corpus can support.

**Evidence question:** What temperature range and substance classes do the heat-capacity measurements in the corpus cover, and is there evidence of deviation from constant β at any end of that range?

**Evidence's Answer:**

## Temperature Range, Substance Classes, and Constancy of the Atomic Heat Product

### Temperature Range

The measurements were made over a single narrow window: **5°C to 10°C above the ambient medium** (centigrade excess), with the ambient medium held at the temperature of melting ice (0 °C). The effective measurement band is therefore approximately **5 °C to 10 °C**. No data are reported at other temperatures. [1819-dulong-petit]

### Substance Classes

**Solids (own experiments):** 13 simple bodies, all measured as fine powders under vacuum (~2 mmHg air pressure) in a silver calorimeter vessel:

| Element | Specific heat | Atomic weight | Product |
|---------|--------------|---------------|---------|
| Bismuth | 0.0288 | 13.30 | 0.3830 |
| Lead | 0.0293 | 12.95 | 0.3794 |
| Gold | 0.0298 | 12.43 | 0.3704 |
| Platinum | 0.0314 | 11.16 | 0.3740 |
| Tin | 0.0514 | 7.35 | 0.3779 |
| Silver | 0.0557 | 6.75 | 0.3759 |
| Zinc | 0.0927 | 4.03 | 0.3736 |
| Tellurium | 0.0912 | 4.03 | 0.3675 |
| Copper | 0.0949 | 3.957 | 0.3755 |
| Nickel | 0.1035 | 3.69 | 0.3819 |
| Iron | 0.1100 | 3.392 | 0.3731 |
| Cobalt | 0.1498 | 2.46 | 0.3685 |
| Sulphur | 0.1880 | 2.011 | 0.3780 |

**Gases (third-party data):** Oxygen, azotic gas (nitrogen), and hydrogen, from Laroche and Bérard. Dulong and Petit cite these but did not measure them directly. [1819-dulong-petit]

### Evidence of Deviation from the Constant Product

**Among solids:** The product ranges from **0.3675** (Tellurium) to **0.3830** (Bismuth). The authors attribute the spread to measurement error and chemical-analysis uncertainty, and treat the product as constant within experimental limits. No systematic departure at either end of the substance range (lightest or heaviest atoms) is identified. [1819-dulong-petit]

**Among gases:** Oxygen and azotic gas agree with the law within what the authors describe as probable experimental error. Hydrogen's product is reported as **"rather too small"** — a stated deviation. The authors ascribe this to a known experimental artifact: hydrogen cools so rapidly relative to other gases that the Laroche–Bérard method introduced a systematic underestimate, not corrected by those authors. The deviation is flagged but not quantified numerically in the text. [1819-dulong-petit]

**Across temperature:** Because the measurement window is a single 5–10 °C band with no comparison at other temperatures, the corpus contains **no evidence bearing on whether the product is constant or deviates at lower or higher temperatures**. That question cannot be answered from this corpus.

### Issue 6: "Smooth elastic sphere transfers force along the line of centres" asserted, not derived

**Category:** THEORY
**Reason:** The fix requires knowing whether the corpus's theory adopts a specific collision law for smooth elastic spheres, and if so whether it is stated as a postulate or as a derivation. Theory channel is needed.

**Theory question:** Does the corpus's theory include a commitment that collisions between smooth elastic spheres transmit force only along the line of centres, and is that commitment stated as an auxiliary postulate or derived from something more primitive?

**Theory's Answer:**

The corpus does not commit to smooth-elastic-sphere collisions in this paper — Maxwell explicitly replaces that model. The central-force (line-of-centres) property appears instead as a stipulated modeling assumption about centres of force, not as a derived result.

Maxwell sets the model by fiat:

> "I propose to consider the molecules of a gas, not as elastic spheres of definite radius, but as small bodies or groups of smaller molecules repelling one another with a force whose direction always passes very nearly through the centres of gravity of the molecules, and whose magnitude is represented very nearly by some function of the distance of the centres of gravity." [`1867-maxwell-dynamical-theory-of-gases`]

The "very nearly" signals that this is a postulated approximation, not a theorem. He draws out its consequence — that the orbits are planar and symmetric about the line of apses — only after positing it:

> "If we regard the molecules as simple centres of force, then each molecule will describe a plane curve about this centre of gravity, and the two curves will be similar to each other and symmetrical with respect to the line of apses." [`1867-maxwell-dynamical-theory-of-gases`]

And he is explicit that the assumption is known to break for richer molecules, which confirms its status as postulate rather than derivation:

> "If we suppose the molecules to be bodies, or systems of bodies, capable of rotation, internal vibration, or any form of energy other than simple motion of translation, these results will be modified… we must content ourselves with the assumption that the value of θ is, on an average, the same as for pure centres of force…" [`1867-maxwell-dynamical-theory-of-gases`]

So: (i) smooth elastic spheres are not the corpus's committed model here — Maxwell names that hypothesis only to reject it on grounds of viscosity data; (ii) the line-of-centres property is stated as an auxiliary modeling postulate about inter-molecular force direction, with no derivation from anything more primitive in this text. Whether it *could* be derived from a sphericity/smoothness postulate is not something the corpus addresses.

### Issue 7: "Species" is used before being defined

**Category:** THEORY
**Reason:** The fix needs to know whether the corpus's theory treats species as a primitive attribute of a molecule or as an equivalence class induced by other properties (mass, internal constitution). Theory channel is needed.

**Theory question:** How does the corpus's theory individuate molecular species — as a primitive label, as an equivalence class on mass and internal constitution, or in some other way — and what does β being "species-invariant" presuppose about that individuation?

**Theory's Answer:**

# How the Corpus Individuates Molecular Species

## The operational definition of "molecule"

The corpus begins with a dynamical, not ontological, criterion: "The molecules of a gas in this theory are those portions of it which move about as a single body" [1867-maxwell-dynamical-theory-of-gases]. Crucially, the paper refuses to commit to a single internal picture:

> "These molecules may be mere points, or pure centres of force endowed with inertia, or the capacity of performing work while losing velocity. They may be systems of several such centres of force, bound together by their mutual actions... Finally, if necessary, we may suppose them to be small solid bodies of a determinate form."

So "molecule" is individuated by dynamical coherence (moves as one body), with internal constitution deliberately underdetermined.

## How "kinds" are individuated

Species enter the formalism as **primitive indexed labels** ("molecules of the first kind", "of the second kind"), with $N_1$, $M_1$ and $N_2$, $M_2$ counting and weighing each. But the labels are not inert: each kind is associated with a bundle of kind-level parameters that govern its dynamics:

1. **Mass** $M_i$ — per-molecule, uniform within a kind.
2. **Force law with itself** — coefficient $K_1$ for first-kind/first-kind encounters, $K_2$ for second-kind/second-kind (entering as $k_1 = (K_1/2M_1^3)^{1/2}$, etc.).
3. **Force law with others** — coefficient $K$ governing cross-species encounters (entering as $k$), which the paper calls "the coefficient of mutual interference of the molecules of the two gases."
4. **Internal-energy ratio** $\beta_i$.

So operationally the individuation is an **equivalence class under a set of dynamical parameters** $(M, \text{self-force law}, \text{cross-force laws}, \beta)$, not a primitive label and not pure mass alone. Two collections that share all of these are indistinguishable within the theory.

The corpus connects this theoretical individuation to chemistry via Gay-Lussac: at equal $p$ and $\theta$, "the masses of the individual molecules are proportional to the density of the gas," letting Maxwell substitute specific gravity $s_i$ for $M_i$.

## What $\beta$ being species-invariant presupposes

$\beta$ is introduced with an explicit caveat about what it is and is not:

> "The ratio $\beta$ will be different for every molecule, and will be different for the same molecule after every encounter with another molecule, but it will have an average value depending on the nature of the molecules, as has been shown by Clausius." [1867-maxwell-dynamical-theory-of-gases]

So $\beta$ is not an instantaneous per-molecule invariant; it is a **kind-level mean** under the equilibration assumption:

> "in a great many encounters the energy of translation and the internal energy of the molecules arrive, by repeated small exchanges, at a final ratio, which we shall suppose to be that of 1 to $\beta - 1$."

And again:

> "If we assume with Clausius that the ratio of the mean energy of internal motion to that of agitation tends continually towards a definite value $(\beta - 1)$, we may conclude that, except in very violent disturbances, this ratio is always preserved."

For $\beta$ to be a well-defined species-level number, the individuation must already carry enough to fix what molecules of that kind *are* internally. Specifically, the presuppositions are:

- **A shared internal constitution within the kind.** Whatever the molecules are — point-systems, rotating bodies, bound groups of force-centres — members of one species must share the same menu of internal degrees of freedom. Otherwise "the nature of the molecules" would not pick out a single limit ratio.
- **Ergodic-style equilibration of translational and internal modes by encounters.** $\beta$ is defined only in the limit where "repeated small exchanges" have driven the ratio to its stationary value. Species-invariance presupposes that this stationary value is reached and that it depends only on the kind, not on the current dynamical history.
- **Internal energy that couples to translation during encounters but is otherwise conserved.** The derivation of the encounter rules assumes "the final velocities differ from the initial velocities only by quantities which may in each collision be neglected," while internal energy still exchanges slowly — a separation of timescales that the individuation must respect.
- **The "pure centres of force" case is a degenerate species.** "If the molecules are pure centres of force, there can be no energy of rotation, and the whole energy is reduced to that of translation" — i.e. $\beta = 1$. So $\beta$ being species-dependent *at all* presupposes species that are not all structureless points.

## Where the individuation is left open

Two gaps are worth flagging because the corpus itself flags them. First, the specific internal structure that fixes $\beta$ is not derived; $\beta$ is read off from empirical specific-heat ratios via $\beta = \frac{2}{3}\frac{1}{\gamma - 1}$. Second, the paper acknowledges it cannot decompose mixed species: in discussing the diffusion of air, it notes "we have assumed that air is a simple gas" while admitting "the constituents of air can be separated by mechanical means." So the theory's individuation is fine-grained enough to distinguish species but does not, within the paper, furnish an independent test for whether a given sample is one kind or a mixture — that comes in from outside (chemistry, atmolysis).

## Short answer

The corpus individuates species as an equivalence class under the parameter tuple $(M, \text{self-force law } K_i, \text{cross-force laws } K, \beta)$, carried in the formalism by primitive subscripts. $\beta$'s species-invariance presupposes that members of a kind share a common internal constitution, that translational-internal energy exchange equilibrates to a stationary ratio depending only on that constitution, and that this equilibration is fast enough relative to bulk dynamics for the ratio to be treated as fixed — while leaving the specific internal structure underdetermined.
