# Review of ASN-0047

I focused on proof rigor at the operation boundaries and on the forward-reference / reviser-drift accretion the note flags. I did not find a hard logical hole in the K.* transition proofs — the elementary cases, K.μ⁻ full-clearance/full-deletion, first-insertion, and the worked-example arithmetic all check out — but the K.μ~ machinery and several axiom glosses carry duplicated and circular meta-prose that a precise reader must work around. The findings below are all REVISE-class.

## REVISE

### Issue 1: Link-subspace fixity reasoning restated three times
**ASN-0047, §Decomposition of K.μ~ ("Link-subspace fixity (Steps (C)–(D))") and the immediately-following "Dual consequence" paragraph, plus §Extended reachable-state invariants (CL-UNIQ prose)**: Steps (1)–(4) establish "functional identity (Steps 1–3) then pointwise identity via CL-UNIQ (Step 4)." The very next paragraph re-derives this as: "The functional identity ... discharges *two* downstream obligations ... (a) Pointwise fixity: ... (b) Post-state CL-UNIQ preservation: ...". Then the CL-UNIQ verification-matrix prose re-explains it a third time: "Steps 1–3 of the link-subspace fixity proof ... establish ... *without* invoking CL-UNIQ ... Step 4 then uses CL-UNIQ *at the pre-state* ...".
**Problem**: Three passages assert the same Steps-1–3-vs-Step-4 split in different words. The "Dual consequence" paragraph is a downstream-consumer inventory ("discharges *two* downstream obligations") that advances no new reasoning — the matrix-row obligation it names is exactly what Step (3) already supplies.
**Required**: State the functional identity once (Steps 1–3) and derive both pointwise fixity and post-state CL-UNIQ inline at that point; delete the "Dual consequence" paragraph and replace the CL-UNIQ matrix-prose with a bare pointer to Steps (1)–(4).

### Issue 2: S3★-under-K.μ~ "true by construction" stated circularly and twice
**ASN-0047, §Decomposition of K.μ~ (opening, and again later)**: Opening: "S3★(Σ') for a K.μ~ event holds by the admissibility filter — clause (i) admits only those π whose induced post-state satisfies S3★(Σ'), so the verification-matrix cell is true by construction." Later: "The matrix entry in ExtendedReachableStateInvariants for S3★ under K.μ~ holds by the admissibility filter (true by construction); Step (B) supplies only the realisability that makes K.μ~ non-vacuous."
**Problem**: Stated this way the claim reads as circular — S3★(Σ') is *assumed* by admissibility (i), then "established" by appeal to that same admissibility. The substantive content that actually discharges S3★ is Step (B.3) ("the realised M'(d) satisfies S3★"), but the two "true by construction" framings bury it and are themselves duplicates. A reader cannot tell from either sentence what is assumed versus what is proved.
**Required**: Drop one of the two framings; state plainly that admissibility (i) *stipulates* S3★(Σ') as a filter, and that Step (B.3) discharges it by exhibiting the K.μ⁻ + K.μ⁺ post-state. Do not describe a stipulated filter condition as "true by construction" of the verification it gates.

### Issue 3: CrossDocDisjoint Case A — defensive counterfactual in proof slot
**ASN-0047, Lemma (Cross-document disjointness chain), Case A**: "(Without the common-level constraint, e₂ could carry additional zero separators in its extension — e.g., the chain `[1] → [1.0.1] → [1.0.1.0.1]` extends each entity through an intervening zero. The argument that the extension positions contain no zeros consumes the equality of zero counts, not merely the prefix relation.)"
**Problem**: This is a defensive justification explaining *why* a hypothesis is load-bearing by imagining a case the lemma's same-level precondition (`zeros(e₁) = zeros(e₂) = z`) already excludes. The proof step it guards ("the remaining positions ... contain `z − z = 0` zeros") already consumes the equality of zero counts explicitly; the counterfactual adds no inference.
**Required**: Delete the parenthetical. The "since e₂'s first #e₁ positions reproduce e₁ exactly ... the remaining positions contain 0 zeros" sentence already carries the argument.

### Issue 4: K.μ~ existence condition restated across three sites with nested defers
**ASN-0047, "Preconditions of K.μ~", "Decomposition", and ValidComposite★ clause 1**: The non-constancy condition ("`M(d)|_{dom_C}` takes at least two distinct values") and its "necessary-but-not-sufficient cardinality" gloss appear in all three. ValidComposite★ clause 1 reproduces the full gloss — "the constant-valued case — including `|dom_C(M(d))| ≤ 1` and any state where every content V-position shares one I-address by transclusion (S5) — admits only net-identity permutations; the weaker cardinality bound `|dom_C(M(d))| ≥ 2` is necessary but not sufficient — see *Decomposition of K.μ~*" — and then defers to the very section that defers back to "Preconditions of K.μ~ above."
**Problem**: The same condition with the same caveat is stated three times, and the cross-references form a defer loop (ValidComposite★ → Decomposition → Preconditions). This is "multiple paragraphs say the same thing" compounded with circular forward pointers.
**Required**: State the condition and its sufficiency caveat once (at "Preconditions of K.μ~"); have ValidComposite★ clause 1 and the Decomposition realisation reference it by name without re-glossing.

## OUT_OF_SCOPE

### Topic 1: Permanent pinning of content-subspace V-position depth
After full K.μ⁻ clearance of `V_{s_C}(d)` (`n'_{s_C} = 0`), a later K.μ⁺ first-insertion may choose a *different* depth `m` than the document previously used — content depth is not pinned the way `m_L(d)` is for links.
**Why out of scope**: The LinkVPositionDepthAxiom "Design intent" makes this asymmetry deliberate (content identity is its I-address, not its V-position). No per-state invariant is violated. Whether content depth should be permanently pinned is a future-design question, not an error here.

### Topic 2: Interior link withdrawal
D-CTG★/D-MIN★ confine K.μ⁻ to per-subspace suffix truncation, so withdrawing an interior link requires withdrawing every later link.
**Why out of scope**: Already catalogued in Open Questions as requiring a separate tombstoning mechanism outside K.μ⁻'s contract.

VERDICT: REVISE
