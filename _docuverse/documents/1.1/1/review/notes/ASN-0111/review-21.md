# Review of ASN-0111

## REVISE

### Issue 1: RL2 defends against a bad-read case the carrier already excludes
**ASN-0111, RL2 (Role preservation)**: "A read that collapsed the endsets into one pool, or that swapped two differing slots, would return a *different* relationship (link equality is componentwise, L6)."
**Problem**: The operation is defined as `readlink(a, Σ) ≡ Σ.L(a)`, a componentwise copy. A pool-collapsing or slot-swapping read is not a possible behaviour of this carrier — it is an imagined alternative implementation. This is reviser drift (a paragraph imagining a case the definition already excludes), not advancement of the claim. The substantive content of RL2 — arity equality plus slot position as a model primitive — stands without the hypothetical.
**Required**: Delete the imagined-malformed-read sentence; keep the positive statement (`|readlink(a, Σ)| = |Σ.L(a)|`, per-slot accessor primitive, componentwise equality, faithful return of slots 4…N).

### Issue 2: RL8 defers to the worked example instead of advancing the claim
**ASN-0111, RL8 (Recorded, not resolved)**: "The worked orphan below demonstrates concretely how this distinguishes *the relationship is gone* from *the relationship is unwitnessed*."
**Problem**: A use-site forward pointer ("below demonstrates") that carries no reasoning. RL8's own body already states the property (depends only on `Σ.L`, succeeds for orphans); the worked orphan stands on its own without being announced. This is the deferral-to-downstream-location pattern.
**Required**: Remove the forward-pointer sentence. The worked orphan instance speaks for itself.

### Issue 3: The readlink-vs-following/searching contrast is restated in three sections
**ASN-0111, "The problem" / "Completeness" / "Recorded relationship versus resolved position"**: the distinction "readlink consults only the link; following/searching consult an arrangement or spec-set" appears in the opening ("We must be careful to separate `readlink` from three neighbouring operations…"), again in Completeness ("The defining contrast between reading a link and finding one…"), and again in "Recorded relationship versus resolved position" ("the deepest distinction the operation embodies, the one that separates `readlink` from following or searching").
**Problem**: Two-plus paragraphs in different sections saying the same thing in different words. The "deepest distinction the operation embodies" framing is essay restatement of what the intro already established; RL8 then delivers the formal content. The repetition is noise the reader must skip past.
**Required**: State the read/follow/search separation once (the intro is the natural site), and let RL8 carry the formal "recorded, not resolved" content without re-motivating the contrast. The worked example's read-vs-search-vs-follow check is concrete verification and may stay.

## OUT_OF_SCOPE

(none — the note correctly defers search, follow, discovery, counting, creation, and editing to their own ASNs.)

VERDICT: REVISE
