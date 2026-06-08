# Review of ASN-0111

The operation is sound: `readlink(a, Σ) ≡ Σ.L(a)` is a pure lookup, and the claims RL0–RL8 plus the well-formedness family follow trivially or by cited foundation results. The worked example checks out arithmetically (δ(2,8) advance to `…1.3`, the LP-Fin chain members, the ghost-type subtree coverage, the nested `a'`/`c` construction). I found no technical gap, missing boundary case, or unproven postcondition. Every finding below is the accretion this review-mode is meant to catch.

## REVISE

### Issue 1: The same operation-contrast is delivered three times
**ASN-0111, "The problem" / "Completeness: the read returns the whole relationship" / "A worked read" (RL1 bullet)**: the from/to-follow vs. search vs. count distinction appears in the intro ("*Following* a link… *Searching*… *Counting*…"), again as "A search is satisfied by a witness… A direct read has no request to satisfy," and a third time in the RL1 bullet ("Contrast a *search* given the content region under `d₁`…").
**Problem**: Two later passages restate the intro's contrast in different words. The first occurrence (or a single consolidated one) carries the point; the repetitions are noise the reader must re-skim. Per the anti-bloat guidance, two paragraphs saying the same thing in different words is a finding.
**Required**: Keep one statement of the read-vs-search/follow/count contrast (the intro). Cut the restatements in the Completeness section and trim the RL1 bullet to the concrete check.

### Issue 2: Essay framing in "Deriving the read"
**ASN-0111, "Deriving the read"**: "The whole interest of the operation lies not in this one line but in what the one line *commits us to* — the properties the returned value must have, and what those properties let a reader learn."
**Problem**: This sentence advances no reasoning; it is commentary on the structure of the note ("the interest lies in what follows"). It is the kind of meta-prose a precise reader works around to reach the next claim.
**Required**: Delete. Proceed directly from the `readlink` definition to RL0.

### Issue 3: A full section devoted to a fact the operation does not deliver
**ASN-0111, "Ownership lives in the read key"**: an entire section, including the *Remark (home from the key)*, establishing `home(a) = N(a).0.U(a).0.D(a)` from the address key.
**Problem**: The section introduces no RL claim and explicitly states the home is recovered from the *key*, "independent of the returned endsets" — i.e. it is not part of what `readlink` returns. It restates L2 (ASN-0043) wrapped in essay ("A relationship is a *claim*, and a claim has an author"). A claimless section about what the read does *not* deliver is essay content in a structural slot.
**Required**: Either attach a labeled claim if ownership-from-key is a guarantee this ASN means to assert, or compress the whole section to a one-line remark citing L2. The "claim has an author" framing should go.

### Issue 4: Defensive/exhaustiveness prose in RL2
**ASN-0111, RL2**: "The quantifier ranges over *all* `|Σ.L(a)|` slots, not a fixed three… while the model admits `N > 3` (L3, ASN-0043, requires only `N ≥ 3`), with slots 4…N returned faithfully under their own indices and no privileged role assigned by this operation."
**Problem**: "ranges over all slots, not a fixed three" and "no privileged role assigned" are exhaustiveness/defensive claims that restate L3 rather than advance RL2. The formal statement `|readlink(a, Σ)| = |Σ.L(a)|` already carries the arity-N content; the prose justifies the quantifier against an imagined fixed-arity reading.
**Required**: State the arity-N case once (slots 1/2/3 are from/to/type, higher slots returned under their indices) and drop the "not a fixed three" / "no privileged role" defenses.

### Issue 5: Recap sentence adds nothing
**ASN-0111, end of "The structure the read must preserve"**: "We can summarise RL1–RL3 in one sentence: the read returns the *complete* relationship, *grouped by role*, *unordered within each role*."
**Problem**: A recap of three adjacent claims the reader has just read. Mild, but it is prose that does not advance the argument.
**Required**: Cut, or fold the three adjectives into RL3's closing line if a summary is wanted.

## OUT_OF_SCOPE

(none — the ASN correctly defers following, searching, counting, creation, editing, and projection to their own ASNs, and does not smuggle in claims for them.)

VERDICT: REVISE
