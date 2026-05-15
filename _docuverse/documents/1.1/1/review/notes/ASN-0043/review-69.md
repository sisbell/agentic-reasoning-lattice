# Review of ASN-0043

## REVISE

### Issue 1: L9 proof's content-side subspace argument is unsupported by L0

**ASN-0043, L9 proof, ghost construction**: "By L0 applied to Σ: `dom(Σ.C) ⊆ {t : subspace_I(t) = s_C}` and `dom(Σ.L) ⊆ {t : subspace_I(t) = s_L}`. ... Since `s_X ≠ s_C` and `s_X ≠ s_L`, T7 gives `g ∉ dom(Σ.C) ∪ dom(Σ.L)` — unconditionally, regardless of the size of these domains."

**Problem**: L0 only constrains `dom(Σ.L)` — it imposes no constraint on the subspace identifiers of content addresses. L0a explicitly acknowledges that ASN-0036's invariants do not fix a global content-subspace constant ("conforming ASN-0036 systems may, in principle, place content in subspaces other than `s_C`"). For a conforming state where some content resides in subspace `s_X`, the ghost `g` constructed in `s_X` could collide with content, and T7 then yields nothing useful. The "unconditionally" qualifier directly contradicts L0a's scoping admission.

**Required**: Either (a) add an s_C-residence precondition to L9 — e.g., "with `(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)`" — matching the regime where the proof actually closes; or (b) revise the construction (e.g., choose `s_X` to avoid every subspace present in `dom(Σ.C)`, which requires content-store state-finiteness not currently axiomatized). The same problem affects the L9 proof's "L0 by subspace (`a` is in `s_L`)" step for the new link address `a`: `a ∉ dom(Σ'.C)` requires content to not be in `s_L`, which L0/L0a do not establish.

### Issue 2: L11a Case (i) — unjustified length equality of homes

**ASN-0043, L11a derivation, Case (i)**: "Chain-prefix-preservation forces each address to agree with its home on positions 1..#home; since `#home(a₁) = #home(a₂)` (both have the four-field document-level structure with zeros = 2) but the homes differ at some position `j ≤ #home`..."

**Problem**: `zeros(s) = 2` does not imply equal length. Document-level tumblers `N.0.U.0.D` have varying lengths depending on the widths of the `N`, `U`, `D` fields. The argument as written handles only the equal-length sub-case and silently drops the unequal-length sub-case (where `home(a₁)` and `home(a₂)` differ in length).

**Required**: Replace with the contrapositive of T4b's unique parse: `home(a) = N(a).0.U(a).0.D(a)` is a deterministic projection of a T4-valid address (UniqueParse, ASN-0034), so `a₁ = a₂ ⟹ home(a₁) = home(a₂)`; contrapositively, `home(a₁) ≠ home(a₂) ⟹ a₁ ≠ a₂`. This needs no length premise.

### Issue 3: Worked example's L9 verification recycles the unsound L0 argument

**ASN-0043, worked example, L9 step**: "Since `subspace_I(g) = 3 = s_X` and `s_X ≠ s_C`, `s_X ≠ s_L`, L0 applied to Σ gives `dom(Σ.C) ⊆ {t : subspace_I(t) = s_C}` and `dom(Σ.L) ⊆ {t : subspace_I(t) = s_L}`, so `g ∉ dom(Σ.C) ∪ dom(Σ.L)` — by subspace separation alone, not by the contingency that no entity happens to be stored at this address."

**Problem**: Same misattribution to L0 as Issue 1. The example's content is in fact `s_C`-resident (verified earlier under L0), so the conclusion holds, but the justification cited is incorrect, and the "by subspace separation alone, not by the contingency" framing is exactly what L0a denies in general.

**Required**: For this specific state, replace the L0-citation with direct enumeration: `dom(Σ.C) = {c₁, c₂}` with `subspace_I(cᵢ) = 1 = s_C ≠ 3`, so `g ≠ cᵢ` by T7; `dom(Σ.L) = {a}` with `subspace_I(a) = 2 = s_L ≠ 3`, so `g ≠ a` by T7. The "structural rather than state-dependent" remark should be removed or qualified.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage relocation

**Why out of scope**: The axiomatization is explicitly flagged by the author as pending relocation to a span/tumbler-algebra ASN. The identity is correct and derivable from existing ASN-0034 primitives (PrefixRelation, OrdinalShift, T1, NAT-discrete). This is an organization decision for a future ASN, not a defect in the current ASN's content.

### Topic 2: ASN-0036 strengthening of content-subspace constraint

**Why out of scope**: A clean fix for Issue 1 via tightening ASN-0036 to fix `subspace_I(b) = s_C` globally for content addresses (lifting L0a's scope from the `s_C`-resident slice to all of `dom(Σ.C)`) belongs in an ASN-0036 revision, not in this ASN. The author has noted this dependency in the Open Questions and L0a's prose.

### Topic 3: Type address hierarchy well-formedness

**Why out of scope**: The Open Question "What must a conforming type address hierarchy satisfy beyond tumbler prefix containment?" is genuine future-ASN territory — type-registry constraints belong in a future ontology/governance ASN, not the link model.

VERDICT: REVISE
