# Revision Consultation — ASN-0002

**Review:** review-10.md
**Date:** 2026-05-05 08:14

## Summary

1 REVISE items analyzed: 0 internal, 1 consulted (1 maxwell-1867, 0 dulong-petit-1819)

## Consultation Results

### Issue 1: Premise (iv) and P.enc_ratio_equilibration are mutually inconsistent at the formal-claim level for β_k > 1 species

**Category:** MAXWELL-1867
**Reason:** The fix requires knowing how Maxwell's 1867 theory itself scopes the centres-of-force encounter modeling relative to the apportionment commitment for species with internal modes — whether the theory restricts (iv), treats it as a partial articulation of a more general encounter force, or restricts the apportionment claim. This is a question about the theory's own commitments and self-imposed scope, not about measured data.

**Maxwell-1867 question:** For species with internal degrees of freedom (β > 1), does Maxwell's 1867 theory present the conservative-central-COM-force characterization of encounters as a complete description (restricted to β = 1 species), as the COM-COM component of a more general encounter force whose internal-coupling part is left unmodelled, or as scoped by some other regime qualifier — and how does the theory locate the apportionment postulate (following Clausius) relative to that characterization?

**Maxwell-1867's Answer:**

# Answer

For β > 1 species, Maxwell presents the conservative-central-COM-force characterization as **none of the three options strictly** — it is closest to the third, but with a specific shape: it is an **averaging assumption** layered onto an admitted gap, not a clean regime restriction or a clean force-decomposition.

## The characterization is acknowledged incomplete for β > 1

Maxwell first develops the encounter analysis under the explicit premise of "simple centres of force" — central, conservative, COM-preserving, with deflection angle θ a function of relative velocity and impact parameter b alone. He then immediately flags that this is inadequate for molecules with internal structure:

> "If we suppose the molecules to be bodies, or systems of bodies, capable of rotation, internal vibration, or any form of energy other than simple motion of translation, these results will be modified. The value of θ and the final velocities of the molecules will depend on the amount of internal energy in each molecule before the encounter, and on the particular form of that energy at every instant during the mutual action." [1867-maxwell-dynamical-theory-of-gases]

So the central-force result is not presented as complete-and-restricted-to-β=1: Maxwell carries β > 1 species through the rest of the paper using the central-force expressions for θ, but only after stating they need modification.

## The scoping is an averaging-plus-smallness assumption, not a force decomposition

The next sentence is where Maxwell tells us how he handles the gap, and it is decisive:

> "We have no means of determining such intricate actions in the present state of our knowledge of molecules, so that we must content ourselves with the assumption that the value of θ is, on an average, the same as for pure centres of force, and that the final velocities differ from the initial velocities only by quantities which may in each collision be neglected, although in a great many encounters the energy of translation and the internal energy of the molecules arrive, by repeated small exchanges, at a final ratio, which we shall suppose to be that of 1 to β−1." [1867-maxwell-dynamical-theory-of-gases]

This is not the second option (COM-COM component of a richer force whose internal-coupling part is left unmodelled). Maxwell does **not** add a separate internal-coupling term to the force law and then drop it. He keeps the central-force law as the operative force, and pays for the gap with two coupled assumptions:

- **Per-encounter negligibility:** internal coupling alters final velocities only by quantities "which may in each collision be neglected"
- **Mean-θ equivalence:** θ averages to the same value as for pure centres of force

Together these license re-using the §2 expressions for ∫(Q′−Q)dφ unchanged for β > 1 species. The internal coupling itself stays out of the formalism — it is not modelled, decomposed, or bounded; it is only assumed to act invisibly in this averaged sense.

## The apportionment postulate sits outside the encounter characterization, following Clausius

The 1 : β−1 ratio is located one level up from the encounter analysis, as a separate postulate about long-run means. It first appears in the introduction:

> "The ratio β will be different for every molecule, and will be different for the same molecule after every encounter with another molecule, but it will have an average value depending on the nature of the molecules, as has been shown by Clausius." [1867-maxwell-dynamical-theory-of-gases]

When Maxwell later needs the ratio to compute total heat in unit volume, he restates it explicitly as an assumption rather than a derivation:

> "If we assume with Clausius that the ratio of the mean energy of internal motion to that of agitation tends continually towards a definite value (β − 1), we may conclude that, except in very violent disturbances, this ratio is always preserved." [1867-maxwell-dynamical-theory-of-gases]

So the apportionment postulate is not a consequence of the encounter dynamics; it is imported, attributed to Clausius, and applied as a long-run average condition.

## How the two pieces relate

The two assumptions are complementary halves of one scoping move:

- **Per-encounter side:** internal coupling is small enough per collision that the central-force, conservative-COM characterization carries the encounter integrals (the A₁, A₂ machinery in §2 and §3).
- **Many-encounter side:** those same small, unmodelled exchanges are postulated — following Clausius — to drive the mean translational : internal energy ratio to 1 : β−1.

The first lets the central-force analysis survive for β > 1 species; the second supplies the energetics the first deliberately ignores. The "intricate actions" of internal coupling appear nowhere in the equations; they are absorbed into these two averaging postulates and cited to Clausius for the apportionment side.
