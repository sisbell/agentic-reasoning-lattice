# Review of ASN-0084

## REVISE

### Issue 1: No worked example exercises a non-S position, yet non-S handling is load-bearing
**ASN-0084, Worked Examples (all five) and R-NS / R-BLK / R-COMM**: Every worked example has `V_S(d)` consisting *entirely* of subspace-1 positions; "the non-S region is empty here" / "the non-S region is also empty" is stated in each Phase 2.
**Problem**: A substantial part of this ASN's content concerns positions in *other* subspaces passing through untouched: R-NS (NS-π pointwise identity), R-FRAME-P/S(a), the non-S branch of R-COMM, R-BLK's "Non-S runs are carried verbatim" plus the cross-group S8-uniq disjointness invoking T10 (ASN-0034). None of this machinery is ever verified against a concrete scenario. By the standard "no concrete example is a REVISE item," the in-scope non-S pass-through is asserted but never demonstrated — exactly the kind of claim a worked example should pin down.
**Required**: Add (or extend an existing example with) a `dom(M(d))` that contains at least one non-S position — e.g., a link-subspace position `[2, 1]` — and trace REARRANGE_K through it: show π fixes it, R-BLK carries its run verbatim, and the reassembled S and non-S runs remain disjoint and cover `dom(M'(d))`.

### Issue 2: R-CS3 states its claim twice
**ASN-0084, "Necessity of CS3"**: The introductory paragraph — "There exist cut sequences that violate CS3 yet satisfy CS1, CS2, CS4, and the whole of R-PRE except CS3 itself — so CS3 is the only clause that rejects them" — is restated by the lemma body: "R-PRE(iv) holds *vacuously* for such a sequence ... so CS3 is the sole clause that excludes it."
**Problem**: Two paragraphs in the same section assert the same proposition in different words (an anti-bloat pattern: "two paragraphs in the same document say the same thing"). The essay framing ("is *load-bearing*: it cannot be derived from the other precondition clauses ... nothing but CS3 stands in the way") adds no content the lemma+counterexample does not already carry.
**Required**: Drop the pre-lemma framing prose; let the lemma statement and its counterexample stand alone.

### Issue 3: R-NS proof contains a redundant re-derivation
**ASN-0084, R-NS proof**: "combined with the frame condition, this stipulation is consistent with the rearrangement defining equation M'(d)(π(v)) = M(d)(v) — substituting π(v) = v yields M'(d)(v) = M(d)(v), already supplied by the frame condition."
**Problem**: The lemma's content is fully discharged by two facts already named one clause earlier (frame condition gives `M'(d)(v) = M(d)(v)`; the bijection's non-S branch gives `π(v) = v`). The quoted sentence re-derives a result it admits is "already supplied" — defensive padding the reader must skip past.
**Required**: Delete the "consistency / substituting" sentence; the preceding two sentences already prove NS-π.

### Issue 4: "Invariant preservation" block pads preservation claims with restatements of what each invariant says
**ASN-0084, "Invariant preservation" / "C-transport"**: e.g. S7b "(which by zeros(a) = 3 asserts the element field is present)"; S7 "(origin(a) = N(a).0.U(a).0.D(a) is a function of the address a and of dom(C) alone; since a's component fields are unchanged ...)".
**Problem**: Showing invariant preservation is legitimate for an operation ASN, but the parenthetical re-explanations of *what each foundation invariant asserts* are use-site inventory, not preservation argument. The load-bearing claim in every case is the same one-liner ("depends only on dom(M(d))" or "C' = C, so transports by identity").
**Required**: State the preservation mechanism once per group (dom-dependent invariants; C-only invariants) and list the labels; drop the per-invariant restatements of foundation content.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond the depth-2 (m₁ = 2) restriction
**Why out of scope**: The note explicitly scopes to `m_1 = 2`, and the singleton-tumbler/ℕ identification depends on it. D-SEQ (ASN-0036) suggests only the last ordinal component varies at any depth, so generalization to `m_1 > 2` is plausible future work — but it is a clean, declared scope boundary, not an error here.

### Topic 2: Operational recovery of the canonical (maximal) partition from B′
**Why out of scope**: R-BLK produces a valid-but-possibly-non-maximal B′ and defers the merge-based reduction (Open Question 6, including confluence). This is correctly flagged as future territory rather than left as a silent gap.

VERDICT: REVISE
