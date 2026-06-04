# Review of ASN-0100

## REVISE

### Issue 1: Defensive not-used-lemma inventory
**ASN-0100, §Discovering the Three Effects / Effect Three**: "The foundation's frozen-store frames do not transfer. INSERT extends `dom(C)` ... so any foundation lemma whose proof assumes the content store is frozen ... — notably ASN-0082's I3-C (`Σ'.C = Σ.C`) and the post-state-invariant lemmas built on it (I3-S2, I3-S3, I3-S7, I3-VP, I3-VD, I3-fin) — cannot be imported; the post-state invariants are re-derived directly in §Verifying the Invariants."
**Problem**: This is defensive meta-prose — an inventory of seven foundation lemmas that are *not* used, plus a rationale for not using them. It advances no reasoning the §Verifying the Invariants derivations don't already carry; the precise reader must skip it. This is the use-site-inventory + defensive-justification pattern.
**Required**: Reduce to at most one clause ("post-state invariants are re-derived directly below, since INSERT grows `dom(C)`") or delete; the re-derivations stand on their own.

### Issue 2: INS.M-exhaustive argument stated twice in full
**ASN-0100, §The Operation: Formal Contract** (Exhaustiveness clause) and **§Atomicity** (uniqueness subsection): the Formal Contract gives the complete step-tracking argument ("when K.μ⁻ fires it retains exactly the Left prefix and removes the Right region, and step 3's K.μ⁺ adds exactly the Insertion and Shifted-right positions ... no fourth region"), and §Atomicity re-derives the same region decomposition under "The post-state Σ' is *uniquely determined* ... *Arrangement of `d`*."
**Problem**: Two paragraphs in different sections establish the same Left ∪ Insertion ∪ Shifted-right exhaustiveness by the same canonical-decomposition tracking. This is the "two paragraphs say the same thing" pattern.
**Required**: Establish exhaustiveness once (it belongs in §Atomicity with the uniqueness argument it shares machinery with) and have the Formal Contract cite it rather than re-prove it.

### Issue 3: Implementation-latitude essay in §Atomicity
**ASN-0100, §Atomicity and Canonical Order**: the "commutes" analysis ("K.μ⁻ commutes with every K.α", "K.ρ commutes with K.μ⁺ at the per-state level", "K.ρ firings commute among themselves") plus the long coupling-consistency paragraph ("Each composite's coupling constraints J0, J1★, J1'★ are obligations on *that composite's own* boundary ...").
**Problem**: This prose explains *implementation freedom* in ordering elementary steps — by the ASN's own statement elsewhere, the concurrency-control mechanism "is below this ASN's abstraction level." The system guarantee is "Σ' is uniquely determined; the decomposition is not." The per-pair commutativity walkthrough explains mechanics rather than the guarantee, and degrades the determinacy conclusion under a wall of case analysis.
**Required**: Condense to the guarantee — three forced orderings (the K.α-chain dependency and the two precondition dependencies) determine the boundary obligations; all other interleavings reach the same Σ'. Drop the per-pair commutativity bullets and the coupling-consistency essay.

### Issue 4: Notation duplication — shift vs. OrdinalShiftBase `+`
**ASN-0100, §The Operation's Inputs and throughout**: the ASN simultaneously uses `shift(t, n)` (OrdinalShift, ASN-0034) and the convention `shift(t, 0) := t` lifted from OrdinalShiftBase's `t + 0 = t` (ASN-0058), then in §Per-subspace span decomposition switches to the mapping-block `+ 1` reading ("reading the mapping-block `+ 1` as `shift(·, 1)`").
**Problem**: Two foundation notations for one operation are carried in parallel, forcing repeated bridging clauses ("reading `shift(p, 0) = p` per OrdinalShiftBase" recurs ~8 times). The repeated bridge is itself accreted scaffolding.
**Required**: State the `shift(·, 0) := t` convention once at first use and stop re-justifying it at every occurrence; the per-site "per OrdinalShiftBase (ASN-0058)" parentheticals are noise after the first.

## OUT_OF_SCOPE

### Topic 1: COPY operational mechanics
**ASN-0100, §INSERT vs. COPY**: "COPY (out of scope here) creates V→I mappings to *existing* I-addresses without allocating new content. The original document remains the home of the bytes; attribution stays with the original author. The Vstream effect can be made indistinguishable from an INSERT ..."
**Why out of scope**: COPY mechanics are explicitly OUT OF SCOPE for this ASN. The minimal contrast needed to fix INSERT's identity-by-allocation is "INSERT allocates fresh; COPY references existing." The two paragraphs describing COPY's home/attribution/indistinguishability behavior specify a different operation. Keep the INS.identity corollaries (they are about INSERT); trim the COPY descriptive prose to the one-line contrast.

VERDICT: REVISE
