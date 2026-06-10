# Review of ASN-0114

The technical core is sound. F0–F8 are correctly derived, the F2 (disconnection forces ≥2 spans) and F5 (LP13-carried permanence) proofs show their steps, and the worked instance discharges F2 and F7 against a concrete link with arithmetic I could check (`a₃ ⊕ δ(2,8) = a₅`, `coverage(e₁) ∩ F = {a₃,a₄,a₇,a₈}`, the `p=a₃ < q=a₅ < r=a₇` gap). All cross-references resolve to foundation ASNs. The findings below are accretion and one depth gap, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: F5's second qualification paragraph restates the first and previews a section that already covers it
**ASN-0114, "Determinism over time" (F5)**: Para 1 already establishes "the recorded addresses are addresses of permanent content identity rather than mutable positions … upgrades coverage-permanence to material-permanence." Para 2 then says: "'Same material' means same content identity, not same coordinates in some document's current view. The recorded end is invariant; its rendering into the live arrangement of a particular document is a separate matter, **addressed below**."
**Problem**: Para 2's first two sentences are Para 1's content-identity point in different words; its only new clause is the forward pointer "addressed below," which previews "A boundary we must respect" — a deferral the intro also makes ("not asked to resolve anything into the current arrangement of some particular document"). The reader skips meta-prose to stay with the claim. This is the "two paragraphs say the same thing" + "multiple sections defer to the same downstream location" pattern.
**Required**: Delete Para 2; let the boundary section carry the rendering-vs-recorded distinction once.

### Issue 2: F6's disclosure paragraph enumerates the non-conforming-address carve-out three times
**ASN-0114, "Confinement: one end tells nothing of the others" (F6), the "First, a partial disclosure of home documents" paragraph**:
- "a covered address may sit at node level (zeros = 0) or user level (zeros = 1), carrying no document field … whose interior tumblers need not be T4-valid at all"
- "For any covered address that is non-conforming — node- or user-level, or a non-T4-valid interior tumbler — no document field exists to read"
- "The 'region is documents' equivalence therefore holds only over the document-bearing (zeros ≥ 2) slice … L4 expressly permits ends whose covered addresses name no document at all"
**Problem**: the same carve-out (node/user-level or non-T4-valid interior ⇒ no document field) is stated three times. The refined point — document is disclosed only on the `zeros ≥ 2` slice — is correct and worth keeping; the triple enumeration of the excluded cases is not.
**Required**: State the carve-out once.

### Issue 3: the wp analysis computes only trivial cases, omitting the one tied to F7
**ASN-0114, the two wp lines**: `wp(followlink(a, i), R is a span-set ∧ coverage(R) = coverage(Σ.L(a).eᵢ)) ≡ a ∈ dom(Σ.L) ∧ 1 ≤ i ≤ |Σ.L(a)|` and `wp(followlink(a, i), result ≠ ⊥) ≡ …` — both equal the precondition (or its negation).
**Problem**: Both wp's reduce to the operation's domain — no backward reasoning is exercised. The informative refinement for this pure read is the one that separates the *success-empty* outcome from *success-nonempty*, which is exactly the state-dependent condition F7 makes load-bearing: `wp(followlink(a, i), R = ⟨⟩) ≡ a ∈ dom(Σ.L) ∧ 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = ∅` (with `coverage(eᵢ) = ∅ ⟺ eᵢ = ∅` by S2 forcing the unique witness ⟨⟩). It is not computed.
**Required**: Add the `R = ⟨⟩` wp, deriving the `eᵢ = ∅` conjunct via S2, so the wp section exercises F7's empty/non-empty split rather than only the domain boundary.

## OUT_OF_SCOPE

### Topic 1: resolution of the recorded endset into a document's V-positions
**Why out of scope**: "A boundary we must respect" correctly excludes V-position projection and arrangement-filtering (the shrinkage of Q15, the per-document divergence of Q11). This matches the scope list ("resolving an endset's spec-set to V-positions of a specific document"). The deferral is handled, not a gap — recording here only to confirm the boundary was checked and the in-scope FOLLOWLINK contract (F1 exactness *to the recorded end*) does not entangle the mutable arrangement.

### Topic 2: conformance of a fixed `{1,2,3}` selector whitelist for arity > 3 links
**Why out of scope**: The ASN generalizes the selector domain to `{1, …, |Σ.L(a)|}` per Nelson's n-set (4/79), so an implementation capping selectors at 3 would under-accept a valid slot on an arity-≥4 link. Whether that is a conformance failure is an implementation-conformance question (touched by Open Question 4), not a defect in this ASN's claims.

VERDICT: REVISE
