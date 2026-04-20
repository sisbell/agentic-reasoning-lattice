# Review of ASN-0043

I examined every formal claim, proof, and verification in this ASN. The link ontology is rigorously constructed.

**L0–L1a**: Subspace partition, element-level, scoped allocation — correctly introduced as new invariants. The content-address conjunct of L0 (`fields(a).E₁ = s_C` for `a ∈ dom(Σ.C)`) is a new constraint beyond ASN-0036, appropriately labeled as introduced. Disjointness follows from T7. Sound.

**GlobalUniqueness**: The argument that T9, T10, T10a are store-agnostic (none reference `Σ.C` or `Σ.L`) is correct — these are properties of the tumbler allocation mechanism itself. The extension of S4 to all allocated addresses is valid.

**L9 (TypeGhostPermission)**: The witness construction is thorough. Key step — choosing `s_X ∉ {s_C, s_L}` — gives unconditional exclusion via subspace separation. All fourteen invariants plus S0–S3 verified explicitly for the extended state. No gaps.

**PrefixSpanCoverage**: Both directions proved by exhaustive case analysis over depth (same, greater, shorter). I verified the critical cases: same-depth exclusion at `j = #x` correctly handles the half-open interval (shift(x,1) itself is excluded); greater-depth exclusion when `t_{#x} = shift(x,1)_{#x}` correctly applies T1(ii) to show `shift(x,1) < t`; shorter-depth exclusion correctly catches both prefix and divergence sub-cases. Sound.

**L11b (NonInjectivity)**: Universal-existential with explicit witness. The compressed invariant verification covers all properties — each with a specific justification, not just checkmarks. Sound.

**L12 (LinkImmutability)**: Correctly parallels S0. Evidence from FEBE protocol (no mutation operations) and implementation (write paths restricted to creation) supports the design commitment.

**L14 and non-transclusion**: The derivation from S3 + L0 is logically valid under the current model. The parenthetical about link V-positions in Gregory's implementation is honest and appropriately deferred — the model extension belongs in a future ASN.

**Worked example**: All properties verified explicitly. The two-step extension verifies L11b, L12, L12a, and L13 non-vacuously across named state transitions (Σ → Σ₁ → Σ₂). The ghost type at `g = 1.0.2.0.1.0.1.1` (content-subspace, unallocated) correctly demonstrates L9 by direct exclusion from the finite domain. The L10 verification with parent type `p = 1.0.2.0.1.0.1` correctly shows span containment via PrefixSpanCoverage.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as a foundation-level result
This lemma is a general property of tumbler span arithmetic — it characterizes the coverage of unit-depth spans over arbitrary tumblers. Future ASNs on content mapping, search, and arrangement operations will need this result. Promoting it to a span-algebra foundation ASN would provide stable reference without re-derivation. It is correctly proved and needed here for L10; the concern is organizational only.

**Why out of scope**: placement, not correctness in this ASN.

### Topic 2: Non-transclusion when the arrangement model extends to link V-positions
The derivation from S3 + L0 is valid under the current model. When a future ASN extends S3 to accommodate link V-positions (which the implementation evidence clearly supports), non-transclusion will need to be independently maintained — either as an invariant on the extended arrangement or restated as an axiom.

**Why out of scope**: the derivation is correct under the current model; the model extension is future work.

### Topic 3: Structural attribution label for links
The link analog of S7 — that `home(a)` uniquely identifies the creating document — is fully derived in the body (from L1a, L1, GlobalUniqueness, T4) but not given its own labeled property. S7 in ASN-0036 has a label; the link analog deserves one for stable cross-ASN reference. However, all constituent pieces are individually labeled and the derivation is explicit.

**Why out of scope**: a labeling convenience for future ASNs, not a gap in this one.

VERDICT: CONVERGED
