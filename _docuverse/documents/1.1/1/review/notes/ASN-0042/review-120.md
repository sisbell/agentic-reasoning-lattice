# Review of ASN-0042

## REVISE

### Issue 1: O17b closes with document-history meta-prose
**ASN-0042, State Axioms (O17b BaptismalRegistryCoupling)**: "This is the one branch-selection fact left primitive here; the membership claim O18 and the freshness conjunct of Freshness-(v) follow from it rather than being asserted independently, so the registry coupling, condition (v), O18, and Freshness-(v) no longer state overlapping facts in parallel."
**Problem**: This sentence advances no reasoning about what O17b *says*. It narrates the note's own consolidation history ("no longer state overlapping facts in parallel") and inventories which downstream claims derive from the primitive — exactly the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern. A reader following the coupling claim must skip it.
**Required**: Delete the sentence. The derivations (O18, Freshness-(v)) already cite O17b at their own sites; the primitive does not need to announce its consumers.

### Issue 2: O7(c) proof and Formal Contract carry the same self-referential classification note
**ASN-0042, Delegation (O7, postcondition (c) proof)**: "Conditions (iii) and (v) are therefore the binding constraints on the recursive delegation; this classification is derived here once, and the O7 header and Formal Contract reference it rather than re-enumerating."
**ASN-0042, O7 Formal Contract (c)**: "(the proof of (c) classifies, once, which conditions bind and which auto-discharge)."
**Problem**: Two slots point at each other to justify where the classification lives ("derived here once, and the O7 header and Formal Contract reference it" / "classifies, once"). This is document-organization meta-prose and the "multiple paragraphs defer to the same location" pattern. The substantive classification (which conditions bind) is the content; the bookkeeping about *not re-enumerating* is noise.
**Required**: State which conditions bind once, plainly, and drop both "derived here once / reference it rather than re-enumerating" clauses and the Formal Contract parenthetical.

### Issue 3: RegistryReachability ends with a use-site inventory
**ASN-0042, State Axioms (RegistryReachability)**: "The consequence is the one this note repeatedly invokes: on any reachable Σ.B ... Wherever `hwm`, `next`, B1, or B6 is used below, it is this invariant that discharges the precondition."
**Problem**: "the one this note repeatedly invokes" and "Wherever ... is used below" enumerate downstream consumers rather than advancing the invariant. The discharge belongs at each use site (and is in fact restated there, e.g. O10's construction "by RegistryReachability"). The closing paragraph duplicates that.
**Required**: Keep the mathematical consequence (next/hwm well-defined, B1/B6 available on reachable registries) as a one-line corollary; remove the "repeatedly invokes / Wherever ... below" framing.

### Issue 4: Freshness-(v) forward-tags O17b that is itself a later axiom
**ASN-0042, Freshness-(v) (derived)**: "the introducing transition takes O17b's baptism branch (its principal-introduction primitive, stated below)."
**Problem**: Freshness-(v) sits in the delegation-predicate block but depends on O17b's principal-introduction primitive defined further down, and O18 (also below) re-derives the same freshness conjunct from the same primitive. The "stated below" tag plus the parallel O18 derivation is the forward-pointer accretion the classifier targets — the freshness fact is asserted in Freshness-(v), re-asserted as O17b's sharpening, and re-derived in O18.
**Required**: Pick one site for the freshness conjunct (O18 is the natural home, being explicitly derived) and have Freshness-(v) cite it without the "stated below" forward tag, rather than threading the primitive through three slots.

## OUT_OF_SCOPE

### Topic 1: Implementation conformance of `tumbleraccounteq` to ω-exclusivity
The node operator's account-level prefix match (`isthisusersdocument`) grants the parent access to delegated sub-account content, which diverges from O8's effective-ownership exclusivity. The ASN already reconciles this by locating exclusivity in ω (longest match) rather than in the containment predicate, so it is not an internal-consistency flaw of this abstract spec; conformance enforcement is access-control territory, explicitly out of scope.

META: The ASN remains squarely on system-guarantee territory — state (Π, Σ.B, pfx), operations (delegation, fork), and invariants (ω well-definedness, refinement, node-locality); the findings are accreted meta-prose, not drift.

VERDICT: REVISE
