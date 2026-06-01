# Review of ASN-0086

## REVISE

### Issue 1: Nullify concludes `a ∈ nullified(Σ')` without gating on P1
**ASN-0086, Definition — Nullify**: "...so R0 at `d_retr` emits the retraction triple ... regardless of whether `a ∈ A_rel^Σ` ... Let `(Σ', _) = Nullify(Σ, d_retr, a)`. By Definition of `nullified`, `a ∈ nullified(Σ')`."

**Problem**: `nullified(Σ') = {a ∈ A_rel^{Σ'} : (E …)}` carries the set-builder restriction `a ∈ A_rel^{Σ'}` (you state this explicitly under Definition — Nullified). The membership `a ∈ coverage(G')` you just established discharges only the existential, not the `a ∈ A_rel^{Σ'}` conjunct. The paragraph deliberately stresses that emission proceeds "regardless of whether `a ∈ A_rel^Σ`," then concludes `a ∈ nullified(Σ')` with no re-invocation of P1. If `a` is a content, document, or ghost address (and `a ≠ b`, the fresh emitter), then `a ∉ A_rel^{Σ'}` and `a ∉ nullified(Σ')` — the stated conclusion is false off the P1 path. R6a, by contrast, is careful here ("By L12a applied to `a ∈ A_rel^Σ`, ... discharging the `a ∈ A_rel^{Σ'}` predicate"); the Nullify derivation should match.

**Required**: Gate the conclusion explicitly on P1: "Under P1 (`a ∈ A_rel^Σ`), L12a gives `a ∈ A_rel^{Σ'}`; together with `a ∈ coverage(G')` this discharges both conjuncts, so `a ∈ nullified(Σ')`." State that the postcondition holds only on the P1 path (consistent with P1's billed role as "establishes the nullification postcondition").

### Issue 2: Redundant frame restatement in the `→` definition
**ASN-0086, State transition relation**: the bullet states "a *K.σ-step* extends `dom(Σ.M)` ... each at a fresh key per its ASN-0093 contract," and the immediately following sentence repeats "each primitive transition extends exactly one of `Σ.C`, `Σ.M`, `Σ.L` at a fresh key and leaves the other two components unchanged."

**Problem**: The two sentences carry the same content (one component extended at a fresh key, others unchanged). Under the anti-bloat classifier this is a "two sentences say the same thing" instance; the reader skips the second to reach the genuinely distinct closure claim ("no removal, replacement, or in-place mutation transition").

**Required**: Collapse to one statement of the frame, retaining only the distinct closure claim that follows.

## OUT_OF_SCOPE

### Topic 1: Retraction stability under categorical (`↝`) transitions
R6a, R6c, and the "audit/active distinction" are proved against `→` (the K-op closure) only; the note explicitly scopes arrangement-modifying and higher-layer transitions out. Whether `nullified` persistence survives arbitrary `↝`-steps issued by future higher layers (and under what consistency model concurrent Observe sees `A_K` transitions) is genuine future territory — already named in the Open Questions — not a defect here.

VERDICT: REVISE
