# Review of ASN-0036

## REVISE

### Issue 1: OrdAddS8a contract carries a redundant precondition inconsistent with OrdAddHom

**ASN-0036, OrdAddS8a Formal Contract**: "Preconditions: v ∈ T satisfying S8a, #v = m ≥ 2; w ∈ T, Pos(w) (TA-Pos, ASN-0034), #w = m, w₁ = 0, actionPoint(w) ≤ m."

**Problem**: The precondition `actionPoint(w) ≤ m` is automatic. ActionPoint's contract in ASN-0034 supplies `1 ≤ actionPoint(w) ≤ #w` for any w with Pos(w); combined with `#w = m`, this forces `actionPoint(w) ≤ m` without further hypothesis. The adjacent OrdAddHom contract explicitly notes and removes this redundancy: "The bound actionPoint(w) ≤ m is not stated separately: ActionPoint's contract in ASN-0034 already gives 1 ≤ actionPoint(w) ≤ #w, and #w = m then forces actionPoint(w) ≤ m." The inconsistency between the two adjacent lemma contracts is a minor but real defect.

**Required**: Either remove the redundant precondition from OrdAddS8a with the same parenthetical note OrdAddHom uses, or restore it to OrdAddHom — pick one convention.

### Issue 2: S7's Well-definedness step uses T4b's projections without explicitly establishing T4-validity

**ASN-0036, S7 proof, Well-definedness paragraph**: "By S7b (element-level I-addresses), every a ∈ dom(Σ.C) satisfies zeros(a) = 3. By T4 (HierarchicalParsing, ASN-0034), zeros(a) = 3 means a contains exactly three zero-valued field separators, and the partial projections supplied by T4b (UniqueParse, ASN-0034) — N(a), U(a), D(a), E(a) — extract the node, user, document, and element fields respectively..."

**Problem**: T4b's *Postconditions* in the foundation explicitly say "`dom(N)` is the T4-valid subset of `T`" — the projections are defined only on T4-valid tumblers, not on every tumbler with `zeros = 3`. The mere count `zeros(a) = 3` does not establish T4-validity (which also requires no adjacent zeros, `a₁ ≠ 0`, and `a_{#a} ≠ 0`). The proof glosses over the necessary derivation: T4-validity comes from S7a + T10a.4 (T4PreservationUnderDiscipline, ASN-0034), which establishes that every output of a T10a-conforming allocator satisfies T4. Without this step, the projections are unjustified on the *zeros = 3* subset; with it, the chain `a ∈ dom(C) → allocated under T10a → T4-valid (T10a.4) → T4b applies` closes cleanly.

**Required**: Insert a sentence in S7's Well-definedness paragraph explicitly invoking T10a.4 between "zeros(a) = 3" and "the partial projections supplied by T4b... are defined." Adding `T10a.4` to the *Depends* list of S7 — currently cites T10a but not the specific postcondition — would parallel the level of explicitness used elsewhere (e.g., GlobalUniqueness is cited specifically).

### Issue 3: S8's contract postcondition asserts subspace preservation under shift but the proof does not address the k ≥ 1 case

**ASN-0036, S8 Formal Contract Postconditions**: "For each run, `shift(aⱼ, k)` preserves the I-address subspace `subspace_I(aⱼ)` — by S7c, the action point of `δ(k, #aⱼ)` falls strictly after the position of `subspace_I(aⱼ)`, so TumblerAdd copies the subspace identifier unchanged."

**Problem**: The proof of S8 produces only the trivial singleton decomposition (nⱼ = 1, so the only value of k is 0, for which `shift(aⱼ, 0) = aⱼ` trivially). The subspace-preservation claim is therefore *vacuous in the proof actually given* — no k ≥ 1 case is exercised. The contract's auxiliary claim about non-trivial shifts is asserted but unused, leaving the reader to verify the cited geometry (action point #aⱼ falls strictly after the position #aⱼ − #E(aⱼ) + 1 of `subspace_I(aⱼ)`, requiring #E(aⱼ) ≥ 2 from S7c) without help. Either the proof should verify the k ≥ 1 case in an "if a longer run existed, it would still satisfy this" form, or the postcondition should be hedged to the singleton case actually established.

**Required**: Add an explicit one-paragraph derivation that for any aⱼ with `zeros(aⱼ) = 3` (S7b) and `#E(aⱼ) ≥ 2` (S7c) and any k ≥ 1, the action point of δ(k, #aⱼ) is `#aⱼ` and the position of `subspace_I(aⱼ)` is `#aⱼ − #E(aⱼ) + 1`, so the inequality `#aⱼ − #E(aⱼ) + 1 < #aⱼ` (equivalent to `#E(aⱼ) ≥ 2`) places the subspace identifier strictly before the action point, and TumblerAdd's prefix-copy rule preserves it.

### Issue 4: D-CTG-depth's construction at j = m − 1 elides a check on the n bound that uses T0(a)'s exact statement

**ASN-0036, D-CTG-depth proof**: "By T0(a) (UnboundedComponentValues, ASN-0034), unboundedly many values of n > (v₁)ⱼ₊₁ exist."

**Problem**: T0(a)'s actual postcondition is component-positional: "for every tumbler t, every component position i, and every bound M, there exists t' agreeing with t at all positions except i where t'.dᵢ > M." Here the proof is asserting the *cardinality* of integers exceeding (v₁)ⱼ₊₁, not the existence of a single witness. The cardinality claim follows from the *iterative application* of T0(a) (or more directly from NAT-discrete + NAT-wellorder), but the proof says "By T0(a)" without bridging from "for every bound M, some t' exceeds M" to "infinitely many values of n > (v₁)ⱼ₊₁ exist." The infinitely-many step is what produces the contradiction with S8-fin.

**Required**: Either cite the appropriate foundation property for unboundedly many ℕ values exceeding a given bound (NAT-wellorder plus an injection argument, or just an explicit construction: the map `M ↦ M + 1` is injective on ℕ and produces values ≥ M + 1 for each M), or rephrase to make the appeal less direct ("T0(a) supplies a witness exceeding any chosen bound, and distinct n yield distinct w by T3, so the resulting set is infinite").

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG, D-MIN, S8a under DELETE/INSERT/COPY/REARRANGE
**Why out of scope**: The ASN explicitly defers operation-specific preservation to each operation's own ASN ("Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN"). The strand model is correctly bounding itself to state-level invariants.

### Topic 2: Subspace alignment between V-positions and their target I-addresses
**Why out of scope**: The Remark following S8a explicitly defers subspace alignment to operations-layer preservation obligations, citing Gregory's evidence (`acceptablevsa` unconditionally true) and Nelson's framing (alignment as a property of specific operations, not arrangements).

### Topic 3: Link-subspace (S = 2) contiguity, minimum-position, and sequential structure
**Why out of scope**: The ASN explicitly binds D-CTG, D-MIN, D-CTG-depth, D-SEQ, and ValidInsertionPosition to the text subspace S = 1; link-subspace semantics (sparse, append-only with tombstones) are deferred to a future ASN.

### Topic 4: Existence of non-trivial (length > 1) correspondence runs under operational regimes
**Why out of scope**: The ASN's Non-canonicality remark and Open Questions both note that conditions producing multi-element runs are operations-layer guarantees, not strand-level theorems. The S8 theorem correctly asserts existence-of-some-decomposition; canonicality is deferred.

### Topic 5: Specific value of m in the ValidInsertionPosition empty case
**Why out of scope**: The ASN explicitly leaves the choice of m beyond `m ≥ 2` to operations-layer convention (citing Nelson's "subdivision by further digits" as deliberately unfixed).

### Topic 6: Subtraction homomorphism for ord — `ord(v ⊖ w) = ord(v) ⊖ w_ord`
**Why out of scope**: Listed as an Open Question, deferred because TA7a's conditional S-membership for subtraction (TA7a.1–TA7a.3) makes the formulation non-trivial; appropriate to defer to a future ASN.

### Topic 7: Computability cost of the sharing inverse
**Why out of scope**: Listed as an Open Question about implementation cost bounds, which is implementation/representation concern rather than abstract invariant.

VERDICT: REVISE
