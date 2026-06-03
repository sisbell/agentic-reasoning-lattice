# Review of ASN-0077

I read the full development — the pointwise `origin` extension (O0), the I-span and V-span lifts, the partition (O1), block uniformity (O2), structural derivation (O3), the permanence/monotonicity family (O5–O8, O11–O14 and their multi-step companions), the operation specification with edge cases, the wp analyses, and the worked example. The proofs are unusually complete: the singleton I-span argument exhausts the `#b < #a`, `=`, `>` cases via T1; O2's M-int bridge discharges the subspace antecedent before invoking S3★/M16a/CL-OWN; O11/O11'/O11★★ correctly partition transitions by the modifies-`M(d)` distinction without a vocabulary-closure appeal; O13/O14 are exhibited with concrete witnesses. Citations are confined to foundation ASNs (0034, 0036, 0047, 0053, 0058, 0098); I found no illegal cross-references. Per the declined-findings notice, I did not re-litigate O0's grounding against ASN-0040/0098.

One genuine completeness gap remains.

## REVISE

### Issue 1: `origins_V` finiteness asserted for the I-span lift but never for the V-span lift
**ASN-0077, "Lifting origin to an I-span" vs. "Lifting origin to a V-span"**: For `origins_I` the ASN states "The result is a finite set of document-level tumblers — finite because `dom(C)` is finite (C-fin, foundation ASN-0047)." The parallel claim for `origins_V` is never made. The V-span lift `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` is the image of `⟦σ⟧ ∩ dom(M(d))` under `origin`, and the operation's output is presented as a set without establishing that it is finite.
**Problem**: Finiteness is a basic well-definedness property of the operation's output. The ASN treats it as a derived consequence worth stating for one lift but silently omits the symmetric consequence for the other. Standard #6 treats unexplored derived consequences as a revision item, and the asymmetry is conspicuous given the otherwise scrupulous I-span/V-span pairing (O6/O7, O8/O12, the wp pair).
**Required**: Add a one-sentence derivation — `origins_V` is finite because `⟦σ⟧ ∩ dom(M(d)) ⊆ dom(M(d))` is finite by S8-fin (ASN-0036), and the image of a finite set under `origin` is finite — paralleling the existing `origins_I` finiteness note.

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from an I-span
The ASN's I-span lift intersects only with `dom(C)`, silently dropping link addresses (acknowledged in the cross-subspace edge case and deferred to Open Question 1). Handling link-address origins from an I-span is new territory, not an error here — the V-span case already reports link origins uniformly via CL-OWN.

### Topic 2: Historical-containment operation over `Σ.R`
The "Not historical containment" exclusion correctly distinguishes current-arrangement origin from the provenance relation `R`. A complementary operation surfacing historical containment, and the invariants coupling the two, belong in a future ASN (Open Question 4), not this one.

VERDICT: REVISE
