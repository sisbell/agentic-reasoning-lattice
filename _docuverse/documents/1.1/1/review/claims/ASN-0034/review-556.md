# Cone Review — ASN-0034/T4a (cycle 1)

*2026-04-25 18:44*

### T4c missing left-identity citation for the `n = 0` instantiation
**Class**: OBSERVE
**Foundation**: NAT-closure's left additive identity `(A k ∈ ℕ :: 0 + k = k)`; NAT-addcompat's strict successor inequality `n < n + 1`.
**ASN**: T4c's Injectivity prose: "NAT-addcompat's strict successor inequality `n < n + 1`, instantiated at `n ∈ {0, 1, 2}` … gives `0 < 1`, `1 < 2`, and `2 < 3`."
**Issue**: At `n = 1` and `n = 2`, the rewrites `1 + 1 = 2` and `2 + 1 = 3` are the numeral definitions and need no further axiom; at `n = 0`, the inequality delivered is `0 < 0 + 1`, and rewriting it to `0 < 1` requires NAT-closure's left additive identity `0 + 1 = 1`. The Depends entry for NAT-closure mentions "posits `1 ∈ ℕ` and closes ℕ under addition" but does not name the left-identity used at this step. T4's Exhaustion derivation cites the same left-identity step explicitly ("NAT-closure's left additive identity … at `n := 1` reduces to `1 ≤ zeros(t)`"); T4c is uneven by comparison.

### T4 Axiom slot mixes per-`k` schema with the positional constraint
**Class**: OBSERVE
**Foundation**: —
**ASN**: T4 Formal Contract, Axiom: "Valid address tumblers satisfy: `zeros(t) ≤ 3`; … `t_{#t} ≠ 0`. … The canonical written form of a T4-valid address tumbler is given by the following schema, quantified per-`k`: `k = 0`: `t = N₁. ... .Nₐ`; …"
**Issue**: The per-`k` schema is structural decomposition that follows from the four positional clauses and the Exhaustion Consequence, not independent axiomatic content. Stating it inside the Axiom slot conflates "what is posited" with "what is entailed, and used to introduce field labels `Nᵢ, Uⱼ, Dₖ, Eₗ`". A downstream consumer cannot tell whether the schema is a redundant axiom clause, a definitional convention naming positions, or a proven consequence. This invites the reader to re-derive the per-`k` form rather than reading it off T4a/T4b.

### T4b lacks an explicit Preconditions slot
**Class**: OBSERVE
**Foundation**: —
**ASN**: T4b Formal Contract — has *Definition*, *Depends*, *Postconditions* but no *Preconditions*. T4c, by contrast, lists "*Preconditions:* `t` satisfies the T4 constraints …".
**Issue**: T4-validity is carried implicitly through `dom(N)`, but the slot conventions used elsewhere in the ASN make the absence noticeable. The Postconditions tail does say "consumers must carry T4-validity as a precondition" — that load-bearing phrase belongs in Preconditions, not in Postconditions.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 588s*
