# Review of ASN-0071

I read the operation definition, the PC / PC-RANGE derivations, the subset and finiteness arguments, and traced every worked scenario (single-address, multi-address, multi-source dedup, cross-depth capture, deep-anchor F-DEEP, empty query).

The proofs hold up under scrutiny:

- **PC** is derived honestly — the componentwise fact handles the per-position case split via T0/T1, and the totality clause closes the universal via well-ordering rather than asserting "by similar reasoning." Both the `t < u` and `t > u⊕ℓ` branches are shown, using prefix-copy below the action point.
- **PC-RANGE** splits `#v = #u`, `#v > #u`, and `#v < #u` separately, and correctly distinguishes the *inclusive* lower boundary (`v_{#u} = u_{#u} ⟹ v = u`, included by equality) from the *exclusive* reach boundary (`v_{#u} = r_{#u}` excluded because `r ∉ ⟦σ⟧`, not by an order relation). The depth guard `#v ≥ #u` is explicitly flagged as what makes the conjuncts well-typed.
- **Edge cases are exercised against concrete state**, not hand-waved: empty query (F-EMPTY), deep anchor finer than source depth (F-DEEP, with both `V_{s_C}=∅` and `#u > m_C` sub-cases), cross-depth coarse-anchor capture of a full depth-3 subtree, shared content at non-adjacent positions, and cross-source deduplication folding a doubly-resolved `a₁`. The exclusion direction is checked against a concrete non-containing document (`d_C`).
- **F-CONTENT** correctly bottoms out in `iaddrs ⊆ dom(C)`; link addresses in `ran(M(d))` cannot produce false matches (disjoint stores).
- The **vspec generalizes ASN-0058's ContentReference** rather than reinventing it — dropping the well-formedness/`#u = m_C` tie deliberately (cross-depth capture, F-FILT silent filtering), which the ASN grounds in Nelson's coarse-coordinate reach. This justifies not reusing the foundation definition directly.

Anti-bloat scan: forward pointers are single and local; the M13/M14 framing recurs in the intro and step 13, but the second instance is a concrete example application, which is permitted. Reachability justifications earn their place (they validate the example states). No defensive exhaustiveness prose, no axiom-rationale accretion, no document-ordering justifications.

No REVISE items.

VERDICT: CONVERGED
