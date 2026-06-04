# Review of ASN-0087

## REVISE

### Issue 1: M-DepthConv content restated 6+ times across the note
**ASN-0087, Inputs / Preconditions / Effect / Worked Example / D-SEQ★ verification / claims table**: the same convention — "when `V_{s_L}(d) = ∅`, `Σ` leaves the depth free / `m_L(d)` is undefined, so MAKELINK fixes `m = 2`; otherwise inherit `m_L(d)`" — is spelled out in full in the Inputs paragraph, restated in two Preconditions rows, restated again in the Effect section, again in the Worked Example, again in the S8-depth invariant row and the D-SEQ★ paragraph, and then a fourth-through-seventh time across the claims rows M-DepthConv, M-Pre, M-Alloc, M-Effect (each of which re-embeds "depth 2 by M-DepthConv for the first link, else `m_L(d)`").
**Problem**: This is the anti-bloat pattern of "two paragraphs say the same thing in different words," compounded across the whole document. The reader must re-parse the identical free-depth/fixed-2 disjunction at every site. The claims table — an index — should point to the convention, not re-derive it in four adjacent rows.
**Required**: State the convention once (M-DepthConv), and at every other site write only "`v_ℓ` per M-DepthConv." Collapse M-Pre/M-Alloc/M-Effect's depth clauses to a single reference.

### Issue 2: J0/J1★/J1'★ discharge stated twice in the same subsection, then a third time in the claims table
**ASN-0087, Composite-Boundary Properties**: the three bullets discharge J0 (frame on `C`), J1★ (`subspace(v_ℓ) = s_L ≠ s_C`), and J1'★ (frame on `R`). The immediately following paragraph — "Note that J0 and J1'★ are vacuous because their quantification universes are empty under MAKELINK's frames on `C` and `R`; J1★ is vacuous because every new V-position MAKELINK introduces is link-subspace" — re-asserts exactly those three discharges in different words. M-Inv-Bdry then states them a third time.
**Problem**: The "Note that…" paragraph advances no reasoning; it summarizes the three bullets that precede it by one line. This is redundant meta-prose in a structural slot.
**Required**: Delete the "Note that…" paragraph. The bullets and the M-Inv-Bdry index entry already carry the content.

### Issue 3: L1c re-derives the full inc-chain that K.λ already guarantees, contradicting the ASN's own stated transfer discipline
**ASN-0087, Per-State Invariants at Σ' (L1c table + step-by-step) vs. Freshness of the Allocation**: For freshness the ASN explicitly declines to re-derive: "We do not re-derive this from the underlying chain lemmas; ASN-0093 already packages the guarantee for every emission of `A_L(d)`, and MAKELINK introduces no allocation step beyond the K.λ it composes, so the result transfers verbatim." For L1c the ASN does the opposite — a six-row chain table with per-step TA5/TA5a verification.
**Problem**: L1c (LinkAllocatorConformance) is a per-state invariant that ASN-0093's K.λ binding precondition + ChainMembershipForOrigin/ChainDiscipline already establish for *every* `A_L(d)` emission. By the ASN's own argument, MAKELINK introduces no allocation beyond K.λ, so L1c transfers verbatim exactly as freshness does. The full chain reconstruction is substrate re-derivation the note elsewhere refuses to do — inconsistent treatment of two structurally identical "inherit-from-K.λ" obligations.
**Required**: Either (a) discharge L1c by the same one-line transfer-from-K.λ used for freshness, or (b) justify why L1c specifically warrants re-derivation when freshness does not. Pick one discipline and apply it to both.

### Issue 4: Home-document-not-privileged point restated across four sites
**ASN-0087, "Discoverability Is Symmetric" / WP Case 2 / Reflexive Endsets / M-DiscSymmetry**: the claim that the home document holds no privileged discovery status (privilege is structural placement, not semantic discoverability) appears as its own section, again as the WP Case 2 closing sentence ("The home-document privilege of MAKELINK is structural… not semantic"), again under Reflexive Endsets ("No reflexive discovery from other documents"), and again as M-DiscSymmetry.
**Problem**: Three of these four restate the identical conclusion. The standalone "Discoverability Is Symmetric" section and the WP closing sentence are interchangeable.
**Required**: Keep one statement (M-DiscSymmetry as the index, plus one in-text derivation) and remove the duplicated assertions.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets
The first Open Question (constraints on endsets whose spans reference not-yet-allocated I-addresses) is genuinely new territory — L4 permits such spans, and the side-effect/standard-authoring analysis bounds their behavior. A normative constraint belongs in a future endset-discipline ASN, not here.

### Topic 2: Composite-level atomicity enforcement
The note correctly identifies that substrate provides no composite atomicity and defers the enforcing mechanism to the protocol layer. That layer's design is out of scope for the operation semantics.

VERDICT: REVISE
