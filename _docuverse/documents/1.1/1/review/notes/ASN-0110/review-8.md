# Review of ASN-0110

## REVISE

### Issue 1: Deduplication key in `Eᵢ` left implicit — value or coverage?

**ASN-0110, RE-result / RE-anon**: "`Eᵢ(I, Σ) = {Σ.L(a).eᵢ : (a, i) ∈ W(I, Σ)}`" and "the set comprehension collapses the two identical contributions."

**Problem**: The touching test is keyed on *coverage* (RE-touch), but the returned set `Eᵢ` is a set of *endset values* (span-set representations), and RE-full returns those values verbatim. RE-anon's collapse argument addresses only *identical values*. The non-obvious case is never addressed: two links whose slot-`i` endsets `e ≠ e'` differ as span-sets but satisfy `coverage(e) = coverage(e')` both touch, so `Eᵢ = {e, e'}` returns **both** as distinct members — there is no coverage-keyed deduplication. This is a genuine semantic decision (the membership/identity criterion is by representation, not by coverage), it stands in deliberate contrast to L8's `same_type` which dedups *by coverage*, and it is exactly the kind of derived consequence the operation must pin down since "touch by coverage, return by value" is a surprising asymmetry.

**Required**: State explicitly that `Eᵢ` is deduplicated by endset *value* (span-set), not by coverage; derive the consequence that coverage-equal but representation-distinct endsets are both returned; contrast with L8.

### Issue 2: Empty endsets in non-type slots not covered in the boundary catalog

**ASN-0110, RE-result / RE-role**: the boundary catalog explicitly treats `I = ∅` (RE-zero), the empty store (RE-conform), and a fully-deleted V-region (RE-Vside), but never the empty *endset*.

**Problem**: `Endset = 𝒫_fin(Span)` admits `∅`, and L3 mandates non-emptiness only for slot 3 — slots 1, 2, and any slot `> 3` may be empty. A link may therefore touch `I` through slot 1 while its slot-2 endset is `∅`. The spec's behavior is unambiguous (`coverage(∅) = ∅`, so `touches(∅, I)` is false and the empty endset never enters `E₂`), but the ASN, which is otherwise exhaustive about boundaries, never states it. This leaves a reader unsure whether an empty slot of a touching link is reported in `E₂` (it is not) versus the slot being reported empty-in-position at the tuple level (RE-arity).

**Required**: Add a one-line note that empty endsets (permitted by Endset in non-type slots) never touch and so contribute nothing to their role-family, distinct from the empty-slot-in-position discipline of RE-arity.

### Issue 3: RE-wp mischaracterizes the K.λ precondition

**ASN-0110, RE-wp**: "the `K.λ` precondition `pre ≡ d ∈ dom(Σ.M) ∧ N ≥ 3 ∧ e₃ ≠ ∅ ∧ ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)` (ASN-0093)."

**Problem**: In ASN-0093, K.λ's binding precondition is `d ∈ dom(M)`, that `ℓ` is *produced by `d`'s link sub-allocator `A_L(d)`* (first/subsequent emission — a binding that determines `ℓ_new`), and `N ≥ 3 ∧ eᵢ ∈ Endset ∧ e₃ ≠ ∅`. Freshness `ℓ_new ∉ dom(L) ∪ dom(C)` is **not** a precondition — it is a derived guarantee (FirstEmissionFreshness/SubsequentEmissionFreshness, ASN-0093). RE-wp both promotes the freshness lemma to a precondition and omits the sub-allocator binding that fixes `ℓ_new`. For a weakest-precondition claim about K.λ, the enabling condition should be stated accurately.

**Required**: Restate `pre` as ASN-0093's actual K.λ binding precondition and cite freshness as a lemma the proof invokes, not as a precondition conjunct.

## OUT_OF_SCOPE

### Topic 1: V-space presentation contract, sub/super-region invariants, pairing reconstructibility, link-count relationship, deletion-history indistinguishability

**Why out of scope**: These are correctly deferred to OQ1–OQ5. The lossy V-presentation of a returned endset (OQ1), the sub/super-region invariant beyond additivity (OQ2), the precise boundary of per-link pairing recovery (OQ3), the relationship to link counts (OQ4), and deletion-history indistinguishability (OQ5) are new territory, not defects in this ASN. No action needed.

VERDICT: REVISE
