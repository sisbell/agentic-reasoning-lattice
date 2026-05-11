# Review of ASN-0036

## REVISE

### Issue 1: OrdShiftHom lacks a dedicated concrete example
**ASN-0036, OrdShiftHom**: The corollary states three postconditions — `ord(shift(v, n)) = shift(ord(v), n)`, `subspace(shift(v, n)) = subspace(v)`, and unconditional S8a preservation — and derives them from OrdAddHom by instantiating `w = δ(n, m)`. OrdAddHom carries two worked instances (a) and (b) that exhibit the boundary behavior. OrdShiftHom carries none.
**Problem**: The standards specifically call out "no concrete example" as a REVISE item. The derivation of OrdShiftHom from OrdAddHom is correct but the reader is left to do the substitution mentally. A worked instance — e.g., `v = [1, 3, 5]`, `n = 2`, showing `shift(v, 2) = [1, 3, 7]`, `ord(shift(v, 2)) = [3, 7]`, and `shift(ord(v), 2) = [3, 7]` — would mirror the OrdAddHom presentation and make the unconditional-S8a clause (c) concrete.
**Required**: Add a worked instance demonstrating all three postconditions.

### Issue 2: ord and vpos definitions lack worked instances
**ASN-0036, "V-position ordinal decomposition" section**: The definitions of `ord(v)` and `vpos(S, o)` are given as pure sequence manipulations. `w_ord` has a single inline example ("At the restricted depth m = 2, w = [0, c] for positive integer c, and w_ord = [c]"). `ord` and `vpos` have none.
**Problem**: The standards require concrete examples that verify key postconditions. The inverse properties — `ord(vpos(S, o)) = o` and `vpos(subspace(v), ord(v)) = v` — are central to the section and should be exhibited on a concrete instance.
**Required**: Add at least one instance, e.g., `v = [1, 3, 5]`, `ord(v) = [3, 5]`, `vpos(subspace(v), ord(v)) = vpos(1, [3, 5]) = [1, 3, 5] = v`.

### Issue 3: S8 existence proof's invocation of S7c is misplaced
**ASN-0036, S8 proof, Existence section**: "By S3 (referential integrity), `a ∈ dom(Σ.C)`, so S7b gives `zeros(a) = 3` and S7c gives `#E(a) ≥ 2` — the I-address has the structural depth required for shifts to be well-defined and to preserve the I-address subspace identifier `subspace_I(a)`."
**Problem**: This sentence appears inside the Existence section, but the formal contract explicitly states "S7c (`#E(a) ≥ 2`) is *not* a precondition of the existence claim — the singleton witness exhibited in the proof invokes `shift(aⱼ, k)` only at `k = 0` (the identity)." The singleton construction does not invoke any shift at `k ≥ 1` and therefore does not need S7c. Placing S7c here suggests it is load-bearing for existence when in fact it is only used by the subsequent auxiliary lemma.
**Required**: Move the S7c reference to the Auxiliary lemma section where it is actually used, or restructure the Existence paragraph to defer the depth claim until the lemma. The contract already gets this right; the proof body should match.

### Issue 4: S8 never exhibits a non-singleton decomposition
**ASN-0036, S8 proof, Existence section and architectural discussion**: The Existence step constructs `(v, a, 1)` for each `v ∈ dom(M(d))` — every run has length 1. The "non-canonicality" remark acknowledges this is the trivial decomposition. The post-proof discussion then asserts that "non-trivial runs arise when consecutive allocations produce consecutive I-addresses (as T10a and TA5(c) ensure operationally)" and discusses `#runs(d)` and Gregory's performance evidence.
**Problem**: The architectural narrative establishes that coalesced runs are the operationally important case (40% CPU hotspot, abandoned consolidation function). But no concrete example shows a non-singleton run satisfying conjunct (b) `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` at `k ≥ 1`. The auxiliary subspace-preservation lemma is stated for `nⱼ ≥ 2` but is never witnessed. A reader cannot verify that the index-arithmetic identity actually holds in a concrete state.
**Required**: Add a concrete state in which a non-singleton run exists, exhibit conjunct (b) at `k = 1` (and ideally `k = 2`), and verify the auxiliary lemma's `subspace_I(shift(a, k)) = subspace_I(a)` on that instance. The worked example for "hello" creating `1.0.1.0.1.0.1.1` through `1.0.1.0.1.0.1.5` is the obvious candidate — it asserts a single run of length 5 but never demonstrates that `shift([1.0.1.0.1.0.1.1], 3) = [1.0.1.0.1.0.1.4]` actually equals `M(d₁)(shift([1, 1], 3))`.

### Issue 5: The "Auxiliary lemma" claim about subspace_I position lacks explicit verification of field-structure preservation
**ASN-0036, S8 proof, Auxiliary lemma**: "Hence the position of `subspace_I(aⱼ)` lies strictly before the action point of `δ(k, #aⱼ)`. By TumblerAdd's three-region component formula (ASN-0034), every component of `aⱼ` at a position strictly before the action point is copied unchanged into `shift(aⱼ, k) = aⱼ ⊕ δ(k, #aⱼ)`. In particular, the component at position `#aⱼ − δⱼ + 1` is copied unchanged, so `subspace_I(shift(aⱼ, k)) = subspace_I(aⱼ)` for every `k ≥ 1`."
**Problem**: The argument identifies `subspace_I(shift(aⱼ, k))` with `(shift(aⱼ, k))_{#aⱼ − δⱼ + 1}`, which presupposes that the field decomposition of `shift(aⱼ, k)` places its element-field boundary at the same component index as `aⱼ`. This is true (because `shift(aⱼ, k)` differs from `aⱼ` only at position `#aⱼ`, leaving all separator zeros unchanged), but the proof never verifies `zeros(shift(aⱼ, k)) = 3` with separators at the same positions. Without this step, the identification `subspace_I(shift(aⱼ, k)) = (shift(aⱼ, k))_{#aⱼ − δⱼ + 1}` is asserted rather than derived.
**Required**: Add one sentence: `shift(aⱼ, k)` modifies only position `#aⱼ` (per TumblerAdd at action-point `#aⱼ`), so the three separator zeros of `aⱼ` are inherited by `shift(aⱼ, k)` at identical positions, giving `zeros(shift(aⱼ, k)) = 3` and an identical field decomposition. The element-field of `shift(aⱼ, k)` therefore begins at position `#aⱼ − δⱼ + 1`, and `subspace_I` is read off that position.

### Issue 6: ValidInsertionPosition's ternary signature is awkward and underspecified for the empty case
**ASN-0036, ValidInsertionPosition Definition**: "*non-empty case (m determined by state).* When V_1(d) ≠ ∅, m must equal the common V-position depth of V_1(d) fixed by S8-depth; any other value of m makes the predicate false. So in the non-empty case the third argument is functionally redundant... *empty case (m an operational input).* When V_1(d) = ∅, no V-position constrains the depth, so m is an operational parameter chosen by the placing operation."
**Problem**: The predicate's third argument toggles between state-determined and caller-supplied based on the value of the first argument. This is unusual signature design and makes the contract harder to use downstream. More substantively, the contract says "The specific value of m beyond the bound m ≥ 2 is not fixed by the strand model" but then asserts "exactly one value of v satisfies the predicate" per choice of m — leaving operations to choose freely. The open question section asks "What operation-layer constraints determine the canonical choice of m" without resolving whether the strand model imposes any additional constraint. As written, two operations could legitimately choose different m's at the same empty state and produce different valid first-position structures.
**Required**: Either (a) split into two separate predicates `ValidFirstInsertionPosition(d, v, m)` for the empty case and `ValidInsertionPosition(d, v)` for the non-empty case, making the signature asymmetry explicit; or (b) state explicitly that the strand model permits any `m ≥ 2` for the empty case and that S8-depth then locks the chosen value — currently this is buried in prose and not in the formal contract.

## OUT_OF_SCOPE

### Topic 1: Subspace alignment between V-positions and I-addresses
**Why out of scope**: The Remark following S8a explicitly defers this to an operations-layer obligation. The deferral is well-justified — Nelson's prose treats alignment as an operation-level property, Gregory's `acceptablevsa` confirms no state-level check — and the open question section restates the question for future ASNs.

### Topic 2: Whether non-trivial correspondence runs arise from specific operations
**Why out of scope**: This is operation-specific behavior (INSERT preserving run coalescence, etc.) and the scope explicitly excludes operation-specific effects.

### Topic 3: Link-subspace contiguity semantics (tombstones, sparse append)
**Why out of scope**: D-CTG/D-MIN are explicitly bound to text subspace `S = 1`. Link-subspace semantics are deferred to a future ASN as stated in the Remark following S8a.

### Topic 4: Uniqueness/minimality of span decomposition
**Why out of scope**: Acknowledged as an open question; S8 claims existence, not uniqueness.

VERDICT: REVISE
