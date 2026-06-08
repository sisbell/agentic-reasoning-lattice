# Review of ASN-0102

## REVISE

### Issue 1: "M the only component that changes" contradicts COPY's own effect on R
**ASN-0102, "What invariants the completed operation must maintain" (final P3 paragraph)**: "and `Σ'.R = Σ.R ∪ {(a_j+i, d)} ⊇ Σ.R` gives `R ⊆ R'`. Every conjunct of P3 holds, with M the only component that changes."
**Problem**: The same sentence shows `R` changing (`Σ'.R ⊇ Σ.R`), and the Definition explicitly says COPY changes "two state components — the arrangement M and the provenance relation R." So "M the only component that changes" is false. P3's actual guarantee (ASN-0047) is that M is the only component that can *lose information* / contract — not the only one that changes; R grows monotonically.
**Required**: Rephrase to "M the only component that can contract / lose information" (R also changes, by extension only), so the conclusion matches both the Definition and P3's meaning.

### Issue 2: Pre-state ("snapshot") resolution rationale is stated three times
**ASN-0102** — the resolution section: "Because the source may include the target itself (`d_s = d`), the evaluation point matters: we resolve against the pre-state `Σ` … and write the result with that state pinned"; **X10(b)**: "the precondition — including the resolution `resolve_Σ(R)` — is evaluated against the pre-state `Σ` … `resolve_Σ(R)` reads `Σ.M(d)` *before the displacement opens the gap*"; **X15**: re-states the same atomic pre-state reading.
**Problem**: The self-transclusion motivation and the "reads pre-state before the gap opens" rationale recur in three slots saying the same thing in different words. X10(b) and X15 are legitimate distinct claims (a SourceHandling guarantee; an atomicity derivation), but the *rationale prose* is duplicated rather than cited. The concrete "Why X10(b)/X15 are load-bearing here" example is fine — it earns its place; the prose triplication does not.
**Required**: Establish pre-state pinning once (the resolution section); have X10(b) and X15 cite it rather than re-motivate it.

## OUT_OF_SCOPE

(none — the four Open Questions correctly defer later-displacement, transclusion-of-transclusion, time-varying views, and unreachable-origin discoverability to future ASNs rather than asserting claims about them.)

VERDICT: REVISE
