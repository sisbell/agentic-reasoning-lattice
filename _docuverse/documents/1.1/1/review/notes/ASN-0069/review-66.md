# Review of ASN-0069

This ASN carries the `review-mode.anti-bloat` classifier, and the dominant problem is exactly what that signals: the core derivations (V1–V12) are rigorous and the worked example is thorough, but the argument is buried under meta-prose that re-litigates the ASN's relationship to J4, defers repeatedly to downstream sections, and pads named properties with rationale and disclaimers. The findings below target prose a precise reader must skip past.

## REVISE

### Issue 1: J4-correspondence inventory after V1 does not advance the identity argument
**ASN-0069, §"Identity by Sub-Allocation"**: "Both of V1's cases match J4 of ASN-0047 as written. J4's *allocation-and-operand-tracking rule* explicitly enumerates the two sub-cases... The *first-fork sub-case* ... is the `k = 1` branch; the *subsequent-fork sub-case* ... is the `k = 0` branch, with this ASN's `d_prev` denoting J4's `prev_version`."
**Problem**: These two paragraphs (the "Both of V1's cases match J4" paragraph and the following "J4 also fixes the content source operand" paragraph) are a use-site/notation-mapping inventory. They restate J4's clause structure and assert correspondence between this ASN's labels and J4's, without proving anything V1 has not already established. The trailing pointer "the literal-inheritance deviation is developed at V4" is a forward-reference deferral. J4 is a foundation definition; a single sentence ("V1 instantiates J4's allocation rule; the one deviation, literal inheritance, is V4") suffices.
**Required**: Collapse the two correspondence paragraphs to one sentence; remove the per-clause mapping and the "developed at V4" deferral.

### Issue 2: V4's "motivation is twofold" is rationale prose in a claim slot
**ASN-0069, §"The Arrangement Layer"**: "This is a design commitment of this ASN — not derivable from J4 alone. The motivation is twofold. First, V8's structural correspondence (below) requires the same V-positions... Second, it matches the natural reading of Nelson's..."
**Problem**: This explains *why the commitment is made* rather than *what it claims*, the "Why the axiom is needed" anti-pattern named in the review directive. It also forward-defers to V8 ("below"). The substance of V4 is the formula; the justification belongs in at most one line.
**Required**: State the commitment and its formula; drop the twofold-motivation essay or reduce to a single clause.

### Issue 3: "Why I-Address Identity Suffices" is an essay that introduces no state, operation, or invariant
**ASN-0069, §"Why I-Address Identity Suffices for the Relationship"**: "What I-address identity captures... What I-address identity does not capture... The minimalism is by design. The fork operation creates a new document that *structurally inherits*..."
**Problem**: The entire section is reflective summary — a captures/does-not-capture inventory plus a closing aesthetic claim ("The minimalism is by design"). It restates V6a/V8/V9/V11 results already proved and lists future concerns already covered by Open Questions. It does not advance any proof or define anything.
**Required**: Delete the section, or fold any genuinely new disclaimer (counterpart correspondence, semantic equivalence not captured) into the Open Questions list.

### Issue 4: V8b's non-monotonicity paragraph drifts into operational mechanics it disclaims as out of scope
**ASN-0069, V8b**: "*Non-monotonicity.* ... subsequent K.μ⁻ on either side may move `v` out of ... and subsequent K.μ⁺ may re-install a binding... K.μ~ may remap an image. ... The operational mechanics of removal, re-installation, and remapping are properties of those elementary transition kinds ... not of the fork operation."
**Problem**: The paragraph describes the behavior of K.μ⁻/K.μ⁺/K.μ~ at length and then explicitly states those mechanics are *not* properties of the fork operation. Prose that develops a case and then disclaims it as out of scope is reviser drift. The two proved facts (Π_g ⊆ F; Π_{Σ'} = F) are nearly trivial set facts and do not need the surrounding mechanics narrative.
**Required**: Keep the two bound claims and their one-line derivations; cut the non-monotonicity exposition or reduce it to "Π_g is not monotone — later arrangement edits to `d_op` or `d_new` may remove or restore witnesses."

### Issue 5: Multiple paragraphs defer the same verification to "The Fork Composite" below
**ASN-0069, V9 derivation and V0 Effects**: V9 — "(verified step-by-step in 'The Fork Composite' below)"; V0 R' line — "the equality is verified by the elementary decomposition in 'The Fork Composite' verification below"; V0 K.ρ note — "the elementary multiplicity is verified per step in 'The Fork Composite' verification below."
**Problem**: Three separate slots defer the same set-equality/multiplicity obligation to the same downstream location. This is the "multiple paragraphs defer to the same downstream location" pattern. Each deferral forces the reader to hold an open obligation and chase it later.
**Required**: State the cumulative R' effect once where it is claimed (V0), with a single pointer to the verification; remove the duplicate deferrals in V9 and the V0 K.ρ note.

### Issue 6: "design commitment / not derivable from J4" framing is duplicated across V4, V4b, and V4b's forward-pointer
**ASN-0069, V4 and V4b**: V4 — "This is a design commitment of this ASN — not derivable from J4 alone." V4b — "The commitment is not derivable from J4 alone... and is not derivable from V4 alone... V4b is a design commitment of this ASN; V0's Effects table below carries the commitment forward as the primary positional characterisation..."
**Problem**: The same "this is a design commitment, not derivable from J4" framing is stated in V4, restated in V4b, and again pointed forward to V0's table. Two paragraphs saying the same thing in different words, plus a forward pointer. The not-derivable-from-J4 point need be made once.
**Required**: Make the design-commitment / non-derivability statement once (at V4); in V4b state only the domain-equality content and its one-line justification, without re-asserting the commitment status or pointing forward to V0.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics of forking during concurrent source modification
**Why out of scope**: The first Open Question asks what must hold "when a fork is invoked while the source's arrangement is being concurrently modified — beyond what the sequential atomic transition axiom supplies." This is genuinely new territory (a concurrency model layered above SequentialTransitionAxiom), correctly deferred rather than treated as a gap here.

### Topic 2: Snapshot vs. living fork distinction
**Why out of scope**: The Open Questions raise distinguishing a frozen-at-fork-time arrangement from one tracking the source's current state. This ASN commits to the snapshot reading (V4/V8b state-relativity); the living-fork variant is a separate operation, appropriately deferred.

META: not needed — the ASN defines a state operation (fork) with abstract invariants and remains in specification territory; it is bloated, not drifted.

VERDICT: REVISE
