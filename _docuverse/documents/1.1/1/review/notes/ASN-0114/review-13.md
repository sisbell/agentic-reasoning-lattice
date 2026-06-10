# Review of ASN-0114

I checked all nine claims (F0–F8), their derivations (the F2 disconnection argument, the F5 closure, the F6 slot-independence step, the F7 wp), the worked instance arithmetic, the boundary cases (`a ∉ dom(Σ.L)`, out-of-range selector, empty non-type slot, type slot `e₃`, disconnected coverage), and every cross-ASN reference (all to foundation ASNs — 0034, 0043, 0053, 0093, 0098 — so all admissible). The technical content is sound: the worked example's `coverage(e₁) = [a₃, a₅) ∪ [a₇, a₉)` with `∩ F = {a₃, a₄, a₇, a₈}` checks out against OrdinalShift and the LP-Fin Corollary, the disconnection witness `a₃ < a₅ < a₇` is valid, and the `R = ⟨⟩` wp reduces correctly through the two S2 collapses. One inconsistency remains.

## REVISE

### Issue 1: F5's premises are stated three different ways, and one of them names a fact the derivation never uses

**ASN-0114, "Determinism over time"** — the section opener says:
> "From immutability and the pure-read frame, a permanence property follows without further assumption."

but the closing paragraph says:
> "F5 as stated is a coverage-permanence claim, and exactly one fact carries it: link immutability (L12, composed along Σ →* Σ' by LP13)."

**Problem**: The two sentences disagree on F5's premise set, and neither matches what the `∎` derivation actually uses. The derivation needs exactly two facts: (i) link immutability composed along the sequence — `Σ'.L(a) = Σ.L(a)` from LP13 — and (ii) F1 applied at *both* `Σ` and `Σ'` to bridge the link value to the result's coverage (the chain `coverage(followlink(Σ',…)) = coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ) = coverage(followlink(Σ,…))` invokes F1 twice). So:

- The opener wrongly names the **pure-read frame (F4)** as a premise. F4 is irrelevant to the formal F5: the transitions in `Σ →* Σ'` are arbitrary *system* transitions, not `followlink` invocations, so `followlink`'s own non-mutation never enters. (F4 is relevant only to the *informal* gloss "two requests separated by intervening operations" — it ensures the two read-requests are not themselves transitions — but that is not what the formal claim quantifies over.)
- The closing "exactly one fact" wrongly **omits F1**, which the derivation plainly applies at each state.

The closing paragraph additionally restates the `∎` derivation it follows ("Because `Σ'.L(a) = Σ.L(a)`, the recorded spans — and hence their coverage — are fixed"), adding no step.

**Required**: State the premises identically in the opener and the wrap-up as **{F1, L12 (composed by LP13)}**; drop "the pure-read frame" from the opener (or, if F4's informal role of keeping the two reads from perturbing the state is genuinely intended, say *that* explicitly rather than listing it as a derivation premise); and delete the redundant closing paragraph or reduce it to the corrected premise list. The formal claim F5 itself is correct — this is an attribution/clarity defect, not a soundness hole.

## OUT_OF_SCOPE

No out-of-scope claims to flag. The ASN's own scope discipline is correct: the "boundary we must respect" section cleanly excludes endset→V-position resolution (filtering against a document's live arrangement), and the Open Questions defer normalization, resolution shrinkage, and the serialization-boundary encoding rather than smuggling them in as claims. The targeted forward-reference accretion patterns (axiom-rationale prose, use-site inventories, document-ordering justifications, repeated downstream deferrals) are absent; the one redundant paragraph is the F5 closer folded into Issue 1.

VERDICT: REVISE
