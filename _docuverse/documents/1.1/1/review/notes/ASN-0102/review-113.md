# Review of ASN-0102

## REVISE

### Issue 1: X14's forced-atomicity argument has a non-exhaustive case analysis

**ASN-0102, X14 (Atomicity)**: "in the displacing case COPY is irreducibly atomic: the displacement and the fill must commit together … Either ordering thus exposes an intermediate state that fails a per-state invariant (D-CTG★/D-SEQ★ forward, X6's non-destruction reverse), so ValidComposite★'s clause (1) … cannot be met by any decomposition."

**Problem**: The argument considers only two decompositions — "displace-then-fill" and "fill-then-displace" — and concludes no decomposition can avoid a gap or a destroyed binding. But a third decomposition exists and is valid: **contract-then-extend** (K.μ⁻ then the amended K.μ⁺).

Concretely, for the displacing case (`p ≤ n_S`, `W ≥ 1`):
- **K.μ⁻** retains the content-subspace prefix `n'_{s_C} = p − 1` (full link retention). This is admissible: `p − 1 < n_S` supplies the required strict contraction. The intermediate content subspace is `{[s_C,1,…,1,c] : 1 ≤ c ≤ p−1}` — contiguous from `[s_C,1,…,1]`, so D-CTG★/D-MIN★/D-SEQ★ all hold. No gap.
- **K.μ⁺** (amended) then binds `[p, p+W)` to the copied I-addresses and `[p+W, n_S+W]` to the displaced images `x_p,…,x_{n_S}` (all in `dom(C)`), yielding the exact COPY post-state, contiguous throughout.

No intermediate state has an `s_C` gap, and X6 is not violated — X6 is a property of COPY's *net* effect, not a constraint on intermediate composite states (K.μ⁻ legitimately drops references, exactly as DELETE does; those references are restored by the following K.μ⁺). Provenance is reproducible by appended K.ρ steps under J1★/J1'★. Hence the post-state *is* reachable by a valid composite, contradicting "irreducibly atomic."

**Required**: Either (a) show why contract-then-extend is disallowed (it does not appear to be, under ValidComposite★ clause (1)), or (b) retract the "forced atomicity" claim and justify defining COPY as a single elementary transition on other grounds (e.g., atomicity as a deliberate semantic/modeling choice, not a necessity). As written, the case analysis is incomplete and the conclusion overclaimed.

### Issue 2: X9(b) restates its own content

**ASN-0102, X9 (SourceHandling)**: "(b) … the source document is not unaltered — it is the target, and its content-subspace arrangement is displaced by `· + W`. The guarantee here is not non-alteration but the pre-state pinning … the target-as-source is read at the pre-state `Σ` and is itself displaced by `· + W`."

**Problem**: Two consecutive sentences carry the same two facts ("displaced by `· + W`" / "not unaltered" ≈ "not non-alteration"), worded twice. Anti-bloat: a paragraph saying the same thing in different words.

**Required**: Collapse to one sentence: source-as-target is read at the pre-state `Σ` and is itself displaced by `· + W` (not unaltered).

### Issue 3: X6 and X15 derive the same copied-vs-displaced disjointness

**ASN-0102, X6 (NonDestructivePlacement)** derives "`[v, v+W) ∩ [v+W, n_S+W] = ∅`"; **X15 (PostStateDensity)** re-derives the identical disjointness via the tiling "`[1, p) ∪ [p, p+W) ∪ [p+W, n_S+W]`, with no overlap."

**Problem**: The copied/displaced range-disjointness is established twice in different words. X6's non-destruction conclusion can cite the tiling rather than re-prove the disjointness.

**Required**: Derive the disjointness once (X15 tiling is the natural home) and have X6 cite it, keeping X6 focused on the surviving-binding/non-overwrite conclusion.

### Issue 4: Essayistic phrasing in X11

**ASN-0102, X11 (BoundaryAbsorption)**: "Absorption is therefore a representational economy that never erases identity: the homedoc that conditions it (Gregory Q12) is precisely `origin` …"

**Problem**: The "representational economy that never erases identity" framing is essay content in a structural slot, and "the homedoc … is precisely `origin`" restates X5/X10. It does not advance the merge-candidate reasoning.

**Required**: Drop the framing sentence; the operative content (boundary across differing origins cannot absorb, X10) is already stated.

## OUT_OF_SCOPE

### Topic 1: The four Open Questions (later displacement/discoverability, references-of-references containment, time-varying views, unreachable allocating document)

**Why out of scope**: These concern link discoverability (link semantics), cross-document provenance evolution under further operations, and reachability — all future-ASN territory. They are correctly posed as Open Questions and the ASN defines no claims for them, so no action is needed; flagging only to confirm they are appropriately deferred, not omitted.

VERDICT: REVISE
