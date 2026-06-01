# Channel Assignment — ASN-0086 review-183

**Date:** 2026-06-01 11:41

## Issue 1: PC-dropping counterexample (wp Case 1) presupposes a Σ' the witness does not guarantee
Reason: The fix is derivable from the ASN's own content — the Emit_K Definition already states the partiality (off-chain `ℓ_prev` makes emission undefined), and the NestedLinkWitness Remark plus the multi-document machinery already in the note supply the needed witness shape (nested pair at `d` plus a distinct clean `d_retr`). No design intent or implementation evidence is required.

## Issue 2: Reduction-to-Emit_K corollary imagines composites the layer's own Definition excludes
Reason: Purely editorial — deleting paragraph 2 (or relocating the `m`-genericity remark to R7a) follows from the relational layer's own Definition ("admits no composites that touch `Σ.L` indirectly"), which is already present in the ASN. No external channel needed.

## Issue 3: R7a Remark is a non-reliance disclaimer wrapping implementation trivia
Reason: The review itself stipulates the udanax-green observation is legitimate; the required action is to strip the defensive meta-framing and keep the plain implementation note, which is a text-trim derivable from the ASN. Gregory is not needed because the implementation claim is being retained, not re-litigated.
