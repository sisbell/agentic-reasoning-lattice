# Review of ASN-0093

This note carries the `review-mode.anti-bloat` classifier. The core mathematics — the K.σ/K.α/K.λ emission rules, the C1c/L1c chain exhibitions, the cross-document disjointness argument, and the nine-step worked example — checks out: I verified the anchor constructions (`b_C(d) = inc(d,2)`, `b_L(d) = inc(b_C(d),0)`), the chain step admissibility, and the freshness closures, and they hold. The findings below are accumulated meta-prose, forward-reference/consumer enumeration, and notational duplication.

## REVISE

### Issue 1: Non-circularity justification embedded in a proof
**ASN-0093, FirstEmissionFreshness lemma (preamble)**: "Throughout this proof, the new key's subspace identifier is read from FirstEmission's structural form, not from L0 at `Σ'`, which would be circular under the simultaneous induction (L0 at `Σ'` itself depends on FirstEmissionFreshness)."
**Problem**: This is a defensive justification about proof ordering — it explains why the proof does *not* take a circular route rather than advancing the argument. It is exactly the "prose justifies document ordering / non-circular by Y argument" pattern. The proof already reads the identifier from FirstEmission's form at each use site; the disclaimer adds nothing a precise reader needs.
**Required**: Delete the preamble sentence. The per-step citations of FirstEmission's structural form already carry the (non-circular) reasoning at point of use.

### Issue 2: Proof-hygiene meta-prose in the induction framing
**ASN-0093, Simultaneous-induction framing**: "The inductive hypothesis at each step is the *conjunction* of every transition-indexed property at the current state `Σ`; the inductive step exhibits each holding at `Σ'` using the conjoined IH. No inductive step uses a conclusion derived in the same step."
**Problem**: "No inductive step uses a conclusion derived in the same step" is a statement of generic proof hygiene, not a claim about this system. Combined with the parenthetical "(once the chain is fixed at `d`'s K.σ-time activation, the conclusion holds once-and-for-all for every chain index `n ≥ 1`)", these are reassurances about the proof method rather than steps of it.
**Required**: Strip the hygiene sentence. Keep only the substantive two-group split (chain-indexed = no induction; transition-indexed = simultaneous induction), which is genuine organization.

### Issue 3: Properties Introduced table duplicates the discharge matrix
**ASN-0093, Properties Introduced**: e.g. the C2 Source cell — "Substrate, content-side analog of L1a; established at K.α (precondition pins `origin(a) = d ∧ d ∈ dom(M)` at the new key); preserved at K.σ/K.λ by frame on `C` and M1's monotonicity of `dom(M)`"; similarly the SubspaceConventionAxiom cell "Underwrites L14 derivation and the L1c chain exhibition."
**Problem**: The Source column restates, verbatim in substance, the per-(invariant, transition) discharge already given in the discharge matrix, and the axiom rows enumerate downstream consumers. A summary index should point, not re-prove. This is duplicated content plus a downstream-consumer inventory.
**Required**: Reduce each Source cell to a one-line origin tag (e.g., "Substrate; analog of L1a") and let the discharge matrix carry the per-transition reasoning. Drop the "Underwrites X and Y" consumer lists from the axiom rows.

### Issue 4: Dual-form provision with consumer enumeration
**ASN-0093, Cross-document disjointness chain lemma**: "Equivalently, the anchors are prefix-incomparable, `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` … so T10 (PartitionIndependence, ASN-0034) closes extension-disjointness directly; consumers may cite either the B7 form or the T10 form."
**Problem**: The lemma states the same disjointness fact twice (B7 stream-form and T10 anchor-form) and then enumerates which form downstream consumers should cite. The "consumers may cite either form" clause is a downstream-consumer inventory; the second derivation is restatement of an already-cited foundation result.
**Required**: State the lemma in the single form the proofs actually consume (the anchor-incomparability/T10 form is what FirstEmissionFreshness and K.α/K.λ cross-document freshness use), cite B7 once as the underlying result, and drop the "consumers may cite either" sentence.

### Issue 5: `ValidAddress` reinvents `T4-valid`
**ASN-0093, M0 / Definitional identification**: "Throughout this substrate, `ValidAddress(d) ≡ d satisfies T4 (HierarchicalParsing, ASN-0034)` — the two terms are interchangeable."
**Problem**: ASN-0043 (foundation) already uses `T4-valid(a)`; ASN-0034 defines T4. Introducing a second name and then using both `ValidAddress` and "T4-valid" interchangeably across the note is notational duplication for a foundation concept — the precise reader must hold two labels for one predicate.
**Required**: Use the foundation term `T4-valid` throughout and remove the `ValidAddress` alias and its definitional-identification paragraph.

### Issue 6: Worked-example summary inventory
**ASN-0093, Worked example (closing paragraph)**: "The extended example confirms invariants M0, M1, C0–C2, C-fin, L0–L14, L-fin at each successor state across three documents, exercises both first-emit and subsequent-emit branches of K.α (Steps 2, 4, 6) and K.λ (Steps 3, 7, 8), verifies the Cross-document disjointness lemma … for both a prefix-comparable document pair (Step 5 …) and a prefix-incomparable pair (Step 9 …) …"
**Problem**: A use-site inventory cataloguing which step exercised which branch. The example body already verifies each invariant inline; the closing roll-call does not advance reasoning.
**Required**: Delete the inventory paragraph, or compress to a single sentence stating that the example exercises both emission branches and both cross-document cases.

### Issue 7: SequentialTransitionAxiom stated but never invoked
**ASN-0093, SequentialTransitionAxiom; ChainMembershipForOrigin proof**: the contiguous-prefix invariant is "proved by induction over transition sequences from `Σ₀`," which presupposes a total order on transitions, yet no proof step cites SequentialTransitionAxiom.
**Problem**: The axiom is the premise that makes "induction over transition sequences" well-defined (no concurrent emission opening a gap in a chain), but it is never explicitly consumed. An axiom that is load-bearing only implicitly reads as framing-only — the reader cannot tell whether it is required or decorative.
**Required**: Cite SequentialTransitionAxiom at the point where ChainMembershipForOrigin's induction relies on a linear transition sequence, or state explicitly that it scopes the whole induction.

## OUT_OF_SCOPE

None — the note correctly confines arrangement mutation, entity stratification, provenance, coupling, and link withdrawal to the Deferred/Open-Questions sections rather than asserting claims about them.

VERDICT: REVISE
