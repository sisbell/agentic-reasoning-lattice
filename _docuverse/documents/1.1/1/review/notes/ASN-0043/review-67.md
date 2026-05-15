# Review of ASN-0043

## REVISE

### Issue 1: PrefixSpanCoverage cited without a host
**ASN-0043, "Cited Lemma — PrefixSpanCoverage"**: "The lemma is cited as established at that layer; the proof has been removed from this ASN pending the formal introduction of the host ASN... The proof, as it stood here, proceeded by inclusion... and exclusion... entirely from ASN-0034 primitives."

**Problem**: The lemma `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}` is load-bearing for L10 (TypeHierarchyByContainment), L13 (ReflexiveAddressing), and the L8/L9 worked-example coverage computations. It is cited as established, but the host ASN does not exist and the proof was removed. The status "cited but pending relocation" leaves the downstream claims grounded on an unestablished result.

**Required**: Either reinstate the proof here as a derived consequence (the prose says it follows from PrefixRelation, OrdinalShift, NAT-addcompat, T1, Divergence, NAT-discrete — all foundation), or formally axiomatize it in this ASN pending relocation. Citing without a host or a proof is an unfilled hole.

### Issue 2: L1c's "k₁ = 2 only" justification is incorrect
**ASN-0043, L1c, "Why k₁ = 2 is the only kᵢ = 2 step in any conforming chain"**: "k₁ = 1 is structurally unreachable: it would yield t₁ with zeros(t₁) = 2, requiring some downstream kⱼ = 2 to seat the field-separating zero — but that downstream step is foreclosed by the same TA5a argument applied at any j ≥ 2 once zeros first reaches 3..."

**Problem**: The "downstream kⱼ = 2 is foreclosed" argument is wrong. TA5a's precondition is `zeros(tⱼ₋₁) ≤ 2`. If k₁ = 1, then zeros(t₁) = 2, and k₂ = 2 satisfies TA5a — it is *not* foreclosed. The chain k₁ = 1, k₂ = 2 produces a tumbler with zeros = 3. The actual structural obstacle is positional: only `inc(·, 2)` introduces zeros, and `inc(t, 2)` places the new zero at position `#t + 1`. For the third zero of `a` to land at position `#s + 1` (required for `h(a) = s`), the `k = 2` step must fire at `t` with `#t = #s` — i.e., at `t₀ = s`. With `k₁ = 1`, position `#s + 1` of `t₁` is permanently positive (subsequent steps preserve or increment it but never zero it), so the third zero appears at position `≥ #s + 2`, giving `h(a) ≠ s`.

**Required**: Replace the TA5a-foreclosure reasoning with the position-of-zero argument. The first paragraph of the justification (no further k=2 after step 1) is fine; the second paragraph is the muddle. This is load-bearing for L1c's `s = h(a)` postcondition, which is in turn load-bearing for L1a, L11a, and L9's freshness arguments.

### Issue 3: L11a's formal statement is tautological
**ASN-0043, L11a**: "`(A a₁, a₂ ∈ dom(Σ.L) :: a₁ = a₂ ⟺ a₁ and a₂ key the same link entry in Σ.L)`. The forward direction is immediate from Σ.L being a partial function over tumblers... The reverse direction is the substantive claim..."

**Problem**: Both directions of the biconditional are immediate from `Σ.L : T ⇀ Link` being a partial function. Under partial-function semantics, "keying the same entry" can only mean "same key", so the biconditional reduces to `a₁ = a₂ ⟺ a₁ = a₂`. The proof routes through chain-prefix-preservation and per-(t, k') discipline to argue "distinct entries can't share an address" — but this is already given by the type signature. The substantive content the prose intends (link addresses globally unique across creation events) is the GlobalUniqueness consequence of L1c + T10a, but the biconditional doesn't express it.

**Required**: Restate L11a to express its intended content. A candidate: "Distinct allocation events produce distinct link addresses" — a direct corollary of L1c plus T10a's GlobalUniqueness. The current statement is vacuous.

### Issue 4: L0a amends ASN-0036 from within ASN-0043
**ASN-0043, L0a**: "L0a *amends ASN-0036*... no S-invariant... fixes that projection to any single value across the content store. L0a is therefore *new* content beyond ASN-0036... The amendment is recorded here pending its absorption into a future ASN-0036 revision."

**Problem**: L0a is presented as a new state invariant on `dom(Σ.C)` — the content store — that this ASN imposes on ASN-0036's content model. The disjointness derivation `dom(Σ.L) ∩ dom(Σ.C) = ∅` via T7 depends on L0a, so ASN-0043's central claim depends on an axiom the ASN itself acknowledges belongs elsewhere. The "pending absorption" framing is a temporary fix that ships in the released ASN.

**Required**: Either land an ASN-0036 revision that absorbs L0a before this ASN cites it (preferred), or scope the disjointness postcondition to "disjointness of dom(Σ.L) from the s_C-resident portion of dom(Σ.C)" and not the full dom(Σ.C). The current cross-ASN amendment-in-place conflates scopes.

### Issue 5: L9 proof — T4-validity of d' not derived
**ASN-0043, L9 proof, "Selection of d'"**: "By the L9 precondition dom(Σ.M) ≠ ∅, pick any d ∈ dom(Σ.M)... By S7d on Σ, d is a T10a-allocated node in 𝒯... d' is a T4-valid document-level tumbler (zeros(d') = 2)..."

**Problem**: T4-validity of `d'` is asserted but not derived. S7d delivers only "T10a-allocated" plus `zeros(d) = 2`; T4-validity requires citing T10a's root T4-validity axiom and T10a.4 (T4PreservationUnderDiscipline) along `d`'s allocator chain from the root. T4-validity of `d'` is then load-bearing at multiple downstream sites: constructing `g = d'.0.s_X.1`, discharging TA5a's `k = 2` precondition, and applying T7's T4-validity precondition.

**Required**: Add the derivation: "By S7d, d is the terminus of a T10a-conforming allocator chain from 𝒯's root. T10a's axiom fixes the root as T4-valid; T10a.4 propagates T4-validity along each step. Therefore d (= d') is T4-valid."

### Issue 6: L1c chain length and L1b interaction implicit
**ASN-0043, L1c**: "`(A a ∈ dom(Σ.L) :: (E s ∈ T, n ≥ 1, t₀, t₁, ..., tₙ, k₁, ..., kₙ :: ...))`"

**Problem**: L1c admits `n ≥ 1`, but combined with L1b's `#E(a) ≥ 2`, the minimum chain length is `n = 2`: a single `inc(s, 2)` step yields a tumbler with element field `[1]` of depth 1, violating L1b. The interaction is left implicit; readers must derive the actual structural floor.

**Required**: State the joint floor: either tighten L1c to `n ≥ 2`, or note in prose that `n ≥ 1` is L1c's local floor but L1b sharpens it to `n ≥ 2`.

### Issue 7: Worked example — ASN-0036 invariants only spot-checked
**ASN-0043, "Worked Example", "Verification"**: The verification explicitly names only "S3 (ReferentialIntegrity, ASN-0036)" from ASN-0036's invariant set.

**Problem**: The L9 and L11b proofs invoke joint conformance with "all L- and S-invariants" — S0, S1, S2, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. The worked example, which exists to ground the model concretely, doesn't name these. Most are trivial to check (S7b: zeros(c₁) = zeros(c₂) = 3; D-MIN: min(V_1(d)) = [1, 1]; D-SEQ: V_1(d) = {[1, k] : 1 ≤ k ≤ 2}) but their absence makes the example's joint-conformance claim unverifiable by inspection.

**Required**: Add one-line confirmations for at least S7a, S7b, S7c, S7d, S8a, S8-depth, D-CTG, D-MIN, D-SEQ on Σ. The example otherwise is solid; this gap is in completeness, not correctness.

## OUT_OF_SCOPE

### Topic 1: Resolution semantics for ghost type targets
**Why out of scope**: L8 establishes that type matching is by address, and L9 admits ghost targets. The question "what does it mean to `follow` a link whose type is a ghost" is a resolution/operation question that belongs in a future operations-and-effects ASN, not here.

### Topic 2: Self-referential links (link `a` with endset containing `a`)
**Why out of scope**: L13 + L4 admit self-references structurally (no invariant forbids them), and the worked example exhibits link-to-link reference without exhibiting self-reference. Self-reference well-formedness, fixed-point semantics, and termination of resolution would be future-ASN material, not a gap in this ASN's structural contract.

VERDICT: REVISE
