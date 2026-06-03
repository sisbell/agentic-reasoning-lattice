# Review of ASN-0069

## REVISE

### Issue 1: Document(d_new) is re-proved by induction when the foundation supplies it directly
**ASN-0069, §"Identity by Sub-Allocation"**: "We establish `Document(d_new)` in both cases by induction on `A_v(d_src)`'s emission count. *Base case (first fork).* ... K.δ-ID.zeros-0/1 at `k = 1` gives `zeros(d_new) = zeros(d_src) = 2`, hence `Document(d_new)`. *Inductive step (subsequent fork).* ... `zeros(d_new) = zeros(d_prev) = 2`, hence `Document(d_new)`. ∎"

**Problem**: ASN-0047's *Allocator hierarchy* (a foundation here) states for the version sub-allocator: "A_v(d) — d's version sub-allocator. First emission is inc(d, 1). **Outputs inhabit E_doc.**" Since `E_doc = {e ∈ E : Document(e)}`, every emission of `A_v(d_src)` — including `d_new` — is a document by direct citation, and `zeros(d_new) = 2` then follows by T4c. The two-case zeros induction re-grounds a fact the foundation already publishes (Standard 7: ASNs may use foundation definitions without restating them). This is the anti-bloat over-derivation pattern. Note the *parent* induction immediately following is genuinely needed (the foundation gives no `parent(A_v output) = parent(d_src)` clause), so only the Document/zeros induction is redundant.

**Required**: Replace the Document induction with a one-line citation of ASN-0047's Allocator hierarchy (`A_v(d_src)` outputs inhabit `E_doc`, hence `Document(d_new)`, hence `zeros(d_new) = 2` by T4c). Keep the parent induction.

### Issue 2: §"Sharing, Not Duplication" refutes a discipline that J4 already forecloses
**ASN-0069, §"Sharing, Not Duplication"**: "There are two candidate disciplines: *Duplication.* ... *Transclusion.* ... The duplication discipline contradicts Nelson's central design commitment. It produces two distinct I-addresses ... Royalty splits collapse; link survivability fails ... duplication forces a K.α step for every byte, which the foundation's J0 ... requires to be paired with placement ..."

**Problem**: The operation this ASN derives is J4 (ForkComposite, foundation), whose clause (ii) *defines* the inherited arrangement via the bijection `φ` with `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})` — i.e., transclusion is built into the foundation composite, and duplication is not an admissible instantiation at all. The multi-sentence refutation of duplication (origin severing, royalty collapse, link survivability, J0 coupling) argues against a case the carrier J4 already excludes. The section itself then concedes "J4's defining clause makes the discipline explicit." This is the anti-bloat pattern of imagining and refuting a precondition-excluded case.

**Required**: Reduce the duplication contrast to a single sentence noting J4 clause (ii) fixes the range to `ran(M(d_op))` (no K.α), then cite J4 for V3/V4. Retain at most the Nelson "inclusion" grounding; drop the extended consequence-by-consequence refutation.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork during source modification
**Why out of scope**: The first Open Question (fork invoked while source arrangement is concurrently modified, beyond the sequential atomic axiom) is genuinely new territory — a concurrency-model ASN, not a defect here.

### Topic 2: Fork of a transcludent source
**Why out of scope**: The Open Question on forking when `M(d_src)` already references I-addresses with `origin ≠ d_src` extends the model; correctly deferred.

VERDICT: REVISE
