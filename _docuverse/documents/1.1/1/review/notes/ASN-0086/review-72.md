# Review of ASN-0086

This is a substantial ASN doing real specification work: it layers a relational vocabulary on top of ASN-0043's links and ASN-0093's allocation contracts, defines the active/audit distinction, and proves a reduction theorem for state-affecting operations. The bulk of the proofs are thorough — R0's invariant-by-invariant L-preservation argument, R0a's two-case prefix argument, R6c's induction, the worked sketch tracing concrete tumbler values through four steps. The WP analysis is non-trivial and splits regimes correctly. The Consequences sections are well-typed (COROLLARY / POLICY / ARCHITECTURE).

I found one substantive REVISE issue. It's load-bearing because it threads through R7a, the relational-layer reduction corollary, and the scope of R0a-Cor1/R0a-Cor2.

## REVISE

### Issue 1: R7a's proof relies on ChainMembershipForOrigin, which is not in the substrate-conforming catalog

**ASN-0086, Definition of substrate-conforming layer**: "every operation it publishes over `(Σ.C, Σ.M, Σ.L)` preserves every invariant the underlying substrate ASNs posit at each step. Concretely, this is the full invariant catalog of ASN-0043 — L0 ... L-fin — together with the ASN-0036 invariants ... and the ASN-0093 substrate invariants M0 ... C-fin."

**ASN-0086, R7a proof, discharge (4)(i)**: "By R0a-Cor1 at Σ', for each `d_k` the homed set `{a ∈ dom(Σ'.L) : home(a) = d_k}` is `{incʲ(d_k.0.s_L.1, 0) : 0 ≤ j ≤ J_{d_k}^{Σ'}}` — a contiguous prefix of `A_L(d_k)`'s chain enumeration."

**Problem**: R0a-Cor1 is "a direct re-expression of ASN-0093's ChainMembershipForOrigin lemma." ChainMembershipForOrigin is a derived ASN-0093 lemma from SubAllocatorAxiom + K.λ's contract — neither the lemma nor the axiom appears in the substrate-conforming catalog. The listed L-invariants are weaker:

- L1c admits *any* T10a-conforming chain `(t₀, …, tₙ)` with `k₁ = 2` and `k_i ∈ {0, 1, 2}` for `i ≥ 2`. In particular, taking `d = 1.0.1.0.1`, the chain `d → 1.0.1.0.1.0.1 → 1.0.1.0.1.0.2 → 1.0.1.0.1.0.2.1 → 1.0.1.0.1.0.2.1.1` is L1c-admissible (each step T4-preserving, zero-count = 3 throughout).
- The terminal address `a* = 1.0.1.0.1.0.2.1.1` satisfies L0 (`E(a*)₁ = 2 = s_L`), L1 (`zeros(a*) = 3`), L1a (`home(a*) = d`), L1b (`#E(a*) = 3 ≥ 2`), and L1c. Every listed L-invariant for a link at `a*` holds.
- But `a*` is *not* on `A_L(d)`'s sibling chain — `A_L(d)` produces only depth-2 element fields (per R0a-Cor2's own conclusion). K.λ's first/subsequent rule cannot deposit at `a*`.

A substrate-conforming layer (per the listed catalog) could in principle extend `Σ.L` with `a*`, producing a `Σ'` at which R0a-Cor1 fails (the homed set at `d` is no longer a contiguous prefix of `A_L(d)`'s chain). R7a's discharge (4) "K.λ's first/subsequent rule, evaluated against the origin-scoped homed-set at `Σ_{prev}'`, produces exactly this chain element" then fails — there is no K.λ-step that produces `a*`.

This means R7a's claim ("the `Σ.L`-affecting effect of the transition decomposes into a finite sequence of class-(iii) →-steps") is technically unproven under the strict catalog. The proof of R7a depends on a strictly stronger condition on substrate-conformance than what the catalog supplies.

The same gap propagates to R0a-Cor2's universal claim ("for every reachable state Σ, `#E(a) = 2` strictly for every `a ∈ dom(Σ.L)`"). If "reachable" includes substrate-conforming ↝-reachability, the claim doesn't hold; if "reachable" means →-reachable only, R7a's claim that ↝ effects reduce to → loses its grounding.

The relational layer's reduction Corollary ("The relational layer's state-affecting operations reduce to `{Emit_K}`") is *not* affected by this gap — the relational layer's operations are *by definition* K.λ-specialized, so the reduction holds by construction. R7a is load-bearing only for the categorical claim about *arbitrary* substrate-conforming layers.

**Required**: Choose one of:

(a) Add ChainMembershipForOrigin (or SubAllocatorAxiom together with the chain-discipline lemmas) explicitly to the substrate-conforming catalog. The proof's reliance becomes legitimate. Note that this strengthens "substrate-conforming" beyond the listed invariants and should be acknowledged.

(b) Reinterpret "substrate-conforming" as "preserves every substrate property, including derived lemmas" and adjust the prose: replace "Concretely, this is the full invariant catalog" with language making explicit that the listed invariants are non-exhaustive and that derived chain properties (ChainMembershipForOrigin) are also preserved.

(c) Weaken R7a's claim to assume layers emit only at A_L-chain link addresses (i.e., to layers respecting ChainMembershipForOrigin by construction), and explicitly note that arbitrary L1c-admissible link emissions are outside R7a's scope. This is honest about the gap but reduces R7a's categorical force.

A short side derivation showing that L1c + a sibling-frontier-discipline-shaped condition entails ChainMembershipForOrigin would also work — but the substrate-conformance definition would still need to carry that side condition explicitly.

## OUT_OF_SCOPE

### Topic 1: Cross-layer composition and coordination on T_admissible

**Why out of scope**: The Open Questions section explicitly raises "Can higher layers introduce new admissible types `K ∈ T_admissible` dynamically without coordination, given L9 (TypeGhostPermission), and what happens when two layers independently choose colliding type addresses?" — appropriately deferred.

### Topic 2: Higher-arity links and active subsets over them

**Why out of scope**: The ASN explicitly restricts to standard-triple links and notes "Higher-arity links (L3, NEndsetStructure, ASN-0043) exist in `dom(Σ.L)` but are not members of any `L_K`; they admit an analogous construction with additional slot positions, which we do not pursue here." Listed in Open Questions.

### Topic 3: Concurrency and atomicity model for Observe vs. Emit

**Why out of scope**: Open Questions raises "Must Emit be atomic with respect to concurrent Observe, and if so, what is the consistency model under which `A_K` transitions are observed?" Sequential atomicity is inherited from ASN-0093's SequentialTransitionAxiom; concurrent semantics is a separate concern.

VERDICT: REVISE
