# Review of ASN-0069

## REVISE

### Issue 1: Forward-reference accretion — repeated deferrals to V1 for the allocation formulas
**ASN-0069, §"What Must Be Constructed"/J4-intro and §"Identity by Sub-Allocation"**:
- J4-intro: "the distinction that matters here is identity-source versus content-source; the corresponding `d_new` allocation formulas are deferred to V1."
- §"Identity by Sub-Allocation", item (i): "(i) the next address a fork emits is `next(s.B, d_src, 1)` (NextAddress, ASN-0040), whose explicit sub-case formulas are stated in V1".

**Problem**: Two paragraphs in two different sections defer to the same downstream location (V1) for the same content — the `inc(d_src,1)` / `inc(d_prev,0)` formulas. The second deferral is *inside the very section that derives V1*, so the reader is told the formulas are "stated in V1" while standing in the section that states V1 a few lines later. This is the "multiple paragraphs defer to the same downstream location" meta-prose the anti-bloat pass targets; it does not advance the argument, it only signposts it.

**Required**: Drop the "deferred to V1"/"stated in V1" meta-pointers. The J4-intro can name the identity-source vs content-source distinction without pre-announcing where the formulas live; §"Identity by Sub-Allocation" should simply present the NextAddress consequence and let V1 carry the formulas at its point of statement.

### Issue 2: Additional bare forward pointers ("X below") that signpost rather than reason
**ASN-0069, §"Structural Correspondence" and §"Provenance Recording"**:
- After V8: "the general transitive correspondence across a fork chain — `d_src ↔ d^k_new` for any `k` — is V11 below."
- V9 consequence paragraph: "the fork records `(a, d_new)` (V9) and the operand-side record `(a, d_op)` (V12(d))" — V12(d) is derived later, in §"Permanence Across Source and Fork."

**Problem**: These are navigation pointers to later labels embedded in running prose. Each forces the reader to hold an unresolved reference while parsing the current claim. The "is V11 below" remark adds nothing the V11 entry will not state in place; the V12(d) citation inside V9's consequence creates a dependency from an earlier claim onto a later one.

**Required**: Remove the "is V11 below" sentence (V11 is self-introducing). For the V9 consequence, either move the `{d_op, d_new}`-membership remark to after V12 (so V12(d) is already available), or state only the V9-supported half (`(a, d_new) ∈ R'`) at the V9 site and let the operand-side record appear with V12(d).

## OUT_OF_SCOPE

### Topic 1: Concurrent fork vs. concurrent source modification
The first Open Question (guarantees when a fork is invoked while the source is concurrently modified, beyond SequentialTransitionAxiom) is genuinely new territory — it requires a concurrency model the present sequential-atomic substrate does not expose. Correctly deferred, not an error here.

VERDICT: REVISE
