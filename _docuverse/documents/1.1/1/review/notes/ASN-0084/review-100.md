# Review of ASN-0084

## REVISE

### Issue 1: R-CANON's ordinal-arithmetic and predecessor/successor facts are licensed only at depth 2 / V_S(d), but the lemma is applied to non-S runs whose subspaces this ASN does not depth-restrict

**ASN-0084, R-CANON proof**: "We first record a fact used twice: at the fixed depth of V_S(d), each V-position has a unique immediate ordinal predecessor and successor, and shift is strictly increasing and injective in its amount (TS4, TS2, ASN-0034)."

**Problem**: R-CANON is stated and used over an arbitrary covering, disjoint partition of *all* of `dom(M'(d))`, which includes non-S runs (the sixth worked example invokes R-CANON for a partition containing the link run `([2,1], L, 1)`). The proof's forward-extension and backward-extension arguments both turn on uniqueness of the immediate ordinal predecessor/successor and on equalities like "`v″ + (j+1)` has ordinal `ord(u)+1 = ord(v)`, so `v″ + (j+1) = v`" — i.e. that a V-position is determined by (subspace, ordinal) at a fixed depth, and that `ord(·) − 1` / `ord(·) + 1` are well-defined. The scope restriction of this ASN fixes only the **text** subspace at depth 2 ("documents with m_1 > 2 are outside the scope of this ASN"); S8-depth (ASN-0036) explicitly permits *distinct subspaces to have distinct depths*. The singleton-ordinal identification and `ord(c') − ord(c)` machinery are erected only for depth-2 `V_S(d)`. For a non-S run at depth > 2, `ord(v) = [v₂, …, vₘ]` is not a singleton, so "`ord − 1`," the truncated subtraction, and "unique immediate ordinal predecessor at the fixed depth" are not discharged. The recalled fact "at the fixed depth of V_S(d)" does not cover these runs, yet the proof applies the resulting reasoning to every run of B′.

**Required**: Either (a) restrict R-CANON's hypothesis/conclusion to the subspace-S (depth-2) portion of the partition and discharge maximality of carried-over non-S runs by a separate argument (they are π-fixed and inherited verbatim from the pre-state maximal partition), or (b) generalize the predecessor/successor and ordinal-determination facts to arbitrary subspaces — citing S8-depth for per-subspace uniform depth and a general same-length immediate-successor result — so the proof's two uses are licensed at every run's actual depth, not only at depth 2.

### Issue 2: Forward-reference / deferral prose bridging R-BLK to R-CANON

**ASN-0084, paragraph following R-BLK**: "R-BLK delivers a partition that is disjoint, covering, and consistent, but explicitly *not* claimed maximal. The worked examples below each finish by exhibiting a partition with no mergeable adjacent pair and naming it the *canonical* (S8-maximal) decomposition. That step needs justification… We supply the bridge."

**Problem** (anti-bloat classifier): The substantive content here — the local (mergeable-pair-free) vs. global (S8-maximal) distinction — is legitimate, but it is wrapped in deferral to downstream worked examples ("The worked examples below each finish by…") and filler ("That step needs justification:… We supply the bridge"). This is prose that motivates *why* R-CANON exists and points forward rather than advancing the argument; the reader must work past it to reach the lemma.

**Required**: Keep the one-sentence local-vs-global distinction; drop the deferral to the worked examples and the "we supply the bridge" framing. The lemma's statement already announces what it does.

### Issue 3: Use-site pointer at the end of R-BLK naming a downstream worked example

**ASN-0084, end of R-BLK**: "The 4-cut worked example below exhibits a B' containing a mergeable pair (B and H, merging into a width-3 run)."

**Problem** (anti-bloat classifier): A lemma's body enumerating a downstream consumer/example is a forward use-site pointer that does not advance R-BLK's claim. The worked example already demonstrates the mergeable pair on its own; the pointer is redundant meta-prose.

**Required**: Remove the sentence. If the existence of post-rearrangement merges needs stating, state it as a property at the point of claim, not as a pointer to an example below.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: The Open Questions correctly defer the generalization beyond 4 cuts and the algebra of composing rearrangements; these are new territory, not defects in the present pivot/swap treatment.

VERDICT: REVISE
