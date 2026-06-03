# Review of ASN-0071

## REVISE

### Issue 1: "(S5)" mis-cites a foundation label that means something else

**ASN-0071, "We work within the strand model..."**: "Sharing is unrestricted: distinct `(d, v)` pairs may map to the same I-address (S5)."

**Problem**: There is no foundation claim S5 establishing arrangement sharing. In the foundation set, ASN-0053's S5 is **SplitWidthComposition** (`d ⊕ d' = ℓ`) — entirely unrelated. ASN-0047 has no S5. The property actually being cited (distinct V-positions referencing one I-address) is ASN-0058's **M13 (SharedContent)** / **M14 (IndependentOccurrences)**. A reader verifying the dependency is sent to the wrong claim.

**Required**: Cite ASN-0058 M13 (and M14 for independence), or restate the property; remove the colliding "(S5)" label.

### Issue 2: "(S7)" mis-cites a foundation label that means something else

**ASN-0071, "The query"** and **"Discovery through sharing"**: "Link addresses have unique home documents recoverable directly from the tumbler via `origin` (S7)" and "`origin(a₁) = d_A` (S7)".

**Problem**: ASN-0053's S7 is **CoveringExistence** (every finite position set has a covering span-set) — unrelated to `origin`. ASN-0047 defines no bare S7 (only S7a–S7d, none provided). The home-document property for links is ASN-0047 **L1a (LinkScopedAllocation)** (`origin(a) ∈ E_doc` for link addresses); `origin` for content is grounded by P6. The "(S7)" citations point at the wrong claim throughout.

**Required**: Replace "(S7)" with the correct foundation claim (L1a / P6 / the `origin` definition).

### Issue 3: "J1" is not a defined coupling constraint

**ASN-0071, "A worked scenario," step 7**: "The composite (steps 5–7) discharges J1's coupling constraint."

**Problem**: ValidComposite names J0, **J1★**, and **J1'★**. There is no bare "J1". The constraint actually discharged (new content-subspace range entry `a₁` in `M(d_B)` forces `(a₁, d_B) ∈ R`) is J1★.

**Required**: Cite J1★ (and note J1'★ for the converse if intended).

### Issue 4: K.μ~ listed among elementary transitions in the finiteness argument

**ASN-0071, "Finiteness," step (b)**: "the others (K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ) leave `E` unchanged by their frame clauses."

**Problem**: The argument is "each *elementary* transition adds at most one entity," but K.μ~ is explicitly a **named composite, not atomic** (per ValidCompositeAmended: "The named composite K.μ~ is not atomic"). Enumerating it alongside elementary transitions and invoking "their frame clauses" is a category error. Benign for the conclusion (its K.μ⁻+K.μ⁺ decomposition also fixes `E`), but the structure of the induction over elementary steps should not list a composite.

**Required**: Drop K.μ~ from the elementary-transition enumeration (it is covered by K.μ⁻ and K.μ⁺), or state separately that composites decompose into the listed elementary steps.

## OUT_OF_SCOPE

### Topic 1: Relationship between `find` and the historical relation `R`
The Open Questions correctly defer the `find`-vs-`R` semantic gap, transition-contraction invariants, distributed-replica completeness, and visibility filtering. These belong in separate ASNs; no flag.

VERDICT: REVISE
