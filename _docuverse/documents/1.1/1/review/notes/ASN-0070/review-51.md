# Review of ASN-0070

## REVISE

### Issue 1: F-subspace proves its postcondition twice — once in Depends, once in the Consequence Derivation

**ASN-0070, F-subspace (IOSubspaceCorrespondence)**: The Depends paragraph already carries the full forward proof of the postcondition — "By S3★-aux, `subspace(v) ∈ {s_C, s_L}`. In the `s_C` case, S3★ gives `M(d)(v) ∈ dom(C)` and L0 gives `subspace_I(M(d)(v)) = s_C = subspace(v)`; … Either case yields `subspace_I(M(d)(v)) = subspace(v)`." The Consequence Derivation then re-runs the same `s_C`/`s_L` case split to establish the biconditional `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)`, re-deriving the forward direction from S3★ rather than reusing the postcondition equality just proved.

**Problem**: The set-decomposition `R(d,e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))` follows in one step from the postcondition equality `subspace(v) = subspace_I(M(d)(v))` together with S3★-aux and L14. Instead the Consequence ignores the established postcondition and rebuilds the case analysis from primitives. The only genuinely new ingredient in the Consequence is the reverse direction's appeal to L14; everything else duplicates the Depends proof.

**Required**: Derive the Consequence decomposition from the already-proven postcondition equality (apply L0/L14 to the image `M(d)(v)`), removing the restated forward case split.

### Issue 2: Defensive meta-prose explaining why S3★-aux is needed

**ASN-0070, F-subspace, Depends**: "The equality is not delivered by composing S3★ and L0 alone, since both S3★ clauses are conditional on `subspace(v)`'s value and need not fire for an arbitrary natural `subspace(v) = v₁`; S3★-aux supplies the exhaustiveness that makes the case split total."

**Problem**: This sentence argues *why* a dependency is required rather than stating what it contributes — the anti-bloat pattern "new prose explains why the axiom is needed rather than what it says." The subsequent sentence ("By S3★-aux, `subspace(v) ∈ {s_C, s_L}`") already does the work; the rationale clause is the kind of defensive justification the precise reader must skip.

**Required**: Delete the "not delivered by composing … alone" clause; the citation of S3★-aux at its use point is self-justifying.

### Issue 3: The vacuous-subspace convention is restated verbatim across four locations

**ASN-0070, V-Restricted Denotation / F1 / F-canon-form / F-canonical**: The clause "when `m_S(d)` is undefined (… `V_S(d) = ∅`), `Σ_V^S = ⟨⟩` by the vacuous-subspace convention" appears in the V-Restricted Denotation definition (where it is established), and is then restated in F1's postcondition, in F-canon-form's closing sentence, and again in F-canonical's closing sentence.

**Problem**: This is the "multiple paragraphs say the same thing in different words" pattern. The convention is defined once; the three downstream restatements add no content beyond a reference.

**Required**: State the convention once in V-Restricted Denotation and replace the downstream restatements with a bare citation (e.g., "vacuous case per V-Restricted Denotation").

## OUT_OF_SCOPE

### Topic 1: Cross-home / transclusion-lineage resolution relationships
**Why out of scope**: The Open Questions correctly defer the relationship between resolutions across documents with shared transclusion lineage and across multi-home endsets. These are new operations/relations, not defects in the inverse-image definition this ASN fixes.

### Topic 2: Concurrency semantics of `follow` under concurrent modification
**Why out of scope**: `follow` is specified as a state-pure query against a single state `Σ`; concurrency semantics require a transition-interleaving model that belongs to a future ASN.

VERDICT: REVISE
