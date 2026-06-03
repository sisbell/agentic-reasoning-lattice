# Review of ASN-0102

## REVISE

### Issue 1: The symbol `p` is overloaded with two distinct meanings

**ASN-0102, "The source designation and its resolution" / P1 / P4**: The source is "a content reference sequence `R = ⟨r₁, …, r_p⟩`" (so `p` = number of references), and `k = (+ i : 1 ≤ i ≤ p : k_i)`. But P4 sets `v = [s_C,1,…,1,p]` with `1 ≤ p ≤ n_S + 1` (so `p` = insertion-position last component), and X12/X16/the worked example all use this second meaning ("we copy at `v = [1,3]`, so `p = 3`").

**Problem**: The two meanings collide inside a single precondition. P1 reads "Since `p ≥ 1` and each reference has positive resolved width … the total width satisfies `W ≥ 1`" — here `p ≥ 1` must mean *number of references*, yet three paragraphs later `p` is the insertion position. A reader cannot tell which `p` is meant without reconstructing context, and the `W ≥ 1` argument silently depends on the reference-count reading. Dijkstra would not tolerate a symbol that changes denotation between P1 and P4.

**Required**: Rename one of the two. Use a distinct symbol for the reference count (e.g. `R = ⟨r₁, …, r_q⟩`, `k = (+ i : 1 ≤ i ≤ q : k_i)`) and reserve `p` for the insertion-position component, or vice versa. Audit every occurrence (P1, the cardinal-question `k` sum, X11's "`r` distinct origins" which is yet a third single-letter count, X14's `k` sum).

### Issue 2: X10's name and table summary overstate the guarantee for the self-source case

**ASN-0102, X10 (table)**: "SourceNonInterference — no source document's arrangement, content, or origins are altered."

**Problem**: When `d_s = d` (self-transclusion, explicitly admitted), the source document *is* altered — it is the target, and its content-subspace arrangement is displaced. The formal claim in the body is correctly scoped (`(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))` plus a *snapshot-resolution* property for `d_s = d`), but the claim name and the Claims-Introduced table assert the stronger, false universal "no source document … is altered." The guarantee that actually holds for `d_s = d` is not non-alteration but pre-state resolution — a different property.

**Required**: Scope the name/summary, e.g. split X10 into (a) non-interference for sources `d' ≠ d` and (b) snapshot resolution for `d_s = d`; or state the table entry as "no source document *other than the target* is altered; the target-as-source is read at the pre-state." As written the table claim contradicts the case the body then discusses.

### Issue 3: `wp(COPY, S3★)` is called a "biconditional" but is a universal membership condition

**ASN-0102, "What is preserved" (wp computation)**: "Hence the whole of S3★ reduces to a single biconditional obligation on the copied region: `wp(COPY, S3★) ≡ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C))`."

**Problem**: The displayed formula is a universally-quantified membership statement, not a biconditional. S3★ restricted to the copied region is the implication `subspace = s_C ⟹ image ∈ dom(C)`; since `subspace = s_C` is a fact (P3), the wp is just the consequent — there is no "if and only if." The word "biconditional" is simply wrong for the obligation stated, in the one place the proof is doing its load-bearing reduction.

**Required**: Replace "single biconditional obligation" with "single membership obligation" (or similar). The math is right; the description of it is not.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by later operations
The first open question (origin/discoverability under subsequent displacement) concerns interaction with INSERT/DELETE/REARRANGE mechanics, which are out of scope for this ASN. Correctly deferred.

### Topic 2: Chained provenance when a reference-importing document is itself a source
The second open question belongs to a future provenance/version ASN; not an error here.

VERDICT: REVISE
