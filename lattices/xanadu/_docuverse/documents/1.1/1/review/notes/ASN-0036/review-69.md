I'll review the six integrated properties: `ord(v)`, `vpos(S, o)`, `w_ord`, `OrdAddHom`, `OrdAddS8a`, and `OrdShiftHom`.

Let me read the ASN carefully.

<tool_call>
{"name": "Read",
"arguments": {"file_path": "/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0036/formal-statements.md"}}
</tool_call>

# Integration Review of ASN-0036

I verified each integrated property against its proof, preconditions, postconditions, dependencies, and registry entry.

**ord(v)**: Definition strips first component; postcondition `ord(v) ∈ S` when `v` satisfies S8a follows from `zeros(v) = 0` forcing all components positive. Precondition `#v ≥ 2` prevents zero-length result. Clean.

**vpos(S, o)**: Reconstruction prepends `S`; both inverse properties are immediate sequence identities. S8a postcondition correctly conditioned on `S ≥ 1` and positive `oᵢ`. Clean.

**w_ord**: Projection strips first component of displacement; `actionPoint(w_ord) = actionPoint(w) - 1` follows from `w₁ = 0` shifting the first-nonzero index down by one. Clean.

**OrdAddHom**: Component-by-component verification is complete. Both sides expand to `[v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`. The well-definedness check (`actionPoint(w_ord) = k-1 ≤ m-1 = #ord(v)`) is correct. Postcondition (b) — subspace preservation — follows from `k ≥ 2` making TumblerAdd copy `r₁ = v₁`. Postcondition (c) — full decomposition — correctly applies vpos's inverse property to `r = v ⊕ w` with `#r = m ≥ 2`. Both instances verify. Clean.

**OrdAddS8a**: The three regions of TumblerAdd are analyzed correctly: components 1 through `k` are unconditionally positive (from S8a on `v` and the action-point component of `w`); only tail components `w_{k+1}, ..., w_m` can fail. The equivalence with `ord(v ⊕ w) ∈ S` is correctly derived — both reduce to the same condition on tail components. Instance (b) correctly demonstrates the boundary case. Clean.

**OrdShiftHom**: OrdAddHom preconditions verified for `w = δ(n, m)`: `δ(n,m)₁ = 0`, `#δ(n,m) = m`, `actionPoint = m ≤ m`, `δ(n,m) > 0` since `n ≥ 1`. The projection `(δ(n,m))_{ord} = δ(n, m-1)` is correct. S8a preservation: `actionPoint(δ(n,m)) = m` makes the OrdAddS8a tail condition vacuous (empty range). Clean.

**Placement**: New section sits between S8 (span decomposition) and D-CTG (arrangement contiguity) — after all dependencies, before material that could use these tools. No pre-existing property references the new ones. No dangling or broken references.

**Registry**: All six entries have correct labels, statements, and dependency lists. Status values (`introduced` for definitions, `lemma from` for OrdAddHom/OrdAddS8a, `corollary from` for OrdShiftHom) are consistent with the registry's existing conventions.

## REVISE

(none)

VERDICT: CONVERGED
