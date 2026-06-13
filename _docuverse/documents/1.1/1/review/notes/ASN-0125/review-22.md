# Review of ASN-0125

This is a mature, carefully argued note. EL0–EL3 are sound (the mutation/intent/carrier eliminations hold), the operation contracts EL6–EL7 discharge their frame and freshness obligations with the disciplined/unconditional split handled correctly, EL-DM's induction covers every editing-layer operation including the empty-store base, and the worked example verifies the key postconditions against a concrete fork/standoff/churn sequence with internally consistent addresses. The constructions in EL9(2) and EL10 correctly handle the non-surgical contraction boundary (suffix-drop + re-seat) and the j=1 / j=n cases. I checked the operation edge cases (same vs distinct homes, value-identical successor, revert, editing a claim, retraction-class exclusion via DC) and found them covered. The anti-bloat patterns appear largely cleaned by prior cycles — the EL13→EL14(d) deferral is genuine de-duplication, not accretion, and the remaining remarks are responsive to the problem's posed question rather than meta-prose.

One substantive gap remains.

## REVISE

### Issue 1: The currency query can return retracted versions, and EL14(d)'s disclosure does not surface this

**ASN-0125, Df-SUCC / Df-CUR / EL14(d)**: `succ_o(Σ) = {(old(e), new(e)) : e ∈ Ŝ^Σ ∧ addr(e) ∉ nullified(Σ)}` and `current(y, Σ) = {z ∈ reach_o(y, Σ) : ¬(E w :: (z, w) ∈ succ_o(Σ))}`.

**Problem**: `succ_o` filters claims by the **claim address** `addr(e) = b`, never by the endpoint links `old(e)`, `new(e)`. But EL9(3) makes activity a first-class axis for *any* link — "`active(a, Σ) ≡ a ∉ nullified(Σ) can only fall ... by an explicit ... retraction tuple" — and a successor (edited reading) is a link like any other. EL-DM's step confirms that `Nullify` targeting any `t ∈ dom(Σ.L)` deposits only a unit-depth `[R]`-tuple and preserves edit-discipline. So this sequence is reachable inside the disciplined editing layer:

1. `editlink(a, ·, d_s, d_a)` → successor `a'`, claim `b`, giving `(a, a') ∈ succ_o`, `current(a) = {a'}`;
2. `Nullify(Σ, d, a')` → `a' ∈ nullified(Σ)`, but `b ∉ nullified`, so `(a, a')` stays in `succ_o`.

Now `current(a) = {a'}` with `a'` retracted. The supersession sink and its own activity are independent (exactly EL9's "three axes" claim), so `current` is in fact *activity-agnostic* — yet the ASN never says so. EL14(d) enumerates the disclosure the layer "owes the reader" — `current(y)` entire, "each member with its supporting claims and their homes ... the original always still readable" — and the "any narrowing" examples are *trust the original owner's claims, prefer this curator, follow per-home latest*. Member activity is in none of them. A reader taking EL14(d) at face value can therefore rely on a retracted link as the current version, with nothing in the currency output marking it inactive. EL15(d) addresses a nullified *claim* dropping from `succ_o`; it does not address a nullified *endpoint*, so this consequence is genuinely unexplored.

**Required**: Either (a) state explicitly that `current(y)` is activity-agnostic and that member activity (`active(·)`, EL9(3)) is a separate query the reader must layer; or (b) add member activity to EL14(d)'s disclosure obligation (so the disclosed set carries each member's retraction status alongside its supporting claims); and in either case derive the consequence — that a supersession sink and its activity are independent, so `current(y)` membership does not imply the member is operative.

## OUT_OF_SCOPE

### Topic 1: An activity-filtered currency operation as a first-class layer primitive
**Why out of scope**: Defining `current_active(y, Σ) = current(y, Σ) ∩ {x : active(x, Σ)}` as a distinct, contracted operation (with its own monotonicity behaviour, given EL5(c)'s non-monotone `succ_o` compounded with EL5(b)'s monotone `nullified`) is a refinement, not a defect in the present claims. The in-scope obligation is only to acknowledge the interaction and complete EL14(d)'s disclosure; the operationalization belongs to a later note (adjacent to Open Question 2's independence-of-axes question).

VERDICT: REVISE
