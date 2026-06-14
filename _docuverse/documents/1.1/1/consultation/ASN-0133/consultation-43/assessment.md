# Channel Assignment — ASN-0133 review-43

**Date:** 2026-06-14 14:05

## Issue 1: targets_of's rebuild formula is actually members'
Reason: Internal. The corrected term `{y ∈ ⋃({c ∈ A_K : x ∈ addrs_F(c)}, addrs_G) : ¬filtered(y)}` is dictated by `targets_of`'s definition (D3, which the finding itself cites) instantiated into the PC3 `⋃`/`∃`-over-fixed-base device the note already invokes. This is a transcription fix governed by a settled formal definition — no design-intent or implementation evidence adjudicates it.

## Issue 2: Worked example — the ρ_R′ digression illustrates an excluded case, then defers
Reason: Internal. Type isolation of `(ρ_P, ρ_R)` is already proved in the note and the OQ4 pointer already exists; collapsing the ρ_R′ construction and its "corollary of Q5a" repair to one sentence is pure structural pruning of content the note has already established.

## Issue 3: Worked example — type-isolation restated four-plus times
Reason: Internal. Deduplicating a single structural fact ("no rule writes `attn`/`tgt`") that the note states correctly four times — picking the canonical statement and having the other passages cite it — needs no external input.

## Issue 4: Q6 — post-proof restatement of the hypothesis packages
Reason: Internal. Deleting the redundant post-∎ package restatement while retaining the load-bearing drop-H-RF/drop-H-FAIR necessity contrast is editorial; the proof already forecloses the "third independent hypothesis" confusion the deleted text defends against.
