# Review of ASN-0101

## REVISE

### Issue 1: Empty forward-reference deferral in the operation section
**ASN-0101, "The operation"**: "DEL's admission to ASN-0047's ValidComposite★, and the precise sense in which it interacts with that protocol's coupling constraints, is recorded in D10."

**Problem**: This sentence advances no reasoning at its location — it is a pure pointer telling the reader that content lives elsewhere (D10). The forward-reference accretion pattern: a structural slot used to announce a downstream location rather than to say anything. The preceding sentences already establish DEL is a new atomic transition kind; D10's heading is self-locating.

**Required**: Delete the sentence. D10 stands on its own; the body does not need to pre-announce it.

### Issue 2: Defensive meta-prose about proof posture in D8
**ASN-0101, D8, "The composite-boundary properties P4★, P4a, P7a are not per-state invariants"**: "We therefore do not claim DEL *preserves* these three as per-state invariants, nor do we assume them at the DEL pre-state. What we establish is the strictly weaker and licensed fact that DEL *cannot break* them — it is neutral-to-helpful for each — so it never converts a boundary-satisfying state into a violating one; the affirmative boundary obligation is discharged at the composite level by the composite's non-DEL steps, not by any per-step assumption."

**Problem**: This paragraph explains *why the proof is shaped the way it is* rather than discharging an obligation. The three per-property arguments that follow (P4★ monotone-shrinking, P4a witness-persistence, P7a unchanged-truth-value) are self-contained and already say "DEL cannot break X." The quoted sentence is reviser-drift justification — a defense of the proof's posture that a reader must read past to reach the actual arguments.

**Required**: Replace with a single clause stating the obligation ("DEL is shown neutral-to-helpful for P4★, P4a, P7a below") and let the per-property arguments carry the rest.

### Issue 3: D8 and D10 duplicate the composite-boundary-property argument
**ASN-0101, D8**: the per-property arguments establishing DEL "cannot break" P4★, P4a, P7a.
**ASN-0101, D10, "Composite-boundary obligations"**: "D8 establishes that DEL cannot break any of the three, so no DEL step, terminal or interior, can turn a boundary-satisfying state into a violating one. The composite-level addition is therefore only this: the affirmative establishment of P4★, P4a, P7a at `Σ'` is the work of the composite's non-DEL steps — the same K.α/K.μ⁺/K.ρ machinery by which ASN-0047 discharges these boundary properties for DEL-free composites — which every DEL step preserves."

**Problem**: Two paragraphs in different sections carry the same content (DEL cannot break the three boundary properties; the affirmative discharge belongs to non-DEL steps). D8 already concludes this with full per-property arguments; D10 restates it as prose and re-attributes the affirmative discharge to non-DEL steps. The "see D8 / discharged at composite level" deferral plus restatement is the multiple-paragraphs-deferring-to-the-same-content pattern.

**Required**: State the boundary-property handling once. D10 should cite D8's conclusion in one sentence ("P4★, P4a, P7a hold at `Σ'` by D8") without re-deriving the neutral-to-helpful claim or re-explaining the non-DEL-step division of labor.

### Issue 4: Essay commentary about the examples in D9's wake
**ASN-0101, end of cross-document transclusion example**: "*A note on D9 bullet 2 across the examples.* Each example populates only one subspace of `d`, so D9's second bullet holds vacuously (`V_{S'}(d) = ∅` for the unaffected subspace); its load-bearing content follows immediately from D6's stronger frame `(A v ∈ V_{S'}(d) :: M'(d)(v) = M(d)(v))` by intersecting the projection's defining set with `V_{S'}(d)`."

**Problem**: This is use-site commentary explaining that the worked examples *do not* exercise a particular bullet of D9. It advances neither the operation nor a claim; it is a meta-observation about what the examples cover, the kind of accretion that builds up around a claim across cycles. D9's second bullet is already justified in D9's own proof (via D6); this note adds nothing the claim does not have.

**Required**: Delete the note. If example coverage genuinely needs documenting, it belongs in one line at the head of the examples section, not as a trailing per-bullet aside.

## OUT_OF_SCOPE

### Topic 1: Versioning / historical reconstruction mechanism
**Why out of scope**: The ASN correctly confines itself to DEL's non-destruction guarantees (D2, D5) and explicitly defers the multi-step reconstruction machinery to future work. The "note on recoverability" section stays within scope by asserting only what DEL does not disturb. No revision needed.

VERDICT: REVISE
