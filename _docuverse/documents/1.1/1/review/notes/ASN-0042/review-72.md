# Review of ASN-0042

## REVISE

### Issue 1: O8's `delegated_{Σ_d}(π, π')` abbreviation is malformed under the transitive-closure binder
**ASN-0042, O8 (IrrevocableDelegation)**: "`(A π, π', a, Σ_d, Σ' : Σ_d reachable from Σ₀ ∧ delegated_{Σ_d}(π, π') ∧ Σ_d →⁺ Σ' ∧ π' ∈ Π_{Σ'} ∧ a ∈ dom(π') ∩ Σ'.B : ω_{Σ'}(a) ≠ π)`"
**Problem**: The Definition of `delegated` fixes the abbreviation rule: "Where a formula already binds a transition `Σ → Σ'`, we write `delegated_Σ(π, π')` ... with that same `Σ'`." The 4-place predicate requires a *single* edge (`delegated(Σ, Σ', π, π')` holds only if `Σ → Σ'`). But O8 binds `Σ'` via `Σ_d →⁺ Σ'` (reflexive-transitive closure), not a single edge. Resolving the subscript form against this `Σ'` yields `delegated(Σ_d, Σ', π, π')`, whose `Σ_d → Σ'` conjunct is false whenever the path has length > 1 — so the antecedent is unsatisfiable exactly in the multi-step case the theorem is meant to cover. The proof body silently repairs this by introducing `Σ_d^{post}` (the introducing successor) and arguing `Σ_d^{post} →* Σ'`, but the formal contract does not. The contract and the proof are using two different objects for `Σ'`.
**Required**: State O8 with an explicit single-step introducing successor, e.g. `delegated(Σ_d, Σ_d^{post}, π, π') ∧ Σ_d^{post} →* Σ'`, and update the formal-contract Preconditions to match. The same care is needed wherever a subscript-form `delegated` sits inside a `→⁺` / `→*` binder.

### Issue 2: The six delegation conditions are stated in full twice
**ASN-0042, State Axioms (O15)** and **Delegation**: O15 lists conditions (i)–(vi) inline; the Delegation section then says "We restate the six conditions here for ready reference" and reproduces (i)–(vi) verbatim with the same glosses.
**Problem**: Two paragraphs in different sections saying the same thing in different words — exactly the pattern the anti-bloat classifier asks to surface. A reader must now keep two copies in sync; they will drift across cycles.
**Required**: Keep the normative statement in one location (the Definition of `delegated`) and have the other site cite it by name without restating the conjuncts.

### Issue 3: Meta-prose justifying document structure rather than advancing claims
**ASN-0042, multiple sites**:
- O15: "Condition (iii) — `π' ∈ Π_{Σ'} ∖ Π_Σ`, the delegate is newly introduced — restates the outer binder as an explicit conjunct so the labels are contiguous." — prose about label numbering, not content.
- PrefixBaptismCoupling closing paragraph: "The named derived property collects the four foundation steps — O14's seventh clause ... O15 ... O18 ... and B0 ..." — a use-site/premise inventory that re-lists what the proof just used.
- DelegatorAllocatesPrefix invariant: "The two-views-of-one-act coupling between the principal and baptismal registries is O18's content; this property locates the single allocator." — restates provenance of the property rather than its statement.
- O17: "The property is load-bearing because `acct(a)` and `N(a)` depend on T4b ... without it, O6's proof ... and O9's proof ... have gaps." — explains *why the axiom is needed* rather than what it says.
- "On registry monotonicity" and "Reachability convention" paragraphs (State Axioms): defensive scaffolding explaining which monotonicity is meant and that contracts "restate the reachability precondition explicitly whenever the proof relies on it."
**Problem**: Each forces the reader to skip past non-advancing prose to reach the actual claim. Compounds across revision cycles.
**Required**: Delete the structural/justification commentary. Where a distinction is genuinely load-bearing (e.g., baptismal- vs allocator-domain monotonicity), state it once as a one-line note at the single point of use, not as a standing paragraph.

### Issue 4: Repeated deferral chains pointing forward to the same later location
**ASN-0042, Worked Example and Delegation**: Numerous "(exercised in *Verifying O8* below)", "(This sub-delegation is exercised in *Verifying O8* below.)", "developed in prose below", "see the Scope note ... below", and the O7(c) recursion deferring detail to the witnessing chain.
**Problem**: Multiple paragraphs deferring to the same downstream site is a flagged accretion pattern; it fragments a single argument across the document.
**Required**: Collapse the cross-pointers — present each sub-result once, at the point it is actually used, rather than announcing it early and discharging it late.

### Issue 5: O2 finiteness step relies on O1b before invoking it
**ASN-0042, O2, Step 3**: "There are at most `#a` possible lengths ... so `|C(a)| ≤ #a`. The covering set is finite."
**Problem**: The bound `|C(a)| ≤ #a` counts *one principal per length*, which requires injective length-to-principal assignment — i.e. O1b. Step 3 does not cite O1b (it is first used in Step 4). As written, without O1b the length argument bounds the number of distinct covering *prefixes*, not covering *principals*; finiteness of `C(a)` would then need FiniteRegistry instead. The conclusion is true but the cited justification is incomplete at the point it is made.
**Required**: Either cite O1b in Step 3 (each length yields at most one prefix, and by O1b at most one principal), or ground Step 3's finiteness on FiniteRegistry and reserve the length argument for Step 4's maximum.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer machinery
**Why out of scope**: The ASN correctly records transfer as an open question (O3 discussion, Open Questions) rather than specifying it — transfer would need a registry external to the address structure, which is genuinely new territory and properly deferred, not an error here.

### Topic 2: Authentication / session-to-principal binding
**Why out of scope**: The Scope note ("Identity is exogenous") frames this as a model boundary and explicitly declines to make a verifiable claim, consistent with the listed out-of-scope item "concrete authentication mechanisms." Correctly handled.

VERDICT: REVISE
