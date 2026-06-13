# Review of ASN-0123

This is an unusually careful note. The operation is *derived* from its guarantees rather than asserted, the foundation-bridging is done with eyes open (VN-B1 re-proves ASN-0040's B1 rather than citing it across transition systems; PS makes the ASN-0042/ASN-0047 hybrid explicit and derives `ω` totality instead of assuming it), and the hard proofs — the severance theorem (V9), the antichain SA, the K.δ case analysis in VN-B1 — hold up under scrutiny. I checked V0–V13, V-WF, the PS coverage induction, and the SA/G2 chain step by step; the reasoning is sound. Two issues, one a genuine internal inconsistency.

## REVISE

### Issue 1: The VD biconditional is false, by the ASN's own severance theorem

**ASN-0123, "VD (VersionNamespaceDiscipline)" and the Claims table**: "Under VD, ancestry is decidable from the identity alone in the owned case: `derives(v, d) ⟺ v ∈ E ∧ v ∈ S(d, 1)`" — and the unqualified table form "under VD, `derives(v, d) ⟺ v ∈ E ∩ S(d, 1)`".

**Problem**: The forward direction (`derives(v, d) ⟹ v ∈ S(d,1)`) is refuted by a construction the ASN itself supplies. `derives` is defined as "`derives(v, d)` holds iff some `VERSION(·, d)` invocation produced `v`" — which includes **cross-owner** invocations. By V9, a cross-owner fork `VERSION(π, d_src)` with `π ≠ ω(d_src)` produces `v` for which `derives(v, d_src)` holds and `v ∈ E`, yet `¬(d_src ≼ v)` is a *theorem* (severance, V9a). Since every stream member extends its parent (S1/StreamPrefix, `S(d_src,1) ⊆ {t : d_src ≼ t}`), `v ∉ S(d_src, 1)`. So `derives(v, d_src) ∧ v ∈ E ∧ ¬(v ∈ S(d_src,1))` — the `⟹` direction fails.

This is not merely a precision slip; it contradicts V7, which correctly states that a cross-owner fork's derivation "falls in neither `S(d, 1)` nor `{e : d ≺ e}`" and is "recoverable only through the shared-content witness, never the registry." The biconditional claims *all* derivation is registry-decodable; V7 and V9 prove it isn't. The "in the owned case" prose is not part of the formula, and the claims-table form carries no qualifier whatsoever.

**Required**: Restrict the biconditional to address-encoded (owned) derivation. Acceptable forms: "for `v ∈ S(d,1)`: `derives(v,d) ⟺ v ∈ E`"; or the one-directional `v ∈ E ∩ S(d,1) ⟹ derives(v,d)` paired with an explicit statement that the converse fails for cross-owner forks (severance); or a distinct `derives_addr(v,d) := derives(v,d) ∧ d ≼ v` that the biconditional decides. The claims-table entry must carry the same restriction.

### Issue 2: The operation's domain restriction is disclosed in prose but absent from the precondition list

**ASN-0123, "The Operation" — Preconditions**: the bulleted preconditions are P-src (`d_src ∈ E_doc`), P-prin (`π ∈ Π`), P-bdy (composite boundary).

**Problem**: VERSION is partial in a way the bullets do not capture. The cross-owner branch "requires `zeros(pfx(π)) = 1`," and a node-tier non-owner — `zeros(pfx(π)) = 0` (which O1a admits into `Π`, as the ASN itself notes) with `ω(d_src) ≠ π` — is explicitly **not served**: "such a principal must establish an account first, an out-of-scope prior act VERSION does not cover." The operation's true domain is therefore `{(π, d_src) : d_src ∈ E_doc, Σ a boundary, (ω(d_src) = π ∨ zeros(pfx(π)) = 1)}`, but P-src ∧ P-prin ∧ P-bdy admit inputs outside it. The precondition-section prose does disclose the restriction (and the identity clause states the guard), so this is a completeness/placement defect rather than a missed case — but the precondition bullets are precisely where a contract delimits applicability, and as written they overstate the domain. The unconditional V0–V13 theorems implicitly assume an applicable invocation, which makes the precise domain load-bearing.

**Required**: Elevate the conditional precondition to the bulleted list (e.g. "P-tier: `ω(d_src) = π ∨ zeros(pfx(π)) = 1`") so the stated domain matches the operation's domain of definition.

## OUT_OF_SCOPE

No coverage gaps belonging to a future ASN were found beyond those the note already enumerates. The Open Questions correctly defer concurrent-fork serialization (interior-state observability is honestly flagged in the atomicity remark, not papered over), the recoverability of cross-owner derivation direction from symmetric provenance (the live consequence of Issue 1's severance), link-subspace carry-through (V2b proves it cannot carry mechanically; whether any guarantee *should* is rightly left open), and withdrawal/supersession under permanence. These deferrals are well-placed.

VERDICT: REVISE
