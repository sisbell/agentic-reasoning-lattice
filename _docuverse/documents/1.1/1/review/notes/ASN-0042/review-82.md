# Review of ASN-0042

This is a mature ownership model and the proofs are, on the whole, rigorous and complete — coverage, exclusivity, refinement, irrevocability, and the fork construction are all carried with explicit case analysis and concrete witnesses. The note carries the `review-mode.anti-bloat` classifier, and that is where the work remains: forward-reference accretion, duplicated framing, and meta-prose around axioms have built up across cycles. My findings are concentrated there, with one over-elaboration-of-a-vacuous-case finding.

## REVISE

### Issue 1: Duplicated "owns is pair-decidable / ω needs the registry" framing

This same distinction is stated in at least three places in different words:

- Intro: "Authorization decisions reduce to prefix comparison; identifying *which* principal authorizes requires the registry."
- O1 section: "The definition governs the two-place predicate `owns(π, a)`, not the one-place effective-owner function `ω(a)`. The latter ranges over the principal registry to select the longest matching prefix, so its evaluation requires `(a, Π_Σ, pfx)`…"
- Exclusivity Invariant: "Gregory's `tumbleraccounteq` decides *containment*… The predicate enumerates no registry and computes no longest match, so it cannot by itself single out one owner."

**Problem**: Two/three paragraphs in the same document saying the same thing — an anti-bloat pattern. The reader re-derives the same point at each site.

**Required**: State it once (the Exclusivity Invariant site is the load-bearing one, since it justifies longest-match). Remove the O1-section restatement and compress the intro line.

### Issue 2: Premature forward reference to ω inside O1

**ASN-0042, O1 (PrefixDetermination)**: "The latter ranges over the principal registry to select the longest matching prefix, so its evaluation requires `(a, Π_Σ, pfx)` — the registry is consulted to enumerate candidates. Deciding `owns(π, a)` requires only the tumbler pair `(pfx(π), a)`…"

**Problem**: `ω` is not defined until the *Exclusivity Invariant* section (≈six sections later). O1 explains ω's evaluation requirements before ω exists. This is forward-reference accretion — the explanation belongs where ω is introduced.

**Required**: O1 should establish only that `owns(π, a)` is decidable from `(pfx(π), a)`. Drop the ω contrast here; let it land at ω's definition.

### Issue 3: Defensive use-site inventory of the reachability premise

**ASN-0042, O2 Formal Contract, Preconditions**: "Reachability is inherited from O4 (DomainCoverage), which Step 1 of the proof invokes for non-emptiness of the covering set `C(a)`. Steps 2–4 (chain ordering, finiteness, uniqueness) are state-local and do not introduce additional reachability obligations beyond O4's."

**Problem**: A use-site inventory enumerating which proof steps do/don't consume a premise. This is defensive justification, not argument advancement — the kind of meta-prose the reader must work around.

**Required**: "Reachability is inherited from O4 (invoked in Step 1)." The per-step accounting adds nothing.

### Issue 4: Repeated deferral and ordering prose around the delegation predicate

Several sites defer to O15 or justify the placement of the `delegated` definition:

- "*delegation predicate* `delegated_Σ(π, π')` (formally defined immediately following the inline statement of the conditions)"
- Delegation section: "The content of conditions (ii) (authorization), (vi) (top-down order), and (vii) (freshness) is stated with O15 above."
- O7(c) and OwnershipDomainPermanence both re-narrate conditions (ii)/(vi)/(vii) by deferring upward.

**Problem**: Multiple paragraphs deferring to the same location, plus prose justifying definition ordering — both flagged anti-bloat patterns.

**Required**: Define `delegated` once with its seven conditions; have downstream sites cite the condition number without restating "stated with O15 above" or re-describing the conditions in prose.

### Issue 5: Protocol-rationale prose around axioms (O13, O17)

- O13: "The prefix is a tumbler, and the tumbler algebra provides no operation that mutates an existing tumbler in place. Since addresses are permanent (T8)… altering it would require rewriting every address in the domain — an operation the system does not support."
- O17: "This is ASN-0040's B10… We cite B10 directly rather than reaxiomatize: the foundation produces no addresses outside `Σ.B` satisfying T4."

**Problem**: Both explain *why the axiom/import is needed* rather than *what it says* — the "Why the axiom is needed" sub-prose pattern. O17's "we cite directly rather than reaxiomatize" is pure protocol rationale.

**Required**: O13 states immutability; the design grounding can stay as one Nelson/Gregory clause but drop the "would require rewriting every address" justification. O17 should just import B10; delete the reaxiomatize-vs-cite commentary.

### Issue 6: Over-elaboration of the node-level O10 case the design excludes

**ASN-0042, O10 / Worked Example**: The note devotes substantial prose and a full worked sub-case to a *node-level* principal "requir[ing] modification of content at address `a`," repeatedly caveating that the single baptism yields only a namespace slot ("content placement under a node-level principal requires a second baptism `Bop(a', 2)`…").

**Problem**: The ASN's own grounding states "Nelson confines the node operator's role to account allocation" — a node operator requiring content modification is contrary to the specified design, so this branch is essentially vacuous. The multi-paragraph treatment (Form A/B split caveats, second-baptism descent, "structural significance differs across the two cases") is engineering for a scenario the model says does not arise.

**Required**: Keep O10's general statement and the account-level witness (the case Gregory's `docreatenewversion` actually exercises). Collapse the node-level treatment to one sentence noting the fork yields a namespace slot and content placement is a further organizational baptism. Remove the duplicated "the fork *as ownership boundary* is the structural act; content placement is the organizational continuation" sentences (stated in both the O10 body and the Worked Example).

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions correctly record transfer as unresolved; the divergence of provenance (O6) from effective ownership (O2) under a hypothetical transfer regime is future territory, not a defect here.

### Topic 2: Identity binding / authentication
The "Principal Identity and the Trust Boundary" section properly places `session.account = pfx(π)` outside O1–O10. No revision needed; this is a correct scoping decision, not a gap.

META: not applicable — the ASN stays squarely in state/operations/invariants territory (predicate, registry, transition discipline, longest-match resolution); it has not drifted into implementation mechanics.

VERDICT: REVISE
