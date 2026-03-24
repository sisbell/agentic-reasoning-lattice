I'll read the ASN content and foundation statements carefully, then audit for cross-boundary issues.

The ASN is long and detailed. Let me work through each audit category systematically.

### [UNJUSTIFIED DOMAIN EXTENSION]: `home` applied to content addresses in L9 proof

**Foundation**: `origin(a)` (ASN-0036) — defined on `dom(Σ.C)`: "For every `a ∈ dom(Σ.C)`, the *origin* is the document-level prefix obtained by truncating the element field: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`"

**ASN**: L9 (TypeGhostPermission) witness construction: "Choose a document prefix `d'` under which no address has been allocated — that is, no `b ∈ dom(Σ.C) ∪ dom(Σ.L)` has `home(b) = d'`"

**Issue**: `home(a)` is defined in this ASN only for `a ∈ dom(Σ.L)` ("For a link at address `a ∈ dom(Σ.L)`"). The L9 proof applies `home(b)` to `b ∈ dom(Σ.C) ∪ dom(Σ.L)`, which includes content addresses where `home` is not defined. For `b ∈ dom(Σ.C)`, the authoritative function is `origin(b)` from ASN-0036. The two functions use the same formula, so the proof's reasoning is sound, but `home` is used outside its declared domain.

**What needs resolving**: The L9 proof must use `origin(b)` for `b ∈ dom(Σ.C)` and `home(b)` for `b ∈ dom(Σ.L)`, or the ASN must define a unified document-prefix extraction function covering both domains and use that.

---

### [UNJUSTIFIED DOMAIN EXTENSION]: Overclaim on T4 scope

**Foundation**: T4 (HierarchicalParsing, ASN-0034) — "Every tumbler `t ∈ T` **used as an address** contains at most three zero-valued components..." and "The function `fields(t)` extracting node, user, document, and element fields is well-defined and computable from `t` alone."

**ASN**: Two places claim broader scope:
- Home and Ownership section: "T4 (HierarchicalParsing, ASN-0034) defines `fields` for **all tumblers in `T`** — the field structure is a property of the tumbler, not of what the tumbler addresses."
- Definition — LinkHome: "The domain extension is justified: `origin`'s formula relies only on `fields`, which T4 defines for **all tumblers**"

**Issue**: T4 constrains tumblers "used as an address" and defines `fields` in that context. The ASN claims `fields` is defined for "all tumblers in T," which would include non-address tumblers like displacements (e.g., `δ(n, m) = [0, ..., 0, n]`), which may not satisfy T4's structural constraints (no adjacent zeros, no leading/trailing zeros, positive non-separators). The ASN's derivations only apply `fields` to link addresses (which ARE address tumblers by L1), so no downstream result is affected — but the justification overstates T4's scope.

**What needs resolving**: The ASN's characterization of T4 should say `fields` is defined for tumblers satisfying T4's format constraints (equivalently, tumblers used as addresses), not for all tumblers in T. The justification for applying `fields` to link addresses should cite L1 (zeros = 3) as establishing that link addresses satisfy T4's format.
