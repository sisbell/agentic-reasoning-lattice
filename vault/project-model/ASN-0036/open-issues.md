### Finding 1: [stale-label] GlobalUniqueness
**Location**: deps:S4
**Detail**: Property S4 references GlobalUniqueness which does not exist in any active ASN's export

### Finding 2: [stale-label] GlobalUniqueness
**Location**: deps:S7
**Detail**: Property S7 references GlobalUniqueness which does not exist in any active ASN's export

### Finding 3: [stale-label] T0(a)
**Location**: deps:D-CTG
**Detail**: Property D-CTG references T0(a) which does not exist in any active ASN's export

### Finding 4: [stale-label] T0(a)
**Location**: deps:D-CTG-depth
**Detail**: Property D-CTG-depth references T0(a) which does not exist in any active ASN's export

### Finding 5: [stale-label] OrdinalShift
**Location**: deps:ValidInsertionPosition
**Detail**: Property ValidInsertionPosition references OrdinalShift which does not exist in any active ASN's export

### Finding 6: [stale-label] TumblerAdd
**Location**: deps:ValidInsertionPosition
**Detail**: Property ValidInsertionPosition references TumblerAdd which does not exist in any active ASN's export

### Finding 7: [prose-only] T0 (ASN-0034)
**Location**: prose
**Detail**: Prose cites T0 (ASN-0034) but no property table entry lists it in follows_from

## Category 1: Stale Labels

(none)

All foundation labels cited in ASN-0036 (T0, T0(a), T1, T3, T4, T5, T8, T9, T10, T10a, TA5, TA7a, TumblerAdd, OrdinalShift, GlobalUniqueness, etc.) exist in the current ASN-0034 foundation.

---

## Category 2: Structural Drift

(none)

All cited foundation content is consistent with current ASN-0034 statements. T8 is cited as `allocated(s) ⊆ allocated(s')` — matches. GlobalUniqueness is cited as "for every pair of addresses produced by distinct allocation events: a ≠ b" — matches. T4 field structure, T5 prefix contiguity, TA5 sub-properties (a)–(d), and TumblerAdd constructive definition are all used accurately.

---

## Category 3: Local Redefinitions

**S4 (Origin-based identity)** is listed under "Properties Introduced" but is a direct instance of GlobalUniqueness (ASN-0034).

GlobalUniqueness (ASN-0034): *Invariant:* for every pair of addresses `a, b` produced by distinct allocation events in any reachable system state: `a ≠ b`. The precondition requires only that the allocations conform to T10a — no condition on stored values.

S4 (ASN-0036): "For I-addresses `a₁`, `a₂` produced by distinct allocation events: `a₁ ≠ a₂` regardless of whether `Σ.C(a₁) = Σ.C(a₂)`." Preconditions: `a₁, a₂ ∈ dom(Σ.C)`, distinct allocation events, T10a conformance.

S4 restricts GlobalUniqueness to `dom(Σ.C) ⊆ T` and annotates value independence — but GlobalUniqueness already covers all of T and its proof makes no reference to stored values. The S4 proof body confirms this: "GlobalUniqueness yields `a₁ ≠ a₂` directly." There is no additional mathematical work. S4 should be classified as a corollary cited from GlobalUniqueness (ASN-0034), not as an introduced property.

---

## Category 4: Registry Misclassification

(none)

---

## Category 5: Missing Dependencies

(none)

All foundation citations are to ASN-0034, which is the sole declared dependency.

---

## Category 6: Exhaustiveness Gaps

(none)

---

`RESULT: 1 FINDING`
