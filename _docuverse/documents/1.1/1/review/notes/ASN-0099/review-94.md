# Review of ASN-0099

The specification is technically strong: every operation in the operative vocabulary `V` is accounted for (F9 covers `V ∖ {K.λ}`, F9-λ covers `K.λ`), the V-side discoverability is correctly framed as a weakest precondition rather than an overclaimed persistence theorem (F21–F23), boundary cases (`I = ∅`, `dom(Σ.L) = ∅`, empty constraint set/target, empty scope) are handled, and the worked example exercises the load-bearing claims against concrete states. The findings below are anti-bloat and clarity items, not correctness defects.

## REVISE

### Issue 1: F4 Strengthening 1 uses an over-engineered witness
**ASN-0099, F4 (MatchIndividuation), Strengthening 1**: "Witness link `a`: arity 3 with slot 1 `(β, δ(1, #β))`, slot 2 `(γ, δ(1, #γ))`, slot 3 `(α, δ(1, #α))`, where β and γ are same-length siblings of `α` ... we check every slot: slot 1's coverage ... slot 2 likewise; slot 3's coverage ... contains `α.0 ∉ I`."

**Problem**: The design point — that "`coverage ⊆ I`" disagrees with F1's overlap test — is established by the minimal one-slot witness already used in Strengthenings 2 and 3: slot 3 `(α, δ(1, #α))`, slots 1–2 empty, `I = {α}`. F1 admits (`α ∈ coverage(e₃) ∩ I`); the alternative rejects because `coverage(e₃) = {t : α ≼ t} ∋ α.0 ∉ {α}`. The `β, γ` sibling machinery and the slot-1/slot-2 checks add no reasoning — they are redundant verification of slots that play no role in the disagreement. This is exactly the "exhaustiveness claim" pattern the anti-bloat pass targets, and it is inconsistent with the adjacent witnesses that use the minimal form.

**Required**: Replace Strengthening 1's witness with the one-slot construction (matching Strengthenings 2/3), or state explicitly why the multi-slot form is needed for this strengthening specifically. If there is no such reason, drop slots 1–2 and their per-slot checks.

### Issue 2: Imprecise "V-extents partition R ∩ dom(Σ.M(d))"
**ASN-0099, "The Image Set"**: "ASN-0058's mapping-block decomposition gives the image as a union of I-runs, one per maximal correspondence run, whose V-extents partition `R ∩ dom(Σ.M(d))` (B2, ASN-0058)."

**Problem**: B2 (Disjointness) and B1 (Coverage) partition `dom(M(d))`, not `R ∩ dom(M(d))`. When `R` is a contiguous V-span that cuts a maximal run, that run's *V-extent* extends outside `R`, so the full V-extents do not partition `R ∩ dom(M(d))` — only their restrictions to `R` do. As written the citation overstates what B2 delivers.

**Required**: Either restrict to the run-intersections (`V(βⱼ) ∩ R partition R ∩ dom(M(d))`) or soften the prose to "the runs intersecting `R` cover `R ∩ dom(M(d))` disjointly," and cite B1+B2 rather than B2 alone.

## OUT_OF_SCOPE

### Topic 1: Combined `findlinks_filtered_scoped(C, S, Σ)` and the K.λ-to-query latency bound
**Why out of scope**: Both are correctly listed in the ASN's own "What We Have Not Specified" / "Open Questions" sections. The filtered and scoped forms are each fully specified with their F2∧F3 and F15 transfer obligations; their composition is a future increment, not a gap in this ASN. The latency bound is a temporal-model concern outside this state-transition specification.

### Topic 2: Standalone K.μ⁺ V-side effect on `findlinks_V`
**Why out of scope**: The ASN deliberately characterizes the dangerous (contracting) V-side case via F21 and the composite via F23; standalone extension is benign-monotone and follows directly from LP9. A dedicated claim would be additive, not corrective.

VERDICT: REVISE
