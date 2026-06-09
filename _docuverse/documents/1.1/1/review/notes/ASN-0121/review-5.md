# Review of ASN-0121

## REVISE

### Issue 1: The "forced" derivation of FL-DEF has slack — soundness does not exclude nullified links

**ASN-0121, "The answer is forced"**: "*Soundness*: `(A a : a ∈ R : sat(a, q, Σ))` — nothing returned fails a criterion. ... The weakest predicate on an addressable link that soundness *permits* into `R` is `sat(a, q, Σ)`; the predicate that completeness *forces* into `R` is the same `sat(a, q, Σ)`. The two demands meet with no slack between them, leaving no design freedom."

**Problem**: Soundness as stated constrains only `sat`, not addressability. Retraction is not one of the four matching criteria, so a *nullified* link `a` with `sat(a, q, Σ)` true does "satisfy a criterion" and is permitted into `R` by soundness; completeness does not force it in but also does not forbid it. Hence both

- `R_min = {a ∈ addressable(Σ) : sat(a, q, Σ)}`, and
- `R_max = {a ∈ dom(Σ.L) : sat(a, q, Σ)}` (including nullified satisfying links)

satisfy the two stated demands. The result is therefore **not** uniquely forced; there is exactly the design freedom of whether to return retracted-but-satisfying links — precisely the freedom FL-DEF is meant to close (Nelson's "not currently addressable"). The phrase "the weakest predicate on an addressable link that soundness permits" silently assumes `R ⊆ addressable(Σ)`, a restriction never demanded.

**Required**: Add the demand that a candidate answer return only currently addressable links — either a third requirement `R ⊆ addressable(Σ)`, or strengthen soundness to `(A a : a ∈ R : a ∈ addressable(Σ) ∧ sat(a, q, Σ))`. With that, `R_min = R_max` and FL-DEF is genuinely forced.

### Issue 2: FL-CUR's biconditional does not follow from FL-SND ∧ FL-CMP alone

**ASN-0121, FL-CUR**: "This is the conjunction of FL-SND (`a ∈ findlinks(q, Σ) ⟹ sat(a, q, Σ)` — no returned link fails) and FL-CMP (`a ∈ addressable(Σ) ∧ sat(a, q, Σ) ⟹ a ∈ findlinks(q, Σ)` ...); the two implications compose into the biconditional".

**Problem**: The forward direction of the biconditional `a ∈ findlinks(q, Σ) ⟹ a ∈ addressable(Σ) ∧ sat(a, q, Σ)` requires `a ∈ findlinks ⟹ a ∈ addressable`. FL-SND supplies only the `sat` conjunct; the `addressable` conjunct comes from FL-DEF's set-builder (`result ⊆ addressable`), not from FL-SND. As stated, composing the two implications yields only `membership ⟹ sat` and `addressable ∧ sat ⟹ membership`, which is not the claimed biconditional. This is the same root cause as Issue 1 (soundness omits addressability).

**Required**: Cite FL-DEF (or the strengthened soundness from Issue 1) for the `a ∈ findlinks ⟹ a ∈ addressable` step, rather than attributing the full forward implication to FL-SND.

## OUT_OF_SCOPE

(none — the deferred topics in "Open Questions," including version-qualified inquiry, the V-spec/I-address agreement invariant, and cross-store federation, are appropriately marked as future work rather than claimed here.)

VERDICT: REVISE
