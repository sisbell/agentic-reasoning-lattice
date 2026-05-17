# Review of ASN-0086

## REVISE

### Issue 1: R0a antichain corollary terminology inconsistent with worked example

**ASN-0086, R0a's antichain corollary**: "both are siblings in the depth-1 link-element-field allocator at base `d.0.s_L.1`"

**Problem**: The worked sketch consistently refers to the allocator rooted at `d.0.s_L.1` (= `a₁`) as the "depth-2 link-allocator" (e.g., "this spawn creates the depth-2 link-allocator rooted at `a₁`, which we write `A_{a₁}`" and the L1c verification at `b₁`: "within the *depth-2 allocator `A_{a₁}`*"). The R0a corollary's "depth-1 link-element-field allocator" terminology is incompatible: `d.0.s_L.1` has element-field length 2 (E(a₁) = [s_L, 1]), so the allocator rooted at this base enumerates element-field-depth-2 addresses.

**Required**: Replace "depth-1 link-element-field allocator at base d.0.s_L.1" with "depth-2 link allocator at base d.0.s_L.1" or simply "the link allocator rooted at d.0.s_L.1" to match the worked example's terminology and the actual element-field structure.

### Issue 2: R0 Step 2 Case A freshness justification conflates spawn with deposit

**ASN-0086, R0 proof, Step 2 Case A**: "The at-most-once constraint binds the step-(iii) spawn pair `(d.0.s_L, 1)`; Case A's hypothesis — no prior link allocations under `d` — precludes any prior spawn at `(d.0.s_L, 1)`, since any such spawn would have produced an address in `LS(d) ∩ dom(Σ.L)`."

**Problem**: A spawn at `(d.0.s_L, 1)` creates the allocator `A_{d.0.s_L.1}` with `d.0.s_L.1` as its base, but per T10a this places `d.0.s_L.1` in *the allocator's* `dom(A)`, *not* in `dom(Σ.L)`. The address enters `dom(Σ.L)` only when a link emission deposits there. So a prior spawn at `(d.0.s_L, 1)` does *not* directly produce an address in `dom(Σ.L)` — only a prior spawn *plus* a prior link emission would. The note's argument conflates these.

The conclusion (freshness of `a`) holds for a cleaner reason: Case A's hypothesis directly gives `home(a) = d` and `{a' ∈ dom(Σ.L) : home(a') = d} = ∅`, hence `a ∉ dom(Σ.L)`, regardless of whether the spawn previously occurred. Whether `(d.0.s_L, 1)` has been spawned is orthogonal — the L1c chain witnesses *some* T10a-conforming reachability of `a`, and if the spawn has occurred the chain re-traces it without re-issuing it.

**Required**: Replace the "precludes any prior spawn" argument with the direct deduction `a ∉ dom(Σ.L)` from Case A's hypothesis + `home(a) = d`, and note that the L1c chain can witness an already-occurred or about-to-occur spawn equivalently (consistent with the substrate primitive's "L1c chain is required to exist as a conformance witness on Σ; it is not required to be operationally re-traversed by the emission" framing earlier in the note).

### Issue 3: Nullify's choice of home(a) is a convention without justification

**ASN-0086, Definition of Nullify**: "`Nullify(Σ, a) ≡ Emit_R(Σ, home(a), ∅, {(a, δ(1, #a))})`"

**Problem**: Nullify fixes the retraction tuple's home document at `home(a)` without explanation. By L4 (EndsetGenerality) and L11a, endset spans may reference any tumbler addresses including across documents — there is no substrate-level requirement that a retraction be sited at the target's home. Alternative choices (a caller-supplied `d_retr ∈ dom(Σ.M)`, a system-wide retractions document, the calling user's owned document) are all admissible by the substrate, and would preserve R6's single-tuple-scope argument equally well (the antichain conclusion of R0a applies within whatever document the retraction is homed at). The note's R6 single-tuple-scope argument depends only on R0a's antichain + P3 + subspace-distinctness — not on `home(retraction) = home(target)`.

The omission matters because downstream readers may interpret the home choice as a substrate guarantee rather than a convention, and the operation's signature gives no parameter for caller selection.

**Required**: Either (a) acknowledge `home(a)` as a convention motivated by locality/audit ergonomics, with a note that the substrate admits other home choices and that Nullify is a *standard form* among admissible retraction shapes; or (b) generalize Nullify's signature to `Nullify(Σ, d_retr, a)` with `d_retr ∈ dom(Σ.M)` as caller-supplied (and document why the `home(a)` form remains the canonical instantiation). Either way, the design choice should be visible.

### Issue 4: R5's "no opposing invariant" enumeration omits ASN-0036 and ASN-0034 invariants

**ASN-0086, R5 Stage 2**: enumerates all ASN-0043 L-invariants (L-fin, L0, L0a, L1, L1a, L1b, L1c, L2, L3, L4(c), L5, L6, L7, L8, L9, L10, L11a, L11b, L12, L12a, L12b, L13, L14, L14a) plus "The R-properties already derived (R0–R4) similarly impose no restriction on what addresses an emitted endset may contain."

**Problem**: ASN-0036 (S0, S1, S2, S3, S5, S7a–d, S8a, S8-fin, S8-depth, S9, D-CTG, D-MIN, D-SEQ) and ASN-0034 (tumbler-algebra invariants) are not enumerated. While each of these is genuinely orthogonal to link-endset content (their scope is content/arrangement/tumbler-algebra, not link endsets), the "no opposing invariant" argument is exhaustive only if every invariant in scope is checked. A careful reader following R5's pattern would expect a one-line acknowledgment that the other foundation ASNs' invariants are orthogonal by scope.

**Required**: Add a single concluding sentence to R5 Stage 2 — e.g., "ASN-0036 invariants (S0–D-SEQ) scope to `(Σ.C, Σ.M)` and ASN-0034 invariants scope to the tumbler algebra; neither references link-endset content, so they are orthogonal to the construction by scope."

## OUT_OF_SCOPE

### Topic 1: Determinism of Emit_K's b-choice in Case B

**Why out of scope**: Emit_K under R0 Step 2 Case B selects "any existing link b ∈ dom(Σ.L) with home(b) = d," and different b-choices can yield different `a = inc^i(b, 0)` when the sibling stream has gaps. R0a's antichain holds for any b-choice, so the R-properties are unaffected, but Emit_K's operational behavior is not deterministic without a specific b-selection rule (udanax-green uses "lowerbound + 1"). A future implementation-discipline ASN could pin this down; it doesn't belong here.

### Topic 2: Active-subset machinery for higher-arity links

**Why out of scope**: The note explicitly scopes L^Σ to standard-triple (arity-3) links and acknowledges that higher-arity links exist in `dom(Σ.L)` but are outside any `L_K`. Extending A_K to multi-arity relations `A_K^{(n)}` is appropriately deferred to the open question on multi-arity links.

### Topic 3: Cross-document retraction protocols and authorization

**Why out of scope**: Who is authorized to emit retractions, whether retractions of cross-document tuples require coordination, and whether subtree-broad retractions ("Crafted-span retractions" in the Nullify section) should be permitted by policy — all are policy-layer questions above the substrate. The note correctly admits subtree-broad retractions as substrate-permissible and notes that authorization is layered above.

VERDICT: REVISE
