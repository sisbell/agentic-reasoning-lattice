# Review of ASN-0025

## REVISE

### Issue 1: P3 exhaustiveness claim is ungrounded
**ASN-0025, Operations Under Permanence**: "INSERT, CREATE LINK, and CREATE VERSION are the only operations that extend Σ.A with fresh addresses"
**Problem**: This is a universal claim — "the only operations" — but the ASN never establishes that these six operations are exhaustive. Gregory's implementation includes `docreatenewdocument` (creating a new document from scratch, not a version of an existing one), which allocates a fresh orgl address in I-space. CREATE DOCUMENT is not a special case of CREATE VERSION — CREATE VERSION requires `d ∈ Σ.D` (an existing source document), while CREATE DOCUMENT has no source. If CREATE DOCUMENT extends Σ.A, the "only" claim is false.
**Required**: Either add CREATE DOCUMENT as a seventh operation with P0 ∧ P1 and J0 verification, or replace "the only operations" with a qualified statement (e.g., "Among the operations defined here, only INSERT, CREATE LINK, and CREATE VERSION extend Σ.A"). The first option is preferable — the operation is straightforward (allocate document address, initialize empty V-space, J0 holds vacuously) and closes the classification.

### Issue 2: P7 asserted as axiom but is derivable
**ASN-0025, Content Identity**: "P7 (Creation-Based Identity). Content identity is determined by creation, not by value."
**Problem**: P7 is labeled "introduced" in the properties table, treating it as an independent axiom. But its content is fully derivable from existing machinery. The "only if" direction (same I-address implies same creation event) follows from GlobalUniqueness (ASN-0001): no two distinct allocations produce the same address, so a shared I-address necessarily traces to a single allocation. The "if" direction is trivially true (one allocation event, one set of addresses). The two consequences stated under P7 — independent creation yields distinct addresses, transclusion preserves addresses — follow from T4 + T10 (distinct prefixes) and P3 (COPY allocates nothing), respectively. Since "creation event" is not formally defined in the state model, P7 as stated is an informal principle wrapping derivable facts.
**Required**: Either (a) derive P7 explicitly from T9, T10, GlobalUniqueness, and P3, and label it "derived" in the properties table, or (b) formally define "creation event" (e.g., as a single invocation of INSERT, CREATE LINK, or CREATE VERSION) and then state P7 as a theorem over that definition.

### Issue 3: Correspondence derivation cites wrong premise
**ASN-0025, Structural Consequences**: "This requires P0 (shared addresses persist across all subsequent states) and P5 (transclusion preserves identity)."
**Problem**: P5 is defined under the COPY operation: "COPY makes source I-addresses visible in target without new allocation." But the correspondence argument is about versions, not transclusions. CREATE VERSION shares I-addresses through V-space mirroring, which is a different mechanism — the new document's V-space is initialized as a copy of the source's V-space. The relevant property is CREATE VERSION's postcondition (Σ'.v(d') mirrors Σ.v(d)), not P5. Citing P5 here conflates two distinct sharing mechanisms and could mislead formal verification efforts.
**Required**: Replace the P5 citation with a reference to CREATE VERSION's V-space mirroring postcondition. If the shared-identity property is meant to cover both COPY and CREATE VERSION, generalize P5 to a shared principle and cite the general form.

### Issue 4: P8 is not a property of the abstract model
**ASN-0025, Location Transparency**: "P8 (Location Transparency). The I-address is independent of physical storage location."
**Problem**: The abstract model Σ has no notion of physical storage location — Σ.ι is a mathematical partial function from IAddr to Byte. P8 is vacuously true within the model. As stated, it is a conformance requirement on implementations, not a property derivable from or testable against the state model. Yet it appears in the properties table alongside formal invariants (P0, P1) and formal postconditions (P3, P4, P5).
**Required**: Either reformulate P8 as a concrete property of the model (e.g., "No component of the tumbler type IAddr constrains or encodes current physical storage location; the node field records originating provenance at creation time") or move P8 to a separate implementation requirements section, distinct from the formal properties.

### Issue 5: P2 mislabeled in properties table
**ASN-0025, Properties Introduced table**: P2 listed as "introduced"
**Problem**: The text explicitly derives P2 from P0 ∧ P1 by induction over state transitions: "From P0 ∧ P1 we derive immediately: P2 (No Reuse)." The derivation is complete and correct. But the properties table labels P2 as "introduced," same as the axioms P0 and P1.
**Required**: Change P2's status in the table from "introduced" to "derived (from P0 ∧ P1)."

## OUT_OF_SCOPE

### Topic 1: Formal V-space postconditions
The ASN formalizes I-space effects precisely (e.g., Σ'.A = Σ.A ∪ B) but describes V-space effects in prose ("positions shift forward by width n"). For permanence analysis, the informal V-space descriptions are sufficient to verify J0 and frame conditions. Full V-space formalization (shift functions, position arithmetic, subspace constraints) belongs in a future ASN on editing operations.
**Why out of scope**: The ASN's thesis is I-space permanence. V-space is the mutable counterpart whose formal treatment is a separate concern.

### Topic 2: REARRANGE detailed semantics
REARRANGE is described as "permutes content within document d" with postcondition P4 (multiset preservation). Whether this is a cut-and-paste, swap, or general permutation is unspecified. P4 is sufficient for permanence analysis but not for a complete editing specification.
**Why out of scope**: Editing operation semantics beyond their I-space effects are future work.

### Topic 3: Link structure immutability
The ASN establishes that link I-addresses are permanent (CREATE LINK extends I-space; P0 ∧ P1 apply). Whether the link's endset content — encoded as part of the link's I-space entry — is immutable depends on how link content is modeled. This requires a link-focused ASN.
**Why out of scope**: Link modeling is a distinct topic; the permanence machinery (P0 ∧ P1) applies to link addresses by construction, but the internal structure of link content needs its own treatment.

VERDICT: REVISE
