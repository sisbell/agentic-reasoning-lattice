# Review of ASN-0086

## REVISE

### Issue 1: Definition — Nullify duplicates the wp Case 1 load-bearingness analysis
**ASN-0086, Definition — Nullify**: "this is P0, and discharging K.λ's home precondition is what gates the emission, so P0 is the sole condition controlling whether a →-step occurs" … "Thus P1 gates only the postcondition `a ∈ nullified(Σ')`, not emission."

**Problem**: This multi-paragraph derivation of the P0/P1/P2 *roles* (which condition gates emission, which gates the postcondition, why P2 is absent) is re-run in the wp Case 1 paragraph, which independently establishes that P0 gates execution ("dropping P0 … Nullify does not execute"), P1 gates the postcondition, and P2 is "consequently absent from the wp." Two locations say the same thing in different words — exactly the accretion the anti-bloat classifier flags. A definition slot is not where a gating/load-bearingness derivation belongs.

**Required**: State `Nullify` tersely (the alias plus the three named conditions and their bare meaning). Let the wp Case 1 analysis carry the role-derivation; delete the overlapping prose from the definition.

### Issue 2: wp Case 2 domain restriction asserts a false equivalence
**ASN-0086, wp Case 2, Domain restriction**: "both (i) substrate-conforming *and* (ii) satisfy the unit-depth retraction discipline … — equivalently, Σ reached using only the relational layer's operations."

**Problem**: The equivalence holds in one direction only. Relational-layer-reachability implies both (i) and (ii) (the layer is substrate-conforming and commits to the discipline), but the converse fails: a direct K.λ caller that happens to respect both disciplines reaches states in (i)∧(ii) that are not relational-layer-reachable. The note's own Step 4 of the Worked Sketch exhibits exactly such a direct-K.λ transition from a substrate-conforming, unit-depth-disciplined state. "Equivalently" overstates the set identity.

**Required**: Replace "equivalently" with the correct one-directional gloss (e.g., "in particular, this includes every Σ reached using only the relational layer's operations"), or drop the parenthetical.

### Issue 3: Emit_K's declared domain is broader than the operation's realizability
**ASN-0086, Definition — Emit_K**: "Where Σ ranges over the state-local-conforming sub-space … `Emit_K` is a function over this domain."

**Problem**: R0 itself states that emission can fail over a merely state-local-conforming Σ: "Over a merely state-local-conforming Σ this can fail (Remark — NestedLinkWitness permits an off-chain `ℓ_prev` … so no legitimate K.λ-edge need exist)." Concretely, emit `a'' = inc(t_n, 1)` at the current frontier `t_n` of home `d`; then `max{homed} = a''` is off-chain, `a_emit(Σ,d) = inc(a'', 0)` is not produced by `A_L(d)`, and K.λ's gating precondition fails — no `Σ'` exists. So `Emit_K` is *partial* over the declared domain, total only over the substrate-conforming sub-space. Declaring the domain as the full state-local-conforming sub-space (and the wp Case 1 quantification ranging over it) is inconsistent with this.

**Required**: Either restrict `Emit_K`'s declared domain to substrate-conforming states, or state explicitly that `Emit_K` is partial over the state-local-conforming sub-space and identify the defined sub-domain. The wp Case 1 "domain of quantification" remark should be reconciled accordingly.

### Issue 4: Reduction corollary contains essay prose justifying R7a's presence
**ASN-0086, Corollary (reduction to Emit_K)**: "R7a's contribution is not to this trivial case but to its converse generality … The relational layer is thus the `m = 1` instance of a guarantee R7a establishes for arbitrary `m`."

**Problem**: The corollary proof establishes the reduction in two sentences ("its only state-affecting operations are `Emit_K` and its alias `Nullify` … at `m = 1`, with nothing to decompose"). The remaining prose argues *why R7a is worth having* rather than advancing the reduction — meta-justification of a lemma's relevance, the kind of accretion the classifier asks to surface at source.

**Required**: Trim to the operative reduction. If the "covers composite extensions" point is worth keeping, state it as one clause, not a paragraph contrasting "trivial case" with "converse generality."

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe, and ordering of Observe results
**Why out of scope**: The note correctly defers these to the Open Questions (consistency model for concurrent `Emit`/`Observe`, ordering guarantees on `Observe` results). These are new territory — a concurrency layer — not defects in this ASN's single-threaded `→`-step semantics.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The restriction to standard-triple links is stated and scoped explicitly ("Higher-arity links … are not members of any `L_K`"); the generalization is a future ASN, not a gap here.

VERDICT: REVISE
