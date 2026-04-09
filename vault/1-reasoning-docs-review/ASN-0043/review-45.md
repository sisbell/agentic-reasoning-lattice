# Review of ASN-0043

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as a span-algebra property
PrefixSpanCoverage is a general fact about tumbler spans — it characterizes the coverage of a unit-depth span at any tumbler as exactly the prefix-extension set. It is correctly proven here and used in L9, L10, and L13, but it has no link-specific content. A future span algebra ASN would be its natural home, cited by this ASN rather than proved inline.
**Why out of scope**: general tumbler/span property, not a link ontology question.

### Topic 2: Well-formedness of compound link structures
L13 permits link-to-link references, enabling arbitrary relational graphs (chains, trees, DAGs, cycles). No well-formedness constraint governs these structures — the ASN acknowledged this in its open questions. Whether acyclicity, reachability, or bounded depth should be required (or merely conventional) is a question for a future compound-structure ASN.
**Why out of scope**: requires defining traversal semantics over link graphs, which is operational territory.

## Analysis

The ASN is rigorous throughout. Every property is either an axiom with consistency witnessed by the worked example, or a lemma with a fully expanded proof. Specific observations:

**L9 (TypeGhostPermission).** The witness construction is the strongest proof in the ASN. It chooses a third subspace `s_X ∉ {s_C, s_L}` (guaranteed by T0(a)), making the ghost address unconditionally outside `dom(Σ.C) ∪ dom(Σ.L)` via T7 alone — no cardinality argument needed for the ghost, only for the fresh link address. All 16 invariant checks are explicit. The L1c verification correctly distinguishes the "existing allocations" case (next sibling via `inc(·, 0)`) from the "first link address" case (child-spawning sequence from the document prefix).

**PrefixSpanCoverage.** The exclusion direction handles all three depth cases — same depth, greater depth, shorter depth — with explicit T1 case analysis at each divergence point. The shorter-depth case correctly observes that a shorter tumbler either prefixes `x` (contradicting `t ≥ x` by T1(ii)) or diverges before position `#x` (placing it above `shift(x, 1)`). No case is elided.

**L11b (NonInjectivity).** The proof correctly constructs a conforming extension with a duplicate link value at a fresh address. The finiteness/infinitude argument (L-fin vs T0(a)) guarantees unoccupied addresses exist. All invariant checks are present, including L14a (via S3 and unchanged arrangements) and L1c (next sibling output of the allocator).

**Worked example.** The three-state sequence (Σ → Σ₁ → Σ₂) non-vacuously verifies L12 and L12a across two transitions, L11b via the duplicate link at `a'`, and L13 via the meta-link at `a₂`. The L1c allocation sequence is fully expanded as a three-step T10a chain with TA5a bounds checked at each step.

**Consistency.** The initial state satisfies all axioms simultaneously — verified explicitly for each of L0–L14, L-fin, L14a, and S0–S3. The extensions preserve all invariants. No circular dependencies exist among the introduced properties.

**Foundation usage.** All references are to ASN-0034 (Tumbler Algebra) or ASN-0036 (Streams), both listed as verified foundations. No cross-ASN references to non-foundation ASNs. The ASN uses foundation definitions (T4, T7, T10a, T12, OrdinalShift, GlobalUniqueness, S0–S3, S7b) without reinventing notation.

**L0 content-store constraint.** L0's second conjunct — `(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)` — is a new constraint on the content store not present in ASN-0036. This is legitimate: ASN-0036 had no need to fix a subspace identifier when only one entity type existed. The constraint is consistent with ASN-0036's existing invariants and necessary for the T7-based disjointness derivation.

VERDICT: CONVERGED
