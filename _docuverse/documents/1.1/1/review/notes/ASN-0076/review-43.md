# Review of ASN-0076

## REVISE

### Issue 1: The subspace-disjointness freshness argument is restated verbatim within E0

**ASN-0076, E0 (successor step, sub-cases (a) and (b))**: Sub-case (a) reads "For `ℓ_new ∉ dom(Σ.C)`, we use the same subspace argument as sub-case (b): by AllocatorHierarchy `subspace_I(ℓ_new) = s_L`, by L0 (ASN-0047) every `a ∈ dom(Σ.C)` satisfies `subspace_I(a) = s_C`, and by SC-NEQ (ASN-0047) `s_C ≠ s_L`; hence `ℓ_new ∉ dom(Σ.C)`." Sub-case (b) then states the identical chain again: "By AllocatorHierarchy ... `subspace_I(ℓ_new) = s_L`; by L0 ... `subspace_I(a) = s_C`; by SC-NEQ ... `s_C ≠ s_L`; hence `ℓ_new ∉ dom(Σ.C)`."

**Problem**: The `dom(C)`-freshness argument is identical across both emission sub-cases — only the `dom(L)`-freshness part differs (empty-set condition vs. L11a). Sub-case (a) both states the argument inline *and* forward-references sub-case (b) for "the same argument," which is then restated in full. The reader re-parses the same three-citation chain. This is the forward-reference/duplication accretion the anti-bloat classifier targets.

**Required**: Factor the `ℓ_new ∉ dom(C)` step out once ("In both sub-cases, the subspace argument — `subspace_I = s_L` (AllocatorHierarchy), content addresses carry `s_C` (L0), `s_C ≠ s_L` (SC-NEQ) — gives `ℓ_new ∉ dom(C)`"), and let each sub-case supply only its distinct `dom(L)`-freshness reasoning. Remove the self-referential "same argument as sub-case (b)" pointer.

### Issue 2: Defensive re-explanation of coverage being state-independent

**ASN-0076, The Composite**: "the full prefix-closure of `ℓ_old` in `T`, an infinite set of tumblers fixed combinatorially and independent of what is allocated (coverage consults no state component; Definition — Coverage, ASN-0098)." **E7**: "(coverage is combinatorial; Definition — Coverage, ASN-0098)."

**Problem**: That coverage is a combinatorial, state-independent function is already fixed by Definition — Coverage (ASN-0098, a foundation). Re-explaining it twice in parentheticals is a defensive justification of a settled foundation fact. The construction uses only `ℓ_old ∈ coverage(E_from)` (reflexivity of `≼`); the "infinite set of tumblers fixed combinatorially and independent of what is allocated" elaboration does not advance the argument.

**Required**: State `coverage(E_from) = {t : ℓ_old ≼ t}` (citing L13/PrefixSpanCoverage) and the single fact actually used (`ℓ_old ∈ coverage(E_from)`). Drop the "infinite set ... independent of what is allocated" essay clause and the duplicated "coverage consults no state component / is combinatorial" parentheticals.

## OUT_OF_SCOPE

### Topic 1: Supersession-type recognition convention and successor-resolution policy
**Why out of scope**: Which span designates the authoritative successor, whether `τ_sup` is recognizable to a conforming reader, and how readers compute "current" successors are reader/application-layer policy questions. The ASN correctly defers these to Open Questions; they are new territory, not defects here.

VERDICT: REVISE
