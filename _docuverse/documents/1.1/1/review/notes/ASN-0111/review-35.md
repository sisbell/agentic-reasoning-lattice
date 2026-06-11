# Review of ASN-0111

## REVISE

### Issue 1: Definedness contract stated two incompatible ways
**ASN-0111, "Deriving the read" / RL0**: "*defined when* `a ∈ dom(Σ.L)`" … "so the read either delivers the whole relationship or **reports that no link lives at `a`**. There is no partial-success middle state."
**Problem**: The formal contract makes `readlink` a partial function — undefined off `dom(Σ.L)`, like every precondition-gated operation in the foundations (K.α, K.λ, etc.). The prose then describes an off-domain invocation that *reports* failure, which is the behaviour of a total operation with a distinguished error outcome. These are different signatures, and the difference is implementation-relevant: since the ASN itself establishes that the structural screen is necessary-but-not-sufficient, a caller cannot in general establish membership before invoking, so whether the operation can be invoked off-domain and what it then yields must be pinned down. The supporting wp paragraph ("fails (rather than becoming ill-defined) when `a ∉ dom(Σ.L)`") talks about the postcondition proposition but feeds the same ambiguity.
**Required**: Choose one reading. Either (a) keep `readlink` partial and strike the "reports that no link lives at `a`" clause (the no-partial-success point survives as: when defined, the result is the entire value), or (b) make the operation total with an explicit failure value in the signature (e.g., `readlink : T × Σ → Link ∪ {⊥}`) and restate RL0 and the wp against that codomain.

### Issue 2: RL6 has no formal statement; the no-flattening commitment is not checkable as written
**ASN-0111, RL6**: "the read discloses `a'` as the tumbler address it is — returned as an address whether it names content or another link, not flattened into whatever further reading of `a'` might yield."
**Problem**: "Discloses as the tumbler address it is" and "not flattened" are not postconditions; nothing in RL6's statement could be verified or falsified against a candidate implementation. The content actually intended is a *locality* property: the result depends only on the single store entry `Σ.L(a)`, never on `Σ.L(a')` for addresses in the returned coverage. Note that RL7 as stated ("pure function of `(a, Σ.L)`") is too weak to deliver this — a function of the whole link store may consult `Σ.L(a')` and flatten, yet still be a pure function of `(a, Σ.L)`.
**Required**: State RL6 formally, e.g.: for any reachable `Σ₁, Σ₂` with `a ∈ dom(Σ₁.L) ∩ dom(Σ₂.L)` and `Σ₁.L(a) = Σ₂.L(a)`, `readlink(a, Σ₁) = readlink(a, Σ₂)` — i.e., `readlink` is a function of `(a, Σ.L(a))` alone, immediate from the definition. This simultaneously sharpens RL7 and makes "no dereference of nested link addresses" a one-line corollary rather than a gloss.

### Issue 3: Structural-screen prose duplicated, with inconsistent condition lists
**ASN-0111, end of "The link as a readable object" and the paragraph following RL0's wp**: "a reader holding a candidate tumbler can test them as a structural screen before invoking the read (RL0)" vs. "A reader holding a candidate tumbler can test the necessary structural conditions from the address alone — `zeros(a) = 3 ∧ subspace_I(a) = s_L` — … necessary but not sufficient".
**Problem**: Two paragraphs in different sections say the same thing in different words — the accretion pattern this review mode flags. Worse, they disagree on what the screen is: the first passage's "them" refers to three conditions (`zeros(a) = 3`, `subspace_I(a) = s_L`, `#E(a) ≥ 2`), the second lists only two, silently dropping `#E(a) ≥ 2` (which is equally address-computable, and equally necessary by L1b).
**Required**: State the screen once, in the RL0 section, with one consistent condition list (`zeros(a) = 3 ∧ subspace_I(a) = s_L ∧ #E(a) ≥ 2`); reduce the earlier passage to at most a forward pointer or remove it.

### Issue 4: Worked example's subtree-containment step cites the wrong T1 case
**ASN-0111, "A worked read", from-set bullet**: "by T1 case (ii) that interval contains the entire subtrees beneath `…1.1` and `…1.2`".
**Problem**: T1 case (ii) justifies only the lower bound for extensions of `…1.1` (proper prefix ⇒ `s < t`). The upper bound `t < [1.0.1.0.1.0.1.3]` for every such `t` is T1 case (i) at divergence position 8 (`1 < 3`, resp. `2 < 3`); and for elements of the subtree beneath `…1.2`, the *lower* bound `s < t` is also case (i) (divergence at position 8, `1 < 2`), not case (ii). As the sole citation, case (ii) covers one of the four obligations. Given the per-step citation convention the foundations enforce, this is a miscitation, not a stylistic nit.
**Required**: Either cite both T1 cases for the respective bounds, or take the cleaner route: decompose the interval as `[…1.1, …1.2) ∪ […1.2, …1.3)` and apply PrefixSpanCoverage (ASN-0043) to each unit sub-interval, which yields exactly the two subtrees.

### Issue 5: Claim labels skip RL3 and RL4 without explanation
**ASN-0111, claim labels and Claims Introduced table**: the sequence runs RL0, RL1, RL2, RL5, RL6, RL7, RL8.
**Problem**: In a self-contained note, the gap reads as two claims having been deleted in a prior cycle with the numbering left behind. A reader has no way to tell whether RL3/RL4 exist elsewhere, were withdrawn, or are reserved.
**Required**: Renumber the claims contiguously (RL0–RL6), or, if the labels are load-bearing for external references, add a one-line note that RL3/RL4 are intentionally retired.

## OUT_OF_SCOPE

### Topic 1: Distinguishing identical-valued links and read-level validity guarantees
**Why out of scope**: The three Open Questions (what a reader may conclude about continued validity, FOLLOWLINK's empty-vs-unwitnessed distinction, address-borne identity of value-identical links) are correctly deferred — they concern traversal and identity semantics beyond a pure store read, and the ASN already marks them as open rather than claiming them.

VERDICT: REVISE
