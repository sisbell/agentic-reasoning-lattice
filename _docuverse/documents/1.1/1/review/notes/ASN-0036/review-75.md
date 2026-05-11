# Review of ASN-0036

## REVISE

### Issue 1: D-CTG-depth proof duplication
**ASN-0036, "Arrangement contiguity" section**: The contradiction argument constructing infinitely many intermediates appears twice — once informally after "At depth m ≥ 3, D-CTG combined with S8-fin forces a stronger restriction" (a *Proof.* block introducing the construction), and again as the proof of the labeled "D-CTG-depth (SharedPrefixReduction)" with essentially identical structure (suppose v₁ < v₂ with first disagreement at j ∈ {2, …, m−1}, construct w with arbitrary n at position j+1, contradict S8-fin via T0(a)).
**Problem**: Same argument is presented twice. The first occurrence is unlabeled and reads as a motivating preview; the second is the formal proof. This duplicates content without adding clarity.
**Required**: Either delete the first occurrence (folding the contradiction argument into D-CTG-depth's proof only), or explicitly mark the first as an illustrative preview ("We motivate D-CTG-depth by example, then state and prove it formally below") and shorten it to a one-paragraph sketch.

### Issue 2: Missing Depends sections in lemma formal contracts
**ASN-0036, "V-position ordinal decomposition" section**: The formal contracts for `ord(v)`, `vpos(S, o)`, `w_ord`, `OrdAddHom`, `OrdAddS8a`, and `OrdShiftHom` have *Preconditions*, *Definition*/*Postconditions*, and *Frame* slots, but no *Depends* slot.
**Problem**: Foundation ASNs (e.g., T9, T10a, TumblerAdd) include explicit *Depends* lists naming every foundation result consumed. Downstream ASNs that cite these lemmas (operations layer, link ontology) need this metadata for citability and for tracking what must be in scope. The proofs reference TumblerAdd, TA0, OrdinalShift, OrdinalDisplacement, but the contracts don't surface these.
**Required**: Add an explicit *Depends:* list to each of `ord`, `vpos`, `w_ord`, `OrdAddHom`, `OrdAddS8a`, `OrdShiftHom` enumerating the foundation results consumed, matching the foundation-ASN format.

### Issue 3: Inconsistent formal contract presentation
**ASN-0036, throughout**: Several properties have formal contract blocks (e.g., S1, S4, S5, S6, S7, S8a, S8, D-CTG-depth, D-SEQ); others — including the load-bearing S0, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8-depth, S9, D-CTG, D-MIN, ValidInsertionPosition — do not.
**Problem**: A reader cannot uniformly cite preconditions, postconditions, and frame for every claim. ValidInsertionPosition in particular is the central structural notion for insertion but lacks the *Preconditions/Postconditions/Frame* presentation given to its dependents. The Properties Introduced table partially compensates but doesn't substitute for per-claim contracts.
**Required**: Add explicit Formal Contract blocks for every introduced property (S0, S2, S3, S7a–d, S8-fin, S8-depth, S9, D-CTG, D-MIN, ValidInsertionPosition), with at least Preconditions/Postconditions/Frame slots. For "design requirement" properties, use an *Axiom* slot in place of *Postconditions*.

### Issue 4: S8 proof omits S7c citation for I-address subspace preservation under shift
**ASN-0036, S8 proof, correspondence run definition**: The definition uses `M(d)(shift(v, k)) = shift(a, k)`, and the surrounding prose states "A parallel uniformity holds for I-addresses within a correspondence run: all I-addresses in a run share the same tumbler depth and prefix" — relying on TumblerAdd's prefix-copy rule.
**Problem**: The subspace identifier of `a` (namely `E(a)₁`) is preserved under `shift(a, k) = a ⊕ δ(k, #a)` only because the action point `#a` falls strictly after the subspace identifier — which requires `#E(a) ≥ 2`, i.e., S7c. The proof asserts this preservation as if it followed from TumblerAdd alone, without naming S7c as the precondition that makes the prefix region include the subspace identifier. The proof's V-position parallel uses S8a's `#v ≥ 2` explicitly; the I-address parallel should cite S7c symmetrically.
**Required**: In the S8 proof's discussion of I-address shifts, explicitly cite S7c (`#E(a) ≥ 2`) as the premise that places the subspace identifier strictly before the action point of `δ(k, #a)`. Mirror the rigor of the V-position argument (which cites S8a's `m ≥ 2`).

### Issue 5: Subspace function for I-addresses informal
**ASN-0036, throughout**: For V-positions, `subspace(v) = v₁` is explicitly defined. For I-addresses, the text repeatedly writes `E(a)₁` inline for the subspace identifier (in S7c, in OrdAddHom's surrounding prose, in S8 discussion) without giving an explicit definition such as `subspace_I(a) := E(a)₁`.
**Problem**: Downstream ASNs (operations on text vs. link subspaces, cross-subspace queries) need a stable named function to cite. Using `E(a)₁` inline scatters the concept across the document and impedes citation. The asymmetry with V-position's `subspace(v) = v₁` is also confusing.
**Required**: Define `subspace_I(a) = E(a)₁` (with preconditions `a ∈ dom(C)`, S7b ensures `zeros(a) = 3` so E(a) is defined, and S7c ensures `#E(a) ≥ 1`) and use this name throughout. Alternatively, overload `subspace(·)` for both V-positions and I-addresses, with the case distinction made explicit.

### Issue 6: OrdShiftHom S8a preservation as prose rather than formal postcondition
**ASN-0036, OrdShiftHom contract**: "Postconditions: `ord(shift(v, n)) = shift(ord(v), n)`. When `v` satisfies S8a, OrdAddS8a applies; since `δ(n, m) = [0, ..., 0, n]` has action point `m`, there are no tail components after the action point — the OrdAddS8a condition is vacuously satisfied. Therefore `shift(v, n)` unconditionally satisfies S8a when `v` does."
**Problem**: The S8a-preservation claim is a substantive postcondition — it is the property downstream operation ASNs will cite when reasoning about position shifts. Burying it in explanatory prose after the equation makes it hard to cite as a separable result. The equation `ord(shift(v, n)) = shift(ord(v), n)` and the S8a-preservation conclusion are two distinct postconditions.
**Required**: Promote S8a preservation to an explicit numbered postcondition: "Postconditions: (a) `ord(shift(v, n)) = shift(ord(v), n)`; (b) When `v` satisfies S8a, `shift(v, n)` satisfies S8a." Keep the derivation prose as justification.

### Issue 7: Initial depth m mechanism not formally addressed
**ASN-0036, "Valid insertion position" section**: "The lower bound m ≥ 2 is necessary... For m ≥ 2, δ(n, m) has action point m, and since m > 1, TumblerAdd copies component 1 unchanged — OrdinalShift preserves the subspace identifier. This is the canonical minimum position required by D-MIN. The choice of m is a one-time structural commitment: once any position is placed, S8-depth fixes the depth for all subsequent positions."
**Problem**: The "one-time structural commitment" mechanism is asserted but not formally derived. ValidInsertionPosition's empty case admits *any* depth `m ≥ 2`; nothing in the ASN's invariants fixes which depth gets chosen. If the first operation places `v = [1, 1]` (m = 2) and a later operation places `v' = [1, 1, 1]` (m = 3) in the same subspace, S8-depth is violated — but the strand model has no mechanism preventing this. The "commitment" is delegated to operation-layer behavior, but the ASN doesn't formally state this delegation.
**Required**: Either (a) commit to a canonical depth (e.g., `m = 2` matching Gregory's implementation) at the strand-model level, or (b) explicitly state that the choice of `m` is an operation-layer concern and add an Open Question. The current formulation reads as if S8-depth enforces consistency, but S8-depth is a state invariant — it doesn't constrain how the first position is chosen.

## OUT_OF_SCOPE

### Topic 1: Subtraction homomorphism for ord
**Why out of scope**: The Open Questions section already asks "Under what conditions on w does the subtraction homomorphism `ord(v ⊖ w) = ord(v) ⊖ w_ord` hold" and the round-trip property. Establishing these would extend the V-position arithmetic toolkit, but the strand model currently needs only the addition/shift directions for state characterisation. Subtraction belongs in the operations-layer ASN where DELETE's frame condition will be specified.

### Topic 2: Run consolidation and uniqueness of decomposition
**Why out of scope**: The Open Questions ask whether the decomposition has a unique maximal form. This is a property of the representation, not of the state invariant S8 itself. S8 only requires existence of some finite decomposition; uniqueness/canonicalisation is a separate concern that interacts with operation semantics.

### Topic 3: Link subspace contiguity semantics
**Why out of scope**: D-CTG, D-MIN, D-CTG-depth, D-SEQ are explicitly bound to the text subspace `S = 1`. The remark notes that the link subspace `S = 2` has sparse, append-only-with-tombstones semantics. Formalising link-subspace structure belongs in a future ASN (link ontology / endset structure).

VERDICT: REVISE
