# Review of ASN-0036

The proofs here are largely careful and honest — the S8 decomposition openly scopes itself to the singleton witness, the within-subspace incompatibility lemma covers both `j < m` and `j = m`, and D-CTG-depth/D-SEQ are derived in genuine steps. My findings are concentrated in the accretion patterns this note's `review-mode.anti-bloat` classifier asks me to surface, plus one internal inconsistency between the S8 deferral language and the worked example.

## REVISE

### Issue 1: S8's conjunct-(b) scoping disclaimer is stated twice
**ASN-0036, Span decomposition (intro prose and S8 postconditions)**: The intro says "the witness exhibited here is the singleton decomposition … (b) holds only at its base case … and is never exercised for nⱼ > 1. The existence of any maximal run with nⱼ > 1 is not established here; see Open Questions." The postconditions then repeat: "No run with nⱼ > 1 is established here, so (b)'s k > 0 content is not exercised; the existence and uniqueness of maximal runs is deferred to Open Questions."
**Problem**: Two paragraphs in the same section say the same thing in different words, and both defer to the same downstream location (Open Questions). This is the accretion pattern of duplicated deferral.
**Required**: State the singleton-only scope once — in the postconditions, where it constrains the claim — and delete the duplicate from the intro prose.

### Issue 2: Worked example asserts maximal runs the theorem deliberately does not establish
**ASN-0036, Worked example (Σ₁, Σ₂ checks)**: "*Check S8*: the arrangement admits a single maximal correspondence run (v₁,a₁,n₁) = (1.1, 1.0.1.0.1.0.1.1, 5)" and "*Check S8*: M(d₂) decomposes into two correspondence runs … (1.1, …, 3) … (1.4, …, 2)."
**Problem**: S8's established content is the singleton decomposition; the ASN says twice that runs with nⱼ > 1 are "not established here." Labeling the example's nⱼ = 5, 3, 2 runs as "Check S8" conflates a concrete by-hand computation with the theorem's deferred content, and a careful reader hits the tension between "not established" and the confident exhibition of length-5 runs.
**Required**: Reword so the example reads as a concrete instance verifying conjunct (b) by direct computation (which is legitimate and valuable), explicitly distinguished from the singleton existence claim S8 actually proves — not as "Check S8."

### Issue 3: subspace_I notation carries a defensive non-obligation clause
**ASN-0036, after S7c**: "We write subspace_I(a) = E(a)₁ … This is a notational convenience used in motivation and examples; it carries no proof obligation of its own (its well-definedness and positivity follow directly from S7b and S7c)."
**Problem**: The clause explains *why the notation is safe to ignore* rather than advancing its meaning — meta-prose around a definition. The "what" (subspace_I = E(a)₁) is the only load-bearing content.
**Required**: Keep the definition; drop the "carries no proof obligation" justification.

## OUT_OF_SCOPE

### Topic 1: Existence/uniqueness of maximal correspondence runs
**Why out of scope**: Already correctly deferred in Open Questions; the singleton decomposition is sufficient content for this ASN. No action needed beyond Issues 1–2.

### Topic 2: Operation preservation of D-CTG, D-MIN, S2 under INSERT/DELETE/COPY/REARRANGE
**Why out of scope**: Operation frame/postconditions are explicitly excluded by the Scope section and tracked in Open Questions. The base-case verification (empty arrangement) is the right amount of operation-touching for a state/invariant ASN.

VERDICT: REVISE
