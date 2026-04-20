# Review of ASN-0043

## REVISE

### Issue 1: Incomplete justification for T4 format compliance of link addresses

**ASN-0043, Home and Ownership**: "Link addresses satisfy these constraints by L1 (`zeros(a) = 3`), so `fields` is well-defined for them."

**ASN-0043, Definition — LinkHome**: "`zeros(a) = 3` (L1), which guarantees both that all four fields are present and that T4's constraints are met."

**Problem**: `zeros(a) = 3` does not guarantee T4's format constraints. A tumbler can have exactly three zeros while violating T4 — e.g., `0.0.1.0.5` has three zeros but adjacent zeros and a leading zero. What guarantees the constraints is T4 itself: it is an axiom constraining all tumblers "used as an address." Link addresses are address tumblers (keys in `Σ.L`), so T4 applies to them directly. L1 provides the zero count, placing them at element level — but L1 is not the reason they satisfy the format constraints.

The earlier revision correctly removed the overclaim that `fields` works for "all tumblers in T." But the replacement attributes constraint compliance to L1 instead of to T4, collapsing two distinct roles: T4 guarantees the format, L1 establishes the level.

**Required**: State the chain: (1) link addresses are tumblers used as addresses (keys in `Σ.L`), so T4 constrains them to satisfy the format; (2) L1 establishes `zeros(a) = 3`, placing them at element level with all four fields present; (3) therefore `fields` is well-defined. Two passages need this fix: the "Home and Ownership" paragraph and the LinkHome definition's justification sentence.

## OUT_OF_SCOPE

### Topic 1: Non-transcludability provisional on current S3
L14 derives that links cannot appear in arrangements from S3 + L0. The L12 parenthetical acknowledges S3 may need extension to accommodate links in the arrangement layer. When arrangement semantics are extended, the non-transcludability derivation should be re-examined.
**Why out of scope**: POOM structure and V-stream mechanics are excluded by the scope section. The derivation is correct under current S3.

## RESOLVED

### [UNJUSTIFIED DOMAIN EXTENSION]: `home` applied to content addresses in L9 proof
**Justification**: The L9 witness construction now correctly uses `origin(b)` for `b ∈ dom(Σ.C)` and `home(b)` for `b ∈ dom(Σ.L)`: "no `b ∈ dom(Σ.C)` has `origin(b) = d'` and no `b ∈ dom(Σ.L)` has `home(b) = d'`." Each function is applied within its declared domain.

VERDICT: REVISE
