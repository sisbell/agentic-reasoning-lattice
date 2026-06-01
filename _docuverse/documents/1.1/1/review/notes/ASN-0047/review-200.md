# Review of ASN-0047

## REVISE

### Issue 1: ParentAllocatorDispatch is proven only for `A_v(d)` but invoked for account-level allocators

**ASN-0047, *Allocator hierarchy under documents* (ParentAllocatorDispatch) and *K.δ case (ii) discharge* (k = 2, Sub-case A)**: The sub-lemma's proof ("*Proof of the two cases*") establishes the dispatch only for `A_v(d)` — its cases (a') and (b') are both about the version sub-allocator of a document. But K.δ k = 2 Sub-case A invokes it for an *account* operand: "By ParentAllocatorDispatch ..., t ∈ E with parent(t) a node forces t to be an emission of A_account(parent(t)) — ... so the membership obligation t ∈ dom(A_account(parent(t))) discharges directly via T10a.6."

**Problem**: T10a.6 supplies *uniqueness* of the owning allocator, not its *identification*. Concluding that the account `t`'s unique owning allocator is specifically `A_account(parent(t))` requires the structural fact that account-level (`zeros = 1`) addresses under a node are emitted only by that node's account sub-allocator. That fact is true by the K.δ construction but is established nowhere; the cited lemma's case analysis does not cover it. The same overstatement carries the spawnPt premise for the first-account and first-document descents, which the entire k = 2 activation discharge rests on.

**Required**: Either generalize ParentAllocatorDispatch's case analysis to every entity-hierarchy sub-allocator level (node→account, account→document, document→version), or add an explicit account-level (and document-level) identification step showing that the unique T10a.6 owning allocator of an account is `A_account(parent(t))`.

### Issue 2: The "depth is re-pinned after clearance" claim is stated three times in near-identical prose

**ASN-0047, *Link-subspace V-position depth (operational)*; K.μ⁺ precondition (*First content insertion*); K.μ⁺_L precondition (depth bullet)**: Three separate paragraphs assert the same rule — that a subspace's V-position depth is the live S8-depth value while the subspace is non-empty, is *not* a permanent per-document constant, is re-pinned at any `m ≥ 2` after full clearance, and "matches the implementation."

**Problem**: This is the duplication the anti-bloat classifier flags ("two paragraphs in the same document say the same thing in different words"). The content subspace paragraph even says "applies mutatis mutandis to the content subspace," then a separate paragraph restates it for content anyway. A reader must reconcile three copies to confirm they agree.

**Required**: State the live-depth-re-pinning rule once (e.g., at the `m_L(d)` definition, generalized to both subspaces) and replace the other two occurrences with a one-line back-reference.

### Issue 3: Forward-reference deferral cluster in the K.μ~ admissibility argument

**ASN-0047, *Decomposition of K.μ~***: Admissibility clause (i) is "an assumed condition on π, shown realisable by Step (B) below"; Step (A) is "consumed" by Step (B); Step (B)'s S3★ obligation defers to "the admissibility filter (above)"; the *Necessity and sufficiency* proof defers to Steps (A)/(C)/(D); ValidComposite★ clause (1) defers to "its definition above"; and the verification-matrix K.μ~ cells defer to "Steps 1–3 of the link-subspace fixity proof."

**Problem**: The realisability/admissibility argument is distributed across five mutually-deferring fragments (Step A ↔ Step B, filter ↔ Step B.3, necessity ↔ Steps C/D). The note flags "multiple paragraphs in different sections defer to the same downstream location." The reader cannot verify any single fragment without holding the others open; in particular the S3★(Σ') ↔ subspace-preservation dependency between Step (A) and Step (B.3) reads as circular until the "filter vs. realisability" distinction is reconstructed by the reader.

**Required**: State once, at the head of the section, that admissibility (i) is a *filter* (S3★(Σ') is a hypothesis on the π considered) and that Step (B) establishes *non-vacuity* (the decomposition realises such π). Then each step can cite that framing instead of re-deferring across sections.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: J4 fork starts the forked document's link subspace empty and explicitly defers any link-inheritance mechanism to a future ASN; this is new territory, not an error.

### Topic 2: Link withdrawal / tombstoning reconciliation with D-CTG★/D-MIN★
**Why out of scope**: The open question on a separate withdrawal mechanism (status flag / tombstone) is correctly deferred — D-CTG★ admits only suffix truncation, and a non-suffix withdrawal primitive is future work, not a defect here.

VERDICT: REVISE
