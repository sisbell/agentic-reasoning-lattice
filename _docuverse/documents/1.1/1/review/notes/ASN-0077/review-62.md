# Review of ASN-0077

## REVISE

### Issue 1: O5★ misapplies the Closure schema's value-preservation grammar

**ASN-0077, Claim O5★ derivation**: "We therefore take as the single-step guarantee the conjunction of two such per-store clauses, `c₁ ≡ [a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]` and `c₂ ≡ [a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L)]`, together with the value-preservation clause `c₃ ≡ [origin'(a) = origin(a)]` at the accessor `origin`."

**Problem**: The Closure schema (★) of ASN-0098 admits value-preservation clauses `f(Σ')=f(Σ)` only with "each accessor `f` well-defined once its accompanying membership clause holds." The accessor `origin(a)` is well-defined only on `dom(C) ∪ dom(L)` — a *disjunction* of two membership clauses, not a single accompanying clause. As stated, `c₃` is unconditional and its accessor's domain is a union, which does not fit the schema's per-clause grammar. The derivation correctly notes the *hypothesis* is disjunctive and case-splits the *conclusion* at the end, but never ties `c₃`'s accessor well-definedness to an accompanying membership clause at the intermediate states — which is precisely what the schema's grammar requires before it may be invoked.

**Required**: Split `c₃` into conditioned per-store clauses (`c₃_C ≡ [a ∈ dom(Σ.C) ⟹ origin'(a)=origin(a)]` and `c₃_L` symmetrically), each carrying its accompanying membership clause, so the accessor is well-defined exactly where the schema demands; then lift the conjunction. Otherwise the schema is being applied outside its stated clause grammar.

### Issue 2: Meta-prose in O5 derivation about an unused fact

**ASN-0077, Claim O5 derivation**: "(The link case is independently strengthened by LP13 (UnconditionalLinkPersistence, ASN-0098), which closes link permanence to multi-step `Σ →* Σ'` and additionally fixes `Σ'.L(a) = Σ.L(a)`; for O5 only the single-step membership-preservation half is consumed.)"

**Problem**: This parenthetical names a foundation fact, states what it additionally provides, and then states it is *not* consumed by O5. It advances no step of the O5 argument — a reader following the proof must skip it. It is defensive meta-prose explaining what is deliberately not used.

**Required**: Delete the parenthetical. If LP13's multi-step strength is needed, it is already invoked at O5★/O11★★ where it does work.

### Issue 3: Duplicated membership-preservation sourcing after O0

**ASN-0077, after Claim O0**: "Membership preservation for `dom(L)` is supplied directly by P3 (ArrangementMutabilityOnly, ASN-0047) ... and by LP13 (UnconditionalLinkPersistence, ASN-0098), which closes link permanence to multi-step `Σ →* Σ'`."

**Problem**: This sentence pre-stages membership preservation that O5 and O5★ then re-derive from the same premises (P3, LP13). Two locations assert the same dependency on the same foundations for the same fact; the post-O0 sentence carries no claim that consumes it locally.

**Required**: Remove the standalone sentence and let O5/O5★ cite P3 (and, for the multi-step case, the lifting lemma) at point of use.

## OUT_OF_SCOPE

### Topic 1: Historical containment via Σ.R
The note correctly defers a complementary operation reporting historical containment (from `Σ.R`) and its coupling invariants to a future ASN. Recorded in Open Questions; no action needed here.

### Topic 2: Surfacing the intermediate transclusion chain
An operation that exposes the chain `d₁ → … → dₙ` rather than the direct origin is named as out of scope and left to a separate operation. Appropriate.

VERDICT: REVISE
