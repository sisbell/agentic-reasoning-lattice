# Review of ASN-0071

## REVISE

### Issue 1: Depth-wise/breadth-wise discrimination stated three times, then deferred to the worked scenario
**ASN-0071, *The query***: three consecutive paragraphs — "The third relaxation — dropping ContentReference's `#u = m`...", "A coarse anchor names its whole subtree...", and "The `actionPoint(ℓ) = #u` precondition enforces exactly this discrimination..." — each restate the same permitted-depth-descent vs. forbidden-sibling-sweep point, closing with "The worked scenario below exhibits both against a live arrangement."
**Problem**: This is forward-reference accretion. The abstract discrimination is argued once in PC, restated three ways here, then re-exhibited concretely under "Interior action point, rejected against an arrangement." A reader following the `actionPoint(ℓ) = #u` precondition must skip past the motivational triplet to reach the claim.
**Required**: Collapse to a single sentence stating what `actionPoint(ℓ) = #u` confines (`⟦σ⟧` varies only at component `#u` and deeper), and let the worked scenario carry the demonstration. Drop the "the worked scenario below exhibits both" deferral.

### Issue 2: The extent/occurrence-recovery recipe is duplicated verbatim across two sections
**ASN-0071, *Partial overlap suffices*** and ***Set semantics***: the former says "to recover an extent measure, the requester must compute `|ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)|` for each returned `d` separately"; the latter says "To recover occurrence counts, the requester must separately compute the cardinality of `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ)` for each returned `d`."
**Problem**: Two paragraphs in the same document saying the same thing in different words.
**Required**: State the recovery recipe once; remove the duplicate.

### Issue 3: Derivation-provenance meta-prose around the ContentReference relaxation
**ASN-0071, *The query***: "ASN-0058's C0a states this conclusion, but only for a well-formed ContentReference; the vspec relaxation discards exactly that well-formedness ... so we cannot borrow C0a and must argue directly." Likewise "C0 establishes only the equality `actionPoint(ℓ) = m`; the `≥ 2` half is the depth bound, not a consequence of C0. We lift both consequences into an explicit precondition..."
**Problem**: This is prose explaining *why* a local proof exists relative to a foundation, rather than advancing the proof. The PC argument that follows stands on its own; the "why we can't cite C0a" framing is the kind of provenance bookkeeping the anti-bloat pass targets.
**Required**: State the vspec preconditions and prove PC directly. One sentence noting PC is the relaxed analogue of C0a suffices; drop the "cannot borrow / must argue directly / lift both consequences" justification chain.

### Issue 4: The depth-1 anchor exclusion is re-justified at each use site
**ASN-0071, *Resolution*** ("The `actionPoint(ℓ) ≥ 2` precondition is what licenses this position-1 step: the depth-1 anchor it excludes (exhibited in *The query*)...") and again in ***The operation*** ("the depth-1 anchor it excludes (exhibited in *The query*)").
**Problem**: The `u = [1]`, `ℓ = [2]` example is fully worked in *The query*; the two later references re-explain its purpose rather than simply invoking `actionPoint(ℓ) ≥ 2`. Multiple sections deferring back to the same exhibit.
**Required**: Invoke the precondition by name at the use sites without re-narrating what it excludes.

## OUT_OF_SCOPE

### Topic 1: Invariant connecting `find` across an arrangement-contracting transition
**Why out of scope**: The ASN correctly defers this to the Open Questions (the K.μ⁻ before/after relationship). It is genuinely new territory — a transition-relational property — not a gap in this state-function specification.

### Topic 2: Reconciliation of `find` currency with provenance `R` history
**Why out of scope**: The *Permanence and currency reconciled* section frames it as a separate `R`-based query mechanism; the formal relationship belongs in a future ASN, as the Open Questions note.

VERDICT: REVISE
