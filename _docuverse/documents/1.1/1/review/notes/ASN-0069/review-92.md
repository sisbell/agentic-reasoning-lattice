# Review of ASN-0069

## REVISE

### Issue 1: V5 re-derives the frame-composition argument that V5a states in full generality
**ASN-0069, §"Frame: Source Isolation"**: V5's derivation — "The argument is by frame composition. K.δ's frame condition... K.μ⁺'s frame condition... K.ρ's frame condition... The composition: across the entire fork composite, `M(d_src)` is unchanged." — followed immediately by V5a: "Each arrangement-modifying transition carries the frame condition `(A d' : d' ≠ d_target : M'(d') = M(d'))`... Composing these per-transition frame conditions along the sequence... gives `M'(d*) = M(d*)`."

**Problem**: V5 is exactly the `(fork composite, d* = d_src)` instance of V5a, and its derivation is the same composition-of-per-transition-frames argument carried out at lower generality. This is the "two passages establish the same thing in different words" pattern. The document itself confirms the subsumption: §"Permanence Across Source and Fork" cites "(V5a, instantiated at `d* = d_new` and at `d* = d_src` respectively)" — using V5a where V5 would do, treating V5's separate derivation as redundant.

**Required**: State V5a first (or directly after V5's statement) and reduce V5 to a one-line corollary — "V5 is V5a at `d* = d_src`, since the fork composite has no step M-targeted at `d_src`." Drop the independent K.δ/K.μ⁺/K.ρ frame walk in V5.

### Issue 2: Empty-case vacuity bookkeeping is argued twice
**ASN-0069, §"The Empty-Source Case"**: "The single organising principle is quantifier domain: the structural properties — V1, V2, V3, and V12(a) — hold substantively... while *every* property whose universal quantifier ranges over `V_{s_C}(d_op)` or `V_{s_C}(d_src)` holds vacuously..."

**ASN-0069, §"Worked Example", "Empty source (V7)"**: "V9's universal quantifier... ranges over the empty set... and is satisfied vacuously; V12(c) and V12(d) likewise quantify over the empty range and hold vacuously. V12(a) — joint permanence... holds substantively..."

**Problem**: The worked example re-derives the substantive-vs-vacuous classification already established in §"The Empty-Source Case". A worked example's job is to instantiate the concrete result (empty fork: `d_new° = inc(d_src°, 1)`, `M'(d_new°) = ∅`, `R' = R`), not to re-run the vacuity argument property-by-property.

**Required**: In the worked example, show the concrete empty-fork outcome and cite §"The Empty-Source Case" for *why* the dependent properties degrade; do not re-enumerate which quantifiers collapse.

### Issue 3: Motivational bridge paragraph that does not advance the argument
**ASN-0069, §"Identity by Sub-Allocation"**: "An alternative implementation could fork by performing only K.δ and producing an empty new document. That would satisfy V1, V2, and the basic identity guarantees. What that implementation would *lack* is the inherited content that makes the fork meaningfully a *version of* something."

**Problem**: Unlike the POOM and V-space-layout remarks (which are tied to concrete implementation evidence and serve the abstract-vs-implementation distinction), this paragraph is a purely hypothetical bridge to the next section. It establishes nothing about the operation; it is editorial transition prose between §Identity and §"Sharing, Not Duplication".

**Required**: Delete, or replace with a single clause noting that K.δ alone yields the empty fork (already V7) and that §"Sharing, Not Duplication" derives the content-inheritance phase.

## OUT_OF_SCOPE

(none — V6a's link-discoverability inheritance is a legitimate fork consequence. The review checklist explicitly cites "wp for 'link discoverability is preserved'" as expected depth, and V6a confines itself to what the fork preserves rather than defining link operation mechanics. The `coverage`/`project`/`discoverable_from` primitives are local definitions used only to *state* the preservation, not a foundation reinvention; they are acceptable.)

VERDICT: REVISE
