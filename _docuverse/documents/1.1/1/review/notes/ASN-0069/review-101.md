# Review of ASN-0069

## REVISE

### Issue 1: Two sections both defer the `d_new` allocation formulas to V1
**ASN-0069, §"What Must Be Constructed"**: "The distinction that matters here is identity-source versus content-source; the corresponding `d_new` allocation formulas are deferred to V1."
**ASN-0069, §"Identity by Sub-Allocation", item (i)**: "the next address a fork emits is `next(s.B, d_src, 1)` (NextAddress, ASN-0040), whose explicit sub-case formulas are stated in V1."

**Problem**: This is the forward-reference accretion pattern "multiple paragraphs in different sections defer to the same downstream location." Both passages tell the reader the allocation formulas live in V1 without stating them. A reader following the argument hits the same "see V1" pointer twice across two sections before reaching V1.

**Required**: Keep a single deferral. The §"Identity by Sub-Allocation" item (i) deferral is the natural one (it sits in the section that builds toward V1); drop the redundant "deferred to V1" clause from the §"What Must Be Constructed" J4 paragraph, which can simply note the identity-source/content-source distinction without re-promising the formula location.

### Issue 2: Open Questions restate results the ASN has already established
**ASN-0069, §"Open Questions"**: "What invariants must hold when a fork is followed immediately by deletion of content from the source — must the fork's inherited arrangement remain referentially valid, and through what mechanism?" and "What must the system guarantee about correspondence under the special case where the fork operation is applied with the source equal to its own previous fork — i.e., forks of forks within a single editorial session?"

**Problem**: Both are answered in the body. The fork-then-deletion question is exactly the worked example's "*Subsequent edits*" paragraph, which shows the fork's arrangement survives source deletion (V5a) with content persistence (V12(b)) and provenance persistence (V12(c)) — the "mechanism" the question asks for. The fork-of-fork correspondence question is V11 (transitive identity along unedited fork chains) plus the worked example's chain paragraph. An open question that the same document closes is noise the reader must reconcile.

**Required**: Remove these two from Open Questions, or narrow them to the genuinely-unanswered residue (e.g., correspondence under *edited*-source chains, which V11's premise explicitly excludes; or deletion ordering beyond the single-step atomic case).

## OUT_OF_SCOPE

### Topic 1: Mixed first-fork/subsequent-fork chains in V11
V11 restricts to "first-fork" chains (each step is the first fork of its immediate source). Correspondence along a chain that interleaves subsequent forks (k=0 emissions) is not derived. This is a reasonable boundary for this ASN, not an error — the restriction is stated explicitly in the premise. A general-chain correspondence theorem belongs to a future ASN.

VERDICT: REVISE
