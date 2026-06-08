# Review of ASN-0113

## REVISE

### Issue 1: W14's "by position" recovery is ambiguous once a subspace is omitted

**ASN-0113, "Comparing reports across documents" (W14)**: "Because the kind-list `(s_C, s_L)` is fixed (W13), a consumer recovers each `n_S(d)` from the report **by position** — an *emitted* member of kind `S` contributes its boundary-count `n_S(d)` ... while an *omitted* kind `S` is read as `n_S(d) = 0`."

**Problem**: W7 makes the result a *subsequence* of the kind-list — it emits exactly `|occupied(d)|` members and *omits* empty subspaces. So list position no longer aligns with kind. Consider the one-member cases:
- text-only document `d'` (your own worked instance): result `⟨ext(d', s_C)⟩`, member at list position 1, kind `s_C`.
- a link-only document: result `⟨ext(d, s_L)⟩`, member at list position 1, kind `s_L`.

Both are singletons "at position 1," but of different kinds. A consumer reading **by list position** (position 1 = text, position 2 = link) would mis-attribute the link-only singleton to text. The kind can only be recovered from the member's *subspace identifier* — `start₁ = S` (W2/W10) — not from its index in the sequence. This directly contradicts W13's own framing of the result as members "drawn from" a fixed list (a subsequence), and the worked instance for `d'` exhibits exactly the singleton that makes position-1 ambiguous.

**Required**: Restate the recovery procedure so the consumer iterates the fixed kind-list `(s_C, s_L)` and, for each kind `S`, checks whether a member with `start₁ = S` is present (contributing its boundary-count) or absent (read as `n_S = 0`). The recovery is *by subspace identifier*, not *by list position*. Adjust the W14 prose and the worked-instance note accordingly.

## OUT_OF_SCOPE

### Topic 1: behavior under relaxed D-CTG★ (fragmentation)
**Why out of scope**: W5's converse correctly establishes that contiguity is *necessary* for single-span exactness, and the note defers the operational consequence (emit a fragmented span-set vs. report a bounding span) to an open question. Under the maintained D-CTG★ the case never arises; this is genuine new territory, not a defect here.

### Topic 2: cross-vintage comparison when kind-lists differ
**Why out of scope**: How a consumer reads "absent subspace" across documents of differing vintages (absent-means-zero vs. absent-means-unsupported) is correctly held as an open question, not resolved in this ASN.

VERDICT: REVISE
