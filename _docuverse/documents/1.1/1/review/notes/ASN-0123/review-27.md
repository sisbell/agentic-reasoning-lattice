# Review of ASN-0123

I reviewed this as a derivation-from-guarantees specification of CREATENEWVERSION over the ASN-0047 extended state. I verified the load-bearing proofs from scratch rather than trusting the prose, with particular attention to the novel local lemmas (SA, VN-B1, nextv) and the severance theorem, since those carry the weight.

## REVISE

None. The proofs I checked are sound, the boundary cases are covered, and the depth requirements are met. Detail on what I verified follows, so this is not a rubber stamp.

**Re-verified from scratch (the three most load-bearing claims):**

- **SA (StoredAddressAntichain).** Reconstructed independently: a stored `a = [d₀,0,s,k]` and `b = [d',0,s',k']` with `a ≺ b` force `#d' ≥ #d₀+1`, so `d'` contains `d₀`'s two zeros *plus* `a`'s separator at `#d₀+1`, giving `zeros(d') ≥ 3` against `zeros(d') = 2`. The antichain holds, and its use in G2/V10 to collapse subtree coverage to `{a}` is legitimate (the necessity-of-range-preservation argument in G2 turns precisely on this).

- **VN-B1.** The induction over K.δ is exhaustive on the four arrival routes into `S(d,1)` — Node and `k=2` excluded structurally (zeros / penultimate-separator), `k=1` pinned to `c₁` with `m=0` forced by freshness, `k=0` pinned to `j = m+1` via T4-validity of the operand and the IH. Contiguity is genuinely established without B2, and the deliberate refusal to cite B2 (whose stated precondition is *global* B1, silent on the `(account,2)`/`(node,2)` namespaces) is correct and well-flagged.

- **Severance (V9a).** The chain `d_src ≼ v ⟹ pfx(π_o) ≼ v ⟹ #pfx(π_o) ≤ #pfx(π)` (O5(ii)) `⟹ pfx(π_o) ≺ pfx(π)`, then the case split on `pfx(π) ↔ d_src` (Z-mono contradiction vs. O2 maximality contradiction) closes both branches. Crucially, the structural derivation of O5(ii) from the depth-2 stream form `[pfx(π),0,k]` is **non-circular** — the form comes from ASN-0040's SiblingStream postcondition, not from O5 — so the theorem does not smuggle in what it proves.

**Boundary cases checked and handled:** empty source (`n=0`, composite degenerates to the lone K.δ, all couplings vacuous, V9w vacuously true); first version (`m=0`, `nextv = c₁`); cross-owner; node-tier non-owner correctly excluded from the domain (P-tier satisfies neither disjunct); node-tier *owner* admitted to the owned branch with V8's proof tier-agnostic. Both worked instances (carry-through and cross-owner) are arithmetically correct — I recomputed the zero-counts, the `a₁ ⋠ a₂` step, the `project = {[1,1],[1,3]}` landing, and the `|R'∖R| = |A| = 2 < n = 3` provenance count.

**Things I scrutinized as potential gaps but found justified (recording so they are not re-raised):**

1. *Cross-owner identity underspecification.* `v` is left as "the document identity π allocates" rather than a closed form like `nextv`. This is forced, not sloppy: pinning `v = next(E, pfx(π), 2)` would require document-namespace contiguity, which is ASN-0103 territory (out of scope). The ASN instead proves every guarantee parametrically over the form `[pfx(π),0,k]`, and no claim depends on the specific `k`. Sound scope discipline.

2. *V0 distinctness phrasing* is owned-centric ("the version sub-allocator A_v is T10a-conforming"), but the general GlobalUniqueness statement it also invokes covers the cross-owner `v ∈ A_doc(pfx(π))` (equally a T10a node). Conclusion holds for both branches.

3. *PS as a cross-foundation bridge.* The ASN is explicit that reading ASN-0042's `ω` over ASN-0047 states is a hybrid the foundations do not assemble, derives registry coverage from PS(i)–(iii) (the `e₁ = 1` induction is correct: `k>0` appends, `k=0` touches only `sig(t)=#t ≥ 3` for non-node operands), and flags that the implementation does not enforce PS (deviation 4). This is the right way to handle a load-bearing conformance assumption — stated, not buried.

**Depth requirements met:** derived consequences are pursued (severance → V7 downward-navigation limit → V9w witness; identity/content non-injectivity at *totality* in V12); proofs are explicit (no "by similarly," no checkmark-as-proof for multi-case claims); two concrete worked instances verify the key postconditions against implementation-grounded addresses; and precondition *necessity* is analyzed non-trivially — P-bdy is shown load-bearing for V9w by constructing the failing interior state where `a ∈ A` but `(a,d_src) ∉ R`, which is wp-flavored analysis on a non-trivial postcondition.

## OUT_OF_SCOPE

The ASN correctly excludes document-creation-from-nothing, version comparison, the editing operations, link creation, content delivery, and replication, and defines no claims for them. Its eight Open Questions (concurrency serialization, derivation-direction recoverability under symmetric provenance, link-subspace carry, location-fixed windowing, withdrawal/permanence coexistence, provenance-vs-derivation semantics, correspondence under divergence) are genuinely future-ASN territory, not gaps in this one — in particular the honest admission that a cross-owner fork's derivation direction is unrecoverable from state (and, in the empty-source degenerate case, unrecoverable entirely) is correctly left as Open Question 2 rather than papered over.

VERDICT: CONVERGED
