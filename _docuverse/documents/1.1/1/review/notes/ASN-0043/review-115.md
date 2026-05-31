# Review of ASN-0043

## REVISE

### Issue 1: Symbol `ℓ` is reused within L9 for two different objects
**ASN-0043, L9 (TypeGhostPermission)**: the formal statement binds `(s, ℓ) ∈ Σ'.L(a).type` — where `ℓ` is a span's *length* tumbler — yet the witness paragraphs then write "the padded payload" and "For the payload `ℓ = (∅, ∅, {(g, δ(1, #g))}, ∅, ..., ∅)`", reusing `ℓ` for the entire *link tuple*.

**Problem**: Within a single lemma the same symbol denotes a span-length tumbler (in the quantifier) and an `N`-tuple of endsets (in the proof). The two are different types. The bound `ℓ` in the formal statement is also vestigial — only `s` appears in the matrix `|Σ'.L(a)| = N ∧ s ∉ dom(Σ'.C) ∪ dom(Σ'.L)`, so the length component is bound but never read. A precise reader must disambiguate by type on each occurrence. The same lemma additionally overloads `s` (span start in the quantifier) against the L1c seed `s` and the subspace constants `s_C, s_L, s_X`.

**Required**: Rename the payload tuple in L9's proof (e.g. to `ℓ_g` or reuse the `ℓ`-as-payload convention used in FSP only, and pick a distinct length symbol in the span pair). Either drop the vestigial length binding (`(s, _)` / nest an inner existential) or give it a non-colliding name. The fix is mechanical but the collision is a genuine clarity defect in a formal statement.

## OUT_OF_SCOPE

### Topic 1: Whether a conforming link must carry at least one non-empty content endset
L3 requires only `Σ.L(a).e₃ ≠ ∅`; slots 1 and 2 may both be empty, so `(∅, ∅, Θ)` is conforming — and L9 in fact uses exactly this degenerate link as its existential witness. Whether a link connecting *nothing* to *nothing* (carrying only a type) should be admitted, or whether a future invariant should require `F ≠ ∅ ∨ G ≠ ∅`, is a design refinement.
**Why out of scope**: The model deliberately permits the empty endset (Endset definition; Nelson's "inane"/heading-link case under L7). Constraining it is new territory, not an error in this ASN.

VERDICT: REVISE
