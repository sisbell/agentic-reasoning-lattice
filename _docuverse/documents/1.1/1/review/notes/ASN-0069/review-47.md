# Review of ASN-0069

## REVISE

### Issue 1: V10(b) miscites V5a Corollary 2's instantiation

**ASN-0069, "Independence Among Forks" (V10(b))**: "V5a Corollary 2 — pairwise independence, instantiated at the pair (d¹, d²) = (d_new¹, d_new²) — gives that modifications M-targeted at d_new¹ preserve M(d_new²) and symmetrically."

**Problem**: V5a Corollary 2 reads "no step is M-targeted at d¹: M''(d¹) = M'(d¹)" — under this convention, d¹ is the *preserved* document. The instantiation (d¹, d²) = (d_new¹, d_new²) therefore yields "no step M-targeted at d_new¹ preserves M(d_new¹)" — not V10(b)'s claim "mods at d_new¹ preserve M(d_new²)". To derive the latter, the corollary must be instantiated with d¹ = d_new² (the preserved).

V11's first premise-scope remark uses the convention d¹ = preserved consistently: "instantiating at (d¹, d²) = (d^{i-1}_new, d_target) ... the corollary guarantees M(d^{i-1}_new) is preserved". V10(b) silently inverts this convention without flagging the swap. The "and symmetrically" addendum requires two applications with both orderings (d¹ = d_new² for the M(d_new²)-preservation direction, d¹ = d_new¹ for the symmetric direction), but only one mapping is named, leaving the reader to reconstruct which direction the corollary actually delivers.

**Required**: Either (a) restate V10(b) with the correct instantiation — d¹ = d_new² for the M(d_new²)-preservation claim, and d¹ = d_new¹ for the symmetric direction — naming both applications explicitly; or (b) re-state Corollary 2 so that d² is the preserved (matching V10(b)'s labeling), and propagate the change to V11's remark for consistency.

### Issue 2: V8a redundant with V8b's per-transition enumeration

**ASN-0069, "Structural Correspondence" (V8a)**: V8a is restricted to K.α and claims correspondence persistence over fork-time V-positions; V8b's per-transition enumeration explicitly covers K.α (alongside K.λ, K.ρ, K.δ, K.μ⁺_L, and third-document arrangement transitions) as preserving Π_g via the same frame condition `(A d :: M'(d) = M(d))`.

**Problem**: V8a's substance ("V8's correspondence ... is preserved across every K.α step unconditionally") is a special case of V8b's K.α clause ("K.α and K.λ each frame (A d :: M'(d) = M(d)) ... in all three cases Corr_g is invariant"). The text justifies V8a's separate scoping by appeal to "the consumption pattern of its downstream use sites — the post-fork content-allocation argument," but no downstream use site of V8a is identified anywhere in this ASN — V12 cites P0/S0, the worked example cites V5a Corollary 1 for the K.μ⁻ scenario, and every other claim that needs K.α-preservation can consume V8b. Including V8a as a distinct entry in the Properties Introduced table creates redundancy without distinct semantic content.

**Required**: Either (a) identify and cite the post-fork content-allocation argument that consumes V8a specifically, and explain why V8b's K.α clause is insufficient for that consumption; or (b) fold V8a into V8b's enumeration and remove the separate V8a entry from the Properties Introduced table.

VERDICT: REVISE
