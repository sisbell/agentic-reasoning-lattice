# Review of ASN-0036

## REVISE

### Issue 1: S7a Formal Contract misattributes T4c
**ASN-0036, S7a Formal Contract**: "T4c (PrefixHierarchy, ASN-0034) — defines projections N, U, D"
**Problem**: T4c is named **LevelDetermination**, not "PrefixHierarchy". It defines the node/user/document/element address labels via zero count — it does *not* define the projections N, U, D. The projections are defined by **T4b (UniqueParse)**. The body proof of S7 correctly cites T4b ("the partial projections supplied by T4b (UniqueParse, ASN-0034)"), so the citation in S7a's Formal Contract is internally inconsistent with the rest of the ASN.
**Required**: Replace "T4c (PrefixHierarchy, ASN-0034) — defines projections N, U, D" with "T4b (UniqueParse, ASN-0034) — defines projections N, U, D". Correct the parallel entry in the Properties Introduced table ("S7a | ... | design; uses Prefix, T4, T4c") similarly. Also clarify why "Prefix" is listed there — it does not appear in the body's dependency list.

### Issue 2: S8 dependency list omits used premises
**ASN-0036, Properties Introduced table, S8 row**: "theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TumblerAdd, OrdinalShift, OrdinalDisplacement, TS4 (ASN-0034)"
**Problem**: The body proof of S8 invokes S3, S7b, and S7c that are absent from the dependency list: "By S3 (referential integrity), a ∈ dom(Σ.C), so S7b gives zeros(a) = 3 and S7c gives #E(a) ≥ 2 — the I-address has the structural depth required for shifts to be well-defined and to preserve the I-address subspace identifier subspace_I(a)."
**Required**: Add S3, S7b, S7c to the dependency list for S8 in the Properties Introduced table.

### Issue 3: S7 Preconditions list omits T4b
**ASN-0036, S7 Formal Contract**: "*Preconditions:* a ∈ dom(Σ.C) in a system conforming to S7a (document-scoped allocation), S7b (element-level I-addresses), S7d (document allocation discipline), T4 (HierarchicalParsing, ASN-0034), and T10a (allocator discipline, ASN-0034)."
**Problem**: The proof's well-definedness step invokes "the partial projections supplied by T4b (UniqueParse, ASN-0034) — N(a), U(a), D(a), E(a)". T4b is load-bearing for the definition of origin(a), yet it is absent from the Preconditions list. The Properties Introduced table for S7 does cite T4b, exposing an internal inconsistency.
**Required**: Add T4b (UniqueParse, ASN-0034) to S7's Preconditions list.

### Issue 4: D-CTG dependency lists are inconsistent between body and table
**ASN-0036, D-CTG Formal Contract**: body lists "S8a (V-position well-formedness); S8-depth (common depth within subspace); T1 (TumblerOrdering, ASN-0034) — defines the order"; Properties Introduced table lists "design (text subspace); uses T0(a), T1, T3 (ASN-0034)".
**Problem**: The two dependency lists do not overlap correctly. T0(a) and T3 are used in the proof of **D-CTG-depth** (constructing infinitely many intermediates and distinguishing them by canonical representation), not in D-CTG's own statement. Conversely, S8a and S8-depth (needed to interpret subspace and common depth) are missing from the table.
**Required**: Make the body Formal Contract and the Properties Introduced table consistent. The body's list (S8a, S8-depth, T1) is the correct dependency set for D-CTG's statement; the table should match.

### Issue 5: S8a Preconditions cite S7b without explaining its role
**ASN-0036, S8a Formal Contract**: "*Preconditions:* T4 (HierarchicalParsing, ASN-0034) ...; T0 — components are natural numbers; S7b — addresses in dom(Σ.C) are element-level tumblers with zeros(a) = 3."
**Problem**: S7b is a property of *I-addresses*, not of V-positions. S8a constrains V-positions, and the body proof's three conjuncts (zeros(v) = 0, #v ≥ 2, componentwise positivity) all follow from the structural commitment "V-positions are element-field tumblers of depth at least 2" together with T4 and T0. S7b appears in the proof only to motivate the architectural parallel, not as a logical premise. Including it as a precondition obscures the fact that S8a is an independent axiomatic commitment about V-positions. The proof's claim "the same shape as E(a)" is rhetorical, not derivational.
**Required**: Either remove S7b from S8a's Preconditions (since it is not load-bearing for the conjuncts) or rewrite the precondition framing to make clear the relationship is architectural parallelism, not logical entailment.

### Issue 6: D-CTG-depth dependency list omits S8a
**ASN-0036, Properties Introduced table, D-CTG-depth row**: "corollary of D-CTG, S8-fin, S8-depth, T0(a), T1, T3 (ASN-0034)"
**Problem**: The proof of D-CTG-depth establishes `subspace(w) = w₁ = (v₁)₁ = 1 (since j ≥ 2, the first component is copied from v₁)` — this depends on S8a's commitment that v₁ is the subspace identifier (first component) of an element-field-shaped tumbler. S8a is implicit but should be cited.
**Required**: Add S8a to D-CTG-depth's dependency list.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG, D-MIN, and S2 under INSERT/DELETE/COPY/REARRANGE
**Why out of scope**: The ASN explicitly defers operation-specific verification to each operation's own ASN. The strand model states the invariants; preservation is each operation's obligation.

### Topic 2: Subspace alignment between V-position subspace and I-address subspace
**Why out of scope**: The ASN deliberately defers this to the operations layer (Remark following S8a). Whether `subspace(v) = subspace_I(M(d)(v))` is an operation-layer guarantee, not a strand-level invariant.

### Topic 3: Choice of canonical depth m for the empty text-subspace case
**Why out of scope**: The strand model fixes only m ≥ 2; the specific allocation convention is an operation-layer commitment. Nelson explicitly leaves "subdivision by further digits" open.

### Topic 4: Link-subspace (S = 2) contiguity semantics
**Why out of scope**: The ASN binds D-CTG, D-MIN, D-CTG-depth, D-SEQ to text subspace S = 1 and defers link-subspace sparse-tombstone semantics to a future ASN.

### Topic 5: Computability bound on sharing inverse
**Why out of scope**: Open question in the ASN's own enumeration; cost analysis depends on implementation choices for the secondary index.

### Topic 6: Round-trip and subtraction homomorphism for ord/w_ord
**Why out of scope**: Explicitly listed as open questions deferred to TA7a's subtraction analysis.

### Topic 7: Coarser-than-singleton run decompositions
**Why out of scope**: The ASN notes that non-trivial run cardinality is operation-layer (consecutive allocations under T10a, splitting under editing). S8 asserts only existence of *some* finite decomposition.

VERDICT: REVISE
