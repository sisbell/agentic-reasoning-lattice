# Review of ASN-0111

This is a pure-read specification. The proofs are sound, the boundary cases (undefined address, empty connective slot, arity > 3, ghost type, nested link, orphaned link) are all covered, and the worked read is concrete and correct — I checked the tumbler arithmetic (`s ⊕ δ(2,8) = [1.0.1.0.1.0.1.3]`, the first-emission addresses, the `inc(a,0)` sibling, and the three-slot orphan dispatch via LP12/LP-Fin/LP20) and it holds. The substance converges. The findings below are anti-bloat (this note carries `review-mode.anti-bloat`).

## REVISE

### Issue 1: Redundant restatement in the home-from-key remark
**ASN-0111, "Ownership lives in the read key" (Remark)**: "`home(a) = N(a).0.U(a).0.D(a)` is derivable from that key by T4 field projection alone, independent of the returned endsets (L2, ASN-0043) — without consulting any endset, and indeed without performing the read."
**Problem**: The independence-of-the-value claim is stated three times in one sentence — "independent of the returned endsets," then "without consulting any endset," then "and indeed without performing the read." The escalating triple is the kind of meta-prose the reader has to skip past; L2 plus the first phrase already carries the point. The surrounding section reads as the retired RL4 home-disclosure content relocated into a remark rather than trimmed.
**Required**: Keep one statement of the independence (the L2 citation suffices) and drop the two restatements. Condense the remark to the single load-bearing distinction: home is fixed by the read key `a`, not by the returned value.

### Issue 2: Nesting "reader's affair" prose duplicated across claim and worked example
**ASN-0111, RL6 and the nested worked instance**: RL6 states "the read does not silently recurse... Whether and how a reader chooses to follow the nesting by issuing further reads is the reader's affair"; the worked instance restates "the returned address `a'` may be read in turn, but that is a separate `readlink(a', Σ)` the caller chooses to issue."
**Problem**: The non-recursion / reader-chooses-to-follow point is made in full in both places. The worked instance should *verify* RL6 against the concrete `c → a'` target (the address is returned unflattened), not re-narrate the obligation prose.
**Required**: Drop the "reader's affair" essay clause from one site — keep the abstract obligation in RL6, keep only the concrete check (`a' ∈ coverage(readlink(c,Σ).e₂)`, returned as an address) in the worked instance.

VERDICT: REVISE
