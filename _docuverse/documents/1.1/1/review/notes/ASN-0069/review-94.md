# Review of ASN-0069

## REVISE

### Issue 1: Internal inconsistency about when the version sub-allocator activates
**ASN-0069, §"Independence Among Forks" (intro) vs. §"The Fork Composite" (K.δ sub-case A)**:

§"Independence Among Forks" states: "The version sub-allocator `A_v(d_src) = S(d_src, 1)` of `d_src` **activates upon `d_src`'s creation** and produces version outputs by repeated sibling generation."

§"The Fork Composite", sub-case A states: "the `(d_src, 1)` child-spawn (**the K.δ event that activates `A_v(d_src)`** and places its base address `inc(d_src, 1)` into `E`) has not yet fired."

**Problem**: These two passages disagree on the activation point of `A_v(d_src)`. The first locates activation at `d_src`'s creation; the second locates it at the first fork (the `(d_src, 1)` child-spawn). This is not cosmetic: the sub-case A freshness discharge *depends* on the reading that the `(d_src, 1)` child-spawn is itself the activating event ("Sub-case A's governing predicate — `A_v(d_src)` has emitted no prior version — *is* the statement that the `(d_src, 1)` child-spawn ... has not yet fired"). Under ASN-0047's allocator model a sub-allocator's existence is tied to emission of its base, and `A_v`'s base `inc(d_src, 1)` is emitted only by the first fork — so "activates upon `d_src`'s creation" is the wrong one. (Note also that SubAllocatorBundle, ASN-0047, activates only `A_C(d)` and `A_L(d)` on document creation, not `A_v(d)`.)
**Required**: Correct the §"Independence Among Forks" prose so it agrees with the fork-composite model — `A_v(d_src)` is activated by its first emission (the first fork), not at `d_src`'s creation.

### Issue 2: Forward use-site inventory of the B-Seq bridge discharge
**ASN-0069, §"Identity by Sub-Allocation"**: "We discharge them once here; **later uses (V10(a), §"Independence Among Forks") cite this bridge.**"

**Problem**: This enumerates the downstream consumers of the discharge — exactly the forward-reference accretion pattern flagged for this note (a discharge's introduction listing where it will later be cited). The discharge stands on its own; the downstream sites (V10(a), §"Independence Among Forks") already point back to it, so the forward inventory carries no reasoning and is pure bookkeeping the precise reader must skip.
**Required**: Delete the "later uses (V10(a), §...) cite this bridge" clause; keep only the discharge itself.

### Issue 3: Duplicate B-Seq bridge citation within §"Independence Among Forks"
**ASN-0069, §"Independence Among Forks"**: the section-intro paragraph — "B8 (Uniqueness, ASN-0040), same-namespace clause — its precondition package discharged for `A_v(d_src)` by the B-Seq bridge of §"Identity by Sub-Allocation" — gives that no two forks of the same source share a tumbler" — and V10(a) — "The same-namespace clause of B8 (Uniqueness, ASN-0040) applies — its precondition package B-Seq, B0a, B1, B2, B4 is discharged for `A_v(d_src)` by the B-Seq bridge of §"Identity by Sub-Allocation" — giving `d_new¹ ≠ d_new²` directly."

**Problem**: Two paragraphs in the same section state the identical fact (B8's same-namespace precondition package is discharged by the §"Identity by Sub-Allocation" bridge, yielding fork distinctness). V10(a) is the formal carrier of the distinctness claim; the intro paragraph re-states it as preview. This is the "two paragraphs saying the same thing in different words" duplication.
**Required**: Drop the distinctness/discharge restatement from the section-intro paragraph (retain at most the B9-unboundedness scene-setting that V10 does not cover), leaving V10(a) as the sole site.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork during source modification
**Why out of scope**: The first Open Question (guarantees under concurrent source modification beyond the sequential atomic axiom) is genuinely new territory — a concurrency model this ASN does not and need not establish.

### Topic 2: Snapshot vs. living fork distinction
**Why out of scope**: Distinguishing frozen-at-fork-time from live-tracking forks (Open Question 3) is a future arrangement-semantics ASN; V4's literal-inheritance commitment fixes the snapshot reading for this ASN and that is sufficient here.

VERDICT: REVISE
