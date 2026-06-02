# Review of ASN-0047

## REVISE

### Issue 1: Two differently-named results state the same range-invariance fact

**ASN-0047, *Decomposition of K.μ~* and *Link V-position permanence***: The ASN proves the *same* conclusion twice under two distinct labels.

First, **K.μ~-RANGE (range-invariance)**: "`ran(M'(d)) = ran(M(d))`, and consequently `Contains_C(Σ') = Contains_C(Σ)` and `Contains(Σ') = Contains(Σ)`. *Proof.* By K.μ~-FIX, π is a bijection ... `{M'(d)(π(v)) : v} = {M(d)(v) : v}` gives `ran(M'(d)) = ran(M(d))`."

Later, **K.μ~ range-invariance**: "... what it preserves is the *range* ... `ran(M'(d)) = ran(M'(d)|_{dom_C}) ∪ ran(M'(d)|_{dom_L})`; we close the link half ... Taking the union of the two subspace equalities yields `ran(M'(d)) = ran(M(d))`. We label this conclusion **K.μ~ range-invariance**."

**Problem**: This is the anti-bloat pattern "two paragraphs in the same document say the same thing in different words." K.μ~-RANGE already derives `ran(M'(d)) = ran(M(d))` directly from the full-domain bijection equation; the later paragraph re-derives the identical global fact via a per-subspace union argument and assigns it a *second* label (`K.μ~ range-invariance` vs `K.μ~-RANGE`). The cited downstream uses (J3, the P4★ Class (b) discharge) all reference **K.μ~-RANGE**; the second label is never cited and adds no new conclusion.

**Required**: Remove the redundant "K.μ~ range-invariance" derivation, or fold any non-redundant content (the explicit "K.μ~ does not preserve per-position values" clarification) into the single K.μ~-RANGE statement. One fact, one label, one derivation.

### Issue 2: `subspace_I` misattributed to ASN-0036 and defined twice in the Notation section

**ASN-0047, *Notation***: The I-address projections list states "`subspace_I(a)` (ASN-0036): the I-address subspace identifier, equal to `E(a)₁`." The later *Subspace projections* paragraph states "`subspace_I(a) = E(a)₁` (ASN-0043) projects the first component of an I-address's element field."

**Problem**: Two defects in one section. (a) The first citation is wrong — `subspace_I` is defined in ASN-0043 (`Definition — SubspaceI`), not ASN-0036 (whose `subspace(v) = v₁` is the distinct V-position projection); the two bullets contradict each other on the source ASN. (b) Both `subspace` and `subspace_I` are each defined once in their respective projection bullets and then re-defined verbatim in the dedicated *Subspace projections* paragraph — redundant restatement.

**Required**: Fix the attribution to ASN-0043 in the first bullet, and remove the duplicate *Subspace projections* paragraph (or remove the per-bullet definitions), keeping exactly one definition site for each.

### Issue 3: "Link V-position permanence" mixes essay/implementation prose into a structural slot and re-derives clause (iii) off-site

**ASN-0047, *Decomposition of K.μ~*, "Link V-position permanence"**: The paragraph runs: "What is permanent is the link's *I-address* ... Gregory's implementation places each link by append-at-end (`findnextlinkvsa`) and, on removal, leaves a reverse-orphan ... order-of-arrival is encoded once at creation and is not recoverable from the V-position after withdrawal. Nelson's 'permanent order of arrival' (LM 4/12) is therefore carried by the I-address subspace ordinal ... The same V-stream reading underwrites clause (iii): REARRANGE transposes contiguous regions within a document's flat, dense V-stream (Nelson 4/67) ..."

**Problem**: This is essay/implementation-evidence content occupying a structural slot, and its closing sentences re-justify *clause (iii)* (length-preservation) — a clause already defined and motivated in the admissibility list far above. The "imagines/justifies" prose and the relocated clause-(iii) rationale match the flagged accretion patterns: structural prose that does not advance the reasoning the section is responsible for (the K.μ⁻+K.μ⁺ decomposition and link-fixity).

**Required**: Reduce to the load-bearing statement — that clause (v) is a per-transition bar, not a lifetime guarantee, and a withdraw-and-re-add composite legitimately re-seats a link. Move the I-address-vs-V-position permanence discussion and the clause-(iii) V-stream reading out of this proof slot (the permanence point is already discharged on `dom(L)` by L12); do not re-argue clause (iii) here.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
Already captured by the ASN's own Open Question on renumbering-aware contraction (`DELETEVSPAN` is out of scope). The suffix-only K.μ⁻ model is a deliberate boundary, not a defect in this ASN.

VERDICT: REVISE
