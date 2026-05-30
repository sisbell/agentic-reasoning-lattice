# Review of ASN-0042

## REVISE

### Issue 1: Worked Example verifies properties defined in later sections
**ASN-0042, Worked Example**: "*Verifying O7's postconditions for π_A:*" ... "**O6**: `acct(a₂) = [1, 0, 2] = pfx(π_A)`" ... "*Verifying O9 (Node-locality)*" ... "**Fork (O10).**"
**Problem**: The Worked Example exercises O5, O6, O7, O8, O9, and O10 — every one of which is *defined and proved in sections that come after* the Worked Example (Subdivision Authority, Structural Provenance, Delegation, Node-Locality, Fork). The reader must jump forward across half the document to learn what each label means before the verification can be read. A rigor-claiming ASN should not verify claims it has not yet stated.
**Required**: Either relocate the Worked Example after the Fork section (so all of O5–O10 are in scope), or split it so each milestone is verified within the section that introduces the property it exercises.

### Issue 2: Defensive justification prose attached to axiom O5
**ASN-0042, Subdivision Authority Axioms (O5)**: "This formulation avoids applying `ω` to the prefix itself (which may not yet be in `Σ.B`); instead it directly constrains the allocator to be the most-specific covering principal in `Π_Σ`."
**Problem**: This explains *why the axiom is written this way* rather than stating what it asserts — exactly the "why the axiom is needed" meta-prose the anti-bloat pass targets. The axiom's content is the formula; the design rationale is noise the precise reader must skip.
**Required**: Delete the justification, or demote it to a one-line non-normative remark outside the axiom body.

### Issue 3: Duplicated claim across sections — "mutually exclusive futures"
**ASN-0042, O7(c) proof and Worked Example (Sub-account namespaces)**: both contain verbatim "namespace baptism and principal baptism are mutually exclusive futures for the same prefix."
**Problem**: Two paragraphs in different sections state the same proposition in (near-)identical words. This is the "two paragraphs say the same thing" pattern; it compounds across cycles.
**Required**: State the mutual-exclusivity fact once (it follows from O18 freshness), and reference it from the other site without re-asserting.

### Issue 4: Unilateral O10★ restates its own proof body inside the Formal Contract
**ASN-0042, O10 Formal Contract**: "*Unilateral postcondition* ... The unilateral guarantee is unconditional: PrefixBaptismCoupling ensures every sub-delegate's prefix lies in `Σ.B`, so the depth-2 component of every length-(#pfx(π) + 2) Form B sub-delegate prefix is at most `hwm_0`, and `hwm_0 + 1` is never claimed by any sub-delegate..."
**Problem**: This reproduces the Form-B non-coverage argument already given in full in the proof body, and the body itself forward-points to it ("recorded as the Unilateral postcondition in the Formal Contract below"). The contract slot should state the postcondition, not re-run the proof.
**Required**: Reduce the Unilateral postcondition to its claim; drop the embedded re-derivation and the body's forward pointer.

### Issue 5: "Counterpart" framing on O16 restates rather than advances
**ASN-0042, O16**: "This is the address-side counterpart of O15: just as principals enter Π exclusively through bootstrap or delegation, addresses enter `Σ.B` exclusively through allocation by an existing principal."
**Problem**: The sentence re-narrates O16 by analogy to O15 without adding content the formula lacks. This is use-site/relationship meta-prose around an axiom.
**Required**: Cut, or keep only the Gregory corroboration sentence that follows it.

### Issue 6: Defensive symbol-reuse disambiguation paragraphs
**ASN-0042, Ownership Domains (Notation) and State Axioms (Notation)**: "`dom(π)` applies to a principal ... distinct from `dom(A)` of T10a ... argument kind disambiguates." and "We reuse ASN-0040's `.B` registry accessor on this ASN's own state symbol `Σ`, writing `Σ.B` for what ASN-0040 writes `s.B`."
**Problem**: Both are defensive explanations of notation overloading rather than content. Foundation symbols may be used directly; the reader does not need a paragraph licensing the reuse.
**Required**: Either pick non-colliding symbols (e.g., `princdom(π)`) so no disambiguation prose is needed, or compress each note to a parenthetical.

### Issue 7: Multiple cross-section deferrals to the transfer/provenance discussion
**ASN-0042, Permanence and Refinement**: "The provenance-versus-authority divergence such a regime would introduce is discussed under Structural Provenance below." — and SelfOwnershipAtPrefix: "A concrete instance at the boundary `a₆ = pfx(π_A) = [1, 0, 2]` appears in the *Worked Example* below."
**Problem**: Repeated forward pointers ("discussed below," "appears below") deferring content to other sections. Transfer divergence is then discussed in Permanence, again in Structural Provenance, and again in Open Questions — three sites for one idea.
**Required**: Consolidate the transfer-divergence discussion to a single location and remove the deferral pointers.

## OUT_OF_SCOPE

### Topic 1: Formal invariants of an ownership-transfer regime
**Why out of scope**: The provenance/authority divergence that a transfer mechanism would introduce is genuinely new territory; the ASN correctly records it as an Open Question rather than specifying it. No fix required here — flagged only to confirm the omission is deliberate, not a gap in O3.

META: not needed — the ASN stays within abstract ownership semantics (state Π/pfx, delegation operation, invariants O1a/O1b/O2), and its issues are bloat and ordering, not drift into implementation mechanics.

VERDICT: REVISE
