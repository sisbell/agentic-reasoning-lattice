## Question 3 [theory]

> What role do translational, rotational, and vibrational degrees of freedom play in storing thermal energy?

# Translational vs. Internal Energy Storage in Maxwell 1867

The corpus partitions molecular energy into two parts, not three. It distinguishes **translation of the centre of gravity** from **internal motion relative to the centre of gravity**, and it groups rotation and vibration together under "internal motion" rather than giving them separate roles.

## The two-part decomposition

> "The actual energy of a moving body consists of two parts, one due to the motion of its centre of gravity, and the other due to the motions of its parts relative to the centre of gravity. If the body is of invariable form, the motions of its parts relative to the centre of gravity consist entirely of rotation, but if the parts of the body are not rigidly connected, their motions may consist of oscillations of various kinds, as well as rotation of the whole body." [1867-maxwell-dynamical-theory-of-gases]

So rotation appears when the molecule is rigid; oscillations (vibrations) appear additionally when it is not rigid. The corpus treats both as contributors to the same internal bucket.

## The parameter β

Storage across the two buckets is governed by a single ratio:

> "the whole energy of the molecule may be represented by ½Mv²β, where β is the ratio of the total energy to the energy of translation. … The value of β can be determined if we know either of the specific heats of the gas, or the ratio between them." [1867-maxwell-dynamical-theory-of-gases]

For structureless molecules the internal bucket is empty:

> "If the molecules are pure centres of force, there can be no energy of rotation, and the whole energy is reduced to that of translation" [1867-maxwell-dynamical-theory-of-gases]

Following Clausius, the corpus assumes the internal-to-translational ratio relaxes to a fixed value (β − 1):

> "Ē = (β − 1)(ξ² + η² + ζ²)" [1867-maxwell-dynamical-theory-of-gases]

## Total heat in a volume

Summing the three contributions in equation (66):

> "The first term gives the energy due to the motion of translation of the medium in mass, the second that due to the agitation of the centres of gravity of the molecules, and the third that due to the internal motion of the parts of each molecule." [1867-maxwell-dynamical-theory-of-gases]

Only the second and third count as heat; the first is bulk motion. The total invisible agitation per unit volume is ½β(ξ² + η² + ζ²)ρ = (3/2)βp, called "the total heat in the unit of volume" [1867-maxwell-dynamical-theory-of-gases].

## Pressure depends only on translation

Pressure in the corpus is the transfer of translational momentum across a plane — ρξ̄², ρη̄², ρζ̄² — so internal motion does not enter the pressure directly. That is why, although heat-storage scales with β, the equation of state (eq. 102, p = ⅓(ρ/s)θV₀²) involves only the translational mean-square velocity. Internal motion enters thermodynamics through the specific heats:

> "γ = (2 + 3β)/(3β), whence β = (2/3)·1/(γ−1)" [1867-maxwell-dynamical-theory-of-gases]

So a larger β (more internal storage) raises both specific heats and lowers γ.

## What the corpus does *not* say

The corpus does **not** separate rotation from vibration quantitatively, nor does it assign each degree of freedom an equal share (no equipartition statement per degree of freedom is made in this paper). It lumps rotation and "oscillations of various kinds" into Ē and parameterises the lump with a single β fixed empirically via γ. Anything finer — counting rotational vs vibrational modes, or the high-temperature excitation of vibrations — reaches beyond what this corpus supports.
