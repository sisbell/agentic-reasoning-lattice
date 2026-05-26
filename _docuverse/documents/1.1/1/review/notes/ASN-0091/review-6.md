# Review of ASN-0091

## REVISE

### Issue 1: Copy-paste error in 4-cut worked example
**ASN-0091, "Worked Example — 4-cut Swap" / RE-frag verification**: The parenthetical concluding the 4-cut RE-frag verification reads "cardinality 3, since no two consecutive post-state I-addresses extend each other (a₂ + 1 ≠ b₁; b₁ + 1 ≠ a₁)". The symbol `b₁` does not appear in the 4-cut example's setup — it appears only in the 3-cut example, where it was defined as `[d.0.1.1]`. The 4-cut example's pre-state range is `{a₁, a₂, a₃, a₄, a_link}`, with no `b₁`.
**Problem**: The conditions cited are leftover from the 3-cut example and don't apply to the 4-cut setup. A reader trying to verify cardinality 3 from the cited justification will be unable to.
**Required**: Replace with conditions matching the 4-cut example, e.g., "a₃ + 1 = a₄ extends [1, 1] to [1, 2]; a₄ + 1 = a₁ + 4 ≠ a₂ = a₁ + 1; a₂ + 1 = a₃ ≠ a₁".

### Issue 2: Notational conflation in π non-uniqueness paragraph
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: The paragraph writes "any permutation π of dom(Σ.M(d)) that fixes the partition into pre-images `{π⁻¹(a) := {v : Σ.M(d)(v) = a}}_a`".
**Problem**: The notation `π⁻¹(a)` overloads π's inverse — π is a permutation of V-positions, so π⁻¹ maps V-positions to V-positions, not I-addresses to V-position sets. The set `{v : Σ.M(d)(v) = a}` is the pre-image of `a` under `Σ.M(d)`, not under π. The notation conflates two distinct functions.
**Required**: Use `Σ.M(d)⁻¹(a)` (or equivalent) for the pre-image of an I-address under the arrangement.

### Issue 3: Misleading bullet in "What Rearrangement Is Not"
**ASN-0091, "What Rearrangement Is Not"**: The list of negations includes "change the set of V-positions where any link projects onto d (RE-proj transports a set along π, preserving its cardinality and content-identity)".
**Problem**: This bullet contradicts RE-proj, which establishes `project(e, d, Σ') = π(project(e, d, Σ))`. The set DOES change (different members via π); only cardinality and the underlying I-addresses are preserved. As written, the bullet claims preservation of the set itself.
**Required**: Reword to be precise about what is preserved (cardinality, content-identity) versus what is NOT preserved (specific V-positions). For example: "change the cardinality or content-identity of the V-position set where any link projects onto d (the specific V-positions migrate via π, but the cardinality and underlying I-addresses are preserved)."

### Issue 4: Imprecise "unrelated to either" in coalescence witness
**ASN-0091, "Run Decomposition Is Not Invariant" / reverse witness**: The coalescence witness states "where a + 1 and a are consecutive content addresses (both produced by the same sub-allocator chain) but c is unrelated to either".
**Problem**: For the post-state to have exactly 2 maximal runs (as claimed), `c ≠ a + 2` must hold (else post-state [1, 1], [1, 2], [1, 3] forms a single 3-run with values a, a+1, a+2) and `c ≠ a - 1` (else pre-state [1, 2], [1, 3] forms a 2-run). The qualifier "unrelated to either" is imprecise; "unrelated" could plausibly admit `c = a + 2`.
**Required**: State exclusions explicitly, e.g., "c ∉ {a − 1, a, a + 1, a + 2}" or "c lies in a sub-allocator chain disjoint from the chain segment containing a".

### Issue 5: Coalescence direction not formally labeled
**ASN-0091, "Run Decomposition Is Not Invariant"**: RE-frag is labeled as the fragmentation direction (cardinality may strictly increase). The dual coalescence direction (cardinality may strictly decrease) is shown via the reverse witness but is not given a formal claim label.
**Problem**: The prose summarizes "Run-decomposition cardinality is neither monotone nor invariant under rearrangement", but the claims table includes only RE-frag. The "neither" requires both directions, and the asymmetric formalization leaves coalescence informally captured. A future ASN referencing this one would have no labeled handle for the coalescence direction.
**Required**: Either add a parallel claim RE-coal labeling the coalescence direction, or restate RE-frag as a non-monotonicity claim that captures both directions formally (e.g., "RE-frag: maximal-run-decomposition cardinality is neither monotonically increasing nor decreasing nor invariant under REARRANGE; both strict increase and strict decrease are realizable").

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN's open questions section explicitly notes this as future work. ASN-0084's CS3 currently fixes the cut subspace to s_C; a REARRANGE operation on the link subspace would belong in a separate ASN.

### Topic 2: Quantitative bounds on run-decomposition cardinality changes
**Why out of scope**: The ASN provides existence witnesses for both fragmentation and coalescence but no quantitative bounds. Open question 4 in the ASN itself notes this gap. Quantitative analysis is genuinely future work, not a defect of this ASN.

### Topic 3: Completeness of REARRANGE_K relative to abstract class
**Why out of scope**: The ASN's fifth open question asks whether every admissible bijection can be realized by a finite composition of cut-sequence rearrangements. This is genuine open territory about REARRANGE_K's expressive power.

### Topic 4: Behavior under split transcluded spans
**Why out of scope**: The ASN's first open question concerns the guarantees rearrangement must preserve when a cut splits a transcluded span. RE-trans + RE-frag jointly imply such splits can occur; specific semantic obligations are future work.

### Topic 5: Composition with non-REARRANGE operations
**Why out of scope**: The composition section sketches that ASN-0098's per-operation lemmas govern mixed sequences but does not formalize the composite. Full mixed-sequence semantics across the operation vocabulary belongs in a separate ASN.

VERDICT: REVISE
