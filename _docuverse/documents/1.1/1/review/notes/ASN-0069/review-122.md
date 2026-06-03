# Review of ASN-0069

The mathematics here is sound. I checked the frame-composition arguments (V5a, V10b), the two parallel inductions in §"Identity by Sub-Allocation", the K.δ sub-case discharges (both first- and subsequent-fork), the ValidComposite★ verification (including the empty-source K.δ-alone branch), and V11's chain induction with its Σ-as-step-0 convention. The boundary cases that usually break fork specs — empty source (V7), prefix-only K.μ⁻ deletion, second-fork-tracks-prior-version semantics — are all handled and honestly documented. The proofs are real proofs, not checkmarks.

The findings below are the residual meta-prose this note carries under the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Restatement sentence in the operand-distinction paragraph
**ASN-0069, §"What Must Be Constructed"**: "The identity source is `d_src`... The content source operand `d_op` is the document whose content-subspace arrangement is transcribed into `d_new`... **The distinction that matters here is identity-source versus content-source.** J4's precondition..."

**Problem**: The middle sentence restates the distinction the two preceding sentences just drew (one named the identity source, the next named the content source operand). It says the same thing in different words and the reader skips it to reach J4's precondition. Pattern #7 (two statements saying the same thing).

**Required**: Delete "The distinction that matters here is identity-source versus content-source." The two definitional sentences already carry it.

### Issue 2: Method-description meta-prose around J4 adoption
**ASN-0069, §"What Must Be Constructed"**: "The composite is J4 of ASN-0047, named *ForkComposite*. We adopt it as the structural skeleton and derive from first principles what it guarantees, what it forbids, and what it leaves to the source-fork relationship."

**Problem**: The second sentence describes the document's method ("we adopt... and derive...") rather than advancing any claim. It is skippable essay content in a structural slot — nothing downstream depends on it.

**Required**: Drop the second sentence; "The composite is J4 of ASN-0047, named ForkComposite" suffices to anchor the reference.

### Issue 3: V4 restated three times in succession
**ASN-0069, §"The Arrangement Layer"**: V4 is stated formally, then "V4 makes two distinct claims. First, the V-positions are inherited literally... Second, the I-addresses at each position are inherited literally...", then (after the justification paragraph) "For every `v ∈ V_{s_C}(d_op)`, `M(d_op)(v)` is defined... and by V4 `M'(d_new)(v)` is defined and equal to it: the same V-position tumbler carries the same I-address in both arrangements."

**Problem**: V4's content appears three times — the formal statement, the "two distinct claims" unpacking, and the closing "carries the same I-address" sentence. The closing sentence's only non-redundant content is the well-definedness note (`M(d_op)(v)` defined because `v ∈ dom(M(d_op))`); its conclusion merely re-asserts V4.

**Required**: Keep the "two distinct claims" split (it sets up the two-part justification that follows) and fold the well-definedness observation into it; delete the trailing restatement.

## OUT_OF_SCOPE

None. The ASN stays within fork semantics and does not stray into INSERT/DELETE/COPY/REARRANGE mechanics, link semantics, the version DAG, or replication. Its use of K.μ⁻ in the worked example is illustrative of V5a isolation, not a deletion-operation definition.

VERDICT: REVISE
