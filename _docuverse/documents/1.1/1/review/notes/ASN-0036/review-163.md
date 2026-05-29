# Review of ASN-0036

The mathematics here is sound. I checked the load-bearing proofs — S8 (singleton partition), the within-subspace incompatibility lemma, D-CTG-depth, and D-SEQ — case by case, including the boundaries (`m = 2` vs `m ≥ 3`, empty `dom(M(d))`, across- vs within-subspace divergence). The case analysis is complete and the foundation citations discharge what they claim. The worked example exercises S0/S3/S5/S7/S8/D-SEQ against a concrete transclusion+delete lifecycle. The E! claim in S8(a) follows directly from the lemma ("only `v` lies in `I_v`" ⟹ any `p ∈ I_v` is `v` ⟹ `p` is in exactly its own interval), so that is genuinely closed.

The findings below are bloat/redundancy, consistent with this note's `review-mode.anti-bloat` classifier. They do not impugn the proofs, but they are noise the precise reader must work around.

## REVISE

### Issue 1: "The document as arrangement" is essay content in a structural slot
**ASN-0036, §"The document as arrangement"**: "A document is not its content — it is its arrangement of content… 'an evolving ongoing braid.' The braid is the arrangement; the strands are the Istream content."
**Problem**: This is a top-level section that introduces no property, states no invariant, and advances no step of any proof. It is metaphor restating the two-component model already established in §"Two components of state." Pure essay occupying a structural slot.
**Required**: Delete the section, or fold its one operative sentence into the existing two-component motivation if it is doing any work there.

### Issue 2: S5 *Depends* duplicates the proof's verification paragraph
**ASN-0036, S5 Formal Contract / proof**: *Depends* reads "S0 — preserved vacuously by the single-state construction; S1 — preserved vacuously; S2 — required to establish that the constructed `M(d)` is a well-defined function; S3 — established by construction…"
**Problem**: This is a use-site inventory restating the proof body almost verbatim ("S0 and S1 quantify over transitions… hold vacuously. S2… is a function. S3…"). The dependency slot should name what S5 rests on, not re-narrate the verification.
**Required**: Reduce the *Depends* entries to bare premise names (S0, S1, S2, S3, T0, T3); drop the per-entry re-justification that the proof already carries.

### Issue 3: S7 proof re-derives S7d's own postcondition
**ASN-0036, S7 proof, "Uniqueness across documents"**: "By S7d… distinct documents arise from distinct allocation events… GlobalUniqueness then guarantees that the resulting document-level tumblers are distinct."
**Problem**: S7d's *Postconditions* already state "By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers." The S7 proof re-establishes the identical conclusion from the identical premises — two paragraphs saying the same thing.
**Required**: Have the S7 proof cite S7d's postcondition directly ("distinct documents have distinct tumblers, by S7d") rather than reconstructing the GlobalUniqueness step.

## OUT_OF_SCOPE

### Topic 1: Editing operations preserving D-CTG / D-MIN / S2
**Why out of scope**: The ASN correctly scopes out INSERT/DELETE/COPY/REARRANGE frame and postconditions and already records the preservation obligation as an Open Question. The state model and its invariants are the right boundary for this note; operation discharge belongs in a later ASN.

### Topic 2: Computability of the sharing inverse and the orphaned/reachable distinction as queryable state
**Why out of scope**: S5 establishes the *existence* of unbounded multiplicity; the cost bound for inverting "which documents reference `a`" and whether reachability is maintained as queryable state are new territory, already listed under Open Questions.

VERDICT: REVISE
