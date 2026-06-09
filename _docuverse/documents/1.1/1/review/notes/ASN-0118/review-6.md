# Review of ASN-0118

## REVISE

### Issue 1: Resolution machinery reinvents ASN-0058's content-reference algebra
**ASN-0118, "What a spec-set names" / CP0**: defines *V-spec* `ρ = (d_s, σ)`, *spec-set* `R = ⟨ρ₁,…,ρₚ⟩`, and `resolve(R, Σ) = ⟨c₀,…,c_{W−1}⟩`.

**Problem**: ASN-0058 (a foundation) already defines this exact machinery. Its `ContentReference` is `(d_s, σ)` with `σ = (u, ℓ)` a level-uniform V-span; its `ContentReferenceSequence` is "an ordered list `R = ⟨r₁, ..., rₚ⟩` of content references"; and its `Resolution` defines `resolve(d_s, σ)` (reading `M(d_s)|⟦σ⟧`, ordered by V-start, discarding V-coordinates) and `resolve(R) = resolve(r₁) ⌢ … ⌢ resolve(rₚ)`. ASN-0118's V-spec, spec-set, and `resolve` are the same constructs under new names. Per Standard #7, an ASN must use a foundation's definitions rather than reinvent them. The only representational difference is that ASN-0058's `resolve` returns compressed run-pairs `⟨(aⱼ, nⱼ)⟩` while ASN-0118 returns the flat address list — the flat list is just the expansion of the run-pairs, not a new object.

**Required**: Build `resolve(R, Σ)` on ASN-0058's `ContentReference`/`ContentReferenceSequence`/`resolve`, defining the flat sequence as the expansion of ASN-0058's run-pair output. Cite ASN-0058 for the resolution algebra instead of re-deriving it.

### Issue 2: CP0(a) duplicates ASN-0058 C1 (ResolutionIntegrity)
**ASN-0118, CP0(a)**: "Every resolved address already exists. `cᵢ ∈ dom(Σ.C)` for `0 ≤ i < W`, by S3★ applied at each active position."

**Problem**: ASN-0058 C1 (ResolutionIntegrity) already establishes exactly this: "Every resolved I-address is in `dom(C)`: `(A j … : (A i … : aⱼ + i ∈ dom(C)))`." CP0(a) re-proves a foundation result under a new resolution definition. Once Issue 1 is addressed, CP0(a) should cite ASN-0058 C1 rather than re-derive from S3★.

**Required**: Replace the CP0(a) derivation with a citation of ASN-0058 C1 (and C1b for the ordering, C2 for total width if needed).

### Issue 3: Partial-binding behavior is silently decided by `act`, yet listed as an Open Question
**ASN-0118, "What a spec-set names" and Open Questions**: `act(ρ, Σ) = dom(Σ.M(d_s)) ∩ ⟦σ⟧`; Open Question 1 asks "What must COPY guarantee when a named V-span is only partially bound — some positions in the span resolve to content and others to no current binding?"

**Problem**: The definition `act = dom ∩ ⟦σ⟧` already fully decides partial-binding behavior — unbound positions in `⟦σ⟧` are silently dropped, so COPY copies only the bound subset. This collides with two things: (a) the ASN's own claim that a spec-set "designates content *exactly*" (Nelson 4/25) — under partial binding the operation designates only a subset of the named span, not exactly what was named; and (b) ASN-0058's `ContentReference`, whose well-formedness condition `{v : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))` *requires* full binding. So either the V-spec should inherit ASN-0058's full-binding well-formedness condition (and partial binding is genuinely deferred), or the silent-skip semantics is the decision (and the Open Question is mis-stated). As written, the operation is defined on partially-bound spans while the ASN claims that case is unresolved.

**Required**: Either add the full-binding precondition to the V-spec (aligning with ASN-0058) and keep partial binding genuinely out of scope, or state explicitly that `act` resolves partial binding by restriction and remove/reframe Open Question 1 to whatever subtler guarantee remains open.

### Issue 4: S8a of the *placement* positions is attributed to a shift lemma that covers only displaced content
**ASN-0118, displacing-case composite, step (ii)**: "the freshly added V-positions are well-formed (I3-VP)."

**Problem**: I3-VP (ASN-0082) is PostInsertionWellFormedness for *shifted* trailing content. The ASN itself notes that I3 "describe[s] only the shift of trailing content and so do not by themselves establish gap-filling." The placement positions `p + i` are gap-fill, not shifted content, so I3-VP is not the right citation for their well-formedness. Their S8a-ness does hold — `p` is S8a-valid (valid insertion position) and `shift(p, i)` preserves S8a by OrdShiftHom(b) — but the discharge should cite that argument, not I3-VP. K.μ⁺'s precondition explicitly requires the new V-positions (including placement) to satisfy S8a, so this is a real obligation, not bookkeeping.

**Required**: Establish S8a for the placement positions `p + i` via S8a-validity of `p` plus OrdShiftHom (ASN-0036), distinct from the I3-VP citation used for displaced content.

## OUT_OF_SCOPE

### Topic 1: Transclusion into the link subspace
Open Question 6 ("placing a link by reference") is correctly future territory — this ASN scopes placements to `s_C` and need not address `s_L` transclusion.

### Topic 2: Correspondence relation across shared appearances
Open Question 5 (relationship between shared identity and the correspondence relation) is new territory beyond COPY's frame conditions; appropriately deferred.

VERDICT: REVISE
