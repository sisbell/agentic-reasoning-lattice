# Review of ASN-0069

## REVISE

### Issue 1: Parent-equality induction previews itself, then proves the same thing formally
**ASN-0069, §"Identity by Sub-Allocation"**: "the induction chains this per-step preservation across `A_v(d_src)`'s emission count to recover `parent(d_src)` from any emission. The first-emission step uses `k = 1` and reaches `parent(d_src)` directly; each subsequent sibling-stream step uses `k = 0` and reaches `parent(d_prev)`, which the inductive hypothesis identifies with `parent(d_src)`."

**Problem**: This sentence is a prose preview of the *Base case (first fork)* and *Inductive step (subsequent fork)* blocks that immediately follow it — "first-emission step uses k=1 → parent(d_src) directly" is the base case; "subsequent step uses k=0 → parent(d_prev) = parent(d_src) by IH" is the inductive step. Two passages in the same section state the same induction in different words. This is the duplication the anti-bloat pass targets. (The companion `Document(d_new)` induction does this correctly — a single one-sentence intro, no restated structure.)

**Required**: Cut the previewing third sentence ("The first-emission step uses `k = 1`... identifies with `parent(d_src)`"). The formal Base case and Inductive step blocks carry the argument unaided; the per-step relation citation (K.δ-ID.parent-0/1) in the preceding sentence is sufficient orientation.

### Issue 2: Vague downstream deferral in the empty-source section
**ASN-0069, §"The Empty-Source Case"**: "Each Vn whose quantifier ranges over `V_{s_C}(d_op)` holds vacuously in this case; see each property's own clause."

**Problem**: "see each property's own clause" defers to an unenumerated, scattered set of downstream locations rather than advancing the argument. The reader cannot act on it without hunting through every Vn. This is the deferral-accretion pattern.

**Required**: Either drop the sentence (the vacuity is already stated property-by-property where it matters — V4 names it explicitly, V6/V9 fall out of K.δ-alone) or name the specific properties affected (V4, V8, V9, V12(d)) in one line.

### Issue 3: Redundant restatement of the operand distinction in the introduction
**ASN-0069, §"What Must Be Constructed"**: "J4 distinguishes two operands. The *identity source* is `d_src`... The *content source operand* `d_op`... J4's operand-tracking rule fixes it by sub-case, formally stated in V1 below. The distinction that matters here is identity-source versus content-source."

**Problem**: The final sentence ("The distinction that matters here is identity-source versus content-source") restates the distinction the preceding two sentences just drew. The "formally stated in V1 below" clause is a forward pointer to a property four sections away. Both are accretion around the operand setup.

**Required**: Drop the closing restatement sentence; the two definitional sentences already establish the distinction. Drop or inline the "stated in V1 below" pointer — V1 is the natural place a reader looks for the identity, no signpost needed.

## OUT_OF_SCOPE

### Topic 1: `≼`-transitivity proof located in V11a
**ASN-0069, §"V11a"** proves transitivity of the foundation prefix relation `≼` inline, noting "ASN-0034's Prefix contract publishes only the definition... not transitivity." This is correctly handled (the foundation genuinely does not export transitivity, so proving it where needed is legitimate), but the property arguably belongs in the ASN-0034 Prefix contract rather than re-derived per consumer. Not an error in this ASN — a foundation-contract gap to route upward, not a revision here.

VERDICT: REVISE
