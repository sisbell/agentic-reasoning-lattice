## Category 1: Stale Labels

**Finding 1 — T4 cited as "FieldParsing"**
Two occurrences in the body use the label "FieldParsing" for T4:
- Subspace Residence section: "Recall from ASN-0034 (T4, FieldParsing) that every element-level tumbler has the form `N.0.U.0.D.0.E`..."
- Home and Ownership section: "By L1 and T4 (FieldParsing, ASN-0034), the prefix is recoverable from the address alone."

Foundation T4 is labeled **HierarchicalParsing**, not FieldParsing.

**Finding 2 — T7 cited as "SubspaceDisjoint"**
Subspace Residence section: "By T7 (SubspaceDisjoint), tumblers with different subspace identifiers are permanently distinct."

Foundation T7 is labeled **SubspaceDisjointness**, not SubspaceDisjoint.

**Finding 3 — T12 cited as "SpanWellDefined"**
Endset definition: "where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (SpanWellDefined, ASN-0034)."

Foundation T12 is labeled **SpanWellDefinedness**, not SpanWellDefined.

---

## Category 2: Local Redefinitions

(none)

---

## Category 3: Structural Drift

(none)

---

## Category 4: Missing Dependencies

(none)

---

## Category 5: Exhaustiveness Gaps

(none)

---

## Category 6: Registry Mismatches

**Finding 4 — GlobalUniqueness table description omits foundations used in body proof**

The Properties Introduced table states:
> "GlobalUniqueness | LEMMA | No two allocation events anywhere in the system, at any time, produce the same address — **derived from T9 (ForwardAllocation) + T10 (PartitionIndependence)**"

But the body proof covers three cases, and case (iii) — comparable prefixes — additionally uses **T10a (AllocatorDiscipline)**, **TA5(c)** (length preservation under sibling increment), **TA5(d)** (depth increase under child spawning), and **T3 (CanonicalRepresentation)**:

> "By T10a (AllocatorDiscipline), each allocator produces its sibling outputs exclusively via `inc(·, 0)`, which by TA5(c) preserves tumbler length... By T3 (CanonicalRepresentation), tumblers of different lengths are unequal, so `a ≠ b`."

The registry description is inconsistent with the proof in the body. Note: ASN-0036's S4 (OriginBasedIdentity), which proves an analogous result for I-addresses, correctly lists all three dependencies including T10a + TA5(d) + T3.

---

`RESULT: 4 FINDINGS`
