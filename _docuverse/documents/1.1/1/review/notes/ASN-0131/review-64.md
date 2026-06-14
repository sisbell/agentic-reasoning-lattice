# Review of ASN-0131

I checked the definition, every introduced claim, the worked instance, the algebraic laws, and the stability arguments. The note is, with one exception, sound and unusually thorough: the worked-example arithmetic checks out (`shift(a₂,2)=a₄`, `coverage(e₁)⊇{a₂,a₃,a₄}`, the field-agreement disjointness of `e₃`); RE-ADDR's antichain/prefix argument is correct; the union proof and the `⊆` half of intersection are correct and unconditional; both intersection counterexamples (non-injective and injective) are valid and the "no arrangement restriction suffices" diagnosis is justified (the split-witness obstruction lives at the endset's coverage, which arrangement restrictions cannot reach); RE-CWP's weakest precondition is algebraically correct and its strict refinement of D-CWP is real; RE-RET's biconditional holds under its two stated conditions (R-Scope confines the fresh nullification to the target, so other bearers survive); and the `Σ.L`-evolution bridge correctly licenses importing ASN-0086's ∀-reachable lemmas across the vocabulary gap. The content-subspace restriction, decidability, and boundary cases (RE-BND) are all handled.

One precision flaw remains.

## REVISE

### Issue 1: Open Question 4 asks for the condition the body has already given exactly

**ASN-0131, "Composing regions" / RE-UDIST-∩ / Open Question 4**:

Body: "`⊇` — and hence equality — holds *exactly* when `(∀ (i, e) ∈ Avail(Σ) : touch_{W₁}(e) ∧ touch_{W₂}(e) ⟹ touch_{W₁ ∩ W₂}(e))`"

OQ4: "the weakest specialisation of `(∀ (i, e) ∈ Avail(Σ) : touch_{W₁}(e) ∧ touch_{W₂}(e) ⟹ touch_{W₁ ∩ W₂}(e))` — under which intersection-equality ... is recovered"

**Problem**: The body proves X := the touch-implication is the *exact* (necessary and sufficient) condition for equality, and that proof is correct — since `⊆` is unconditional and `RE(W,d,Σ) = {(i,e) ∈ Avail(Σ) : touch_W(e)}` with `Avail` region-independent, `⊇ ⟺ X`. OQ4 then asks for "the weakest specialisation of X under which equality is recovered." But a *specialisation* of X is a condition `C` with `C ⟹ X`, and `C ⟹ X ⟺ C ⟹ equality` (because X *is* equality); the weakest `C` with `C ⟹ X` is X itself. So OQ4, read literally, asks for the condition the body has already supplied — it is either trivial or means something its wording does not say. The body's surrounding prose carries the missing qualifier — "The weakest condition *of this joint form*" (the two-lever coverage-single-meet ∧ image-distribution form) — but OQ4 drops "of this joint form" and substitutes "weakest specialisation of [X] ... under which equality is recovered," reintroducing the circularity. The RE-UDIST-∩ table entry repeats the bare "Equality holds exactly when X ... (Open Question 4)" without resolving the tension.

**Required**: Separate the two clearly. State that X is the exact condition (settled, not open), and reframe OQ4 as the weakest *structurally-restricted* condition sufficient for X — of the two-lever "joint form" the body already names, or expressed on coverage/image structure directly (e.g., a single-meet cardinality bound plus the image-distribution gap) so that the per-endset `touch` quantifier is eliminated. Drop "the weakest specialisation of [X] ... under which equality is recovered," which names the already-given answer.

## OUT_OF_SCOPE

(none) — the note stays within RETRIEVEENDSETS; it cites ASN-0127's image/discovery machinery rather than rebuilding it, names FINDLINKSFROMTOTHREE only for contrast, and defers replication/non-co-resident stores (OQ5) and link-subspace regions (OQ7) without claiming them.

VERDICT: REVISE
