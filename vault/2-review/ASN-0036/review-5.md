# Review of ASN-0036

## REVISE

### Issue 1: S8 partition uniqueness depends on S8-depth but this dependency is unstated

**ASN-0036, Span decomposition / Properties table**: "The singleton runs partition dom(M(d)) — each position falls in exactly one run" and "S8 … theorem from S8-fin, S2"

**Problem**: The existence proof asserts uniqueness of the singleton partition without verification. The interval-based partition property `(E! j :: vⱼ ≤ v < vⱼ + nⱼ)` requires that no two singletons' intervals overlap within dom(M(d)). Without S8-depth this fails: if dom(M(d)) contains both `s.3` (depth 2) and `s.3.1` (depth 3) in the same subspace, then `s.3.1` falls in both its own interval `[s.3.1, s.3.2)` and in the interval `[s.3, s.4)` of the singleton for `s.3` — since `s.3 < s.3.1 < s.4` by T1 prefix extension. S8-depth prevents this by confining all V-positions in a subspace to uniform depth, ensuring no dom(M(d)) members exist between consecutive same-depth ordinals `s.x` and `s.(x+1)`.

The prose gestures at the dependency ("S8-depth allows us to define 'consecutive V-positions' precisely") but neither the existence proof nor the properties table acknowledges S8-depth as a formal prerequisite.

**Required**: (a) The existence proof must show the uniqueness step: with S8-depth, distinct same-depth ordinals produce non-overlapping unit intervals, so no `v ∈ dom(M(d))` falls in two singletons' intervals. Two cases suffice — same subspace (ordinal separation) and different subspace (first-component separation). (b) The properties table must list S8 as "theorem from S8-fin, S2, S8-depth."

### Issue 2: S7 omits GlobalUniqueness from stated dependencies

**ASN-0036, Properties table**: "S7 … from S7a, S7b, T4 (ASN-0034)"

**Problem**: S7 claims origin(a) "uniquely identifies the allocating document across the system (by GlobalUniqueness, ASN-0034)." The uniqueness of origin — that distinct documents produce distinct document-level prefixes — depends on GlobalUniqueness. S7a + S7b + T4 ensure origin is well-defined and correctly extracts the document prefix, but they do not establish that distinct documents have distinct prefixes. Without GlobalUniqueness, two different documents could (hypothetically) share a tumbler prefix. The properties table omits this dependency.

**Required**: List S7 as "from S7a, S7b, T4, GlobalUniqueness (ASN-0034)."

## OUT_OF_SCOPE

### Topic 1: Set of documents as state component

The state model uses Σ.M(d) for "document d" but does not formally define the set of documents D as a state component. A future ASN covering document lifecycle should define D, its membership invariants, and its relationship to the tumbler hierarchy.

**Why out of scope**: Document creation and lifecycle is explicitly listed as out of scope.

### Topic 2: Unique maximal run decomposition

The ASN proves existence of a finite decomposition but does not address uniqueness of the coarsest (fewest runs) decomposition. A proof that greedily merging adjacent compatible runs yields a unique maximal partition would strengthen S8.

**Why out of scope**: This is a structural theorem about the decomposition lattice, not a correctness issue in the current invariants. The ASN properly identifies it as an open question.

VERDICT: REVISE
