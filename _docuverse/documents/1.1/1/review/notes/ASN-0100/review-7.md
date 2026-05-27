# Review of ASN-0100

## REVISE

### Issue 1: Forced-ordering enumeration omits K.μ⁻ → K.μ⁺

**ASN-0100, §Atomicity and Canonical Order**: "Among the elementary firings, the forced orderings are exactly three, and every other pair commutes at the per-state level"

**Problem**: The claim that all non-enumerated pairs commute is false for K.μ⁻ vs K.μ⁺ in interior insertions. Consider j = 0 (insertion at beginning) with non-empty V_{s_C}(d): shift(p, 0) = p ∈ dom(M(d)) pre-state. If K.μ⁺ fires before K.μ⁻, K.μ⁺ would attempt to add `p ↦ a_0` while pre-state M(d)(p) ≠ a_0, violating K.μ⁺'s functional extension precondition `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))` (ASN-0047). Same conflict arises for any interior insertion (j ∈ {0, ..., N−1}) because at least one Insertion position overlaps pre-state V_{s_C}(d). The "exactly three" enumeration covers only K.α-involving orderings, but K.μ⁻ → K.μ⁺ is a fourth forced ordering whenever K.μ⁻ fires.

**Required**: Add K.μ⁻ → K.μ⁺ as a fourth forced ordering (conditional on K.μ⁻ firing), with the precondition-violation argument above. Alternatively, replace "exactly three" with "the forced orderings involving K.α firings are three" and add a separate clause noting that K.μ⁻ must precede K.μ⁺ for interior insertions because of K.μ⁺'s functional extension precondition.

### Issue 2: "Permanently" overstates the m_C invariant

**ASN-0100, §Sequential text-subspace structure**: "S8-depth — a per-state invariant under ValidComposite★ — fixes `m_{s_C} = m` for `d` permanently; every subsequent text-subspace position in `d` must have depth `m`"

**Problem**: K.μ⁻ is in ValidComposite★'s vocabulary and can shrink V_{s_C}(d) to ∅ (by setting n'_{s_C} = 0; ASN-0047). At such a state, S8-depth holds vacuously, imposing no constraint on m_C. A subsequent INSERT then re-enters ValidFirstInsertionPosition(d, p, m') with caller-chosen m' that need not equal the prior m. So "permanently" and "every subsequent text-subspace position must have depth m" are too strong as stated.

**Required**: Soften to "fixes m_{s_C} = m for d at every state in which V_{s_C}(d) remains non-empty" or "every subsequent text-subspace position must have depth m as long as V_{s_C}(d) does not become empty".

### Issue 3: Relationship between I3 and INSERT's post-state could be sharper

**ASN-0100, §Effect Three and throughout the invariant verification**: The ASN repeatedly cites I3 (PostInsertionShift), I3-V, I3-CS, I3-CX, I3-VD, I3-VP, I3-fin, I3-S2, I3-S3 (ASN-0082) as discharge lemmas, with parenthetical caveats that I3's model is "shift-only" and "structurally smaller" than INSERT's post-state.

**Problem**: I3-V (PostInsertionVacating) and I3-CS (PostInsertionDomainClosureSubspace), if read literally and applied to INSERT's post-state, would assert that the Insertion positions shift(p, k) are NOT in dom(M'(d)) — directly contradicting INS.M-insert. The ASN says these clauses "do not cover" INSERT's post-state but is not explicit that they *fail* against INSERT's M'(d) when read as predicates. A reader checking I3-CS line-by-line might be confused.

**Required**: Add an explicit statement that I3-V, I3-CS, I3-CX describe an alternative (shift-only) operation whose post-state is properly contained in INSERT's, and that these specific clauses do not hold of INSERT's M'(d). The ASN should cite I3 only for its positive shift clause (used directly) and explicitly disclaim the closure/vacating clauses for INSERT's post-state — they are properties of a hypothetical shift-only operation, not of INSERT.

### Issue 4: Cross-subspace D-CTG★ at K.μ⁻ intermediate state for link subspace

**ASN-0100, §Atomicity, "After step 2's K.μ⁻"**: "The link subspace is retained verbatim (`n'_{s_L} = n_{s_L}`), so S8a and S8-depth (with m_L unchanged) inherit from the pre-state on `V_{s_L}(d)`."

**Problem**: The ASN verifies S8a and S8-depth at the K.μ⁻ intermediate for the link subspace, but does not explicitly verify D-CTG★, D-MIN★, and D-SEQ★ for V_{s_L}(d) at the intermediate. While these are preserved by full retention, the ASN's per-state invariant treatment should explicitly note this (the per-state invariants of Class (a) in ASN-0047 include D-CTG★, D-MIN★, D-SEQ★ across both subspaces). A reader auditing the intermediate state's per-state invariants would not find an explicit discharge for the link-subspace forms.

**Required**: Extend the K.μ⁻ intermediate analysis to explicitly note that D-CTG★, D-MIN★, and D-SEQ★ for V_{s_L}(d) are preserved by full retention (since the link subspace is unchanged) — even if obvious, the per-state invariant audit should be complete.

### Issue 5: Worked example does not verify all key postconditions

**ASN-0100, §A Worked Example**: The example instantiates INSERT and verifies INS.M-left, INS.M-insert, INS.M-shift, and INS.inv.seq for the interior case.

**Problem**: The review instructions specify "the ASN should verify its key postconditions against at least one specific scenario from the implementation evidence (e.g., 'INSERT XY at position 3 into ABCDE — check POST1, POST3, POST5 against the result')". The worked example covers the M-effects and D-SEQ★ but does not concretely verify the projection-shift correspondence INS.proj, the discoverability preservation INS.inv.discov, or J0/J1★ couplings against the specific scenario. These are the non-trivial postconditions where verification adds value.

**Required**: Extend the worked example to compute, for a specific link with a specific endset coverage, the pre-state project(ℓ, i, d, Σ) and post-state project(ℓ, i, d, Σ') and verify that they agree under the region-aware shift map π. Show at least one concrete trace of J1★ being discharged (e.g., (a_{new0}, d) ∈ R' but not in R).

### Issue 6: Open Question conflates already-resolved scope

**ASN-0100, §Open Questions**: "Must INSERT operate on values atomically as a sequence, or may an implementation chunk a long insertion into smaller pieces while preserving observable equivalence at the abstract level?"

**Problem**: This question is already answered by the ASN's own specification: an implementation may chunk INSERT into multiple successive INSERTs (e.g., n INSERTs of width 1 instead of one INSERT of width n) only if it provides the composite-atomicity environmental assumption for each chunk separately, but the resulting Σ' will *not* generally equal the Σ' of a single INSERT — the chain emissions interleave with the K.μ⁻/K.μ⁺ steps differently, and intermediate states would observably differ. The ASN's discussion of composite atomicity already constrains this.

**Required**: Remove or refine this open question. It is either resolved (chunking changes observable equivalence at the substrate level) or it should be restated as a precise question about a specific observable property.

## OUT_OF_SCOPE

None to flag — the ASN explicitly scopes out COPY, DELETE, REARRANGE, link-subspace insertion, version derivation, and inter-server replication, all of which match the review's declared OUT_OF_SCOPE topics.

VERDICT: REVISE
