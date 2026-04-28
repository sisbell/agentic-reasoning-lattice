## Dependencies to Add

(none)

No LLM-confirmed MISSING findings were produced across any audited ASN.

---

## Label Collisions (consider rename)

**B1 / B2 / B3** — defined independently in both ASN-0040 and ASN-0058 with different meanings.

- **ASN-0040** uses B1/B2/B3 as proof sub-case labels in the TA3 verification case analysis (zero-padded equality, digit-count comparisons).
- **ASN-0058** introduces B1/B2/B3 as first-class block decomposition predicates: Coverage, Disjointness, Consistency.

The scanner matched the shared label text and flagged ASN-0040 as a potential source, but in every affected ASN the block decomposition predicates from ASN-0058 are what is actually being used.

| Affected ASN | Labels involved |
|---|---|
| ASN-0051 | B1 |
| ASN-0059 | B1, B2, B3 |
| ASN-0061 | B1, B2, B3 |
| ASN-0065 | B1, B2, B3 |
| ASN-0067 | B1, B2, B3 |
| ASN-0079 | B3 |

No missing dependency results from any of these — each affected ASN already declares ASN-0058. The issue is label namespace collision between ASN-0040's internal proof labels and ASN-0058's exported predicates. Consider renaming ASN-0040's sub-case labels (e.g. BC1/BC2/BC3 for "branch case") to eliminate ambiguity.

---

## Label Overlaps (informational)

These ASNs introduce properties locally that happen to share label names with exports from another ASN. No action required; the local definitions are independent.

| ASN | Labels | Conflicting ASN | Notes |
|---|---|---|---|
| ASN-0040 | S0 (StreamOrdering), S1 (StreamPrefix) | ASN-0036 | Locally originated in ASN-0040 ("from TA5(a)–(d)"); ASN-0036 uses the same labels independently |
| ASN-0053 | S0–S9 (Convexity … NormalizationUniqueness) | ASN-0036 | All ten introduced in ASN-0053; ASN-0036 is a downstream consumer, not the source |
| ASN-0058 | B1 (Coverage), B2 (Disjointness), B3 (Consistency) | ASN-0040 | Introduced in ASN-0058's Block Decomposition definition; ASN-0040's same labels are unrelated proof sub-cases |

---

## Clean

ASN-0034, ASN-0036, ASN-0042, ASN-0043, ASN-0045, ASN-0047
