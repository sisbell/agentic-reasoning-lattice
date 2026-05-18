# Review of ASN-0086

## REVISE

### Issue 1: R0 Step 2 Case B asserts contiguity of prior siblings that the construction does not require

**ASN-0086, R0 proof, Step 2 Case B**: "Sibling-stream uniqueness for the extension is supplied by T10a.7 (each `incⁱ(b, 0)` is a distinct enumeration index) together with L12 (LinkImmutability, ASN-0043), which keeps the prior occupied prefix `b, inc(b, 0), …, incⁱ⁻¹(b, 0)` in `dom(Σ.L)` so the least-`i` selection is well-defined."

**Problem**: R0 is stated outside the disciplined regime; R0a (which guarantees contiguity) is conditional on the sibling-frontier discipline and only appears later. Without that discipline, dom(Σ.L) could contain `b` and `inc²(b, 0)` but not `inc¹(b, 0)`. The "prior occupied prefix" claim is then false: positions `inc¹` through `incⁱ⁻¹(b, 0)` need not all be in dom(Σ.L). The least-`i` construction does not depend on contiguity — it depends only on T10a.7 (infinite sibling stream) and L-fin (finite dom(Σ.L)).

**Required**: Drop the contiguity claim. Replace with: "the sibling stream is infinite by T10a.7; dom(Σ.L) is finite by L-fin; therefore finitely many siblings of `b` lie in dom(Σ.L), and the least index `i ≥ 1` with `incⁱ(b, 0) ∉ dom(Σ.L)` is well-defined."

### Issue 2: R6b is a tautological restatement of the definition, mislabeled as a lemma

**ASN-0086, R6b**: "**R6b — SingleDepthRetraction.** By Definition of `nullified`, the existential ranges over `L_R^Σ` (the audit slice), not `A_R^Σ` (the active subset). Deciding `a ∈ nullified(Σ)` therefore requires only one level of existential check..."

**Problem**: The "proof" is purely an appeal to the existential range in the Definition of `nullified`. No substantive derivation occurs. As a LEMMA labeled adjacent to R6a (a genuine derivation from R3 + R2 + coverage purity) and R6c (induction-based), R6b's status as a lemma is misleading.

**Required**: Either expand R6b to substantively derive a non-tautological consequence (e.g., explicitly contrast with an alternative definition that quantifies over `A_R^Σ` and would yield recursive evaluation), or demote to a "Definition consequence" / "Remark" with appropriate framing.

### Issue 3: R7a's replay sequence does not explicitly discharge L0/L1/L1b/L1c at each replay step

**ASN-0086, R7a proof**: "...the substrate emission primitive's class-(iii) frame admits a `→`-step `Σ_{prev}' → Σ_k` emitting `(F_k, G_k, K_k)` at `a_k`: L1a is now discharged (`home(a_k) = d_k ∈ dom(Σ_{prev}'.M)`), and `a_k ∉ dom(Σ_{prev}'.L)` because the class-(i) prefix held `Σ_{prev}'.L = Σ_{prev}.L`..."

**Problem**: The substrate emission primitive's preconditions are (1) `a_k ∉ dom(Σ.L)`, (2) L0/L1/L1a/L1b at `a_k`, and (3) L1c on Σ. The proof addresses L1a and freshness only. L0 (`a_k.E₁ = s_L`), L1 (`zeros(a_k) = 3`), L1b (`#E(a_k) ≥ 2`), and L1c (T10a-conforming chain) all need to hold at the replay state, not just at Σ'. The argument is that these are structural properties of the address — hence state-independent once they hold at any state — but this should be made explicit, because the substrate primitive's preconditions are evaluated against the input state of each replay step, not against Σ'.

**Required**: Add explicit verification: "L0, L1, L1b are structural properties of `a_k` itself, independent of state; they hold at `a_k` because the original ↝-step's post-state Σ' satisfied them, and address-structural properties are state-invariant. L1c's chain admissibility is similarly structural over tumbler addresses and T10a child-spawn admissibility; it transfers from Σ' to Σ_{prev}' provided class-(i) prefix steps don't remove or modify the chain's intermediate tumblers (which they don't, since they only extend dom(Σ.M))."

### Issue 4: Frame condition (iii) names the class "Emit_K" but Emit_K is later defined as a strict subset

**ASN-0086, Setup, "Frame conditions on the primitive transitions"**: "- (iii) *Link emission (`Emit_K`):* `dom(Σ'.L) = dom(Σ.L) ∪ {a}` for a fresh link address `a ∉ dom(Σ.L)`..."

**Problem**: The "(`Emit_K`)" parenthetical here implies that class (iii) IS Emit_K. But the "**Substrate emission primitive.**" paragraph immediately below establishes class (iii) as the broader "emit-at-any-L1c-conforming-fresh-address" primitive, and "Three Operations" then defines Emit_K as "the sibling-frontier-disciplined subset of this primitive". The same symbol is being used for two different things — broad primitive vs. disciplined subset.

**Required**: Strike the "(`Emit_K`)" parenthetical from the Frame condition (iii) and replace with a descriptive label such as "*Link emission (substrate primitive form):*" or "*Link store extension:*". Reserve the symbol `Emit_K` for the disciplined operation defined in Three Operations.

### Issue 5: The "witness-only reading" of L1c is asserted but not formally grounded

**ASN-0086, R0 proof, Step 2 preamble**: "By the substrate emission primitive's witness-only reading of L1c (Setup), each L1c chain in what follows is a *conformance witness* on `Σ`, not an operational sequence — the chain is required to exist, but no intermediate spawn is re-issued, and intermediate addresses are not required to be in `dom(Σ.L)` or `dom(Σ.C)`."

**Problem**: L1c in ASN-0043 says "There exists a T4-valid document-level seed `s` and a T10a-conforming step sequence terminating at `a`" — it does not explicitly distinguish "operational" from "witness" interpretations. The note repeatedly leans on the "witness-only reading" (in R0, R7a, R0a Stage 2) to argue that L1c chain steps need not have been individually executed. This is treated as a definitional commitment of the substrate primitive but the commitment is asserted multiple times without consolidation.

**Required**: Consolidate the witness-only reading into one explicit commitment in Setup (e.g., as part of the Substrate emission primitive paragraph), with a brief justification that L1c's existential quantifier over chains is sufficient for the substrate to admit emission — no operational re-execution of intermediate spawns is required. Then subsequent uses can cite this consolidated commitment rather than repeating the rationale.

### Issue 6: Arrangement-modification frame's L12a citation misrepresents what L12a establishes

**ASN-0086, Setup, "Broader transition relation `↦`"**: "...holds `Σ'.L = Σ.L` by ASN-0043's L12 (LinkImmutability, value preservation) + L12a (LinkStoreMonotonicity, domain non-extension for non-emitting steps) — neither L-invariant admits modification or removal from `Σ.L` across any state transition, and arrangement-modifying steps emit no link."

**Problem**: L12a asserts monotonicity (`dom(Σ.L) ⊆ dom(Σ'.L)`), not "domain non-extension for non-emitting steps". L12a allows extension; it forbids only removal. The actual non-extension property for arrangement-modifying steps comes from the definitional partition of ↦ (arrangement-modifying steps are *defined* not to emit links). The trailing clause "arrangement-modifying steps emit no link" acknowledges this, but it's the *definitional commitment*, not an L12a consequence.

**Required**: Restate the citation: "holds `Σ'.L = Σ.L` because (i) ASN-0043's L12 forbids modification of existing entries, (ii) ASN-0043's L12a forbids removal, and (iii) arrangement-modifying steps are *defined* not to extend dom(Σ.L) (they live in `↦ \ →` by the partition definition)."

### Issue 7: The proof of R0a's Stage 2 inductive step does not address the discipline's enforcement at class-(iii) steps

**ASN-0086, R0a proof, Stage 2 Step**: "For class (iii), the discipline hypothesis on this step constrains the fresh address `a` to be constructed by R0 Step 2 (Case A or Case B), not just any substrate-primitive-permissible address."

**Problem**: The proof asserts that discipline forces R0 Step 2's construction but doesn't establish what specifically the discipline rules out at each step. The Implementation Notes say the discipline "never deposits at a strict prefix-extension of an existing link address" — but the inductive proof should explicitly show that a non-disciplined emission (e.g., depositing at `a' = a₁.1` for existing `a₁`) would break the antichain. Without this, the proof's reliance on the discipline is opaque.

**Required**: Add an explicit "non-disciplined counterexample" paragraph showing that if class (iii) deposited at `a' = a₁.1` for existing `a₁ ∈ dom(Σ.L)`, then `a₁ ≼ a'` would hold and the antichain conclusion would fail. This makes precise what the discipline buys.

### Issue 8: The Worked Sketch verifies R-claims by inspection without systematic coverage

**ASN-0086, Worked Sketch**: The sketch walks through Step 1 (Nullify) and Step 2 (re-emission), checking specific computations (`coverage`, `L_K`, `L_R`, `nullified`, `A_K`) but does not explicitly trace which R-claim is being witnessed at each step.

**Problem**: The sketch could verify each substantive R-claim against the example explicitly (e.g., "Step 2 demonstrates R0: a₂ is a fresh address distinct from a₁; R2: a₁'s value is preserved across Σ_0 → Σ_2; R3: L_K monotonically grew from {(a₁,...)} to {(a₁,...), (a₂,...)}; R6a: a₁ remains nullified at Σ_2"). Without this mapping, the sketch reads as a procedural walkthrough rather than a verification.

**Required**: Add explicit R-claim citations at each computation step ("By R3: L_K^{Σ_1} ⊇ L_K^{Σ_0} = {(a₁, F₁, G₁)} ✓"). The sketch already touches R0a-Cor1/Cor2 explicitly at the end; extend the pattern back through the rest of the example.

### Issue 9: R5's generalization claim has no proof

**ASN-0086, R5 proof, closing**: "The construction generalizes: any endset content built from L13-admissible canonical spans, possibly extended by L4(c)-licensed cross-subspace spans, is similarly admissible because R0's verification depends only on L3 well-formedness, not on span targets."

**Problem**: The proof exhibits one concrete emission `(∅, G_self, K)` and argues invariant-preservation for it. The generalization to "any endset content" is asserted in one sentence at the end. While the underlying claim ("R0's verification depends only on L3 well-formedness") is true (and can be verified by inspecting R0 Step 4), the leap from one example to "any" warrants a brief explicit derivation: enumerate which R0-Step-4 invariants are endset-content-dependent (only L3) and which are not.

**Required**: Replace the one-line generalization with an explicit short paragraph: "Examining R0 Step 4 invariant-by-invariant, the only endset-content-dependent check is L3 (well-formedness of the triple structure: arity 3, F,G ∈ Endset, K ∈ T_admissible non-empty). L0/L1/L1a/L1b/L1c depend on the address a' alone; L2/L5/L6/L11a–L14a depend on structural properties of a' and Σ. Any endset content satisfying L3 therefore admits the same emission argument."

## OUT_OF_SCOPE

### Topic 1: Multi-arity link relations

**Why out of scope**: The note restricts to standard-triple links (|Σ.L(a)| = 3) and acknowledges in Open Questions that higher-arity relations admit an analogous construction. This is appropriate deferral.

### Topic 2: Cross-subspace content (non-s_C-resident)

**Why out of scope**: The Setup hypothesis globally restricts content to s_C-resident addresses. The note's Open Questions includes the slice-wise reformulation question. Adding cross-subspace content handling is genuine new territory, not an error in this ASN.

### Topic 3: Concurrency model for Emit/Observe

**Why out of scope**: Open Questions explicitly raises atomicity and consistency model questions. This is new territory requiring concurrent-systems machinery not currently present.

### Topic 4: Promoting the sibling-frontier discipline to substrate level

**Why out of scope**: Open Questions raises whether the discipline (currently conditional on implementation) should be tightened into the substrate primitive. This is a future design question rather than a flaw in the present ASN's positioning of the discipline as an implementation hypothesis.

### Topic 5: Tightening L1b's `#E ≥ 2` to `#E = 2` at the substrate level

**Why out of scope**: Open Questions raises this; R0a-Cor2 establishes `#E = 2` within the disciplined regime. Whether L1b itself should be tightened is a substrate-level design question, not an ASN-0086 issue.

VERDICT: REVISE
