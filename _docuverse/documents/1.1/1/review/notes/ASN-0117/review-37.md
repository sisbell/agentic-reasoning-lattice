# Review of ASN-0117

This ASN is in strong shape. The two-realisation split (K.μ⁻ + K.μ⁺ composite when `R ≠ ∅`, lone K.μ⁻ when `R = ∅`) is correctly forced by K.μ⁺'s strict-extension precondition; the coupling discharge (J0, J1★, J1'★ evaluated initial-to-final) is sound, with J1★'s range-based trigger correctly shown false for every survivor; the wp derivation's range identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` checks out, including the SD-based disjointness step and the per-link (not per-slot) quantifier structure; the boundary cases (leading-span delete with empty-then-repopulated subspace, suffix delete, delete-everything, within-document sharing, cross-document transclusion, multi-position suffix shift) are all exercised concretely; and the S8★ re-cut paragraph does genuine work, supplying S8's preconditions conjunct by conjunct at the post-state. I verified the K.μ⁻ retention-count arithmetic (`J − 1 < N` for `R ≠ ∅`; `n'_{s_C} = N − c < N` for `R = ∅`) and the intermediate-state precondition discharge for both steps. The anti-bloat scan found no defensive meta-prose rising to a finding: the notational-convention paragraph, the count-vs-pair parenthetical under DEL-REMOVE, and the quantifier-structure paragraph in the wp section all carry proof-relevant content. One notation defect remains.

## REVISE

### Issue 1: `ord(w)` applies a V-position operator to a displacement; the foundation already names this object `w_ord`
**ASN-0117, §"What shifts, and what the shift must preserve" and DELETE *Precondition***: "write `c = ord(w)` for the count of deleted slots" and "`Pos(w)`, with `c = ord(w) ≥ 1`"
**Problem**: ASN-0082's OrdinalExtraction defines `ord(·)` for a *V-position* `v` with `#v = m ≥ 2` — and `w` is not a V-position: it has `w₁ = 0`, which S8a excludes. The foundation provides a separate definition for precisely this case, OrdinalDisplacementProjection (`w_ord = [w₂, …, wₘ]` for displacements with zero first component), and this ASN itself uses `w_ord` in the same section (`σ(v) = vpos(S, ord(v) ⊖ w_ord)`, `ord(r) ⊖ w_ord = ord(p)`). The result is two notations for one object, one of which applies a function outside its declared domain — exactly the discipline the ASN's own well-definedness remark ("establishing that an argument is in a function's domain before using it") invokes. There is also a silent type coercion: `ord(w)` would be the singleton tumbler `[c]`, while `c` is used as a natural number; the singleton-to-natural identification exists in the foundation (ASN-0084, OrdinalStripping) but is licensed there for V-position ordinals at depth 2, not invoked here.
**Required**: Define the count directly from the displacement's components — since the precondition already fixes `#w = 2` and `w₁ = 0`, the cleanest form is `c = w₂` (equivalently `w = [0, c]`, so `w_ord = [c]` per ASN-0082's OrdinalDisplacementProjection, identified with `c` by ASN-0084's depth-2 convention). Remove both occurrences of `ord(w)`.

## OUT_OF_SCOPE

### Topic 1: Deletion in the link subspace
**Why out of scope**: DELETE is specified for `S = s_C` only, matching the foundation contraction (ASN-0082 is stated for `S = 1`). Un-arranging a link V-position from a document (the K.μ⁻ vocabulary admits `n'_{s_L} < n_{s_L}`) is genuinely new territory — it interacts with CL-OWN/CL-UNIQ and with link discoverability in a way no foundation contraction covers — and belongs in a future ASN, not in this one.

### Topic 2: Text deletion at V-position depth `m > 2`
**Why out of scope**: The foundation contraction (ASN-0082) carries the precondition `#p = 2`, and this ASN correctly inherits it. Generalising the left-shift to deeper text subspaces (where D-CTG-depth's shared-prefix reduction governs) requires new foundation work first; its absence here is not an error.

VERDICT: REVISE
