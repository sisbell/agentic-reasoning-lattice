# Review of ASN-0047

## REVISE

### Issue 1: Forward-reference accretion around ValidComposite★ — duplicated skeleton and repeated deferrals
**ASN-0047, *Coupling and isolation* / *Scoped coupling constraints***: "ValidComposite★ (forward pointer). … Validity is defined by ValidComposite★, stated in full in *Scoped coupling constraints* below; its two clauses are (1) … and (2) …" and later "This is the full statement of the two-clause skeleton fixed in the *Coupling and isolation* preamble above".

**Problem**: One concept (ValidComposite★) is stated twice — once as a two-clause skeleton in the forward-pointer paragraph, once in full at its definition — and four to five paragraphs in different sections defer to the same downstream location. Besides the forward pointer itself: P4★ ("stated in full in *Scoped coupling constraints* below"), P4a ("ValidComposite★, per the skeleton fixed … above"), and the K.ρ/K.μ⁺ trigger paragraph ("its full statement and wp derivation appear in *Scoped coupling constraints* below"). This is precisely the flagged forward-reference accretion pattern: the skeleton enumeration is redundant with the full statement, and the reader must skip across sections to assemble one definition. (This is distinct from prior declined sprawl findings — it concerns one duplicated definition, not document size.)

**Required**: Reduce the forward pointer to a single bare reference line (e.g., "validity is ValidComposite★, defined in *Scoped coupling constraints*") and delete the two-clause skeleton enumeration from the preamble, since the full two-clause statement already appears at the definition site. Collapse the per-paragraph "stated in full below" deferrals to the same bare reference.

### Issue 2: J4 step (ii) invariant-discharge list omits S8★ and D-SEQ★
**ASN-0047, *Coupling and isolation*, J4 step (ii)**: "Step (ii) must produce a content-subspace arrangement on d_new … and discharges the per-state arrangement invariants (S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★) at the post-state."

**Problem**: ExtendedReachableStateInvariants lists S8★ and D-SEQ★ as per-state invariants that must hold at *every* reachable state, including the fork's post-state Σ'. J4's discharge enumeration omits both. The matrix elsewhere derives D-SEQ★ from the listed shape invariants and establishes S8★ per-subspace, but J4's general statement neither lists them nor notes their derivation, so the "every invariant conjunct addressed" obligation is not met for the fork composite at the general-statement level (the worked examples verify D-SEQ★ but not S8★).

**Required**: Add S8★ and D-SEQ★ to J4 step (ii)'s discharge list, or append a one-clause note that D-SEQ★ follows from the listed D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a and that S8★ follows from ASN-0036's S8 on the content-subspace projection with S8★(s_L) vacuous (V_{s_L}(d_new) = ∅).

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
**Why out of scope**: The ASN's K.μ⁻ models suffix-only contraction; interior compaction-and-renumbering is correctly deferred as an open question and belongs to a future ASN, not this one.

VERDICT: REVISE
