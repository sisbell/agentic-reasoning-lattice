# Review of ASN-0047

## REVISE

### Issue 1: Path 2 coverage list is incomplete relative to the mutual-exclusivity claim
**ASN-0047, *Three discharge paths for `e ∉ E` — named rules***:
"*Path 2 ...* *Coverage:* (a) the initial ghost-base k = 1 step ... (b) *every* k = 0 sibling allocated downstream of that step in the present transition history, rooted at the ghost-base K.δ event."

Then: "The three paths partition admissible K.δ events ... The premises are mutually exclusive: path 1 requires `InEntityAllocatorDomain(t)`, path 2 requires its negation."

**Problem**: If path 2's premise is `¬InEntityAllocatorDomain(t)` and the three paths partition admissible K.δ events, then path 2 must cover *every* case where `t ∈ E` but `¬InEntityAllocatorDomain(t)`. The explicit coverage list omits at least two such cases that the K.δ preconditions admit: (c) K.δ k = 1 from a ghost-chain document with `t ∈ E_doc ∧ ¬InEntityAllocatorDomain(t)`; (d) K.δ k = 2 from a ghost-chain entity with `t ∈ E ∧ ¬InEntityAllocatorDomain(t)`. Neither is excluded by any precondition (k=1 only requires IsDocument(t); k=2 only requires t ∈ E). So the partition claim and the coverage list are inconsistent.

**Required**: Either expand the coverage list to enumerate all `¬InEntityAllocatorDomain(t)` configurations (k = 0, 1, 2 on ghost-chain operands), or restate the coverage as "all K.δ events with ¬InEntityAllocatorDomain(t)" and present (a)/(b) as exemplars rather than as the enumeration. The current text leaves the discharge mechanism for (c) and (d) unspecified.

### Issue 2: T10a's T2 spawning rule premises are not rigorously discharged for A_v(t)
**ASN-0047, K.δ live-operand k = 1 paragraph**: "A new version sub-allocator `A_v(t)` activated at the K.δ event under T10a's standard spawning machinery, with `parent(A_v(t)) = t`, `spawnPt(A_v(t)) = t`, `spawnParam(A_v(t)) = 1`. T10a's T2 spawning rule (ASN-0034) admits this activation here precisely because `t ∈ E_doc`."

**Problem**: T2 (per ASN-0034's AllocatedSet) requires `parent(A_v(t)) ∈ Act(s)` AND `spawnPt(A_v(t)) ∈ dom_s(parent(A_v(t)))`. With both equal to t, the second clause is `t ∈ dom_s(t)`. Whether dom_s of an allocator contains the allocator's own anchor is not established here — T10a's `dom(A) = {t₀, t₁, …}` typically refers to allocator A's emissions, and conflating the "parent allocator t" with "t in its own emissions" is left implicit. The argument that ghost-base activation fails ("T2's spawnPt premise fails because `t ∉ dom_s(parent(A_v(t)))`") inherits the same ambiguity — it succeeds only if `dom_s(parent(A_v(t)))` is precisely characterized.

**Required**: Explicitly characterize what `parent(A_v(t))`'s tracked domain contains, and verify the spawnPt clause discharges for live t but fails for ghost t. Without this, the path 1 vs path 2 routing for k=1 events rests on an unspecified mapping from documents to T10a allocator roles.

### Issue 3: InEntityAllocatorDomain's formal definition is imprecise
**ASN-0047, K.δ "Two scopes" definitions**: "InEntityAllocatorDomain(t) := t ∈ T ∧ (E A ∈ Act(·) : A is an entity-level allocator ∧ t ∈ dom(A)) ∧ t ∈ E"

**Problem**: "A is an entity-level allocator" is not defined — entity addresses span nodes (zeros=0), accounts (zeros=1), and documents (zeros=2), each with potentially different allocator structures. SubAllocatorAxiom adds A_C(d) and A_L(d) which are content/link sub-allocators (not entity-level). The boundary between "entity-level" and "sub-allocator" is unstated. Additionally `Act(·)` lacks a state argument — should be `Act(s)` for some explicit s.

**Required**: Define "entity-level allocator" formally (e.g., enumerate which allocator kinds are entity-level: the account's document sub-allocator, the parent-document's version sub-allocator A_v, etc., and exclude content/link sub-allocators A_C/A_L from the qualifier). Fix the Act(·) reference to Act at the state under consideration.

### Issue 4: K.μ⁻'s strict-contraction precondition admits a trivial counter to clause B
**ASN-0047, K.μ⁻ precondition**: Clause (B) requires `(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)`.

**Problem**: The quantifier requires existence over `V_S(d) ≠ ∅`. Consider a state where exactly one subspace is non-empty — say V_{s_C}(d) ≠ ∅, V_{s_L}(d) = ∅. The clause demands strict contraction at some non-empty subspace. If the desired K.μ⁻ leaves V_{s_C} unchanged (n'_{s_C} = n_{s_C}), the existential is unsatisfied — but no link-subspace activity is possible either. This is the trivial "no-op" K.μ⁻, correctly rejected. But what about contracting at a *currently-empty* link subspace? That's also impossible (cannot remove from ∅). Either case is correctly handled; the concern is whether the wording captures the intent or leaves a gap. The text says "exhaustive": the case analysis covers (a) suffix, (b) interior hole, (c) prefix hole — all per-subspace. Case (a) at `n'_S = n_S` is "no change" (zero-suffix), which is admissible per-subspace but fails the at-least-one-strict-contraction whole-arrangement gate. This composition is sound but tangled: clause (A) admits no-change per subspace, clause (B) forbids all-no-change globally. The relationship between the case-(a) "zero-suffix" sub-case and clause (B)'s strictness requirement isn't laid out explicitly.

**Required**: Add a worked sub-case showing that case (a) with `n'_S = n_S` (zero-suffix) on every subspace, while admissible by clause (A), violates clause (B) and so is rejected at the whole-arrangement level. This closes the seam between the per-subspace and whole-arrangement admissibility checks explicitly.

### Issue 5: J4 fork composite underspecifies V-position structure of d_new
**ASN-0047, J4 Definition**: "(ii) K.μ⁺ populating M'(d_new) with `ran(M'(d_new)) ⊆ ran(M(d_src))`"

**Problem**: J4 constrains the I-address range but not the V-position structure of d_new. By S8-depth, the new arrangement must have uniform depth within each subspace, but the depth m_{s_C}(d_new) is unconstrained — it could differ from m_{s_C}(d_src). Without correspondence between V-positions of d_new and d_src, the abstract sense in which d_new "displays the same content in the same order" as d_src is unclear. The worked example implicitly chooses matching depth and matching V-positions, but the abstract spec admits any contiguous-from-[s_C, 1, …, 1] choice of arbitrary depth m ≥ 2.

**Required**: Either constrain V-positions of d_new to match d_src structurally (e.g., `M'(d_new)(v) = M(d_src)(v)` for v ∈ V_{s_C}(d_src)), or explicitly state that V-position structure is implementation-defined within the constraints of D-CTG★, D-MIN★, and S8-depth, and discuss the consequences for "version of" semantics.

### Issue 6: K.μ~ table classification mismatches its definition
**ASN-0047, Temporal decomposition table**: The "Elementary transitions" column lists "K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~ (composite)" for M's mutability mode.

**Problem**: K.μ~ is consistently identified elsewhere as a *named composite*, not an elementary transition ("K.μ~ is *not an elementary transition*. It is a *named composite* of K.μ⁻ + K.μ⁺"). The column header is "Elementary transitions"; listing K.μ~ there even with the "(composite)" annotation contradicts the categorization. Either the column heading or K.μ~'s placement should be corrected.

**Required**: Either rename the column to "Transitions modifying this component" or remove K.μ~ from the elementary column and note separately that the named composite K.μ~ also modifies M.

### Issue 7: K.μ~-FIX cites D-SEQ before D-SEQ★ is fully derived
**ASN-0047, K.μ~-FIX paragraph** (under Decomposition of K.μ~): "D-SEQ at the pre-state gives V_{s_C}(d) = {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n}; D-SEQ at the post-state (from K.μ~'s D-CTG and D-MIN postcondition) gives V_{s_C}(d') = ..."

**Problem**: D-SEQ★ is derived from D-CTG★ + D-MIN★ + S8-fin + S8-depth + S8a. But D-SEQ at the *post-state* requires those invariants to *hold at the post-state*, which is part of the K.μ~ admissibility checking itself. The K.μ~-FIX argument depends on D-SEQ at both endpoints, but D-SEQ at the post-state is what we're trying to prove (along with everything else). The acyclicity certificate offered earlier in the ASN handles this for invariant induction, but the K.μ~-FIX argument as stated is presented as a direct derivation, not an inductive one. The role of the inductive hypothesis at the K.μ~-FIX step deserves explicit mention.

**Required**: Either clarify that K.μ~-FIX is consumed inside the induction (D-SEQ at post-state is the post-state goal being established by the same elementary case analysis), or restate the K.μ~-FIX argument to depend only on the K.μ~ contract's stated postconditions (S8a, S8-depth, D-CTG★, D-MIN★) and the inductive hypothesis on the pre-state, making the staging explicit.

## OUT_OF_SCOPE

No items to flag — the ASN respects all listed out-of-scope topics (no named operations, no authority model, no atomicity claims, no implementation mechanics for POOM/enfilade/span index).

VERDICT: REVISE
