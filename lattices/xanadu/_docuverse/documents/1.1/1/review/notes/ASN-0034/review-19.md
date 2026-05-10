# Review of ASN-0034

The mathematical content of this ASN is rigorous. Every proof I checked — T5, TA1/TA1-strict, TA3/TA3-strict, TA4, ReverseInverse, TA-LC, TA-MTO, D1, PartitionMonotonicity, GlobalUniqueness — is correct, handles boundary cases, and avoids hand-waving. The issues below are confined to the mechanically-extracted YAML dependency graph, which contradicts the ASN's own property table and proof text in several places.

## REVISE

### Issue 1: Three circular dependencies in the YAML graph

**Problem**: The YAML contains three cycles that contradict the derivation order established in the ASN text:

**(a) TA-strict ↔ T12.** TA-strict lists T12 in `follows_from`, but T12 lists TA-strict (for span non-emptiness). The ASN's "Verification of TA-strict" derives the property from TumblerAdd and T1 alone — T12 is defined later and depends on TA-strict, not the reverse.

**(b) Divergence ↔ TA1-strict.** Divergence lists TA1-strict in `follows_from`, but TA1-strict lists Divergence. The ASN's "Definition (Divergence)" is a standalone definition partitioning T1's two ordering cases. TA1-strict uses the definition; the definition does not use TA1-strict.

**(c) TumblerAdd ↔ TA4.** TumblerAdd (status: `introduced`) lists TA4 in `follows_from`, but TA4 (status: `from`) lists TumblerAdd. TumblerAdd is the constructive definition; TA4 is verified using it. The direction TA4 → TumblerAdd is correct; the reverse is not.

**Required**: Remove the reverse edges — T12 from TA-strict, TA1-strict from Divergence, TA4 from TumblerAdd.

### Issue 2: Spurious dependencies — YAML contradicts the ASN property table

Seven properties have `follows_from` entries in the YAML that are not used in the corresponding derivation. In each case the ASN's own "Properties Introduced" table gives the correct (smaller) dependency set.

| Property | YAML `follows_from` | ASN table says | Spurious entries |
|----------|---------------------|----------------|------------------|
| TA-strict | T1, T12, TA0, TA1, TA4, TumblerAdd | from TumblerAdd, T1 | T12, TA0, TA1, TA4 |
| Divergence | T1, TA0, TA1, TA1-strict | from T1 | TA0, TA1, TA1-strict |
| TumblerSub | Divergence, T1, TA1, TA1-strict, TA3 | from Divergence, T1 | TA1, TA1-strict, TA3 |
| T9 | T10, T10a, T8, TA5 | lemma (from T10a, TA5) | T10, T8 |
| T12 | T1, T5, TA-strict, TA0 | from T1, TA0, TA-strict | T5 |
| T0(b) | T0(a) | introduced | T0(a) |
| TumblerAdd | TA4 | introduced | TA4 |

Notes on specific cases:

- **T12 / T5**: The ASN explicitly states "We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous" — T5 is deliberately excluded from T12's derivation.
- **T9 / T10**: T10 concerns distinct allocators; T9 is purely about a single allocator's stream. T8 appears only in the consequence ("A consequence of T8 and T9 together..."), not in T9's derivation.
- **T0(b) / T0(a)**: The ASN states "T0(b) follows from T's definition as the set of all finite sequences over ℕ" — independent of T0(a).
- **TumblerAdd / TA4**: TumblerAdd is a constructive definition (`status: introduced`) with no logical dependency on the partial-inverse property it is used to verify.

**Required**: Update each property's `follows_from` to match the ASN property table. See the table above — retain only the non-spurious entries.

### Issue 3: Spurious transitive dependencies in TS5 and D2

**TS5 YAML `follows_from`**: [T4, TA0, TS1, TS3, TS4, TumblerAdd]
**TS5 derivation** (Section "TS5"): "Write n₂ = n₁ + (n₂ − n₁)... By TS3... By TS4..."

Only TS3 and TS4 are cited. T4, TA0, TS1, TumblerAdd are transitive dependencies of TS3/TS4 that should not appear in TS5's direct `follows_from`.

**D2 YAML `follows_from`**: [D0, D1, TA-LC, TA0, TumblerAdd, TumblerSub]
**D2 derivation** (Section "D2"): "By D1, a ⊕ (b ⊖ a) = b. So a ⊕ w = a ⊕ (b ⊖ a), and by TA-LC, w = b ⊖ a."

Only D1 and TA-LC are cited. D0, TA0, TumblerAdd, TumblerSub are transitive.

**Required**: TS5 `follows_from` → [TS3, TS4]. D2 `follows_from` → [D1, TA-LC].

### Issue 4: Name mismatches in YAML

| Label | YAML `name` | ASN parenthetical |
|-------|-------------|-------------------|
| TA1-strict | "strict (Strict order preservation)" | "Strict order preservation" |
| TA-LC | "LC (LeftCancellation)" | "LeftCancellation" |
| TA-MTO | "MTO (ManyToOne)" | "ManyToOne" |
| TA-RC | "Right cancellation fails" | "RightCancellationFailure" |

**Problem**: The first three have redundant label-prefix artifacts from mechanical extraction. TA-RC uses a different naming convention than the ASN.

**Required**: Update names to match the ASN parentheticals.

## OUT_OF_SCOPE

(none — the ASN is well-scoped and the open questions are genuine future work)

VERDICT: REVISE
