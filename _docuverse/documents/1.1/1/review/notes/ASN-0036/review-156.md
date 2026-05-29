# Review of ASN-0036

The state model (S0–S5), attribution chain (S7-family), and the partition/contiguity stack (S8, D-CTG, D-CTG-depth, D-MIN, D-SEQ) are technically sound. I checked the S8 within-subspace incompatibility lemma (both branches j<m and j=m), the across-subspace argument via T5/T10, the D-CTG-depth infinite-witness construction against S8-fin, and the D-SEQ four-step assembly — each holds, with boundaries (empty arrangement, m=2 vs m≥3, zero multiplicity) covered. The worked example exercises S0, S3, S5, S7, S8, D-SEQ across three states, and the two same-valued 'l' characters at distinct addresses concretely witness S4. My findings are confined to residual prose, consistent with the note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: "The document as arrangement" section advances no formal claim and reaches into out-of-scope versioning
**ASN-0036, The document as arrangement**: "Yet they remain distinct documents with independent arrangements: identity rests on document identifiers (tumblers, per T3) or arrangement functions, not on rendered content. Conversely, a single document's arrangement changes across versions while the underlying Istream content is unchanged."
**Problem**: This section introduces no Property and discharges no postcondition. Its load-bearing sentence asserts a *document-identity criterion* that is not formalized anywhere in this ASN, and the "changes across versions" clause trades on version semantics, which the Scope list excludes ("document creation and lifecycle ... versioning"). The remaining in-scope content (arrangement ≠ content; address-identity not value-identity) is already established by S4 and the two-stream framing in "Two components of state." The precise reader must read past it to reach no new obligation. The braid analogy itself is fine (analogies are protected); the unformalized identity claim and the versioning reach are the issue.
**Required**: Either drop the section, or trim it to the analogy alone and remove the document-identity / cross-version assertions (which belong to a document-lifecycle or version ASN).

### Issue 2: Duplicated explanation of the subspace identifier
**ASN-0036, S8a prose** ("Its first component `v₁` is the subspace identifier (1 for text, 2 for links); the `0` in full tumbler notation ... is a field separator, not a subspace identifier") **and Arrangement contiguity intro** ("Write `S = subspace(v) = v₁` for the subspace identifier (the first component of the element-field V-position)").
**Problem**: The same fact — `v₁` is the subspace identifier — is explained twice in different words in different sections. The second restatement is more than the section-local notation `S` requires.
**Required**: State the subspace-identifier reading once (S8a, where the separator-vs-identifier distinction is genuinely load-bearing) and let the D-CTG section introduce only the abbreviation `S = v₁` without re-explaining its meaning.

## OUT_OF_SCOPE

### Topic 1: Subspace alignment between `subspace(v)` and the subspace field of `M(d)(v)`
**Why out of scope**: S3 permits a text V-position to map to a link-subspace I-address; nothing here forbids it. The ASN already names this as an operations-layer preservation obligation in Open Questions. Correctly deferred — flagging only to confirm the deferral is intentional, not a gap in this ASN.

VERDICT: REVISE
