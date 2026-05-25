# Review of ASN-0069

## REVISE

### Issue 1: V1's parent-equality induction for the subsequent-fork case is too compressed

**ASN-0069, V1**: "parent(d_new) = parent(d_src) (by KDeltaParentK01 at the first fork; by KDeltaParentK01 applied at each step of A_v(d_src)'s emission chain combined with induction on the chain for subsequent forks)."

**Problem**: KDeltaParentK01 at k=0 gives `parent(d_new) = parent(d_prev)`, not `parent(d_src)`. The bridge requires induction on `A_v(d_src)`'s emission chain: base case (first emission via `inc(d_src, 1)` has `parent = parent(d_src)` by KDeltaParentK01 at k=1), inductive step (each subsequent emission via `inc(d_prev, 0)` inherits `parent` from prior emission, which by IH equals `parent(d_src)`). V1's parenthetical reference to induction is a hand-wave for a load-bearing property. Compare with V2's structural-ancestry induction in the same section, which is fully spelled out with base case, inductive step, and component-by-component verification.

**Required**: Spell out the parent-equality induction explicitly, matching the standard set by V2.

### Issue 2: V0 does not explicitly preclude interleaving within the fork composite

**ASN-0069, V0**: "A *fork* of d_src is a composite state transition Σ →* Σ'" and "the composite is K.δ + K.μ⁺ + K.ρ × n, where n = |ran(M'(d_new))|".

**Problem**: ValidComposite★ defines a composite as a sequence of elementary transitions. V0's phrasing names the constituent steps but does not explicitly preclude other transitions interleaving between them. If a K.μ⁻ on `d_src` fires between K.δ and K.μ⁺, V4 (arrangement inheritance) and V5 (source isolation) would no longer compose cleanly — K.μ⁺ would read a modified `M(d_src)`, and V5's claim of unchanged `M(d_src)` across the composite would fail. V11 explicitly handles the analogous concern at the inter-composite level ("no transition between consecutive fork composites modifies any source's arrangement"), but V0 is silent at the intra-composite level. The verification section's "By V5 applied to the first fork, M¹(d_src) = M(d_src)..." implicitly assumes no interleaving but does not derive this from V0's stated form.

**Required**: V0 should state explicitly that the fork composite is the *uninterrupted* sequence K.δ + K.μ⁺ + K.ρ × n (or K.δ alone in the empty case), with no other transitions firing between the elementary steps.

### Issue 3: V8b's restoration discussion buries the load-bearing claim

**ASN-0069, V8b**: V8b's body consists of an extended paragraph describing K.μ⁻/K.μ⁺ restoration mechanics — contiguity constraints from D-CTG★/D-MIN★, operator choice of restoration I-addresses, P0's role in keeping originals available, an explicit numerical example with positions 4/5/6/7, and methodological asides about admissible K.μ⁺ disciplines.

**Problem**: V8b's load-bearing facts are (i) `Π_g ⊆ F` at every reachable state and (ii) `Π_{Σ'} = F` at the post-fork state. The restoration mechanics paragraph clarifies why `Π_g` is not monotonic, but spans roughly thirty lines and restates K.μ⁻/K.μ⁺ semantics already defined in ASN-0047. The operational details (which V-positions must be filled in what order, what choices the operator has for restoration I-addresses, when the original is recoverable) are properties of the K.μ⁻/K.μ⁺ transitions, not of the fork operation. The reader has to extract V8b's operative claim from operational narrative that belongs to ASN-0047.

**Required**: Tighten V8b's body to the core claim, the brief derivation, and a one-line non-monotonicity remark with forward reference to K.μ⁻/K.μ⁺ semantics in ASN-0047. Remove the explicit restoration example and the methodological asides.

## OUT_OF_SCOPE

(None — the Open Questions section already enumerates appropriate out-of-scope topics for future ASNs, including concurrent fork during source modification, snapshot-vs-living-fork semantics, transcludent source documents, and fork-then-source-deletion behavior.)

VERDICT: REVISE
