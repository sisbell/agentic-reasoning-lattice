# Channel Assignment — ASN-0112 review-53

**Date:** 2026-06-10 22:24

## Issue 1: Quotation attributed to Nelson without citation, in non-verbatim form
Reason: The fix turns on whether the arrangement/composition distinction and the "Pure Vstream operation" phrase actually appear in Nelson's source (and where), or are the ASN's own gloss — only the theory channel can verify the attribution before we either pin-cite it or demote it to paraphrase. Gregory is irrelevant; no implementation fact is at stake.
Nelson question: Does Literary Machines (or the concept notes) actually state the arrangement-vs-composition distinction — rearrangement leaves extent unchanged, adding/removing content changes it — and use the phrase "Pure Vstream operation"; if so, what are the exact wording and pin-cites?

## Issue 2: V12 attributes the emptiness decision to `σ_d`, which does not exist in the empty case
Reason: The fix is internal — V0 and V11 already establish that the span-set `⟨⟩`/`⟨σ_d⟩` distinction is what discriminates emptiness, so rewording V12's subject from `σ_d` to the returned span-set requires no external evidence.

## Issue 3: Redundant recap of D-CTG★'s scope inside the V5 proof paragraph
Reason: The fix is internal — it is a pure prose deletion of a duplicated scoping statement; the proof's content (steps (i)–(ii)) is unchanged and no design intent or implementation fact bears on which sentence to keep.
