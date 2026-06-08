# Review of ASN-0111

## REVISE

### Issue 1: RL7's quantifier paragraph is accreted defensive prose
**ASN-0111, RL7 (Determinacy)**: "We are careful about the quantifier here. L12 (ASN-0043) is a single-step guarantee: for one transition `Σ → Σ'`... so it needs the multi-step lift, not L12 alone. That lift is already available: LP13..."
**Problem**: The proof needs exactly one move: cite LP13 (which discharges both definedness and value-preservation across `Σ →* Σ'`) and conclude `readlink(a, Σ') = Σ'.L(a) = Σ.L(a)`. The surrounding text — that L12 is "single-step," that the claim "needs the multi-step lift not L12 alone," "we are careful about the quantifier here" — defends against a citation the proof never makes. This is the "new prose explains why a lemma is needed rather than using it" pattern.
**Required**: Reduce to one sentence: "Stability across `Σ →* Σ'` follows from LP13 (UnconditionalLinkPersistence, ASN-0098), giving `a ∈ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)`; hence `readlink(a, Σ') = readlink(a, Σ)`." Drop the L12-vs-LP13 deliberation.

### Issue 2: The read-vs-follow/search contrast and the "gone vs unwitnessed" point are restated across four sections
**ASN-0111, multiple sections**: the follow/search/count distinction appears in the intro ("three neighbouring operations"), in RL1's worked example ("Contrast a *search*..."), in "Recorded relationship versus resolved position," in RL8, and again in the worked orphan ("A *follow* of `F`... would resolve to the empty set, and a *search* would find nothing"). The specific "distinguishes *the relationship is gone* from *the relationship is unwitnessed*" is stated three times (section intro, RL8, worked orphan).
**Problem**: The reader must re-read the same contrast to confirm it is the same contrast. The worked orphan instance demonstrates it concretely and completely; the prose sections then repeat it in different words — the "two paragraphs say the same thing" pattern compounded across the note.
**Required**: State the read-vs-follow/search distinction once (the intro already scopes it out), and let the worked orphan carry the gone-vs-unwitnessed demonstration. Remove the duplicate prose in "Recorded relationship versus resolved position" and the RL8 body that restate it.

### Issue 3: "the read reveals ownership for free" conflates the operation's output with key-derivability
**ASN-0111, "What the read reveals..." / RL4**: "Because the read is keyed by the address and the address encodes the home, the read reveals ownership for free."
**Problem**: `readlink(a, Σ) ≡ Σ.L(a)` returns endsets only; `home(a)` is not in the returned value. RL4 itself is precise ("determined by the read key `a` alone... independent of the returned endsets"), but the body prose attributes to the *read* a disclosure that is actually the caller parsing a key they already hold. The operation does not output home.
**Required**: Tighten the prose to match RL4 — ownership is derivable from the key that names the read, not returned by the read.

## OUT_OF_SCOPE

### Topic 1: Reader-side conclusions about continued validity, empty-vs-unwitnessed distinguishability, and value-identity collision
**Why out of scope**: The three Open Questions correctly defer these — they concern guarantees a reader may *conclude* (validity from a read alone, distinguishing an empty connective slot from unwitnessed content, distinguishing equal-structure links by identity). These are new territory for downstream notes, not defects here.

VERDICT: REVISE
