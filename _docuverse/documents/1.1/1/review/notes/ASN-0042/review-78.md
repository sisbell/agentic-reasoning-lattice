# Review of ASN-0042

## REVISE

### Issue 1: Meta-prose deferral paragraph in State Axioms
**ASN-0042, State Axioms ("Preservation pointer")**: "Three structural invariants — O1a (account-level boundary), O1b (prefix injectivity), and per-principal T4 validity — are *stated* at their points of first use ... but share a single inductive *preservation* argument, located together in the **Delegation** section below ... Wherever the body below defers one of these invariants 'across transitions,' that single location is the referent."
**Problem**: This is the "multiple paragraphs defer to the same downstream location" + "prose justifies document ordering" pattern. It advances no reasoning; it is a routing table for the reader. The three preservation proofs in the Delegation section already announce their own base cases and triggers — the pointer is redundant scaffolding.
**Required**: Delete the paragraph. Let each invariant's preservation proof stand where it is written.

### Issue 2: The "forevermore" thesis is restated three times
**ASN-0042, Permanence and Refinement / OwnershipDomainPermanence / O8 design confirmation**: "its precise reading — refinement-only, alterable by no act external to a principal's domain"; "This is Nelson's 'forevermore': not that `ω` is static within `dom(π)`, but that no external act can alter it"; and again under O8's *Design confirmation*.
**Problem**: The same conceptual point ("forevermore ≠ static; means no external act") is asserted in three sections in different words — the "two paragraphs say the same thing" pattern compounded to three. The precise reading belongs at exactly one anchor.
**Required**: State the refined reading once (at OwnershipDomainPermanence, where it is proved) and have the other two sites cite it without re-paraphrasing.

### Issue 3: `fields(a)` collides with foundation T4b's `fields(t)`
**ASN-0042, The Account-Level Boundary**: "We adopt the local abbreviation `fields(a) ≡ (N(a), U(a), D(a), E(a))` for the tuple of T4b's four partial projections ... used as informal shorthand throughout this ASN whenever convenient."
**Problem**: Foundation T4b already defines `fields(t)` as the decomposition function. Redefining the identical symbol as a 4-tuple shadows the foundation (Standard #7). A reader cannot tell whether a later `fields(a)` means the foundation function or this tuple.
**Required**: Use the foundation projections `N(a), U(a), D(a), E(a)` directly, or pick a non-colliding name for the tuple. Drop the shadowing abbreviation.

### Issue 4: O18 is classified as an axiom but presented as an induction
**ASN-0042, O18 and Properties table**: Table row "O18 ... axiom"; text: "The base case is supplied by O14's seventh clause ... which establishes the membership conclusion for the bootstrap state ... The inductive step is the formula above."
**Problem**: A proof system must know which statements are assumed and which are discharged. The text frames O18 with a base case (O14 vii) and an inductive step — the shape of a derived invariant — yet the summary table calls it an axiom. The base-case discussion actually belongs to PrefixBaptismCoupling's induction (which is where O14 vii and O18 are combined), not to O18 itself. The conflation makes O18's status ambiguous.
**Required**: State O18 purely as the per-transition axiom (the formula), and move the "base case / inductive step" framing into PrefixBaptismCoupling, which is the property whose induction consumes them. Reconcile the table label with the text.

### Issue 5: Worked Example re-derives proofs rather than instantiating them
**ASN-0042, Worked Example ("Verifying O8 (Irrevocability) for π_N over a₁ across multiple states" and "Account-level permanence")**: the example traces three states and concludes "The mechanism is exactly what the proof of O8 articulates: π_N's prefix [1] has length 1, π_A's prefix has length 3 ... Any state with π_A in Π exhibits a covering principal strictly longer than π_N's prefix."
**Problem**: A concrete witness is welcome, but this passage restates O8's longest-match argument in prose (and the adjacent "Account-level permanence" paragraph overlaps the same content). The value of a worked example is checking the *numbers* against the postcondition, not re-proving the theorem. This is the "essay content / relocated proof" pattern in the example slot.
**Required**: Keep the per-state numeric checks (the `ω_{Σᵢ}(a₁)` values); delete the re-derivation of the mechanism and fold the redundant "Account-level permanence" prose into the numeric trace.

### Issue 6: Defensive aside in O7(c) recursion witness
**ASN-0042, O7 postcondition (c)**: "A bare appeal to T0(b) (UnboundedLength) does not suffice — its length-`n` witnesses carry `zeros = 0`, violating condition (iv) — but this account-level chain extends to arbitrary length while keeping `zeros = 1`."
**Problem**: This is a defensive justification anticipating an objection the construction never raises — the witness given already keeps `zeros = 1`. Explaining why an *alternative* (unused) construction would fail is meta-prose around the argument, not part of it.
**Required**: Present the account-level chain directly. Drop the "bare appeal to T0(b) does not suffice" rebuttal.

## OUT_OF_SCOPE

### Topic 1: Where the longest-match / `ω` computation lives in a conforming implementation
The ASN correctly notes that Gregory's `tumbleraccounteq` decides containment, not longest-match, and that `ω` requires the principal registry. The enforcement question — who computes `ω`, and how the session's claimed prefix is validated — is explicitly assigned to the trust boundary and to authentication mechanisms, both listed OUT OF SCOPE. The model-level treatment here is internally consistent; no revision needed.

### Topic 2: Ownership transfer reconciling provenance (O6) with authority (O2)
Raised as an open question. Belongs to a future ASN, not this one.

VERDICT: REVISE
