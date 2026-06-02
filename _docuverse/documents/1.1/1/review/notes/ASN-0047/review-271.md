# Review of ASN-0047

I checked the transition model against the foundation ASNs, verified the worked-example arithmetic and boundary cases (empty document, full clearance, first/subsequent emission, orphan link, transclusion-equal reorder), and applied the `review-mode.anti-bloat` lens for forward-reference accretion. The mathematics is largely sound; my findings are about forward-reference accretion and duplication, not correctness gaps and not scope.

## REVISE

### Issue 1: "K.μ~ range-invariance" is derived downstream and forward-referenced from three sites whose premises are all local

**ASN-0047, *Decomposition of K.μ~* (final paragraph), *Coupling and isolation* J3, and the P4★ Class (b) discharge**: The named result is *used* in two places before it is *derived*:
- *Decomposition of K.μ~*: "By K.μ~ range-invariance (established in the P4★ Class (b) discharge under *Extended reachable-state invariants*), ran(M'(d)) \ ran(M(d)) is empty…"
- J3: "By K.μ~ range-invariance (established in the P4★ Class (b) discharge …), Contains(Σ') = Contains(Σ)."
- Derivation: the P4★ Class (b) discharge ("We label this conclusion **K.μ~ range-invariance**…").

**Problem**: The derivation explicitly states its only premises are "the bijection equation" (the K.μ~ definition) and "link-subspace fixity (established in the Decomposition of K.μ~ section)." Both premises are established locally, in the K.μ~ section. Deriving the one-step consequence several sections downstream and then pointing back to it from two earlier sites (plus the J1★ note) is exactly the "multiple paragraphs in different sections defer to the same downstream location" accretion pattern the anti-bloat directive names.

**Required**: Derive K.μ~ range-invariance once, in the *Decomposition of K.μ~* section where its two premises already sit, and have J3, the J1★ note, and the P4★ discharge cite it locally — removing the three forward pointers.

### Issue 2: The J4 operand-source rule is stated three times within J4 and re-cited in the worked example

**ASN-0047, *Coupling and isolation* J4 (intro), *Definition (Fork)* step (ii), trailing J4 prose, and *Worked example: subsequent-version fork* (close)**: The claim "the transcluded content source is the K.δ operand `d_op`, not invariably `d_src`; a subsequent version inherits the prior version's edits" with its evidence (Nelson CREATENEWVERSION / LM 4/66 / Gregory `docreatenewversion` reading the live POOM) appears:
- J4 intro: "The transcluded content source tracks the K.δ operand (step (ii) of the Definition below establishes this and its consequence for subsequent versions)."
- Definition step (ii): the full statement plus the LM 4/66 + `docreatenewversion`-reads-live-POOM citation.
- k=0 worked example close: "This is Nelson's CREATENEWVERSION copying the contents of the document it is invoked on (LM 4/66, here d₂) and Gregory's `docreatenewversion` reading that document's live POOM including all prior edits."

**Problem**: The intro paragraph is a forward pointer to step (ii) that restates the conclusion it defers; the same operand-tracking rule and the same evidence citation are then repeated. This is the "two paragraphs in the same document say the same thing in different words" and "a definition's introduction enumerates/duplicates downstream content" pattern.

**Required**: State the operand-tracking rule and its evidence once (step (ii)). Reduce the J4 intro to a bare statement without the forward-pointer restatement, and reduce the worked-example close to a one-line cross-reference rather than a re-citation.

### Issue 3: L14a inapplicability is explained twice (dedicated prose block + table row)

**ASN-0047, *L14a inapplicability* prose block and *Local extensions and strengthenings* table (L14a row)**: Both passages explain that L14a's `s_C`-resident hypothesis is unmet in the extended state and that S3★ routes link-subspace mappings to dom(L) while CL-OWN forces home-document ownership.

**Problem**: The same reasoning ("hypothesis unmet → inapplicable → S3★/CL-OWN cover the regime, paralleling S3/S3★") is given in full in two places. One is sufficient; the table row should point to the prose rather than restate it.

**Required**: Keep the inapplicability argument in one location (the prose block) and shorten the table row to a one-line statement with a cross-reference.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
Already correctly deferred — the ASN's K.μ⁻ models link-subspace contraction by suffix removal only, and the implementation's compact-and-renumber `DELETEVSPAN` is flagged as a future operation in Open Questions. This is new territory (an operation), not an error here.

### Topic 2: Address-space exhaustion / concurrent allocation under a shared home document
Listed in Open Questions; belongs to a concurrency/capacity ASN, not this transition model.

VERDICT: REVISE
