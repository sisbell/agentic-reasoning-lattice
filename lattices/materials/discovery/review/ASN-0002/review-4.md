# Review of ASN-0002

## REVISE

### Issue 1: "Centres-of-force modeling of encounters" is used before it is defined
**ASN-0002, §"Temperature as a functional of mean translational vis viva"**: "In the equilibrium regime, in the dilute regime, and under the centres-of-force modeling of encounters, the temperature of a body is a strictly monotone function of B.T̄ alone..."
**Problem**: The phrase "centres-of-force modeling of encounters" is load-bearing in three postulates (P.temp_functional, P.temp_functional_species_independent, P.sub_body_temperature) but is not defined at first use. Its formal content is only pinned down by premise (iv) in §"Conservation through encounters," many pages later. Further, the adjacent phrase "centre of force" was earlier introduced in §"The constitutional commitment" as a type of *molecular internal constitution* ("a centre of force endowed with inertia"), which is a different notion from the *encounter modeling commitment* that (iv) later supplies. The reader cannot distinguish the two senses without reading forward.
**Required**: Either (a) give a one-line operational definition of "centres-of-force modeling of encounters" at its first use (or make the forward reference explicit: "in the sense made precise by premise (iv) of §Conservation through encounters"), or (b) restructure so the encounter premises (i)–(iv) are introduced before any postulate that relies on them. Whichever route, disambiguate the modeling phrase from the constitutional phrase.

### Issue 2: P.enc_ratio_equilibration's stated content is tautological under β's definition
**ASN-0002, §"Conservation through encounters"**: "**[P.enc_ratio_equilibration]** In the equilibrium regime the mean ratio of internal to translational vis viva per molecule of a species is (β − 1), maintained as a steady state."
**Problem**: β_k is *defined* in §"The internal compartment and the ratio β" via
  (Σ_{m ∈ species_k} T(m) + m.eint) = β_k · (Σ_{m ∈ species_k} T(m)),
which immediately gives (Σ eint)/(Σ T) = β_k − 1 as an algebraic identity for any body. The statement "the mean ratio is (β − 1)" therefore adds no content unless it is understood as a claim about (i) species-invariance of the equilibrium β (which is what P.beta_species_invariant already asserts) and/or (ii) the dynamical fact that encounters drive the ratio to, and maintain it at, that value. The commentary ("maintained as a steady state," "many-encounter drift toward the species-characteristic ratio") gestures at reading (ii), but the labeled claim itself does not isolate it. The result is that the central β > 1 postulate that distinguishes "following Clausius" from definitional bookkeeping is not cleanly stated.
**Required**: Restate P.enc_ratio_equilibration in terms of what it actually commits to beyond β's definition and P.beta_species_invariant — namely, a dynamical commitment that encounters at the molecule level drive the per-molecule internal/translational ratio to the species-characteristic equilibrium value, and maintain it there. Make explicit that for β = 1 the claim is discharged by the encounter apparatus (no mechanism for T ↔ eint exchange is needed), and that for β > 1 the claim is an *added* postulate at the molecule-level dynamics layer because (iv) does not supply the required exchange mechanism.

META: (none — the ASN is on track; remaining items are clarity and crisp statement, not drift.)

VERDICT: REVISE
