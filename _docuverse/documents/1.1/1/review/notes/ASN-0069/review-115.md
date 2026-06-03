# Review of ASN-0069

This ASN carries the `review-mode.anti-bloat` classifier. The derivation itself is sound — I checked V1 (both inductions), V4/V4b, V5a→V5, V8, V9, V11 (the multi-stage induction closes correctly), V12, and the full ValidComposite★ verification for both the K.δ+K.μ⁺+K.ρ×n and K.δ-alone composites, including the empty-source dispatch. No correctness gaps; edge cases (empty source, prior-version-empty subsequent fork, fork-of-fork chains, sibling forks, interleaved deletion) are handled. The remaining issues are residual meta-prose around forward references, which the anti-bloat pass targets.

## REVISE

### Issue 1: V9a closes with a forward-pointer to the adjacent V9b
**ASN-0069, §"Provenance Recording", V9a**: "What the I-address *does* fix — that `origin(a) ≠ d_new` for any forked-in address — is recorded separately in V9b."

**Problem**: V9b immediately follows V9a. This closing sentence teases V9b's content (`origin(a) ≠ d_new`) and then defers to it ("recorded separately in V9b"). A reader following V9a must skip past a forward-pointer to a claim that is one line down. This is exactly the cross-reference accretion the anti-bloat pass flags — a paragraph deferring to a downstream location that is adjacent.

**Required**: Delete the trailing sentence. V9b states the fact with its own derivation; V9a does not need to pre-announce it.

### Issue 2: V6a contains a scope-deferral sentence that does not advance the claim
**ASN-0069, §"Subspace Selectivity", V6a**: "A general theory of which links *project* to which V-positions — the formal endset-coverage query apparatus — belongs to a future link-operations ASN; here we need only that the link store and the shared I-addresses survive the fork."

**Problem**: This sentence punts a topic to a future ASN and restates what V6a already proved ("the link store and the shared I-addresses survive the fork"). It sits inside the derivation slot of V6a but advances no step of the argument — it is essay content marking a scope boundary. The link-projection topic is already covered by the Open Questions section and the ASN's Scope block.

**Required**: Remove the sentence. V6a's derivation (frame-condition composition giving `Σ'.L = Σ.L`, then the V4 consequence) is complete without it.

### Issue 3: V4's "holds unconditionally / no precondition needed" is exhaustiveness padding
**ASN-0069, §"The Arrangement Layer", V4**: "V4 holds unconditionally: the formal universal is vacuously true when `V_{s_C}(d_op) = ∅` ... and substantively true when `V_{s_C}(d_op) ≠ ∅` ... No precondition on `V_{s_C}(d_op)` is needed."

**Problem**: A universally quantified statement over `V_{s_C}(d_op)` is automatically vacuous on the empty set; spelling out "vacuously true / substantively true / no precondition needed" is a defensive exhaustiveness claim rather than reasoning. The V0 dispatch on emptiness already makes clear which composite fires in each branch.

**Required**: Trim to the bare statement of V4. If the tie to V7's empty branch is worth keeping, a single clause ("vacuous on the empty-source branch of V0") suffices in place of the three-sentence elaboration.

## OUT_OF_SCOPE

### Topic 1: Transitivity of the prefix relation ≼
**ASN-0069, §"Composability", V11a** re-proves that `≼` is transitive by unfolding the Prefix definition and NAT-order. The foundation (ASN-0034 Prefix) states only the derived postcondition `p ≺ q ⟹ #p < #q`, not transitivity of `≼`.

**Why out of scope**: Transitivity of `≼` is a general foundation property, not specific to forking. Re-proving it here is correct given the foundation gap, but the durable fix is to add `≼` transitivity to ASN-0034's Prefix contract; this ASN should then cite it. Not an error in ASN-0069.

VERDICT: REVISE
