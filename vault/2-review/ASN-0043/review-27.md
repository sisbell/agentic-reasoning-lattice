## Consistency Check — ASN-0043 (Link Ontology)

### 1. Stale Labels

(none)

All foundation citations — T4, T7, T9, T10, T10a, TA5, T3, T2, T12, T5, T6, T0(a), T1, T3; S0–S7, S7a, S7b — match current labels in ASN-0034 and ASN-0036.

---

### 2. Local Redefinitions

(none)

No property registered as `introduced` duplicates a foundation property at the same scope and domain.

---

### 2a. Unjustified Domain Extensions

**Finding 1 — `home(a)` reuses the `origin` formula outside its stated domain.**

ASN-0036 defines `origin` with explicit domain restriction:

> "For every `a ∈ dom(Σ.C)`, the origin is the document-level prefix obtained by truncating the element field: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`"

ASN-0043 introduces `home(a)` applying the identical formula to `dom(Σ.L)`:

> "This is the same formula as `origin` (ASN-0036), applied here to link addresses rather than content addresses."

`dom(Σ.L)` is outside `origin`'s stated domain. The body provides justification (T4 defines `fields` for all tumblers; L1 establishes `zeros(a) = 3`), but this is a category 2a finding regardless.

---

**Finding 2 — `GlobalUniqueness` extends S4 beyond its stated domain without citing the extension explicitly in the registry.**

S4 (OriginBasedIdentity, ASN-0036) is stated for I-addresses:

> "For I-addresses `a₁`, `a₂` produced by distinct allocation events: `a₁ ≠ a₂`"

`GlobalUniqueness` applies the same claim — distinct allocation events produce distinct addresses — to all element-level tumblers, including link-subspace addresses. The body argues the underlying axioms (T9, T10, T10a) carry no subspace restriction, but S4 itself is explicitly scoped to I-addresses. This is a domain extension of a foundation property, which is a category 2a finding.

---

### 2b. Incomplete Precondition Transfer

(none)

Both extensions are checked:

- **`home` / link analog of S7**: S7's "Follows from" list is S7a, S7b, T4, T9, T10, T10a, TA5, T3. The ASN supplies L1a (replacing S7a), L1 (replacing S7b), and explicitly cites T4, T9, T10, T10a + TA5(d) + T3. All prerequisites accounted for.
- **`GlobalUniqueness` / S4 extension**: S4's "Follows from" list is T9, T10, T10a + TA5(d) + T3. The ASN addresses each — arguing each carries no subspace restriction — and applies the same three-case structure. All prerequisites accounted for.

---

### 3. Structural Drift

(none)

Foundation definitions are restated accurately where cited. The `Link` definition (sequence of N ≥ 2 endsets) is introduced consistently with the intended design. Citations of S3, T12, OrdinalDisplacement, and OrdinalShift match the foundation text.

---

### 4. Missing Dependencies

(none)

All cited properties come from ASN-0034 or ASN-0036, both declared in the depends list.

---

### 5. Exhaustiveness Gaps

(none)

The L9 witness verification accounts for all invariants: L0–L6, L11a, L12, L12a, L14, S0–S3 are checked directly; L7 (META), L8 (DEF), L10 (LEMMA), L13 (LEMMA) are addressed inline or in the extension steps. The PrefixSpanCoverage proof is exhaustive across depth cases (same, greater, shorter than #x).

---

### 6. Registry Mismatches

(none)

All `introduced` entries are consistent with local proofs or justifications. No property is listed as `cited` with a local proof, or `introduced` while actually restating a foundation statement verbatim.

---

`RESULT: 2 FINDINGS`
