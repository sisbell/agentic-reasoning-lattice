## Foundation Consistency Check — ASN-0043 (Link Ontology)

---

### 1. Stale Labels

(none)

All cited foundation labels are current. Verified: T4/HierarchicalParsing, T5/ContiguousSubtrees, T6/DecidableContainment, T7/SubspaceDisjointness, T9/ForwardAllocation, T10/PartitionIndependence, T10a/AllocatorDiscipline, T12/SpanWellDefinedness, TA5(d)/HierarchicalIncrement, T3/CanonicalRepresentation, T0(a)/UnboundedComponentValues, OrdinalDisplacement, OrdinalShift; S0/ContentImmutability, S1/StoreMonotonicity, S3/ReferentialIntegrity, S4/OriginBasedIdentity, S5/UnrestrictedSharing, S7/StructuralAttribution, S7a/DocumentScopedAllocation, S7b/ElementLevelAddresses — all match the supplied foundation.

---

### 2. Local Redefinitions

(none)

Every property in the Introduced table (L0–L14, GlobalUniqueness, PrefixSpanCoverage, coverage(e), home(a), Endset, Link) is absent from both foundation ASNs.

---

### 3. Structural Drift

**Finding 1.** `home(a)` is defined as `= origin(a)` for `a ∈ dom(Σ.L)`, but the ASN-0036 foundation restricts `origin` to `dom(Σ.C)`.

ASN-0036 defines: *"For every `a ∈ dom(Σ.C)`, the origin is the document-level prefix obtained by truncating the element field: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`."*

ASN-0043 says (under "Home and Ownership"): *"the `origin` function from ASN-0036 applies directly"* and defines:
```
home(a) = origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)
```
for `a ∈ dom(Σ.L)`.

The foundation definition is a partial function with domain `dom(Σ.C)`. ASN-0043 applies it to `dom(Σ.L)` without a formal domain extension — neither by re-stating origin with an extended domain nor by defining `home(a)` directly from the field-extraction formula while treating the extension as a local definition. The equation `home(a) = origin(a)` presupposes `origin` is already well-typed on link-subspace addresses, which the foundation does not establish.

The formula itself is correct; the domain mismatch is the issue.

**Finding 2.** `GlobalUniqueness` claims to extend S4 (OriginBasedIdentity, ASN-0036) beyond I-addresses to all allocation events, but S4 is quantified over `dom(Σ.C)` only.

The registry says: *"extends S4 (OriginBasedIdentity, ASN-0036) beyond I-addresses via T9, T10, T10a, TA5, T3."* The body text invokes GlobalUniqueness for link-address uniqueness (L11a) without formally establishing that the T9/T10/T10a argument, which S4 uses for content-subspace addresses, also applies to link-subspace addresses. The proof needs to explicitly show that forward allocation (T9) in the link subspace produces addresses that satisfy the same partition independence (T10) and allocator discipline (T10a) conditions that S4 relies on for `dom(Σ.C)`.

Same class of issue as Finding 1: a foundation result scoped to `dom(Σ.C)` is extended to `dom(Σ.L)` without formal domain justification.

---

### 4. Missing Dependencies

(none)

Every cited property — including the entire T-series from ASN-0034 and the S-series from ASN-0036 — belongs to a declared dependency.

---

### 5. Exhaustiveness Gaps

(none)

No claim in the ASN asserts coverage of "all" foundation items in a way that omits something present in the foundation.

---

### 6. Registry Mismatches

(none)

All table entries are `introduced`. None of the introduced properties appear in either foundation, so no entry that should be `cited` is mislabeled. Each LEMMA entry has a corresponding argument or witness in the body; each INV entry is stated as a design invariant (paralleling the pattern of S0, S7a, S7b in ASN-0036). No body text gives a local proof for something the table would classify as a foundation cite.

---

## REVISE

1. **home(a) domain extension** — `home(a) = origin(a)` applies `origin` to `dom(Σ.L)` but ASN-0036 defines `origin` only on `dom(Σ.C)`. Either (a) define `home(a)` directly from the field-extraction formula as a local definition without claiming equality with `origin`, or (b) formally extend `origin` to `dom(Σ.C) ∪ dom(Σ.L)` with explicit justification that T4 field parsing applies to link-subspace addresses (which it does — T4 is defined for all tumblers, not just content addresses).

2. **GlobalUniqueness scope extension** — GlobalUniqueness claims to extend S4 beyond I-addresses to all allocations including `dom(Σ.L)`, but the proof must explicitly show that T9/T10/T10a apply in the link subspace. The argument is that T9 (ForwardAllocation), T10 (PartitionIndependence), and T10a (AllocatorDiscipline) are properties of the tumbler arithmetic, not of any particular subspace — state this explicitly in the GlobalUniqueness proof.

`RESULT: 2 FINDINGS`
