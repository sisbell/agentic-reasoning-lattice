# Review of ASN-0069

## REVISE

### Issue 1: V1's claim box recapitulates its own proof

**ASN-0069, §"Identity by Sub-Allocation", V1**: "Document(d_new) (by the Document induction above on A_v(d_src)'s emission count, which combines K.δ-ID.zeros-0/1's zero-preservation at k = 0 and k = 1 with P1-supplied membership d_prev ∈ E_doc at every inductive step), and parent(d_new) = parent(d_src) (by the parent-equality induction above ..., which combines K.δ-ID.parent-0/1's per-step preservation at k ∈ {0, 1} with the inductive hypothesis parent(d_prev) = parent(d_src) at every subsequent-emission step)."

**Problem**: The two inductions are already fully written out in the prose immediately preceding V1 (Document base/step and parent base/step). The V1 box re-narrates the method of each proof. This is essay content in a structural (claim) slot — the box should state the postcondition, not reproduce the argument that was just given. The parentheticals add no reasoning the reader does not already have one paragraph above.

**Required**: Reduce the V1 parentheticals to a bare pointer (e.g., "Document(d_new), parent(d_new) = parent(d_src) — both by the inductions above"). Keep the proof in the prose, not in the claim.

### Issue 2: V11's inline statement embeds the proof's premises as explanatory parentheticals

**ASN-0069, §"Composability", V11 statement**: "...where each step dⁱ⁻¹_new → dⁱ_new is a fork composite that is the *first* fork of its immediate source d^{i-1}_new — so that step i's J4 content source operand d_op equals d^{i-1}_new, and V4 at step i reads M(d^{i-1}_new) — and *each step's source has its content-subspace arrangement unchanged ...* — that is, for every 1 ≤ i ≤ k, ... (with the convention that at i = 1, "step 0's post-state" denotes Σ itself — equivalently the pre-state of step 1 — so the premise at i = 1 is satisfied trivially by reflexivity ...)".

**Problem**: The statement of V11 carries nested em-dash asides that explain *why* the operand is d^{i-1}_new and *how* the i=1 convention is discharged — content that belongs in the derivation, which immediately follows and indeed re-states all of it. The claim becomes unreadable as a claim; the reader must mine a single sentence for the actual postcondition.

**Required**: State V11 as the bare implication (premises: first-fork chain from Σ, per-step unedited operand; conclusion: M^k(d^k_new)(v) = M(d_src)(v) for v ∈ V_{s_C}(d_src)). Move the operand identification and the i=1 reflexivity remark into the derivation, where they are already present.

### Issue 3: V8a is "derived" by forward-reference to V11 with a verbatim-transfer claim

**ASN-0069, §"Structural Correspondence", V8a derivation**: "V11's induction (derived in §"Composability") consumes only V4 at each step ..., the per-step unedited premise on that operand, and V5 at the base step — none of which distinguishes inc(·, 0) from inc(·, 1). The induction therefore transfers verbatim with wⁱ⁻¹ in place of dⁱ⁻¹_new."

**Problem**: Two flagged patterns compound here. (a) Forward-reference accretion: V8a (in §"Structural Correspondence") defers its entire proof to V11, which appears later in §"Composability"; the paragraph before V8 already deferred to V8a ("...is V8a below"), producing a deferral chain V8 → V8a → V11. (b) The derivation is a meta-argument that another claim's proof applies, not a derivation. The configurations genuinely differ — V8a's version stream advances by inc(·, 0) subsequent-forks of a single source d_src, while V11's chain advances by inc(·, 1) first-forks of nested sources — and "transfers verbatim" stands in for showing it.

**Required**: Either (i) restructure so the shared induction is proved once and both V8a and V11 are stated as its instances at the point of proof (eliminating the forward reference), or (ii) if V8a is to remain a corollary, replace "transfers verbatim" with the explicit statement of which induction it instantiates and drop the speculative dependency-audit prose. Do not leave a claim whose only support is a pointer to a downstream proof of a structurally distinct claim.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork during source modification
The Open Questions raise guarantees under concurrent arrangement modification. Correctly deferred — the sequential atomic transition axiom bounds the present treatment, and a concurrency model is future territory.

### Topic 2: Fork of a transcludent source (origin(a) ≠ d_src in M(d_src))
Listed in Open Questions. Belongs to a future ASN; the present derivation legitimately assumes home-document content for its worked claims.

VERDICT: REVISE
