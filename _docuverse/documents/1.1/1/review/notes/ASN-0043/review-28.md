# Review of ASN-0043

## REVISE

### Issue 1: `home` applied to content addresses in L9 proof

**ASN-0043, TypeGhostPermission (L9) witness construction**: "Choose a document prefix `d'` under which no address has been allocated — that is, no `b ∈ dom(Σ.C) ∪ dom(Σ.L)` has `home(b) = d'`"

**Problem**: `home(a)` is defined only for `a ∈ dom(Σ.L)`. For `b ∈ dom(Σ.C)`, the authoritative function is `origin(b)` (ASN-0036). The proof applies `home` to the union `dom(Σ.C) ∪ dom(Σ.L)`, which includes content addresses outside `home`'s declared domain. The underlying reasoning is sound — both functions use the same formula — but the notation is incorrect.

**Required**: Either (a) split the freshness condition: "no `b ∈ dom(Σ.C)` has `origin(b) = d'` and no `b ∈ dom(Σ.L)` has `home(b) = d'`", or (b) define a single document-prefix extraction function (e.g., `docprefix`) covering all element-level address tumblers and use it consistently in both this ASN and the L9 proof.

### Issue 2: T4 scope overclaim in two places

**ASN-0043, Home and Ownership section**: "T4 (HierarchicalParsing, ASN-0034) defines `fields` for all tumblers in `T` — the field structure is a property of the tumbler, not of what the tumbler addresses."

**ASN-0043, Definition — LinkHome**: "The domain extension is justified: `origin`'s formula relies only on `fields`, which T4 defines for all tumblers"

**Problem**: T4 constrains "every tumbler `t ∈ T` *used as an address*" — not all tumblers in T. T4's format constraints (no adjacent zeros, no leading/trailing zeros, positive non-separator components) exclude common non-address tumblers: displacements like `δ(n, m) = [0, ..., 0, n]` start with zero, and zero tumblers violate TA6. The ASN's actual reasoning is correct — it applies `fields` only to link addresses, which satisfy T4's format by L1 (`zeros(a) = 3`) — but the justification text claims `fields` is defined for "all tumblers in T," which overstates T4's scope.

**Required**: Both occurrences must be corrected. The justification should state: `fields` is well-defined for tumblers satisfying T4's format constraints (element-level address tumblers with `zeros = 3`). Link addresses satisfy these constraints by L1, so `fields` applies to them. Remove the "all tumblers in T" characterization.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as a general tumbler-space property
**Why out of scope**: PrefixSpanCoverage depends only on tumbler arithmetic (T1, TA-strict, OrdinalShift) — it has no dependency on links, endsets, or any store. It belongs in a tumbler algebra or span algebra ASN. This is an ASN factoring question, not an error; the proof is correct and self-contained here.

### Topic 2: Explicit finiteness axiom for `dom(Σ.L)`
**Why out of scope**: Neither ASN-0036 nor this ASN states explicit finiteness for `dom(Σ.C)` or `dom(Σ.L)`. The L9 proof's freshness argument implicitly relies on finite allocation history. This parallels ASN-0036's treatment and should be addressed at the foundation level, not in the link ontology.

### Topic 3: Link arrangement semantics
**Why out of scope**: The ASN correctly identifies that S3 (`M(d)(v) ∈ dom(Σ.C)`) prevents link addresses from appearing in arrangements, and that Gregory's implementation gives links V-positions in a dedicated subspace. The ASN defers this tension explicitly: "Accommodating this in the abstract model would require extending the arrangement semantics beyond S3." This belongs in a future ASN extending ASN-0036.

VERDICT: REVISE
