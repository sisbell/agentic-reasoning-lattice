# Review of ASN-0103

## REVISE

### Issue 1: O5 invoked as authority over a registry-free state model

**ASN-0103, "The Operation's Input" / "Ownership and Immediate Referability" / CND.pre, CND.own**: "the authority to allocate `d` beneath `A` is then O5 (SubdivisionAuthority; ASN-0042)" and "the allocation is performed under that prefix (O5...)."

**Problem**: O5's statement quantifies over `Σ.B`, `Π_Σ`, and `allocated_by_{Σ'}(π, a)` — it is a constraint on the *baptismal registry* and *principal set*. The state model this operation is specified over is ASN-0047's `(C, L, E, M, R)`, which carries no `B` and no `Π` component, and `K.δ` "never touches `B`." This is exactly the reasoning the ASN itself uses, correctly, to *decline* the `ω_{Σ'}(d) = ω_Σ(A)` conclusion in CND.own: "ω is defined over ASN-0042's registry `B`, absent from this state model... no foundation result couples `E` to `B`." The same objection applies to O5: it cannot be evaluated over a registry-free transition, so it cannot supply allocation authority here. Invoking it is inconsistent with the ASN's own deferral discipline. (Note O1's `owns(π, a) ≡ pfx(π) ≼ a` is a pure prefix predicate and is fine; the problem is specifically O5, a registry transition axiom.)

**Required**: Either treat the ownership precondition (`pfx(π) ≼ A`, plus authority to allocate) as a stated modeling assumption layered on this state — parallel to CND.A-act — or defer the authority justification to the registry-carrying ASN exactly as the `ω`-valued claim is deferred. Do not cite O5 as a discharged authority over `(C, L, E, M, R)`.

### Issue 2: Freshness `d ∉ E` not closed for node and account entities

**ASN-0103, "Effect One — Freshness"**: heading "Freshness. The address is new: `d ∉ E`," followed by a case analysis covering the document chain (S0), version chains under `A` (B7), off-chain documents (divergence at `#A+1`), and cross-account documents (B7).

**Problem**: The enumerated cases establish distinctness from document-level and version entities only. They never rule out collision with node entities (`zeros = 0`) or account entities (`zeros = 1`) present in `E`. Since `d ∉ E` is the freshness precondition `K.δ` requires, the argument as written does not fully discharge it. The clean uniform closure is already in hand and unused: the ASN proves `D_A = E ∩ S(A, 2)` and `d ∈ S(A, 2)` with `d > max(D_A)`, so `d ∈ S(A, 2) \ D_A = S(A, 2) \ E`, giving `d ∉ E` against *every* entity type at once.

**Required**: Replace (or supplement) the multi-case freshness argument with the one-line closure `d ∈ S(A, 2) ∧ d ∉ D_A = E ∩ S(A, 2) ⟹ d ∉ E`, or explicitly note that `zeros(d) = 2` excludes all nodes (`zeros = 0`) and accounts (`zeros = 1`). Keep the S0/B7 material as the (separate) permanent-distinctness argument against future allocations.

## OUT_OF_SCOPE

### Topic 1: Effective-owner (`ω`) characterization and E↔B coupling

**Why out of scope**: The ASN correctly identifies that `ω_{Σ'}(d) = ω_Σ(A)` requires a registry-carrying state and an `{e ∈ E : ...} = Σ.B ∩ S(A, 2)` coupling invariant that no current foundation supplies, and defers it (last Open Question). This is properly deferred, not an error here — provided Issue 1 above applies the same discipline to O5.

META: not applicable — the ASN defines an operation, its post-state, atomicity, and invariant preservation abstractly over system state; it has not drifted into implementation mechanics.

VERDICT: REVISE
