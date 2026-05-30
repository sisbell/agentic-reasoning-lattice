# Review of ASN-0043

## REVISE

### Issue 1: `subspace_I` misattributed to the foundation, where the named projection differs

**ASN-0043, Subspace Residence (Notational convention)**: "We extend `subspace_I(a) = E(a)₁` (ASN-0036's projection name) uniformly across every tumbler on which T4b's `E` projection is well-defined — i.e., every T4-valid tumbler `a` with `zeros(a) = 3`..."

**Problem**: ASN-0036's foundation contract defines `Definition — SubspaceProjection: subspace(v) = v₁`, signature `subspace : T → ℕ`, projecting the *first component of the whole tumbler* — and its callers (D-CTG, S8-depth, OrdShiftHom) all use the name `subspace`, applied to zero-free V-positions of depth ≥ 2. ASN-0043's `subspace_I(a) = E(a)₁` is a *different* formula (first component of the **element field** of an element-level I-address, `zeros(a)=3`) and a *different* name. The two projections operate on disjoint tumbler classes (V-positions vs. element-level I-addresses) and are not interchangeable. The parenthetical "(ASN-0036's projection name)" therefore asserts a foundation provenance that the foundation contract does not show. By Standard 7, an ASN must use a foundation's notation as the foundation defines it, or own its reinvention explicitly.

**Required**: Either (a) correct the attribution — state that `subspace_I` is introduced by *this* ASN as the element-field analogue of ASN-0036's `subspace`, and justify the relationship — or (b) reconcile the name and formula with the foundation. As written the claim is false against the cited contract, and every downstream invariant (L0, L0a, L1, etc.) inherits the unsound provenance.

### Issue 2: Operational drift in the Slot Distinction section

**ASN-0043, Slot Distinction and Directionality (final paragraph)**: "Despite the slot distinction, access is symmetric. The system must support retrieving any endset of any link with equal facility. Gregory confirms: the `followlink` operation takes a `whichend` parameter (1, 2, or 3)... The retrieval path is identical for all slots..."

**Problem**: This paragraph asserts a *requirement* about a retrieval operation ("The system must support retrieving any endset... with equal facility") and then cites `followlink` as confirmation. Resolution/following and discovery operations are explicitly out of scope for this ASN. No invariant in L0–L14 or L-fin carries a symmetric-access guarantee, so the paragraph advances no claim in this note — it states an operational obligation that belongs to a future operations ASN. (The companion sentence under L6, "A query for 'links from span A' and a query for 'links to span A'... may return different results," has the same defect: query/search semantics are out of scope.)

**Required**: Remove the symmetric-retrieval requirement and the `followlink`/query-result prose, or relocate them to the operations ASN. The structural fact that slots are positionally addressable (L6) is in scope; the retrieval-operation behavior built on top of it is not.

### Issue 3: Duplicated well-definedness justification for `.type`

**ASN-0043, StandardTriple (Named accessor)**: "The side condition `|Σ.L(a)| ≥ 3` that makes the abbreviation well-defined is discharged for every conforming link by L3."
**ASN-0043, L8**: "where `Σ.L(a).type` denotes slot 3 — well-defined for every `a ∈ dom(Σ.L)` by L3's `|Σ.L(a)| ≥ 3`..."

**Problem**: The same well-definedness fact (`.type` is defined because L3 gives arity ≥ 3) is stated in two places in the same words. This is the "two paragraphs say the same thing" accretion pattern — the reader must confirm they are identical rather than complementary.

**Required**: State the discharge once (at the Named-accessor definition) and let L8 use `.type` without re-justifying.

## OUT_OF_SCOPE

### Topic 1: Equivalence of distinct span decompositions with identical coverage
**Why out of scope**: The Coverage definition and L8 note that different span decompositions may share coverage; whether such endsets should be treated as query-equivalent is correctly deferred to Open Questions — a future query-semantics ASN, not a defect here.

VERDICT: REVISE
