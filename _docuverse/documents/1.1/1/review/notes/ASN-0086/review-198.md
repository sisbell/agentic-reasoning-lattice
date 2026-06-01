# Review of ASN-0086

I evaluated the typed-relation construction, the conformance hierarchy (substrate- / state-local- / →*-reachable), R0–R7a, the wp analysis, and the worked sketch. The correctness backbone is solid: R0a's two-case antichain, L-ContiguousPrefix's induction, R7a's replay decomposition, and the five-step worked sketch all check out arithmetically and logically. The findings below are concentrated where the `anti-bloat` classifier points — meta-commentary and definitional redundancy — plus one genuine consistency gap in `a_emit`.

## REVISE

### Issue 1: `a_emit` is defined as "the address K.λ deposits" but is actually a total formula that yields a value where K.λ has no valid edge
**ASN-0086, Definition — `a_emit` (Allocator Structure)**: "the *fresh emission address* `a_emit(Σ, d)` is the address K.λ deposits at home `d` in state Σ, per its first/subsequent emission rule: `a_emit(Σ, d) = [d.0.s_L.1]` when … ; `a_emit(Σ, d) = inc(ℓ_prev, 0)` otherwise … The outcome is determined by `(Σ, d)` alone, so `a_emit` is a function of `(Σ, d)`."

**Problem**: The two characterizations diverge at exactly the boundary the note relies on elsewhere. `a_emit` is given as a *total* formula over `(Σ, d ∈ dom(Σ.M))`: at a state-local-conforming-but-not-substrate-conforming state (the Remark — NestedLinkWitness construction), `ℓ_prev = max{homed-set}` is the *nested* key and `inc(ℓ_prev, 0)` computes a concrete value. But the prose says `a_emit` *is* "the address K.λ deposits," and at that same state Emit_K's own definition states K.λ deposits nothing ("the subsequent-emission `inc(ℓ_prev, 0)` would be off-chain … no legitimate K.λ-edge exists at `d`"). So "the address K.λ deposits" is undefined precisely where the formula gives a value. The Emit_K function-ness proof and the wp Case 2 derivation both lean on `a_emit` being a clean total function of `(Σ, d)`, yet the gloss ties it to an operation that is partial over the same domain.

**Required**: Pick one reading. Either define `a_emit` purely as the first/subsequent *formula* over `(Σ, d)` (total, with no claim that K.λ commits it), and separately state that Emit_K commits `a_emit(Σ, d)` only when the frontier is well-formed; or restrict `a_emit`'s domain to states where the K.λ edge exists and drop the "function of `(Σ, d)` alone over the operations' domain" totality claim. As written the two descriptions are not co-extensive.

### Issue 2: Meta-commentary on proof structure inside the K-Step Conformance Preservation proof
**ASN-0086, Lemma — K-Step Conformance Preservation, proof**: "… induction lifts this to any conformance-preserving trajectory — this half is definitional. The substantive content is the K-op claim, which we discharge by clause across all three K-ops."

**Problem**: "this half is definitional" and "The substantive content is the K-op claim" are essay-content about which part of the proof matters, not steps of the proof. A reader must skip past the self-narration to reach the actual clause-by-clause discharge. This is the meta-prose-in-a-structural-slot pattern the anti-bloat pass targets.

**Required**: Delete the structural narration; open directly with the clause discharge ("Clause (a) holds for every K-op by its ASN-0093 contract; clauses (b)–(c) split on whether the op touches `dom(Σ.L)` …"). The definitional-closure observation, if kept at all, is one subordinate clause.

### Issue 3: Lemma — Emit_K function-ness largely restates Definition — `a_emit`
**ASN-0086, Lemma — Emit_K function-ness**: "The address component is `a = a_emit(Σ, d)`, a function of `(Σ, d)` by Definition — `a_emit` …; that well-definedness, established there, holds over the operations' domain … The value `Σ'.L(a) = (F, G, K)` is fixed by the caller-supplied arguments, and K.λ's Frame fixes the rest of Σ'."

**Problem**: Once Definition — `a_emit` has established that the deposited address is a function of `(Σ, d)`, "Emit_K is a function" reduces to "address from `a_emit`, value from caller args, rest from frame" — a one-line corollary. Promoting it to a separately-stated Lemma with its own proof restates `a_emit`'s function-ness, and I find no later invocation of "Emit_K function-ness" by name. A labeled lemma that re-derives an already-established fact and is not cited is accretion.

**Required**: Fold the determinism observation into Definition — Emit_K as a one-sentence remark (address by `a_emit`, value by argument, remainder by K.λ frame), or, if it is genuinely consumed downstream, cite the consumer. Drop the standalone proof.

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations
The note restricts to standard-triple links (`|Σ.L(a)| = 3`) and explicitly excludes higher-arity links from any `L_K`. The generalization to `L_K^{(n)} ⊆ A_rel × ℘(A)^n` is correctly deferred (it appears in Open Questions). Not an error here.

### Topic 2: Concurrency / atomicity of Observe vs. Emit, and ordering of Observe results
The consistency model under concurrent `Emit`/`Observe` and any ordering guarantee on Observe output are new territory, appropriately listed as Open Questions rather than resolved.

### Topic 3: Tightening L1b (`#E ≥ 2`) to `#E = 2` at the substrate
L-ContiguousPrefix-Cor1 derives `#E = 2` for substrate-conforming link addresses, but whether ASN-0043/0093 should admit only `#E = 2` is a substrate-layer design question, correctly deferred.

VERDICT: REVISE
