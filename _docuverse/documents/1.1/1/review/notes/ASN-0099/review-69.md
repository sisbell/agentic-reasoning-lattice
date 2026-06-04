# Review of ASN-0099

The mathematical core is solid: the two-phase factoring (F12), set-additivity (F13/F20/F20a), determinism (F8), and the K.λ-increment characterization (F9-λ) are derived with explicit chains, and the worked example exercises the load-bearing claims against concrete states. My findings are prose-accretion and clarity issues, consistent with this note's `review-mode.anti-bloat` classifier — the layered lemma structure and meta-prose around forward references have accumulated past what the underlying facts warrant.

## REVISE

### Issue 1: A1/A1a is over-layered for "only K.λ modifies Σ.L", and A1a is never stated as its own block
**ASN-0099, "Arrangement Independence" (A1)**: "For every transition Σ → Σ' produced by an operation in V ∖ {K.λ}: dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)). Equivalently, K.λ is the unique operation of V that modifies the link store. ... A1a (published-frame preservation) discharges each."
**Problem**: Three layers (A1a → A1 → F9) plus connecting prose ("Each atomic operation ... publishes `L' = L` ... A1a discharges each. K.μ~ is the non-atomic K.μ⁻ + K.μ⁺ composite, so A1 reaches it through its two atomic constituents...") are stacked on the single fact that only K.λ writes `Σ.L`. A1 and A1a state nearly the same fact — per-op preservation vs. uniqueness of K.λ — and the prose re-derives A1a's content inside A1. Compounding this, A1a is invoked by name as a lemma throughout the worked example (Query 4: "by A1a"; Query 5 steps i–v: "via A1a") but has no statement block in the body — its only statement is the parenthetical "(published-frame preservation)" and the closing claims table.
**Required**: Collapse to a single stated lemma. Either give A1a a one-line body statement and let A1 be a corollary, or fold A1a into A1 and drop the separate name. The "Each atomic operation ... publishes ... discharges each" mechanism prose can go.

### Issue 2: F10's closing sentence restates the finite-total-order argument already given
**ASN-0099, "Result Ordering" (F10)**: body — "Any non-empty finite totally-ordered set admits a unique enumeration by finite induction." Closing — "F10's existence and uniqueness are complete at this point: T1 is a total order on the finite subset dom(Σ.L), and a finite totally-ordered set has exactly one increasing enumeration."
**Problem**: Two sentences in the same section assert the same thing. The closing sentence adds only "are complete at this point" — a meta-announcement of completeness, not new reasoning.
**Required**: Delete the closing sentence; the body sentence already establishes existence and uniqueness.

### Issue 3: "Local Atomicity" final sentence is both redundant and imprecise on "undiscoverable"
**ASN-0099, "Local Atomicity and the Single-State Setting"**: "by the time the K.λ committing a returns, a is in dom(Σ.L) and the next query at any state succeeding the K.λ must include a if a matches. There is no intermediate state in which a exists in dom(Σ.L) but is undiscoverable."
**Problem**: The final sentence restates the preceding atomicity claim, and "undiscoverable" is imprecise in a way the note itself flags elsewhere: per the F11 note, a link in `dom(Σ.L)` may legitimately fail `discoverable_from` for a given document (discoverability is arrangement-conditional). Membership in `dom(Σ.L)` does not entail discoverability, so "exists in dom(Σ.L) but is undiscoverable" describes a state that routinely occurs (orphaned links, LP17) rather than the excluded intermediate state.
**Required**: Drop the final sentence, or restate it in terms of `findlinks` inclusion for a matching query (the actual atomic guarantee) rather than "discoverable."

### Issue 4: F11 and F19 carry near-duplicate I-side/V-side asymmetry prose
**ASN-0099, F11 note**: "F11 is an I-side persistence claim against a fixed query I-set; the V-side analogue ... is not a theorem of this ASN and could not be, since K.μ⁻ can shrink ran(Σ.M(d))..."
**ASN-0099, F19 note**: "Monotonicity is an I-side phenomenon: F19 fixes an I-set and quantifies across the reachable sequence, resting on F11's I-side persistence; the V-side asymmetry noted at F11 applies equally here."
**Problem**: Both notes re-explain the I-side/V-side distinction. F19 already defers to F11 ("applies equally here"), so the lead clause re-establishing the distinction is redundant with that deferral.
**Required**: In F19, keep only the deferral ("the V-side asymmetry noted at F11 applies equally here") and drop the re-derivation of why monotonicity is an I-side phenomenon.

## OUT_OF_SCOPE

### Topic 1: Inverse direction (FOLLOWLINK / endset resolution to V-positions)
**Why out of scope**: Correctly deferred under "What We Have Not Specified." Resolving result endsets back to V-positions is a distinct operation, not a gap in FINDLINKS.

VERDICT: REVISE
