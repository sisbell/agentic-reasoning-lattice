# Review of ASN-0043

## REVISE

### Issue 1: L0a establishes content-side T4-validity twice
**ASN-0043, L0a (ContentSubspaceScope)**: First in the opening paragraph — "ASN-0036's S7b discharges T4-validity (by giving well-definedness of T4b's projections, whose definitional domain is the T4-valid subset of T)" — and again in the derivation paragraph — "for b ∈ dom(Σ.C), by S7b's postcondition that T4b's projections N(b),U(b),D(b),E(b) are well-defined, combined with T4b's definitional domain (UniqueParse) being precisely the T4-valid subset of T — so any b ∈ dom(Σ.C) lies in dom(N)∩dom(U)∩dom(D)∩dom(E), hence is T4-valid."
**Problem**: The same argument (S7b's projection well-definedness ⟹ membership in T4b's domain ⟹ T4-validity) is spelled out twice within one section. This is the "two paragraphs say the same thing in different words" pattern the anti-bloat classifier targets — a reader must read it once to establish well-definedness of `subspace_I`, then re-read it to discharge T7's precondition.
**Required**: State the content-side T4-validity discharge once (it serves both `subspace_I` well-definedness and T7's precondition), then reference it for the second use.

### Issue 2: subspace_I notational convention carries naming-justification meta-prose
**ASN-0043, "Notational convention" (Subspace Residence)**: "The two operate on disjoint tumbler classes (V-positions versus element-level I-addresses) and share neither name nor formula; `subspace_I` is the element-field analogue, named to mark the parallel without conflating the two."
**Problem**: The load-bearing content is the definition — `subspace_I(a) = E(a)₁`, defined on T4-valid `a` with `zeros(a)=3`, `#E(a) ≥ 1`. The clauses justifying the naming choice ("named to mark the parallel without conflating," "share neither name nor formula") are defensive prose about a decision, not reasoning that advances the definition.
**Required**: Keep the definition and the one-clause disambiguation from ASN-0036's `subspace(v)`; drop the justification of the naming.

### Issue 3: defensive proof-path annotation in Home and Ownership
**ASN-0043, Home and Ownership**: "since `d₁ ≠ d₂` as document-level tumblers (by T3) … `home(a₁) ≠ home(a₂)` — directly, without routing through element-level address uniqueness."
**Problem**: "— directly, without routing through element-level address uniqueness" justifies which proof path was *not* taken rather than advancing the claim. The derivation `home(a₁)=d₁`, `home(a₂)=d₂`, `d₁≠d₂` ⟹ `home(a₁)≠home(a₂)` is complete on its own.
**Required**: Remove the trailing clause about the alternate path.

## OUT_OF_SCOPE

(none — the Open Questions section already parks operation-level and transclusion-consistency topics appropriately.)

VERDICT: REVISE
