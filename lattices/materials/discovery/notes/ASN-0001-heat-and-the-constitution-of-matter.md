# ASN-0001: Heat and the Constitution of Matter

*2026-04-20*

We are asking how heat — the thing that flows between hot and cold bodies, that warms us, that vaporises water — connects to what bodies are *made of*. This is not a question about thermometers; it is a question about ontology. The *statical* view, in which matter sits still and heat is a fluid distributed through it, must be set against the *dynamical* view, in which heat is the motion of the constituents themselves. We shall find the second view forced upon us by the inability of the first to accommodate the combined evidence of fluid behaviour, gas pressure, and the empirical near-constancy of heat per atom across the elements.

Let us begin with what we can observe and ask what state must be ascribed to a body to account for it.

## The dynamical commitment

A body at rest, heated, exhibits no visible change in its parts. If heat is to live somewhere — and we restrict ourselves to mechanical accounts — it must live in *invisible* motion. The choice is sharp: theories are *statical* if they suppose molecules at rest relative to the body, *dynamical* if they suppose molecules in motion even while the body is apparently at rest. We commit to the dynamical position and inquire what its consequences must be.

Let us name the abstract objects of the discussion.

A *body* `B` consists of constituents — call them molecules — indexed by some set `I.B`. Each constituent `c ∈ I.B` carries a mass `c.mass ∈ ℝ⁺`, a position `c.x ∈ ℝ³`, a velocity `c.v ∈ ℝ³`, and an internal-state vector `c.q` ranging over a state space appropriate to its kind. The pair `(c.v, c.q)` constitutes the *kinematic state* of `c`. We do not yet specify dynamics; we only insist that this state be available.

Within a region of `B` with bulk velocity `u ∈ ℝ³`, decompose each `c.v` as

  `c.v = u + c.ξ`

where `c.ξ` is the *agitation* of `c` — its velocity residual after the bulk motion is subtracted. The agitation lives at the molecular scale; it is invisible at the bulk scale.

We adopt as our first invariant:

  **P0** *[the dynamical commitment]*: heat in `B` is identified with kinetic energy carried by the agitation field `ξ` together with internal kinetic energy encoded in `q` at each constituent. Heat lives in molecular motion; it is a property of the kinematic state, never a quantity additional to mass and motion.

This is a claim, not an observation. The justification must come from showing that P0 reproduces phenomena no statical account can.

## Why a statical account fails

Suppose, by way of contradiction, that `B` is statical: `c.ξ = 0` and `c.q` is at rest at every `c`. The mechanical state is then the configuration `{c.x : c ∈ I.B}` together with whatever forces hold it. Heat must be encoded in the configuration itself — in some quantity `Q.B` depending only on positions and forces.

Consider what such a body does under deformation. If forces are central and equilibrium positions are fixed, the elastic response to a small change of *form* (shear) bears a fixed ratio to the response to a small change of *volume* (compression). But fluids exhibit *evanescent form-elasticity*: a fluid offers no resistance to slow shear, while offering considerable resistance to compression. No statical model with the form/volume coupling can reproduce this.

This is decisive. To preserve the empirical character of fluids, we must permit the molecules to be in motion — in which case heat, a quantity not visible in bulk equilibrium, has a place to live: in that motion. We retain P0.

## The partition of energy

Consider one constituent `c`. Its kinetic energy decomposes:

  `KE(c) = ½ c.mass · |c.v|² = ½ c.mass · |u|² + c.mass · u · c.ξ + ½ c.mass · |c.ξ|²`

Averaged over many constituents in a small region (with the cross term vanishing by `(N c : c ∈ region : c.ξ) = 0`, the very condition that defines `u`), the bulk kinetic energy density and agitational kinetic energy density separate cleanly:

  `⟨KE⟩ = ½ ρ |u|² + ½ ρ ⟨|ξ|²⟩`

where `ρ` is mass density and `⟨·⟩` denotes the local average. The first term is *bulk* kinetic energy, visible at human scale. The second is agitational, invisible.

Constituents may also carry *internal* kinetic energy — rotation, oscillation of parts. Call this `E_int(c)`. For a constituent that is a *pure centre of force*, `E_int = 0`. For a rigid body with extent, `E_int` captures rotation. For a body with internal elastic linkages, `E_int` captures rotation plus oscillation modes.

We do not, at this level of abstraction, decompose `E_int` into rotational and vibrational pieces. We treat it as a single internal reservoir whose capacity is determined by the constitution of `c`.

Define the *constitution parameter* `β.k` for a kind `k` of molecule by

  `β.k := ⟨total energy per molecule of kind k⟩ / ⟨translational energy per molecule of kind k⟩`

at thermal equilibrium. Then the total kinetic energy per molecule of kind `k` is

  `½ M.k · ⟨|ξ|²⟩.k · β.k`

with `β.k = 1` for pure centres of force and `β.k > 1` otherwise. The value of `β.k` is not derived from molecular structure here; we read it off the measured ratio of specific heats. Constitution enters as a parameter the present theory accommodates rather than predicts.

  **P1** *[partition]*: each kind `k` has a constitution-determined ratio `β.k ≥ 1` fixing the share of translational energy in total energy per molecule of kind `k` at thermal equilibrium.

## Temperature as the equilibrium criterion

Place two bodies in mechanical contact — say, gases of two kinds of molecules sharing a volume. The constituents collide; energy can be exchanged. Let `Φ(k₁→k₂)` denote the rate of vis viva transfer from kind `k₁` to kind `k₂` per unit time per unit volume. Define equilibrium of heat between them by

  `Φ(k₁→k₂) = Φ(k₂→k₁)`

— net zero exchange. Two bodies at *the same temperature* are precisely those for which this equality holds when in contact. The definition is operational: it identifies temperature equality through behaviour, not through any single mechanical quantity.

The theory then *derives* — from the dynamics of binary encounters — that `Φ` is balanced precisely when

  `M.k₁ · ⟨|ξ|²⟩.k₁ = M.k₂ · ⟨|ξ|²⟩.k₂`         (E1)

i.e., the *mean translational vis viva per molecule* is equal across kinds. This result holds independently of the force law mediating the encounters, which is what makes it a statement about temperature rather than about a particular interaction.

  **P2** *[equipartition of translational vis viva]*: at thermal equilibrium between any two kinds `k₁` and `k₂` of molecule in contact, `M.k₁ · ⟨|ξ|²⟩.k₁ = M.k₂ · ⟨|ξ|²⟩.k₂`. The common value depends only on temperature, not on kind.

P2 justifies *defining*

  `τ.B := ½ M.k · ⟨|ξ|²⟩.k`     (any kind `k` present in `B` at equilibrium)

— the mean translational kinetic energy per molecule, well-defined by P2 because the value is the same whichever `k` is chosen. Temperature in any equilibrium body is then a strictly increasing function of `τ.B`. Choose a scale for which

  `θ.B = (2 / 3κ) · τ.B`

for some operational constant `κ` (the choice of `κ` is a unit convention; the abstract content is `τ.B` itself).

  **P3** *[temperature as mean translational vis viva]*: in any equilibrium body, temperature `θ.B` is determined by `τ.B = ½ M ⟨|ξ|²⟩`, the mean translational vis viva per molecule, and is independent of the kind of constituent measured.

## The internal reservoir equilibrates to fixed ratio

Bodies whose constituents are not pure centres of force have internal motion. The theory asserts — and we accept on the corpus's authority for the abstract specification — that repeated encounters drive the *ratio* of mean internal to mean translational energy per molecule of kind `k` toward `β.k − 1`. After sufficient time, the internal reservoir holds `(β.k − 1)` times what the translational reservoir holds. We do not, at this level, derive `β.k`; we treat it as a constitution parameter the experiment must measure.

  **P4** *[internal/translational ratio]*: in any equilibrium body containing molecules of kind `k`, the ratio of mean internal kinetic energy per molecule to mean translational kinetic energy per molecule equals `(β.k − 1)`, a constitution-determined constant.

The total kinetic energy of agitation per unit volume of an equilibrium body of kind `k` is therefore

  `ε.B = (3/2) · β.k · p.B`

where `p.B` is the pressure, whose mechanical interpretation we develop next. The factor `3` arises from three translational components; the factor `β.k` upgrades from translation alone to translation-plus-internal.

## Pressure as translational momentum flux

The mechanical action of constituents on one side of an imaginary plane against those on the other is the transfer of momentum across that plane, summed over crossings. For a *dilute* body — one whose constituents spend most of their time outside one another's force range — this transfer is dominated by free-flight translation. A molecule crosses, carrying momentum `M · c.v`; the bulk component contributes the mean motion (which cancels in equilibrium); the agitation component contributes the pressure.

Working out the bookkeeping for an isotropic equilibrium gives

  `p.B = ⅓ ρ ⟨|ξ|²⟩`

Equivalently, in terms of `τ.B` and the molecular number density `n.B = ρ / M`:

  `p.B = ⅔ · n.B · τ.B`         (E2)

  **P5** *[pressure–vis viva relation, dilute regime]*: in any body whose constituents spend most of their time outside one another's force range, pressure equals two-thirds of the mean translational vis viva per molecule times molecular number density.

Internal energy does not appear in P5. Pressure, in the dilute regime, depends only on translational agitation. This is a critical asymmetry: heat *content* depends on `β`; pressure does not. Internal motion does not push against a wall.

## The Law of Equivalent Volumes

Combine P3 and P5. At common temperature, two dilute bodies of kinds `k₁`, `k₂` at the same pressure satisfy

  `⅔ · n₁ · τ = p = ⅔ · n₂ · τ`     ⟹     `n₁ = n₂`

  **P6** *[equivalent volumes as theorem]*: in the dilute regime, equal volumes of bodies at common temperature and pressure contain equal numbers of constituents, regardless of the kind of constituent.

P6 is a consequence of P0–P5, not an independent postulate. It depends on the dilute regime through P5. In a dense body, where forces contribute to pressure directly, P6 need not hold.

## Heat capacity per molecule

Consider an equilibrium dilute body of kind `k` with `N` constituents. By P3 and P4, its total internal-energy-of-agitation is

  `U.B = N · τ · β.k = N · (3κ θ / 2) · β.k`

Heat capacity at constant volume is

  `C_V(B) = ∂U/∂θ = N · (3κ / 2) · β.k`

Per molecule:

  `c_V(per molecule) = (3/2) · κ · β.k`

This is a *constitution-determined per-molecule constant*. For monatomic kinds (centres of force) `β.k = 1` and `c_V` is universal across kinds. For molecular kinds with internal motion `β.k > 1` raises `c_V` proportionally.

  **P7** *[heat capacity per molecule is constitution-determined]*: in the dilute regime, heat capacity per molecule depends only on the constitution parameter `β.k` of the kind, and is independent of density, pressure, or sample mass.

This is what the theory predicts. To confront it with the empirical record we must turn to the measurements.

## The empirical signature: Dulong–Petit

The 1819 measurements report, for thirteen solid elements, the product of *specific heat per unit mass* and *relative atomic weight*. Calling the specific heat per unit mass `c_s(k)` and the atomic weight `A(k)`, the product is

  `Π(k) := c_s(k) · A(k)`

The thirteen products (in the dimensionless system of the era) range from `0.3675` (tellurium) to `0.3830` (bismuth) — a spread of about `4%` across substances whose specific heats vary by a factor of nearly seven and whose atomic weights vary by a factor of more than six. Thirteen substances of widely differing elemental character clustering within `4%` of one another demands a structural explanation.

The theoretical explanation is immediate. Specific heat per unit mass times atomic weight gives heat capacity *per atom*:

  `c_s(k) · A(k)  ∝  C_V(per atom of kind k)`

By P7, this depends only on `β.k`. The empirical near-constancy of `Π(k)` is therefore the assertion that `β.k` is approximately constant across the thirteen solid elements — that the per-atom internal-motion structure of the simple solid elements at the measured temperatures is, to within `~4%`, independent of which element is considered.

This is a non-trivial statement about the constitution of matter. It says: at temperatures near room temperature, the elemental solids organise their internal motion so that each atom carries approximately the same heat-storage capacity. The constitution of matter — at the level of "what is a constituent and how does it carry energy?" — is, in this regime, surprisingly uniform.

  **P8** *[empirical regularity, restricted regime]*: across the simple solid elements measured in the regime of small temperature excursions near `5–10 °C` above an ice-water reference, heat capacity per atom is approximately constant.

The claim is restricted by the regime of measurement. The corpus measures only solid elements, only at `5–10 °C`, only thirteen substances. Stronger claims — universality across phase, monotonicity in temperature, behaviour at low temperatures, applicability to compounds — are not warranted by what we have. We must mark these explicitly as outside the support of the evidence.

## What the partition does not tell us

We have decomposed energy per molecule into translation and a single lumped internal reservoir. The corpus is forthright that this decomposition cannot be refined further from first principles: it offers no *a priori* count of how internal energy splits between rotation, vibration, and other intramolecular modes. The ratio `β.k` is to be measured from the specific-heat ratio `γ.k = (2 + 3β.k) / (3β.k)`; it is not predicted.

We accept this limit. The abstract specification can record the *shape* of the theory — a single lumped internal reservoir per kind — without filling in the unknown structure. Future deepening, were it to count modes, would refine `β.k` into a sum over modes, but would not contradict the abstract partition.

## Phase as constitutional state

The corpus distinguishes three phases by the time-character of molecular position dynamics:

- *solid*: molecules oscillate about fixed equilibrium positions; no net translation between sites
- *liquid*: molecules continually rearrange relative positions, while remaining throughout under the action of neighbours' forces
- *gas*: molecules spend most of their trajectory outside neighbours' force range; trajectories nearly rectilinear between rare encounters

These are three regimes of the *same* underlying mechanical state — molecules with positions and velocities under forces. They differ in the time-character of position dynamics: bound oscillation, continual rearrangement under continuous force, free flight between rare encounters. We may abstract this with a phase predicate `Π.B ∈ {solid, liquid, gas}`:

  `Π.B = solid     ≡     (A c ∈ I.B : c.x stays bounded within an equilibrium-anchored neighbourhood for all time)`

  `Π.B = gas       ≡     (A c ∈ I.B : the fraction of time c spends outside all neighbours' force range tends to 1 as density decreases)`

  `Π.B = liquid    ≡     ¬(Π.B = solid) ∧ ¬(Π.B = gas), with continual rearrangement under continuous neighbour interaction`

These are *abstract* characterisations. The corpus recognises the categories but admits — for solids and liquids — that the precise law connecting temperature to molecular energy is not yet stated. The theory is quantitative for gases.

  **P9** *[phase as kinematic regime]*: the phase of `B` is determined by the time-character of the constituents' position dynamics under the forces between them; phase transitions correspond to changes in this character.

The corpus contains no measurements of latent heat and no measurements of the same substance across phases. We cannot, from the present evidence, quantify the energy associated with phase transitions. We can, however, reason: if heat is invisible motion (P0), then any energy absorbed during a phase change without temperature rise must be stored either in *rearranging* the constituents against their mutual forces (configurational potential energy) or in *redistributing* the partition between translational and internal reservoirs. The corpus does not measure which.

## What forces between constituents do

We have not yet asked what *forces* between constituents do for the account of heat. They are necessary for several reasons:

First, without forces, isotropy fails. Free-flying molecules in a box would exhibit anisotropic stress — directionally biased pressure depending on initial conditions. Forces between constituents redistribute momentum, equalising the pressure across directions. Without that redistribution, the body behaves like an elastic solid even when populated by free molecules.

Second, without forces, equilibration fails. Energy could not flow between kinds, between translational and internal reservoirs, or between regions of different temperature. Forces enable the encounters by which `Φ` becomes balanced.

Third, with forces of finite range, viscosity arises. The redistribution of momentum is rapid but not instantaneous; the residual anisotropy in the time of relaxation is the phenomenon of viscosity. This too is a regime-dependent consequence: viscosity depends on the law of force.

But — and this is essential — *forces do not, in the dilute regime, contribute directly to pressure*. P5 stands. Pressure in a gas comes from translational momentum transferred at the boundary; the contribution from direct attractions or repulsions across the boundary is negligible because the mean inter-molecular distance exceeds the range of force. Forces shape *trajectories*; pressure tallies the result.

  **P10** *[role of intermolecular force, dilute regime]*: in the dilute regime, forces between constituents (i) equalise stress to isotropy, (ii) drive equilibration of vis viva across kinds and reservoirs, and (iii) generate viscosity; their direct contribution to pressure and to the equation of state is negligible.

In dense regimes — liquids and dense gases — forces *do* contribute to pressure, and P5 must be amended. The corpus does not develop this case quantitatively.

## Synthesis: the connection between heat and constitution

We can now state the connection that P0–P10 jointly establish.

Heat is invisible molecular motion. The *amount* of heat in a body at a given temperature depends on three things together: which kinds of constituents the body contains (through `β.k`), how many constituents there are (through `N`), and what regime the body is in (dilute vs dense; gas vs liquid vs solid).

Temperature, by contrast, depends on one thing only: the mean translational vis viva per molecule. It is independent of which kind, of how many, of the constitution parameter `β`. Temperature is the *democratising* variable of the dynamical theory: at thermal equilibrium, every kind of constituent shares the same translational kinetic energy per molecule.

The Dulong–Petit empirical regularity — the near-constancy of `c_s · A` across solid elements — is direct evidence that the constitution of matter is, in this restricted regime, organised so that heat capacity per atom is approximately constant. This is consistent with P7 (which asserts that heat capacity per molecule depends only on `β.k`); it constitutes an empirical claim that `β.k` is approximately uniform across the simple solid elements at the measured temperature. Stronger empirical confirmation would require measurements across phases, across temperature ranges, and across compounds, which the corpus does not provide.

The deepest commitment is P0. Once we identify heat with motion, the remainder follows: temperature is mean translational vis viva (P3 via P2); pressure is its boundary tally in the dilute regime (P5); heat capacity per molecule is fixed by the constitutional parameter `β.k` (P7); the law of equivalent volumes is a theorem (P6); phase is the kinematic regime of the constituents (P9). The empirical record — Dulong–Petit and the gas specific-heat ratios — is consistent with this picture and constrains the value of `β.k` without yet predicting it.

We are not finished. The theory does not predict `β.k` from first principles; it does not extend quantitatively beyond the dilute regime; it does not account for phase transitions; it does not partition internal energy among modes. Each of these is a place where the abstract specification may, in future, be deepened.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| P0 | Heat in a body is identified with kinetic energy carried by the agitation field `ξ` (velocity residuals after subtracting bulk motion) together with the internal kinetic energy of constituents | introduced |
| P1 | Each kind `k` of constituent has a constitution-determined ratio `β.k ≥ 1` fixing the share of translational energy in total energy per molecule of kind `k` at thermal equilibrium | introduced |
| P2 | At thermal equilibrium between any two kinds in contact, `M.k₁ · ⟨\|ξ\|²⟩.k₁ = M.k₂ · ⟨\|ξ\|²⟩.k₂`; the common value depends only on temperature, independent of force law | introduced |
| P3 | Temperature in any equilibrium body is determined by `τ.B = ½M⟨\|ξ\|²⟩`, the mean translational vis viva per molecule, independent of the kind measured | introduced |
| P4 | The ratio of mean internal to mean translational kinetic energy per molecule of kind `k` equals `(β.k − 1)` at equilibrium, a constitution-determined constant | introduced |
| P5 | In the dilute regime, `p = (2/3) · n · τ`; pressure depends only on translational agitation and number density | introduced |
| P6 | In the dilute regime, equal volumes at common temperature and pressure contain equal numbers of constituents | introduced |
| P7 | In the dilute regime, heat capacity per molecule depends only on the constitution parameter `β.k` of the kind | introduced |
| P8 | Across simple solid elements measured in a narrow temperature range near `5–10 °C` above an ice-water reference, heat capacity per atom is approximately constant | introduced |
| P9 | The phase of a body is determined by the time-character of constituents' position dynamics under intermolecular forces | introduced |
| P10 | In the dilute regime, intermolecular forces equalise stress, drive equilibration, and generate viscosity, while contributing negligibly to pressure | introduced |
| Σ.molecule | `molecule : I.B → (mass : ℝ⁺, x : ℝ³, v : ℝ³, q : InternalState.kind)` | introduced |
| Σ.bulk | `u : Region(B) → ℝ³` (mean velocity field) | introduced |
| Σ.agitation | `ξ : I.B → ℝ³` defined by `ξ.c = c.v − u(region of c)` | introduced |
| Σ.constitution | `β : MoleculeKind → [1, ∞)` | introduced |
| Σ.temperature | `θ : Body → ℝ⁺`, determined at equilibrium by `τ = ½M⟨\|ξ\|²⟩` | introduced |
| Σ.phase | `Π : Body → {solid, liquid, gas}` | introduced |
| Σ.heat | `ε : Body → ℝ⁺`, energy density of agitation, equal to `(3/2)·β·p` in the dilute regime | introduced |

## Open Questions

What does the theory require of any constitution-independent measure of thermal content?

Under what conditions does the partition of energy between translation and internal reservoirs become unique?

What invariants must any extensive thermodynamic quantity preserve when bodies are joined at common temperature?

Under what conditions on the constitution does heat capacity per atom become a multiple of a fixed unit?

What must any account of phase transition preserve regarding the partition of energy across translational, internal, and configurational reservoirs?

What does the theory require of the relation between pressure and intermolecular force in the dense regime where P5 fails?

What invariants must hold of the equilibration process between any two reservoirs (translational and internal, kind and kind, body and body)?

Under what conditions can the constitution parameter `β.k` be derived from a finer account of internal modes rather than measured?

What must the theory require of the dependence of mean translational vis viva on temperature for the temperature scale to be unique up to affine transformation?

What invariants must any measure of heat preserve under isolation from heat and matter exchange?
