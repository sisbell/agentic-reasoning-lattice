# Review of ASN-0025

## REVISE

### Issue 1: J1/J2 preservation asserted without per-operation proof

**ASN-0025, State Model (J1/J2 paragraph)**: "Each operation preserves J1 and J2: INSERT and COPY shift existing text positions forward by the insertion width, maintaining contiguity; DELETE shifts remaining text positions backward, closing the gap..."

**Problem**: The individual operation sections verify P0∧P1 and J0 explicitly but never verify J1 or J2. The state model section asserts preservation for all seven operations in a single paragraph with one-clause justifications. For INSERT, DELETE, and COPY, the contiguity argument is non-trivial — it requires showing that the union of new positions, shifted positions, and unchanged positions produces exactly {1, ..., k±n}. The argument is: pre-state text ordinals form {1, ..., k}; INSERT at ordinal j creates {j, ..., j+n−1}, shifts {j, ..., k} to {j+n, ..., k+n}, leaves {1, ..., j−1} unchanged; the union is {1, ..., k+n}. This is correct but not shown anywhere. DELETE and COPY require analogous arguments. The worked example also omits J1/J2 verification (text ordinals go from {1,2,3} to {1,2,3,4} — trivial but unstated).

**Required**: Add J1/J2 verification to each of INSERT, DELETE, and COPY alongside the existing P0∧P1 and J0 verification paragraphs. Show the set algebra: partition the post-state text ordinals into the three sets (new/shifted/unchanged), confirm their union equals {1, ..., new count}. Verify J1/J2 in the worked example.

### Issue 2: VPos type undefined; "text position" and "link position" predicates informal

**ASN-0025, State Model**: "Σ.v(d) : VPos ⇸ IAddr"

**Problem**: VPos is used as a type throughout the ASN but never formally defined. The V-space postconditions for INSERT, DELETE, COPY, and REARRANGE partition dom(Σ.v(d)) using the predicates "q is a text position" and "q is a link position," which have no formal definition. The state model paragraph says "V-positions carry a subspace identifier: text content occupies subspace 1 (positions with first component 1), links occupy subspace 2 (positions with first component 2)," but this is prose description, not a type definition. Simultaneously, TA7a's ordinal-only formulation says the subspace identifier is "structural context," not a component — creating tension with "first component."

A related consequence: the postcondition clause `(A q : q ∈ dom(Σ.v(d)) ∧ q < p : Σ'.v(d)(q) = Σ.v(d)(q))` in INSERT, DELETE, and COPY does not restrict q to text positions, unlike the companion clause `q ≥ p ∧ q is a text position`. If cross-subspace comparison is undefined under the ordinal-only formulation, `q < p` for a link-subspace q and text-subspace p is not well-formed. The intent is clear (unchanged text positions below p), but the formalization has a gap.

**Required**: Define VPos formally — e.g., as a pair (S, x) where S ∈ {text, link} is the subspace tag and x ∈ ℕ⁺ is the ordinal. Define "text position" and "link position" predicates in terms of this type. Add "q is a text position" to the `q < p` postcondition clauses in INSERT, DELETE, and COPY for consistency with the `q ≥ p` clauses.

### Issue 3: CREATE DOCUMENT precondition informal

**ASN-0025, CREATE DOCUMENT**: "**Preconditions.** The creating user's account address exists in Σ."

**Problem**: Every other operation has formal preconditions (d ∈ Σ.D, p ∈ dom(Σ.v(d)), etc.). CREATE DOCUMENT's precondition is prose. "The creating user's account address" references a concept (user account) not modeled as a state component. The ASN models Σ.D (documents) but not users as first-class state. The precondition cannot be checked against the state model as defined.

**Required**: Either formalize the precondition (e.g., "there exists a user-level I-address prefix u with zeros(u) = 1 such that u ≼ o for the allocated orgl o") or note explicitly that user account modeling is deferred and state what the precondition reduces to for the permanence argument (which needs only freshness of o).

## OUT_OF_SCOPE

### Topic 1: Full REARRANGE zone-level semantics
**Why out of scope**: The ASN explicitly defers zone-level postconditions (3-cut rotation, 4-cut swap with middle shift) to an operation semantics ASN. The constraint-level specification (P4, domain preservation, exterior frame, link frame) is sufficient for the permanence argument. The deferral is appropriate — the permutation details don't affect P0, P1, J0, or J1/J2.

### Topic 2: Link internal structure and endset formalization
**Why out of scope**: The ASN correctly identifies that link endpoint representation belongs to a future link ASN. The link survivability derivation is explicitly conditional: "if link endsets reference I-space addresses... then P0 ∧ P1 guarantee survivability." Formalizing the premise is the link ASN's responsibility.

### Topic 3: Orgl invariants
**Why out of scope**: The ASN assigns orgl(d) ∈ Σ.A to each document but states no invariants about orgls (injectivity, V-space visibility, relation to document identity). These properties may matter for document identity but are not needed for the permanence argument. GlobalUniqueness guarantees distinct creation events produce distinct orgls, but this is not stated as an invariant of Σ.

### Topic 4: Link deletion and link permanence
**Why out of scope**: DELETE's precondition restricts to text-subspace V-positions — links cannot be deleted. Whether this is intentional (Nelson: "all links are permanent") and what "link deletion" would mean belong to a link semantics ASN.

VERDICT: REVISE
