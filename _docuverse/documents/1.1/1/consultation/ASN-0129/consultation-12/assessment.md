# Channel Assignment — ASN-0129 review-12

**Date:** 2026-06-11 17:27

## Issue 1: Default-view rewrite scope sweeps V-TUP projections in, contradicting V-TUP, PD0, and PC3
Reason: Internal. The contradiction is between the note's own clauses, and the note already contains the deciding observation — UV's rewrite predicate is keyed to `K_queried`, which a V-TUP projection of an in-hand tuple lacks — so the fix is a scoping sentence (V-TUP reads are raw stored-value reads at every view) plus naming FP's increment list, all derivable from definitions already present.

## Issue 2: UV's rewrite of `chain`'s returned sequence contradicts the foundation's "BH1 filtering does not rewrite the walk"
Reason: Internal. ASN-0128's Open Question 1 explicitly deferred behavior-surface default-view semantics to this layer, so the resolution authority is this note's, and the reconciliation materials are already in hand: UV's traversal clause (walk = what is traversed, preserved unrewritten), the presentation-vs-state principle, and BH1's colon-explicated "nothing else" scope — the fix is to perform the quote-and-scope reconciliation explicitly, not to re-decide the doctrine against either authority.

## Issue 3: `Map_fin`'s carrier is never defined
Reason: Internal. The carrier is fully determined by content the note already cites — V-PRIM's lookup signature `·[K] : Map_fin → T ∪ {⊥}` over registered classes and BH3's `targets_keyed` join — and the finding supplies the one-line definition (finite partial maps from registered coverage classes to `T`).

## Issue 4: Intro paragraph 2 and the commitments list say the same thing twice (anti-bloat)
Reason: Internal. Pure deduplication between two adjacent structural slots; the required edit (commitments list carries the inventory, intro keeps the consumers/extension-language framing) involves no semantic question.

## Issue 5: PC6's "What the relativization costs" carries conjecture-implication essay content in the theorem's slot (anti-bloat)
Reason: Internal. The fix is relocation and compression of analysis already written — moving the entailment/non-implication chain to C-reach/OQ6 and trimming V-TUP's forward pointer — and the Gregory read-path evidence already quoted inside PC6 (`tumblercmp`, `tumbleradd` placement) moves with the text unchanged, so no new evidence or intent ruling is needed.
