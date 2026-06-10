# Review of ASN-0115

I checked the proofs of the Confinement lemma, the `act` override, and claims R2/R3/R6/R7/R8/R9/R10/R11, and re-verified each worked instance against its claims. The mathematics is sound and unusually careful: R7's comparability handling, R6's no-interior-hole argument (canonical-start derivation from `act ≠ ∅`, terminal-overrun characterization), and the override's load-bearing role in the too-shallow regime all hold up. The boundary cases the guidance demands — empty spec-set (R0, `p=0`), spec naming unbound positions (R6), empty subspace (`V_S(d)=∅`), deep-start (`#s > m_S`, geometrically empty so override is a no-op), and orphaned-but-referenced content (R11) — are each addressed correctly. No improper cross-ASN references; the out-of-scope topics (link-structure reading, extent reporting) are correctly deferred to open questions or "out of scope here" remarks rather than claimed.

I found one item, in the anti-bloat register the note's classifier flags.

## REVISE

### Issue 1: R8 prose restates its own box and previews R9 via a forward reference

**ASN-0115, R8 (paragraph beginning "Within content, identity is structural")**: the closing sentence —

> "That this identity leaves no trace in the delivered stream is the content side of R9's kind-asymmetry: a content item carries only the value `Σ.C(a)`, never the address, so the shared origin is recoverable through the resolution mapping `v ↦ a` but not from the output."

**Problem**: This sentence carries no work R8 needs. Its non-disclosure content — "leaves no trace in the delivered stream" and "a content item carries only the value `Σ.C(a)`, never the address" — is already stated, verbatim in substance, in R8's own box ("each item carries the value `Σ.C(a)`, never the address `a` (R1) ... discloses nothing about the shared origin"). The remainder — "is the content side of R9's kind-asymmetry ... recoverable through the resolution mapping `v ↦ a` but not from the output" — is a forward reference that imports R9's claim (origin recoverable through resolution, not from output) into R8 before R9 is stated. R8's transclusion argument (content positions co-resolve through one shared address, no deduplication, indistinguishable from coincidental value-equality) is complete without invoking "R9's kind-asymmetry." This is the forward-reference accretion the note's `review-mode.anti-bloat` classifier is meant to catch: the same fact stated in three places (R8 box, R8 prose, R9 box), with the prose copy serving only to preview a downstream claim.

The carve-out for "statements of what an operation does or does not do" does not protect this sentence, because the does-not statement is *already in R8's box* — what remains is the redundant restatement plus the forward pointer, whose placement is exactly what the carve-out says to flag.

**Required**: Delete the sentence. The non-disclosure point is in R8's box; the kind-asymmetry (and its content/link split, with the "recoverable through resolution, not output" nuance) is R9's own claim and belongs there. If R8 wants to gesture at R9, a bare cross-reference suffices — it already does this with "(S4, R9)" in the box.

## OUT_OF_SCOPE

(none — the ASN stays within content delivery; out-of-scope topics are deferred, not claimed)

VERDICT: REVISE
