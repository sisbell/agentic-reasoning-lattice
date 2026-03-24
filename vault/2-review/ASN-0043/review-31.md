## Foundation Consistency Check: ASN-0043

### 1. Stale Labels

All labels checked against ASN-0034 and ASN-0036 foundations:

- T4, T5, T6, T7, T9, T10, T10a, T12, T2, T3, T0(a), TA0, TA5 (ASN-0034) — all present ✓
- S0, S1, S3, S4, S5, S7, S7a, S7b (ASN-0036) — all present ✓
- OrdinalDisplacement, OrdinalShift (ASN-0034) — both present ✓

(none)

---

### 2. Local Redefinitions

All 25 `introduced` properties checked. No property in the table is already present in ASN-0034 or ASN-0036 foundations. The `home` function reuses the `origin` formula but under a new name and a new domain (`dom(Σ.L)` vs `dom(Σ.C)`); the ASN correctly registers it as `introduced`.

(none)

---

### 2a. Unjustified Domain Extensions

Two extensions examined:

**`home(a)` extending `origin`:** `origin` is defined on `dom(Σ.C)` in ASN-0036. `home` applies the same formula to `dom(Σ.L)`. The ASN justifies this via T4 ("every tumbler t ∈ T *used as an address*" — link addresses are keys in Σ.L, hence tumblers used as addresses) and L1 (zeros(a) = 3, placing link addresses at element level with all four fields). The justification is complete: T4's quantifier applies uniformly to any system address regardless of which store it keys.

**GlobalUniqueness extending S4:** S4 covers I-addresses (content store); GlobalUniqueness claims all element-level tumblers are distinct across allocation events. The extension is justified: T9, T10, T10a carry no subspace restriction in their quantifiers, as the ASN explicitly argues.

(none)

---

### 2b. Incomplete Precondition Transfer

S7's Follows-from list: S7a, S7b, T4, T9, T10, T10a, TA5, T3.

The ASN's link analog substitutes L1a for S7a and L1 for S7b, and invokes T9, T10, T10a + TA5(d) + T3 for the three uniqueness cases. T4 is invoked in the preceding sentence in the same paragraph ("By L1 and T4… the prefix is recoverable from the address alone"). All prerequisites are accounted for.

S4's Follows-from list: T9, T10, T10a + TA5(d) + T3. GlobalUniqueness accounts for all three.

(none)

---

### 3. Structural Drift

- **Span/T12**: ASN uses "ℓ > 0 and the action point k of ℓ satisfies k ≤ #s" — matches T12 exactly ✓
- **Link definition**: "finite sequence of N ≥ 2 endsets" — consistent with L3 and the definitions block ✓
- **OrdinalDisplacement/OrdinalShift**: δ(1, #x) and shift(v, n) usage matches ASN-0034 definitions exactly ✓
- **T7 application**: ASN uses "a.E₁ ≠ b.E₁ ⟹ a ≠ b" correctly ✓
- **S3 citation**: ASN describes it as "M(d)(v) ∈ dom(Σ.C)" — matches ASN-0036 exactly ✓

(none)

---

### 4. Missing Dependencies

All citations checked. Every property cited originates in either ASN-0034 or ASN-0036. No property from any other ASN (e.g., ASN-0035, ASN-0058) is cited.

(none)

---

### 5. Exhaustiveness Gaps

- **L14 "no state component" claim**: State components are Σ.C (ASN-0036), Σ.M (ASN-0036), Σ.L (ASN-0043). No additional state component appears in either foundation. ✓
- **L12 "no modify operations"**: The five FEBE operations cited are the complete set defined in the Nelson protocol. The foundation ASNs define no additional operations. ✓
- **Comparison table subspace partitioning**: L0 covers dom(Σ.C) and dom(Σ.L). No third store domain exists in the foundations. ✓

(none)

---

### 6. Registry Mismatches

All `introduced` entries checked against body content:

- Properties with body proofs (L9, PrefixSpanCoverage, L11b) are correctly `introduced` with local proofs ✓
- GlobalUniqueness: body gives a derivation argument extending S4; correctly `introduced` (S4 explicitly restricts to I-addresses, so this is new) ✓
- L4: body describes it as "follows from definitions" (L3 + T12) and documents the significance as the *absence* of additional constraints; `introduced` is correct since this is a new design-significant absence claim ✓
- L7 (META): body says "L0–L14 impose no constraint…"; `introduced` META is appropriate ✓
- L12a: body says "direct corollary of L12"; `introduced` correct (L12 is itself introduced) ✓
- No property is listed as `cited` in the table, so no case of a `cited` label with a local proof ✓

(none)

---

`RESULT: CLEAN`
