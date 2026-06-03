# Review of ASN-0070

I checked the inverse-image definition (F0), the canonical-form uniqueness theorem (F-canonical), the contiguity claim, the six worked configurations, and the derived-property catalogue (F-sound through F-multidoc) against the foundations. The mathematics is sound: Step 1's `k < m` vs `k = m` case split is exhaustive and the finiteness exclusion is correct; the consecutivity characterisation and the run-partition argument hold; F-sound/F-complete correctly split the postcondition equality; the boundary cases (empty endset, empty arrangement, vacuous subspace) are handled. All ASN references (0034, 0036, 0043, 0047, 0053, 0058) are to foundation ASNs, so no illegal cross-references. The findings below are clarity and anti-bloat issues, not correctness defects.

## REVISE

### Issue 1: Existence proof interleaved inside the uniqueness argument; theorem mislabeled
**ASN-0070, F-canonical (CanonicalUniqueness)**: The theorem is named "CanonicalUniqueness" but its statement and proof establish *existence and uniqueness* ("there exists exactly one"). Worse, the existence construction labeled "Step 2a — Existence of the canonical form" is physically inserted *between* the "Bridge" paragraph and the "Internal contiguity" paragraph of Step 2's uniqueness argument. A reader tracking the uniqueness chain (Bridge → internal contiguity → right-closure → left-closure → unique reconstruction) is forced to context-switch through a self-contained existence proof mid-stream.
**Problem**: The proof structure obscures which subparts establish existence versus uniqueness; the name advertises only half the content.
**Required**: Either rename to CanonicalExistenceAndUniqueness (or split into two claims), and move Step 2a so the existence construction is not embedded inside the uniqueness sub-argument.

### Issue 2: F-subspace's Consequence re-derives a chain its own postcondition already encapsulates
**ASN-0070, F-subspace, "Consequence" derivation**: "Reusing the postcondition equality `subspace(v) = subspace_I(M(d)(v))` ... By S3★-aux ... S3★ places the image accordingly ... Applying L0 and L14 to the image ..."
**Problem**: The main Depends derivation already discharges `subspace(v) = subspace_I(M(d)(v))` from S3★-aux + S3★ + L0. The Consequence re-walks S3★-aux and S3★ a second time. Only the L0/L14 step (lifting to the biconditional `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)`) is new content.
**Required**: Start the Consequence from the established postcondition equality and add only the L0+L14 biconditional step; drop the re-invocation of S3★-aux/S3★.

### Issue 3: Repeated "System reading" template across the derived-property catalogue
**ASN-0070, F-det / F-origin / F-state / F-multidoc, "System reading" paragraphs**: Four lemmas each close with an essay paragraph of the form "This is the structural form of Nelson's '...'." These restate design intent and do not advance the lemma's formal reasoning; the rhetorical move recurs verbatim in structure four times.
**Problem**: Under the note's anti-bloat classifier, this is essay content occupying structural (lemma) slots — the reader skips past it to reach the next claim, and the repetition compounds across the catalogue.
**Required**: Consolidate the design grounding into a single remark (e.g., one paragraph in the section preamble) rather than appending a templated essay to each lemma. (Judgment call — Nelson commentary is house style in foundation ASNs, but there it sits in dedicated commentary positions, not replicated per derived lemma.)

### Issue 4: Forward-reference gestures justifying representability before it is needed
**ASN-0070, F0 abstract paragraph**: "Within each subspace component, V-positions share common depth ... so each component is level-uniform and amenable to span-set representation." Also F-canon-form clause (i): "width of the form `δ(c, m_S(d))` ... (justified in Step 1 below)."
**Problem**: These pre-justify the span-set representation choice inside the abstract definition, forward-referencing F-canonical's Step 1. The definition's job is to fix `R(d,e)`; the representability argument belongs where it is proved.
**Required**: Remove the representability gesture from F0's abstract paragraph; in F-canon-form, state the width restriction as a definitional clause and let F-canonical carry its justification without the inline forward pointer.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics of `follow` against a concurrently-modified document
**Why out of scope**: Raised by the ASN's own Open Questions; concurrency/transaction semantics are new territory, not a defect in this query specification.

### Topic 2: Resolution relationships across documents sharing transclusion lineage
**Why out of scope**: Listed in Open Questions; cross-version reach correspondence is a future ASN, not an error here.

VERDICT: REVISE
