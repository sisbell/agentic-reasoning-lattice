# Review of ASN-0043

## REVISE

### Issue 1: L13 coverage characterization is weaker than what holds
**ASN-0043, Reflexive Addressing**: "The coverage therefore includes b and all extensions of b — tumblers for which b is a proper prefix."
**Problem**: The word "includes" understates the result. The coverage of `(b, ℓ_b)` is not merely a superset of `{t : b ≼ t}` — it *equals* `{t : b ≼ t}`. No tumbler outside this set can fall in the range `[b, inc(b, 0))`:

- Same depth (`#t = #b`): any `t ≠ b` with `t > b` must differ from `b` at some `k ≤ #b`. Since `inc(b, 0)` agrees with `b` at all positions before `#b`, we get `t_k > b_k = inc(b,0)_k` for `k < #b`, giving `t > inc(b, 0)`. At `k = #b`, `t_{#b} > b_{#b}` forces `t_{#b} ≥ b_{#b} + 1 = inc(b,0)_{#b}`, so again `t ≥ inc(b, 0)`. Only `b` itself survives.
- Greater depth (`#t > #b`): if `t` does not extend `b`, some `k ≤ #b` has `t_k > b_k = inc(b,0)_k`, giving `t > inc(b, 0)`. Only extensions remain.
- Shorter depth (`#t < #b`): agreement at positions `1..#t` makes `t` a prefix of `b`, so `t < b` by T1(ii). Excluded.

This precision matters: it confirms the canonical span contains *exactly* the target entity and its extensions, with no extraneous tumblers. The ASN should state `coverage({(b, ℓ_b)}) = {t ∈ T : b ≼ t}` and sketch the argument.

**Required**: Replace "includes b and all extensions" with "equals {t : b ≼ t}" and add a brief case analysis (same depth / greater depth / shorter depth) showing no non-extension tumbler can fall in the range.

### Issue 2: Worked example omits L13 verification
**ASN-0043, Worked Example**: The verification section checks L0, L1, L1a, L3–L6, L9–L12, L14, and S3 — but not L13 (ReflexiveAddressing).
**Problem**: L13 is the ASN's most structurally distinctive claim: links can point to other links. The example already extends itself for L11 (adding `a'` to demonstrate non-vacuous identity separation), so the precedent for extending exists. A meta-link demonstrating L13 would exercise the reflexive addressing mechanism concretely: construct a second link `a₂` whose from-endset contains the span `(a, ℓ_a)` targeting the first link, verify T12 well-formedness of that span, and confirm L0 (both in the link subspace) and L4 (cross-subspace reference from `s_L` to `s_L`).
**Required**: Extend the worked example with a concrete link-to-link connection — a second link address, a span referencing the first link, and verification of T12 + L0 + L4 + L13 for that configuration.

### Issue 3: Worked example asserts transition-dependent properties without justification
**ASN-0043, Worked Example**: "L12 (LinkImmutability). In any successor state Σ', a ∈ dom(Σ'.L) and Σ'.L(a) = (F, G, Θ). ✓"
**Problem**: L12 constrains state *transitions*, not individual states. A single-state example cannot verify it — there is no successor state Σ' to check against. The ✓ mark gives false confidence. The same issue would apply to S0 if it were checked. By contrast, static properties like L0 and S3 are correctly verified: they are predicates on a single state and can be evaluated directly.
**Required**: Either (a) construct a concrete state transition (e.g., adding a second link) and verify that L12 holds across that transition, or (b) explicitly note that L12 and L12a are transition invariants that are vacuously satisfied in a single-state example because no transition is under consideration. Do not mark them ✓ without one of these treatments.

### Issue 4: Property table omits type classification
**ASN-0043, Properties Introduced**: Each property has Label, Statement, and "Status: introduced" — but no type classification (INV/LEMMA/PRE/POST).
**Problem**: The foundation ASNs classify every property by type: T1 is `(INV, predicate)`, TA0 is `(PRE, requires)`, S1 is `(LEMMA, lemma)`, etc. This classification matters: an INV must hold in all reachable states and must be preserved by every operation; a LEMMA is derived and need not be independently verified; a PRE constrains callers. Without types, a downstream consumer cannot distinguish L0 (an invariant that every operation must preserve) from L9 (an existence lemma that is proved once) from L7 (a meta-property about what the specification does not constrain).

Suggested classification:
- **INV**: L0, L1, L1a, L3, L4, L5, L8, L11, L12, L14
- **LEMMA**: L2, L6, L9, L10, L12a, L13
- **META** (or omit from the formal property set): L7

**Required**: Add a Type column to the properties table with INV/LEMMA classification for each property, consistent with the foundation ASN convention.

## OUT_OF_SCOPE

### Topic 1: Link survivability analysis under content editing operations
**Why out of scope**: How links survive INSERT, DELETE, COPY, and REARRANGE operations on the content they reference — whether endset spans fragment, whether coverage shifts, whether discovery is affected — requires defining those operations and their effects on `Σ.L`. The ASN's scope explicitly excludes operations. This is the domain of a future operations ASN that can build on the ontological foundation established here.

### Topic 2: Well-formedness constraints on compound link structures
**Why out of scope**: L13 establishes that links can point to other links, and the ASN correctly notes that "arbitrary compound links" can be composed. Whether compound structures must satisfy additional constraints (acyclicity, reachability, depth bounds) is a question about the design patterns built atop the link primitive, not about the primitive itself. The ASN acknowledges this in its open questions.

VERDICT: REVISE
