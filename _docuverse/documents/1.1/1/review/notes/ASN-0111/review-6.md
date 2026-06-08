# Review of ASN-0111

## REVISE

### Issue 1: Orphanhood claim in the worked example is justified for only one of three slots

**ASN-0111, "An orphaned instance (RL8)"**: "Suppose that at state `Σ` no document arrangement maps any V-position to the three content I-addresses lying within `coverage(F)` — the connected content is arranged nowhere, so the link is orphaned and `discoverable_from(a, d, Σ)` is false for every `d`".

**Problem**: `discoverable_from(a, d, Σ)` quantifies over *all* slots (LP12, ASN-0098: `⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)`). The link `(F, ∅, Θ)` has three slots. The justification addresses only `coverage(F)` (slot 1). To conclude non-discoverability for every `d`, the example must also dispatch slot 3 — the ghost type `Θ`, whose `coverage(Θ) = {t : [1.0.1.0.9.0.1.1] ≼ t}` is a non-empty (in fact infinite) address set. The empty to-set (slot 2) is trivially unwitnessed and could be stated as such. As written, the strongest conclusion the given reasoning supports is "not discoverable via the from-set," not "false for every `d`." This is exactly a missing case in a concrete verification.

**Required**: Extend the orphaned-instance argument to all slots: note `coverage(∅) = ∅` for the to-set, and argue `coverage(Θ) ∩ ran(Σ.M(d)) = ∅` for every `d` (e.g., since the ghost document `[1.0.1.0.9]` hosts no content, `coverage(Θ) ∩ dom(Σ.C) = ∅`, and by S3★ no arrangement range can reach it). Only then does `discoverable_from(a, d, Σ) = false` for every `d` follow.

### Issue 2: "arranged within this coverage" overloads the technical term *arrangement*

**ASN-0111, "A worked read"**: "The element-level content addresses **arranged within this coverage** are `[1.0.1.0.1.0.1.1]` and `[1.0.1.0.1.0.1.2]` under `d₁` and `[1.0.1.0.2.0.1.1]` under `d₂` — three I-addresses that host content and lie *inside* `coverage(F)`".

**Problem**: In this specification "arrangement" is the technical name for `Σ.M(d)`, and RL8 turns precisely on whether content is *arranged* (mapped by some `Σ.M(d)`) versus merely existing. Here "arranged within this coverage" is used loosely to mean "located within the coverage interval / present in `dom(C)` and lying inside the address range." Because RL8 a few paragraphs later hinges on whether these same addresses are "arranged nowhere," the loose usage collides with the technical one and obscures the distinction the ASN is built to draw (recorded vs. resolved, witnessed vs. unwitnessed).

**Required**: Replace "arranged within this coverage" with non-overloaded wording, e.g. "the content I-addresses lying within `coverage(F)`" or "the `dom(C)` members inside `coverage(F)`," reserving "arranged" for the `Σ.M` sense used in RL8.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
