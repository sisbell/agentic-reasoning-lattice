# Review of ASN-0070

This is a meticulous ASN. The inverse-image core (F0), the per-subspace partition, the canonical-form theorem (F-canonical) with its acyclicity and consecutivity arguments, the contiguity claim, and five worked configurations are all developed with care. The mathematical core holds up under scrutiny. The findings below are citation/justification precision issues, not gaps in the central argument.

## REVISE

### Issue 1: F-multi's structural-admissibility cites S5 for a reachability claim S5 does not make
**ASN-0070, F-multi (Derivation, "Structural admissibility" paragraph)**: "What ensures the hypothesis is not vacuously satisfied is S5 (UnrestrictedSharing, ASN-0036): for any `N ∈ ℕ`, there exists a **reachable state** in which some `a ∈ dom(C)` has more than `N` distinct V-positions of a single document mapping to it."

**Problem**: S5's actual postcondition (foundation) asserts the existence of *the initial state of a model of S0–S3* with that multiplicity — a model-existence claim. It does **not** assert reachability from `Σ₀` in ASN-0047's transition system. The paraphrase silently upgrades "there exists a model state" to "there exists a reachable state," which is exactly the kind of step the rest of this ASN is otherwise careful to discharge. The underlying claim happens to be true (K.μ⁺ imposes no injectivity on the content subspace — unlike CL-UNIQ for links — so two K.μ⁺ steps can map `v₁ → a` and `v₂ → a` from `Σ₀`), but that reachability is established by K.μ⁺'s non-injectivity, not by S5.

**Required**: Either weaken the claim to match S5's scope ("there exists a model of S0–S3 exhibiting within-document multiplicity"), or replace the S5 citation with the actual reachability justification (absence of a content-side injectivity constraint on K.μ⁺ in ASN-0047), and reserve S5 for the abstract-cardinality point it genuinely establishes.

### Issue 2: Inconsistent citation name for the home-document definition
**ASN-0070, Origin Symmetry**: "This projection is named `origin(a)` for content addresses (S7 of ASN-0036) and `home(a)` for link addresses (Definition **LinkHome** of ASN-0043)".
**ASN-0070, F-origin (Depends/Postcondition)**: "`home(M(d)(v))` for link addresses (Definition **Home**, ASN-0043)".

**Problem**: The foundation ASN-0043 defines this as `home(a) — Home`. The ASN cites it under two different names ("LinkHome" and "Home") for the same definition; "LinkHome" does not name any foundation definition. F-persist similarly leans on these projections.

**Required**: Use the foundation's name ("Home") consistently at every citation site.

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting, concurrency semantics, transclusion-lineage relationships, citation/archival contracts
**Why out of scope**: These are the ASN's own Open Questions and concern downstream system-level contracts (how unreached coverage is surfaced, concurrency guarantees, cross-document resolution relationships under shared lineage, representational-compactness mandates). They are new territory for future ASNs, correctly left open here rather than errors in this note. The ASN's decision to fix only V-restricted denotation (not representation) in the postcondition, while offering canonical form as a derived projection, is a defensible scoping choice and not a gap.

VERDICT: REVISE
