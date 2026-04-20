# Review of ASN-0036

## REVISE

### Issue 1: S8a — `zeros(v) = 0` contradicts acknowledged subspace 0

**ASN-0036, S8a**: "Every V-position `v ∈ dom(Σ.M(d))` is an element-field tumbler: `zeros(v) = 0` and `v > 0`. A V-position represents the element field of a full document-scoped address — the fourth field in the T4 field structure. Its first component `v₁` is the subspace identifier (1 for text, 0 for links)."

**Problem**: The formal claim and the exposition are self-contradictory. A V-position in the link subspace has the form `0.x` (with `x > 0`), giving `zeros(v) = 1`, not `0`. The domain characterization `dom(M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ t > 0}` therefore excludes every link-subspace V-position that the same paragraph introduces.

The conflict runs deeper than S8a's own text. T4 (ASN-0034) requires all element-field components to be strictly positive: `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`. A subspace identifier of 0 violates this. A full I-address in the link subspace (e.g., `N.0.U.0.D.0.0.x`) would contain four zeros — two of them adjacent at the subspace boundary — violating T4's syntactic conditions (no adjacent zeros, at most three zeros) and S7b's `zeros(a) = 3`.

No downstream proof in this ASN actually depends on `zeros(v) = 0` — the S8 partition proof uses prefix ordering (PrefixOrderingExtension) and fixed depth (S8-depth), both of which hold regardless of the subspace identifier's value. But the formal statement of S8a is wrong as written.

**Required**: Since links are declared out of scope, remove the mention of subspace 0 from S8a entirely. Restrict the well-formedness claim to the text subspace: `v₁ ≥ 1` (or simply `v₁ = 1` for text). Defer the link-subspace encoding — and its reconciliation with T4's element-field positivity requirement — to a future ASN on links. If the ASN wishes to retain a remark about subspace 0 for orientation, it should be clearly marked as a forward reference outside the formal property statement, with the T4 tension noted.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace coherence of arrangements
The ASN establishes that V-positions and I-addresses each carry subspace structure (text vs. links), but no property constrains the arrangement to preserve subspace identity — nothing prevents a text V-position from mapping to a link I-address. A subspace-coherence invariant (`M(d)(v)` is in the same subspace as `v`) would be the natural companion to S3 but belongs in a future ASN on links and content typing.

**Why out of scope**: This involves the semantics of link content vs. text content, which is explicitly excluded from this ASN's scope.

### Topic 2: Vocabulary convention for subspace 0 vs. T4 positivity
The shared vocabulary defines two subspaces — "text content (1.x) and links (0.x)" — where 0 is the literal first component. T4 (ASN-0034) requires all element-field components to be strictly positive, and T7 implicitly inherits this by defining subspace identifiers as element-field components. The reconciliation (relabeling subspaces to use only positive identifiers, or relaxing T4 for the element field's first component) is a cross-cutting concern that touches the vocabulary, the foundation, and every ASN that mentions links.

**Why out of scope**: This is a foundation-level alignment question, not an error in this ASN's treatment of the text subspace.

VERDICT: REVISE
