# Review of ASN-0114

I checked the substrate framing, all nine claims (F0–F8), the two "collapse" lemmas, every wp computation, and the worked instance. The mathematics is sound throughout: the first/second collapses correctly discharge from ASN-0053 S2; F2's `|R| ≥ 2` argument is valid (`R ≠ ⟨⟩` via first collapse, `|R| ≠ 1` via S0 convexity); F5's L12→LP13 composition is a legitimate foundation invocation; F7's empty/invalid split and the slot-3 non-emptiness corollary are correct; and the worked example's arithmetic (`a₃ ⊕ δ(2,#a₃) = a₅`, the LP-Fin Corollary giving `{a₃,a₄}`, the disconnectedness witness `a₃ < a₅ < a₇`) all check out. Depth obligations (derived consequences, a concrete example, a non-trivial wp for `R = ⟨⟩`) are met. The findings below are prose-level, surfaced under the note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Organizational meta-prose justifying the F0/claim separation (two instances of the same pattern)

**ASN-0114, F0 (FollowLink)**: "The coverage that span-set must carry is governed by the postcondition the wp named above, which we elevate to the central claim F1 rather than restate here."

**ASN-0114, "The selector and its domain" (closing roadmap)**: "Three commitments now remain to justify — the coverage relationship (F1), the pure-read frame (F4), and the distinction between a valid-but-empty end and an invalid selector (F7) — each carried by its own claim rather than packed into the definition, and each with consequences to extract."

**Problem**: Both sentences narrate *why* the coverage/frame/empty-distinction content is held in separate claims rather than folded into F0 ("we elevate to … rather than restate here"; "each carried by its own claim rather than packed into the definition"). This is structural-organization justification occupying a definition slot and a transition slot — the reader following F0 must skip past it to reach the actual definition, and the roadmap's core navigation ("F1, F4, F7; we take them in turn") survives without the justification clause. The separation itself is good practice; the prose defending the separation is the noise, and it appears twice (the recurring-deferral pattern the anti-bloat lens names).

**Required**: Delete the second sentence of F0 — F1 follows shortly and is unmistakably the contract, so no pointer or rationale is needed. In the roadmap, drop "each carried by its own claim rather than packed into the definition, and each with consequences to extract," leaving the bare navigation ("Three commitments remain — F1, F4, F7. We take them in turn.").

## OUT_OF_SCOPE

No new out-of-scope topics. The note correctly excludes endset-resolution-against-an-arrangement (handled in the "boundary we must respect" section as a property of *resolution*, not FOLLOWLINK — and its "does not resolve / would shrink / would vary per document" statements are legitimate statements of what the operation does not do, not bloat), and the Open Questions appropriately defer normal form, multi-document presentation, and wire encoding.

VERDICT: REVISE
