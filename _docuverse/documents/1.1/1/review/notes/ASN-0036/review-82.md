# Review of ASN-0036

## REVISE

### Issue 1: S7a's axiom uses projections that S7b is needed to make total

**ASN-0036, S7a Formal Contract**: "*Axiom (design requirement):* For every `a ∈ dom(Σ.C)`, the document-level prefix `N(a).0.U(a).0.D(a)` is the tumbler of the document whose owner performed the allocation that placed `a` into `dom(C)`."

**Problem**: T4b's projections `N(a)`, `U(a)`, `D(a)` are partial functions — `D(a)` requires `zeros(a) ≥ 2`. The S7a axiom quantifies over all `a ∈ dom(C)` and asserts a property of these projections, but doesn't establish that the projections are total on `dom(C)`. That totality is supplied by S7b (`zeros(a) = 3`), which is stated *after* S7a. S7a's *Depends* lists T4, T4b, T10a but omits S7b. The axiom's intended meaning depends on a property stated later in the document, which is structurally odd.

**Required**: Either (a) list S7b as a dependency of S7a, (b) condition S7a's statement on `zeros(a) ≥ 2`, or (c) bundle the structural premise into S7a explicitly (e.g., "for every `a ∈ dom(C)`, `zeros(a) ≥ 2` and the document-level prefix...").

### Issue 2: S8's formal contract lacks a *Depends* section

**ASN-0036, S8 Formal Contract**: Lists *Preconditions* and *Postconditions* but no *Depends*.

**Problem**: The proof uses TumblerAdd's three-region formula, OrdinalShift, OrdinalDisplacement, T1 case (i)/(ii), T3 (CanonicalRepresentation), T5 (ContiguousSubtrees), T10 (PartitionIndependence), and TS4 (ShiftStrictIncrease) from ASN-0034, plus several local properties (S2, S3, S7b, S7c, S8a, S8-depth, S8-fin). The Properties Introduced table enumerates these at the end, but the formal contract should be self-contained, matching the style of foundation-ASN contracts.

**Required**: Add a *Depends:* section to S8's formal contract enumerating each foundation claim and local property consumed.

### Issue 3: D-CTG-depth's formal contract lacks *Depends*

**ASN-0036, D-CTG-depth Formal Contract**: Lists *Preconditions* and *Postconditions* but no *Depends*.

**Problem**: The proof relies on T0(a) (UnboundedComponentValues — supplies the iteration of witnesses), T1 (LexicographicOrder, case (i)), T3 (distinct components ⟹ distinct tumblers), S8a, S8-fin, S8-depth, and the design constraint D-CTG itself. None appear in the contract's dependency listing.

**Required**: Add a *Depends:* section enumerating consumed claims.

### Issue 4: D-SEQ's formal contract lacks *Depends*

**ASN-0036, D-SEQ Formal Contract**: Same omission as Issue 3.

**Problem**: The proof uses D-CTG, D-CTG-depth, D-MIN, S8a, S8-fin, S8-depth, and T1 (case (i)). None are listed.

**Required**: Add a *Depends:* section.

### Issue 5: S5's formal contract lacks *Depends*

**ASN-0036, S5 Formal Contract**: No *Depends* listing.

**Problem**: The construction must verify candidate states against S0, S1, S2, S3 (vacuously for S0/S1 at a single state; non-trivially for S2/S3). These should appear as dependencies. The same applies to T3 and the carrier-membership reasoning used to ground the constructed states in T.

**Required**: Add a *Depends:* section.

### Issue 6: S8a's positivity step appeals to NAT-zero without citation

**ASN-0036, S8a Proof**: "Every component of `v` is in ℕ, and `zeros(v) = 0` means no component equals 0; therefore every component is strictly positive."

**Problem**: The implication "non-zero natural ⟹ strictly positive" relies on NAT-zero's disjunction `0 < n ∨ 0 = n` instantiated at each component value. The proof's *Depends* lists T4 and T0 but not NAT-zero. This is a foundation citation gap, not a logical error, but the same standard applied throughout the foundations should hold here.

**Required**: Cite NAT-zero (NatZeroMinimum, ASN-0034) in S8a's *Depends*, or strengthen the prose to make the disjunction explicit.

## OUT_OF_SCOPE

(None to flag. The ASN's scope is carefully managed: operation-specific D-CTG/D-MIN preservation, link-subspace contiguity semantics, subspace alignment as a state invariant, and version/document creation semantics are all explicitly deferred. The "Scope" footer and the Remark following S8a are clear about what is being held off for future ASNs.)

VERDICT: REVISE
