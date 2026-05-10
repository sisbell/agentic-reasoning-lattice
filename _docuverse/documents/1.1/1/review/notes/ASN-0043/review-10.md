# Review of ASN-0043

## REVISE

### Issue 1: L11 worked example mischaracterizes non-injectivity applicability

**ASN-0043, Worked Example, L11 verification**: "Non-injectivity: requires |dom(Σ.L)| ≥ 2, so the clause does not apply here."

**Problem**: L11's non-injectivity clause is universally quantified over all conforming states `Σ` and all `a ∈ dom(Σ.L)`. It requires `|dom(Σ.L)| ≥ 1` (so that `a` exists) and asserts the existence of a conforming *extension* with a duplicate value. The clause applies to the initial state, which has one link — its precondition is satisfied. What Step 1 provides is the *witness* for the existential, not the activation of the clause. The statement "requires |dom| ≥ 2" conflates the property of the current state (which is injective when |dom| = 1) with the applicability of the formal statement (which is applicable to any non-empty link store). Compare: L9 (TypeGhostPermission) is similarly an existence claim about extensions, and its worked-example verification correctly treats the initial state as satisfying the clause, not as exempt from it.

**Required**: Replace "requires |dom(Σ.L)| ≥ 2, so the clause does not apply here" with language acknowledging the clause applies and that the extension witnessing it is constructed in Step 1. For example: "The extension witnessing the existential is constructed in Step 1 below."

### Issue 2: L11 combines two claims of different logical character under INV

**ASN-0043, Properties Table**: "L11 | INV | IdentityByAddress — (a) link addresses inherit GlobalUniqueness via T9; (b) every conforming state with a link can be extended to a non-injective conforming state"

**Problem**: L11 bundles two claims that serve different logical roles under a single INV label.

Part (a) — *uniqueness* — is derived from GlobalUniqueness (ASN-0034) via T9. It is a consequence of the foundation, not a new state constraint. Its logical character is LEMMA (a derived property).

Part (b) — *non-injectivity* — is an existence claim: every conforming state with a link *can be extended* to a state where two distinct addresses map to the same triple. This does not constrain states; it shows that certain states are permitted. Its direct analogue in ASN-0036 is S5 (UnrestrictedSharing), which demonstrates that arbitrarily high sharing multiplicity is consistent with S0–S3. S5 is classified LEMMA. L11(b) should follow the same convention.

The INV label suggests a state constraint (as with L0, L3, L12), but neither half constrains. One derives; the other permits. Grouping them under INV obscures which properties of the link model are *requirements* (must hold in every state) versus *permissions* (consistent with the requirements but not mandated).

**Required**: Either split L11 into two properties — L11a (uniqueness, LEMMA derived from T9 + GlobalUniqueness) and L11b (non-injectivity, LEMMA with constructive witness) — or reclassify L11 as LEMMA and acknowledge the compound structure in the table description.

### Issue 3: L4 formal statement is entailed by L3 + the Endset definition

**ASN-0043, Endset Properties, L4**: `(A a ∈ dom(Σ.L), e ∈ {from, to, type}, (s, ℓ) ∈ Σ.L(a).e :: s ∈ T ∧ (s, ℓ) satisfies T12)`

**Problem**: By L3, every link value is a triple of endsets of type `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs satisfying T12. Therefore every span `(s, ℓ)` in every endset already satisfies `s ∈ T` and T12 by the type definition. L4's formal statement is a theorem of L3 + definitions, adding no constraint beyond what the types guarantee.

The substantive content of L4 — that there are *no additional constraints* (cross-document spans permitted, cross-subspace spans permitted, no existence requirement on referenced addresses) — appears only in the informal sub-items (a), (b), (c). These are the design-significant claims, but they lack formal backing within L4 itself. The formal statement captures the floor (T12 holds), while the description in the properties table captures the ceiling ("no single-document, content-only, or existence constraint"). The mismatch means a reader verifying L4's formal statement finds it trivially true from definitions, while the interesting claims are informal.

The ASN partially compensates: L9 witnesses the no-existence-requirement claim, L13 witnesses cross-subspace references, and the worked example shows cross-document implicitly. But L4 itself should acknowledge its relationship to the definitions it restates.

**Required**: Reclassify L4 as a corollary or remark, making explicit that the formal statement is definitional and the sub-items are the substantive contribution. Alternatively, restructure sub-items (a)–(c) as lemmas with explicit witnesses, paralleling how L9 formalizes the ghost-type permission.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage is a general tumbler-space property

PrefixSpanCoverage proves that the unit-depth span at tumbler `x` covers exactly `{t : x ≼ t}`. The proof depends only on T1, T12, and TumblerAdd — no link-specific concepts. It is a property of the tumbler space and span arithmetic, not of the link ontology. Future ASNs needing this result (e.g., a span algebra or query semantics ASN) would have to reference ASN-0043 (a non-foundation) or re-prove it.

**Why out of scope**: Organizational placement, not a correctness issue in this ASN. The proof is rigorous and correctly used for L10 and L13. The question is whether it belongs in a foundation ASN (tumbler algebra or a dedicated span algebra) so that other ASNs can cite it without cross-referencing the link ontology.

VERDICT: REVISE
