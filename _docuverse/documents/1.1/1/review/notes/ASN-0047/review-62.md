# Review of ASN-0047

## REVISE

### Issue 1: Properties Introduced table is incomplete

**ASN-0047, Properties Introduced section, "Foundation restatements" subtable**: The table includes ASN-0043 foundation invariants L1, L1a, L1b, L12, L-fin as "Foundation restatements" but omits ASN-0036 foundation invariants S2, S4, S7a–S7d, S8a, S8-fin, S8-depth, S8, and S9 — all of which appear as named conjuncts in `ExtendedReachableStateInvariants` and `ExtendedTransitionInvariants`. The omission is inconsistent: if "recapitulated for self-contained reference" warrants listing L1 and L12, it equally warrants listing S2 and S9.

**Required**: Either complete the table with the missing ASN-0036 foundation restatements (S2, S4, S7a–d, S8a, S8-fin, S8-depth, S8, S9, plus D-CTG/D-MIN/D-SEQ which are amended), or restrict the table's scope to "new and modified properties only" with a leading note that unmodified foundation invariants are inherited as-is.

### Issue 2: K.δ ghost-base k=1 discussion is repetitive

**ASN-0047, K.δ definition and *Scope and base-liveness***: The same content (T10a doesn't underwrite freshness for ghost operands; K.δ precondition + TA5 determinism discharges `e ∉ E` instead) is stated across three paragraphs — the precondition list's bulleted discussion, *Scope and base-liveness*, and *Discharge of `e ∉ E` in the ghost-operand case*. The argument is correct in each instance but the redundancy makes the case discipline harder to follow at the precondition gate.

**Required**: Consolidate the ghost-base discharge argument into one paragraph (preferably co-located with the k=1 sub-case bullet), with the other two locations replaced by short pointers.

### Issue 3: K.μ~ link-subspace fixity presented as load-bearing when it is a corollary

**ASN-0047, *Decomposition of K.μ~* and *ExtendedReachableStateInvariants* proof, K.μ~ case**: The link-subspace fixity derivation (π = id on dom_L) is presented as if it must be discharged before invariant preservation arguments under K.μ~. But invariant preservation under K.μ~ for S3★, CL-OWN, CL-UNIQ requires only **subspace preservation** (a K.μ~ admissibility constraint) and bijectivity — not fixity itself. For example: under K.μ~, for v ∈ dom_L(M'(d)), v = π(u) for some u ∈ dom_L(M(d)) by subspace preservation; M'(d)(v) = M(d)(u) ∈ dom(L) by S3★ at the pre-state; therefore M'(d)(v) ∈ dom(L). No fixity needed. The fixity argument is a clarifying corollary, not the load-bearing premise.

**Required**: Reorganize so that (a) invariant preservation under K.μ~ is verified directly from subspace preservation + bijectivity, and (b) link-subspace fixity is presented as a separately-derived corollary (with its own derivation chain S3★ + K.μ⁺ amendment + CL-UNIQ), not as a precondition for the invariant arguments.

### Issue 4: Notational inconsistency between fields(a).E₁ and subspace_I

**ASN-0047, Notation section and K.μ⁺_L *Shift-lemma applicability***: The Notation section declares that this ASN uses `fields(a).E₁` exclusively and explicitly says "we do *not* employ an alternative `subspace_I(a)` notation." Yet the K.μ⁺_L analysis (and elsewhere) cites ShiftPreservation from ASN-0036, whose postcondition (iv) is stated as `subspace_I(shift(a, k)) = subspace_I(a)`. The reader must silently identify `subspace_I(a) = fields(a).E₁`. The text notes this once in the foundation citation but doesn't carry the identification into subsequent appeals.

**Required**: Either add a one-line bridge "`subspace_I(a) := fields(a).E₁` per ASN-0036's S7c" in the Notation section, or restate ShiftPreservation's postcondition (iv) in this ASN's notation at first citation.

### Issue 5: Fork example's S8-depth parenthetical conflates two conditions

**ASN-0047, Worked example "fork with subsequent insertion", Step "Insert new content into d₂"**: The verification line reads "V-position [1,3] has first component 1 and depth 2, matching [1,1] and [1,2] (S8-depth, non-vacuously: shared first component)." But S8-depth requires uniform depth within a subspace, while "shared first component" is the subspace identifier — these are distinct conditions. The parenthetical conflates them by attaching subspace identity to the S8-depth label.

**Required**: Split into "S8a (positive components: 1, 3 > 0); S8-depth (uniform depth 2 within subspace s_C, matching pre-existing [1,1] and [1,2])."

### Issue 6: D-SEQ★ derivation under-cites D-CTG★'s contiguity formulation

**ASN-0047, *D-SEQ★ derivation*, Step 1 infinite-cardinality argument**: The argument constructs u_M for each M ≥ 2 and concludes "By D-CTG★, every depth-m positive tuple lex-between v_min and an element of V_S(d) — in particular every tuple lex-between v_min and v — lies in V_S(d)." This implicit reading of D-CTG★ as "between any two elements of V_S(d), every valid intermediate tuple is in V_S(d)" is left to the reader to extract from "V_S(d) is contiguous under the V-ordering." Since D-CTG★ is the load-bearing premise of the contradiction, its precise contiguity content (the closed-interval-membership reading versus, say, an open-interval reading) should be stated explicitly at first use.

**Required**: State D-CTG★'s closed-interval-membership content explicitly at the D-SEQ★ derivation: "By D-CTG★, V_S(d) contains every depth-m positive tuple z satisfying v_min ≤ z ≤ v_max for elements v_min, v_max ∈ V_S(d)."

## OUT_OF_SCOPE

### Topic 1: Version-management semantics

The ASN admits K.δ at k=1 with ghost or live document operand but defers the relationship-to-version-graph, content-allocator linkage between versions, and provenance flow across versions. This is correctly deferred to a future version-management ASN, per the explicit Open Question.

### Topic 2: Link withdrawal mechanism

The amendment to D-CTG★/D-MIN★ makes Nelson's tombstoning withdrawal (LM 4/9) inexpressible as any K.μ⁻ contraction. The ASN correctly flags this as a known gap requiring a separate withdrawal mechanism (status flag, tombstone marker, retraction link) outside the present elementary set.

### Topic 3: Account-level k=1 versioning semantics

K.δ excludes `IsAccount(t)` at k=1 by design; admitting it would require account-version semantics not present in the source material. Correctly deferred.

VERDICT: REVISE
