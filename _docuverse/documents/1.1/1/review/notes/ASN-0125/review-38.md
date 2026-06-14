# Review of ASN-0125

I checked the substantive content closely: EL0's mutation-impossibility wp, the EL-DM induction over the editing-layer vocabulary (base `Σ₀` with `L₀ = ∅`; step over framing transitions, bare `K.λ`, `Nullify`, `assert_sup`, `editlink`), the EL6/EL7 operation contracts (allocation, record, the unconditional-vs-disciplined `nullified` frame, discipline preservation by case-split on whether `a'` is itself a `[K_sup]` claim), the EL4 single-target computation, the EL9(2)/EL10 `K.μ⁻`+`K.μ⁺_L` constructions with their `j = n` boundary, EL11's two-regime biconditional (the zeros+antichain trace), EL13's cross-home commute, EL14(c)/(e)'s standoff and activity-agnostic-membership constructions, and the worked example's address arithmetic. These are correct, boundary cases are handled, foundation lemmas (LP13, R0a, R3, R6a, wp Case 2, EmitAddress, CL-OWN, S3★, T6, T9, T10, PrefixSpanCoverage, LP12) are applied per their statements, all cross-ASN references are to foundation ASNs, and the note stays in operation/invariant territory (not implementation mechanics). The lone remaining item is a prose redundancy that the active anti-bloat mode asks to surface at source.

## REVISE

### Issue 1: EL-DM's editlink bullet duplicates EL7(vi)'s headline sentence
**ASN-0125, EL-DM (DisciplineMaintenance), Step, final bullet**: "*editlink.* EL7(vi): `Σ₂` is edit-disciplined when `Σ` is — precisely what the precondition `DC(ℓ')` secures, and what licenses chaining edits."

**Problem**: The trailing gloss reproduces, nearly verbatim, EL7(vi)'s own opening — "`Σ₂` is edit-disciplined when `Σ` is — this is what `DC(ℓ')` secures, and it is what licenses chaining edits." In EL-DM the bullet's job is to defer to EL7(vi) for the proof; the editorial gloss restates the very claim it points to and adds nothing to the deferral. The immediately preceding bullet — "*assert_sup.* EL6(v): `Σ'` is edit-disciplined when `Σ` is." — is terse and carries no such gloss, so the duplication is also an internal style inconsistency between two parallel deferral bullets. This is the "two paragraphs in the same document say the same thing in different words" pattern flagged for this review mode, and it is the kind of clause-level echo that compounds across cycles if left in.

**Required**: Trim the editlink bullet to match the assert_sup bullet — "*editlink.* EL7(vi): `Σ₂` is edit-disciplined when `Σ` is." — leaving the "what `DC(ℓ')` secures / licenses chaining edits" framing to its single home in EL7(vi).

## OUT_OF_SCOPE

(none) — the scope-excluded topics (MAKELINK, FINDLINKS, FOLLOWLINK, READLINK, RETRIEVEENDSETS, version/document/content/replication operations) are not given claims here; the Open Questions are appropriately deferred forward-looking items, not in-scope claims.

VERDICT: REVISE
