# Review of ASN-0100

## REVISE

### Issue 1: Redundant restatement in Cross-document independence

**ASN-0100, §Cross-document independence (Q3)**: The second paragraph — "The two documents may share I-addresses through transclusion, but the cross-document frame and content preservation together ensure that the shared I-addresses' values and the *other* document's mappings are unaffected." — restates the first paragraph, which already concludes that "any document `d'` that transcludes content from `d` continues to map the same V-positions to the same I-addresses, and those I-addresses continue to resolve to the same values."

**Problem**: Two paragraphs in the same section assert the same guarantee (transclusion sharing + frame ⇒ unaffected) in different words. The second adds no new content; the substantive third paragraph (link-projection independence via LP4) carries the real extension.

**Required**: Delete the second paragraph; let the first paragraph and the link-projection paragraph stand.

### Issue 2: Redundant restatement in Cross-subspace isolation

**ASN-0100, §Cross-subspace isolation**: The second paragraph — "INSERT's shift is scoped strictly to `s_C`; non-text positions are never in the shift's carrier. The frame `INS.frame.subspace` (`V_{s_L}(d') = V_{s_L}(d)` with mappings unchanged) establishes the isolation directly." — restates the first paragraph, which already states "the frame ... directly preserves all subspaces of `d` other than the text subspace. In particular, `V_{s_L}(d') = V_{s_L}(d)`, and link-subspace mappings are unchanged."

**Problem**: The same isolation claim is made twice; both cite the same frame. The Gregory/knife paragraph that follows is the only one adding new (implementation-contrast) content.

**Required**: Collapse the two isolation paragraphs into one.

## OUT_OF_SCOPE

(none — the INSERT-vs-COPY discussion and identity corollaries are kept to a single sentence on COPY and otherwise establish genuine INSERT properties, so they are in scope.)

VERDICT: REVISE
