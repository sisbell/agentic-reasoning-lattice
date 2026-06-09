# Review of ASN-0121

## REVISE

### Issue 1: Home-component address-space declaration contradicts the worked example

**ASN-0121, "What is being matched"**: "The home-component `H` ranges over document-address space; the three endset-components `F, G, Θ` range over I-address space."

**Problem**: The body and the worked example rely on `H` being rooted at *node*, *account*, or *document* level, not just document level. The same section states "`H` may bound residence at the granularity of a node, an account, or a single document," and Trace 6 explicitly constructs `H_node` "rooted at the node `[1]`" — a node address (`zeros = 0`), which is not in document-address space (`zeros = 2`). So the setup's claim that `H` ranges over *document*-address space directly contradicts the operation actually demonstrated in Trace 6 and the FL-RES discussion. `home(a)` is always document-level, but the *request component* `H` is not.

**Required**: Restate the home-component's range to cover the residence/organizational axis (node/account/document-rooted spans whose coverage is the corresponding subtree under T5), reserving the I-address (element-level) axis for `F, G, Θ`. The contrast intended is organizational-prefix space vs. element-level I-address space; "document-address space" is too narrow and is falsified by `H_node`.

## OUT_OF_SCOPE

(none — the version-qualified inquiry and federation-reach questions are correctly recorded as Open Questions, not claimed; retired/sibling operations are not specified here.)

Notes for the record (not REVISE): the forced-answer derivation of FL-DEF from soundness+completeness, the structural proof that `nullified` is a function of `Σ.L` alone, the FL-REACH self-correction restricting containment to *satisfying* discoverable links (with strictness under satisfying orphans), the FL-DIR address witness, and the six-trace worked instance are all rigorous and check out arithmetically (addresses, zero-counts, subtree disjointness, and `athome` membership all verified).

VERDICT: REVISE
