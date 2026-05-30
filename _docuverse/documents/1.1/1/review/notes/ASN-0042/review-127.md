# Review of ASN-0042

## REVISE

### Issue 1: O1's "Ownership *is* the comparison" overclaims relative to the load-bearing ω

**ASN-0042, Ownership as a Structural Predicate**: "If we removed the function and replaced it with any other function that performs the same comparison, the system's ownership behavior would be identical. Ownership *is* the comparison."

**Problem**: O1 defines the *non-exclusive* predicate `owns(π, a) ≡ pfx(π) ≼ a`, and the cited implementation evidence (`tumbleraccounteq` / `isthisusersdocument`) decides account-level prefix containment. But the load-bearing guarantees — O2 (exclusivity), O3 (refinement), O8 (irrevocable delegation) — all rest on the *longest-match* selector `ω`, which the ASN itself concedes `tumbleraccounteq` does **not** compute ("the containment check returns true for *both* distinct principals"). The ASN supplies no implementation evidence that `ω`'s longest-match selection is realized anywhere in udanax-green. So O1's prose claims the existing comparison fully embodies ownership behavior, while the central theorems depend on a selection mechanism the implementation lacks. This is an internal inconsistency between O1's grounding claim and The Exclusivity Invariant's admission.

**Required**: Temper O1 to state that udanax-green realizes only `owns` (account-level containment), and explicitly flag that `ω` (and hence O2/O3/O8) is an abstract guarantee with no current implementation realization — a conformance gap, not a property the existing `tumbleraccounteq` already secures.

### Issue 2: O7(c) statement and proof disagree on which delegation conditions are re-evaluated vs. discharged

**ASN-0042, O7 statement (c)**: "the same five-condition gate applies, but conditions (ii), (iv), and (v) are re-evaluated against the delegation state, so the admissible p'' is state-dependent"

**ASN-0042, O7 proof (postcondition c)**: discharges (i) by choice, (ii) "directly from condition (iv) of the original delegation," and (iv) "at Σ' independent of the choice of p''," then concludes "The remaining obligations on p'' are (iii) and (v)."

**Problem**: Two mismatches. (a) The statement lists (ii) and (iv) as "re-evaluated against the delegation state" (state-dependent), but the proof discharges both at `Σ'` immediately upon entry, independent of any later state — and (iii), which the proof identifies as a genuine binding obligation, is omitted from the statement's enumeration. (b) The statement claims a recursive right at "the prospective delegation state" (potentially much later than `Σ'`), but the proof only establishes satisfiability "immediately upon entry" at `Σ'`; the general case, where intervening delegations may interpose a more-specific cover of `p''`, is not discharged. The proof proves a strictly weaker claim than the statement asserts.

**Required**: Align the statement and proof on the exact partition (discharged: i, ii, iv; binding obligations: iii, v), and either prove the recursive right holds at an arbitrary later delegation state or restrict the statement's claim to satisfiability at `Σ'` upon entry.

### Issue 3: Accumulated restatement of the refinement-only / no-revocation theme

**ASN-0042**, three locations: O3 corollary ("only a *more specific* delegation can supersede it"); O8 *Design confirmation* ("O8 instantiates O3's refinement-only regime at the parent–delegate boundary. The implementation provides no revocation path"); O10 closing ("The construction exhibits the refinement-only regime established at O8").

**Problem**: The anti-bloat classifier on this note flags prose that restates an established result across sections. These three passages assert the same content (refinement-only, no revocation) in different words without advancing new reasoning, and O8/O10 each re-derive the conclusion already carried by O3's formal corollary. This is the "two paragraphs say the same thing in different words" pattern compounding across sections.

**Required**: Keep the formal carrier (O3 corollary / O8 postcondition) and delete the redundant restatements in O8's *Design confirmation* prose and the O10 closing sentence, retaining only any genuinely new content (e.g., the implementation-has-no-revocation-path observation, stated once).

## OUT_OF_SCOPE

### Topic 1: Reconstruction of delegation history from address structure
The final Open Question ("Must delegation events be recorded...") raises whether the address hierarchy alone suffices to recover delegation history. This is genuinely new territory — a provenance/audit guarantee — not a defect in the present ownership-state model. Correctly parked as an open question.

VERDICT: REVISE
