# Review of ASN-0047

## REVISE

### Issue 1: M1 preservation claimed "verified in the Class (a) matrix" but has no matrix row
**ASN-0047, *Inherited from foundation* table and *Class (a)* matrix**: The inherited-table preamble states "Their preservation under this ASN's new transition (K.μ⁺_L) and amended transitions (K.λ, K.μ⁺, K.μ⁻, K.μ~) is verified locally in the Class (a) matrix," and the table lists M1 (ArrangementMonotonicity, `dom(M) ⊆ dom(M')`).

**Problem**: M1 appears as no row in the Class (a) verification matrix, and is absent from the ExtendedReachableStateInvariants per-state list. Every other inherited per-state property the preamble covers (L0, L1, L1a, L1b, L1c, L3, L14, L-fin, C-fin) does have a matrix row; M1 is the lone exception. Its preservation (dom(M) = E_doc grows only by K.δ, framed elsewhere) is plausible but is asserted-by-cross-reference to a verification that does not exist. This is exactly the kind of bookkeeping gap the matrix is meant to close.

**Required**: Either add an M1 row to the Class (a) matrix (K.δ grows dom(M) = E_doc; all other transitions frame the document set; K.μ⁻ contracts `dom(M(d))` not `dom(M)`), or remove M1 from the "verified in the Class (a) matrix" scope and discharge it explicitly where document-set monotonicity is argued (e.g., alongside S7d/P1).

### Issue 2: The "clause (v) is not a lifetime guarantee" disclaimer is stated twice in different sections
**ASN-0047, *Decomposition of K.μ~* and *Link V-position permanence***: First: "This fixity is thus a property of the chosen full-clearance realisation, not a lifetime guarantee on a link's V-position." Later, in a separate section: "exhibiting that clause (v)'s single-K.μ~ fixity does not extend to a lifetime guarantee."

**Problem**: Two paragraphs in different sections make the same point in different words — the "two paragraphs in the same document say the same thing" pattern the anti-bloat classifier asks to surface. The reader meets the disclaimer, then meets it again with no new content. The withdraw-and-re-add construction in *Link V-position permanence* is itself the demonstration; the inline disclaimer in the K.μ~ section is redundant once that section exists.

**Required**: State the not-a-lifetime-guarantee point once (at the construction that demonstrates it, in *Link V-position permanence*) and drop the duplicate inline disclaimer in the K.μ~ decomposition prose.

### Issue 3: "Modeling choice (layer separation)" is meta-prose justifying the strengthening rather than stating a property
**ASN-0047, *Amendments to existing transitions*, D-CTG★/D-MIN★**: "*Modeling choice (layer separation).* D-CTG★/D-MIN★ constrain only the arrangement layer `M(d)`, while link permanence is discharged independently on `dom(L)` by L12, so the strengthening does not contradict tombstoning."

**Problem**: This is a labeled sub-paragraph explaining *why the strengthened property is admissible* (it "does not contradict tombstoning") rather than advancing what D-CTG★/D-MIN★ assert. It is the defensive-justification / "why the property is needed" pattern the classifier flags. The substantive fact — D-CTG★/D-MIN★ scope the arrangement layer, L12 governs `dom(L)` — is already carried by the property statements and by L12's own row; the apologetic framing against tombstoning is the noise.

**Required**: Remove the defensive framing. If the layer scoping needs saying, fold "D-CTG★/D-MIN★ constrain `M(d)`; link permanence is L12 on `dom(L)`" into the property definition without the "does not contradict tombstoning" justification.

### Issue 4: Multiple sections defer to "*Link-subspace fixity and realisation*" for the same load-bearing fact
**ASN-0047, *Decomposition of K.μ~* (Step (A)), Class (a) matrix K.μ~ cells (CL-OWN, CL-UNIQ), and the worked link example (Step 3)**: each routes the reader to the *Link-subspace fixity and realisation* sub-step (and to LRP within it) for the pointwise `π(v) = v` / `M'(d)|_{dom_L} = M(d)|_{dom_L}` fact.

**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream location" pattern. The LRP extraction itself is good single-source practice — the issue is the *accumulation* of deferral pointers around it (Step (A) Case s_L, the matrix CL-OWN cell, the matrix CL-UNIQ cell, and Step 3 of the worked example each re-point to the same place). A reader following any one of these must hold an open forward reference to reassemble the argument.

**Required**: Consolidate the deferrals. Since LRP is already the named single source, let the matrix cells cite LRP directly (one token) and drop the prose re-explanations that restate why fixity holds en route to the pointer; do not re-narrate the fixity argument at each deferral site.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
**Why out of scope**: The Open Question on renumbering-aware interior link withdrawal (modeling `DELETEVSPAN`'s compact-and-renumber against this ASN's suffix-only K.μ⁻) concerns a named operation's mechanics, explicitly deferred by Scope; it is correctly posed as future work, not a defect here.

### Topic 2: Concurrency/serialization of link allocation under a shared home document
**Why out of scope**: Raised as an Open Question; operation atomicity and concurrency are listed OUT OF SCOPE. The SequentialTransitionAxiom suffices for this ASN's guarantees, and the concurrency question belongs to a later ASN.

VERDICT: REVISE
