# Review of ASN-0098

## REVISE

### Issue 1: LP2 proof restates slot semantics it does not use
**ASN-0098, LP2 (SlotInvariance)**: "In particular, the slot-position assignment fixed at link creation — from-set at slot 1, to-set at slot 2, type-set at slot 3, and any additional slots — is structurally preserved."
**Problem**: LP2's proof is complete at "equal sequences have equal entries at every position." The from/to/type slot naming plays no role in that argument — it is recapitulated L3/StandardTriple content sitting in a proof slot. A precise reader must verify it adds nothing, then skip it.
**Required**: Delete the sentence. The slot equation `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` already says everything LP2 establishes.

### Issue 2: "Discovery Independence of Origin" builds a three-document inventory the section then discards in one line
**ASN-0098, Discovery Independence of Origin**: enumerates home document, origin document, and navigating document, then concludes "By inspection, LP12's right-hand side references only `coverage(Σ.L(a).eᵢ)` and `ran(Σ.M(d))`, so discoverability ... is independent of `home(a)` and of the origin documents."
**Problem**: The analytical content is the single inspection sentence — a trivial corollary of the already-proven LP12. The preceding three-document role enumeration imagines distinctions (home vs. origin vs. navigating) that LP12's carrier excludes by construction, exactly the reviewer-drift pattern: prose that raises cases the claim already rules out, only to dismiss them. The "three documents may be the same, all different, or any combination" elaboration advances no reasoning.
**Required**: Collapse to the one-line consequence of LP12. The provenance-indifference fact stands on LP12's right-hand side alone; the role inventory is setup essay.

### Issue 3: The "tight construction is immune to fresh allocation" takeaway is stated three times
**ASN-0098, Achievability paragraph / worked-example "Non-tight contrast" closing / LP19 closing paragraph**: 
- Achievability: "...discharging tightness."
- Worked example: "...the architecture admits both, but only the first is immune to absorbing fresh allocations."
- LP19 closing: "...the canonical construction ... produces tight endsets, and tight endsets are immune to absorbing addresses produced by subsequent K.α or K.λ."
**Problem**: The same architectural message — canonical construction yields tight endsets that cannot absorb fresh allocations — is restated in three different sections in different words. This is the "two paragraphs say the same thing" pattern compounded to three. LP19a + LP19 already *prove* the immunity; the worked-example and LP19 closings then re-assert it editorially.
**Required**: State the takeaway once (the LP19 closing is the natural home, immediately after the proof) and delete the redundant assertions in the Achievability paragraph and the worked-example contrast.

### Issue 4: Recurring Nelson interpretive closers are essay content in proof slots
**ASN-0098, LP10 / LP16 / LP18 / transclusion paragraph**: "This is Nelson's 'if anything is left at each end' condition made precise." / "the architectural mechanism behind Nelson's 'a link to one version is a link to all versions' claim" / "This is the formal expression of Nelson's 'reaching back through to a superseding version' mechanism."
**Problem**: Each proof terminates with an interpretive sentence mapping the result back to Nelson's vocabulary. Individually defensible as grounding; in aggregate they are essay content accreted after the formal slots, and a reader following the displacement arithmetic must repeatedly skip past them. They advance no reasoning the claims do not already carry.
**Required**: Consolidate the Nelson correspondence into a single short discussion (or the existing "Discoverability and Survival" framing), and remove the per-claim closers.

### Issue 5: Degenerate-configuration paragraph carries defensive exhaustiveness framing
**ASN-0098, The Projection Operation**: "Three degenerate configurations follow directly from the definition and require no separate treatment in subsequent claims."
**Problem**: The three facts themselves (empty endset, empty arrangement, empty from/to endsets project to ∅) are concrete and worth stating. The framing clause "require no separate treatment in subsequent claims" is a defensive exhaustiveness assertion — it pre-empts a reviewer rather than advancing the argument.
**Required**: Keep the three concrete facts; drop the "require no separate treatment" framing.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive invariants
**Why out of scope**: The first Open Question (given a V-position, return links whose projections contain it) defines a new operation not present in the working vocabulary; it belongs in a future ASN, correctly listed under Open Questions rather than claimed here.

### Topic 2: V-order / I-order reflection within a projection
**Why out of scope**: The ordering-preservation question (does projected V-order reflect I-order under K.μ~) is genuinely new territory — this ASN deliberately treats projection as a set, not a sequence, and the question is parked in Open Questions appropriately.

VERDICT: REVISE
