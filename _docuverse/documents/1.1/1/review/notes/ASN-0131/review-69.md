# Review of ASN-0131

I read this as a query-operation specification: it defines `RE(W, d, Σ)` (a pure read), establishes its correctness contract (RE-SND/RE-CMP), its algebra (RE-UDIST, RE-UDIST-∩), and its stability under the full transition vocabulary (RE-EDIT, RE-RET, RE-CWP). I checked the proofs, the boundaries, and the worked instance against the foundation claims.

What I verified holds up:

- **Worked instance.** Reachable and internally consistent. The four-position arrangement is a single lockstep correspondence run (S8); the straddling span `(a₂, δ(2,#a₂))` has reach `shift(a₂,2) = a₄` so `{a₂, a₃} ⊆ coverage` with `a₄` excluded; the `e₃` content-disjointness argument (field-agreement forcing `E(c)₁ = s_type ≠ s_C` from `θ ≼ c` under `zeros = 3`) is sound, as is the parallel link-address argument reused in RE-RET. RE-OVL, RE-CLIP, RE-WHOLE, per-endset, and RE-UNIT each read off the result.
- **RE-ADDR.** The antichain argument is correct: unit-depth `L_R` to-sets cover `{u : t ≼ u}`, R0a makes `dom(Σ'.L)` an antichain, so only a self-targeting retraction can cover a fresh `ℓ_new`. "At every arity" is justified by higher-arity retraction-typed links never entering `L_R`.
- **RE-UDIST-∩.** Both counterexamples are valid and reachable (the non-injective `[1,1],[1,2] ↦ a` via S5/M13/M14; the injective two-span endset via split witnesses in `touch_W`), and they correctly establish that *no* arrangement restriction recovers `⊇`. The necessary-and-sufficient touch-implication is exactly the negation of the failure, and the `⊆` half is genuinely unconditional.
- **RE-CWP / RE-RET.** The contraction wp factors correctly (`Avail` region-independent under K.μ⁻'s `Σ.L` frame; image shrinks; "nothing dropped" reduces as claimed; `R = ∅` collapses to `RE = ∅`). The retraction biconditional is sound in both directions — forward via R6a + the flagged Θ-hypothesis, backward via R-Scope confining the fresh nullification to `ℓ` alone.
- **Stability coverage.** Every transition kind is accounted for (K.μ⁺/⁻/~, K.α, K.δ via LP8, K.ρ via LP14, other-document edits via LP5, link-subspace-confined edits via `W ⊆ s_C`, K.λ emission, retraction). The orphaning-vs-region-local-loss distinction (RE-CWP region-local ≠ LP17 global) is correctly drawn.
- **Cross-references.** All to foundation ASNs (0034/0036/0043/0047/0082/0086/0093/0098/0127). The `Σ.L`-evolution bridge (separating `→*`-reachability for R0a/R-Scope from layer-reachability for unit-depth) is dense but load-bearing — without it the ASN-0086 lemmas don't transfer into ASN-0047's transition system. The image and existence/discovery machinery is cited (RE-SEL, the taxonomy paragraph), not rebuilt.

I looked specifically for forward-reference accretion given the anti-bloat classifier. The standing-assumption + bridge paragraphs are front-loaded but serve two later consumers (RE-ADDR and RE-RET), so single early placement is the DRY choice, not duplication. The Θ-absent-the-hypothesis prose scopes a hypothesis rather than imagining an excluded case. The containment-rejection prose is concrete analogy (explicitly not meta-prose). I found no clearly-skippable passage that obscures a claim, and no two paragraphs restating the same fact.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Full-state lift of ASN-0082's shift-based insert/delete
The insert/delete stability in RE-EDIT rests on the "conservative lift" — the assumption that ASN-0082's displacement primitives frame `Σ.L`, `Σ.E`, `Σ.R`. ASN-0082 models only `(C, M)`, so this is sound (insert/delete genuinely never touch links) but not foundation-verified.
**Why out of scope**: The formal lift belongs in a bridging ASN that re-models ASN-0082's primitives over the full `(C, L, E, M, R)` state. The note treats it correctly — as an explicitly flagged modelling assumption, surfaced in both prose and the RE-EDIT claim row — rather than a hidden dependency. Middle-insert/delete are genuinely not reducible to ASN-0047's atomic K.μ movers (K.μ⁻ truncates the tail, not the interior), so excluding them would gut the stability story; the flagged assumption is the least-bad treatment of a real foundation gap. No error in this ASN.

VERDICT: CONVERGED
