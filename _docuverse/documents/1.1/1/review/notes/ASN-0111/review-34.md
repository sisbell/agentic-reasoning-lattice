# Review of ASN-0111

## REVISE

### Issue 1: Worked-example RL5 bullet restates the claim verbatim instead of verifying
**ASN-0111, "A worked read" (RL5 ghost-type bullet)**: "The read of this ghost-typed link is no less complete than any other."
**Problem**: This sentence is a near-verbatim copy of the RL5 claim's own closing sentence ("the read of a ghost-typed link is no less complete than any other"). The bullet's job is to *verify* RL5 against the concrete `Θ` — which it does, via the `coverage(Θ) = {t : [1.0.1.0.9.0.1.1] ≼ t}` computation. The trailing restatement adds nothing beyond the claim already states; it is the "two paragraphs say the same thing in different words" pattern the anti-bloat pass is meant to catch.
**Required**: End the bullet at the concrete verification (the coverage computation and "interpreted as this coverage address-set (L8) ... without dereferencing"). Drop the restated conclusion.

### Issue 2: "they are what readlink will exploit" misattributes the structural screen to the operation
**ASN-0111, "The link as a readable object"**: "These facts are what make a link nameable in the same address space as content, and they are what `readlink` will exploit."
**Problem**: `readlink(a, Σ) ≡ Σ.L(a)` is a bare partial-function application; the lookup does not consult `zeros(a) = 3`, `subspace_I(a) = s_L`, or `#E(a) ≥ 2` at all. The only place those facts are used is the *reader's* RL0 pre-test (necessary-but-not-sufficient screen). Attributing exploitation to `readlink` is inaccurate and conflicts with RL0's own framing that definedness is a fact about `dom(Σ.L)`, not address syntax.
**Required**: Either drop the "what readlink will exploit" clause or reassign it to the reader's RL0 screen, consistent with the RL0 section.

### Issue 3: "Ownership lives in the read key" is a top-level section for a one-sentence non-guarantee
**ASN-0111, "Ownership lives in the read key"**: "This is a property of the address, not a guarantee `readlink` adds."
**Problem**: The section's entire payload is that `home(a)` is recoverable from the key by L2 and is *not* part of the returned value. That is a legitimate boundary note (statements of what the operation does not do are in scope), but giving a non-claim its own section heading over-weights it relative to the labelled claims. Placement, not existence, is the issue.
**Required**: Fold the content into a single sentence under RL1 or the scope framing, rather than a standalone section.

## OUT_OF_SCOPE

### Topic 1: What a reader may conclude about continued validity / discoverability from a read alone
**Why out of scope**: The Open Questions correctly defer this to FOLLOWLINK and projection territory (ASN-0098); RL8 already fixes the recorded-vs-resolved boundary, and no validity-of-resolution guarantee belongs in a pure read.

VERDICT: REVISE
