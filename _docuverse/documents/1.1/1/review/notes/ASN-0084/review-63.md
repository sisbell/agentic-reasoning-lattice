# Review of ASN-0084

## REVISE

### Issue 1: R-SP lemma duplicates the "Invariant preservation" audit; the wp claim is trivial
**ASN-0084, R-SP (RearrangeSufficientPrecondition)**: The statement re-enumerates every ASN-0036 invariant ("S0, S1, S2, S3, S4, S5, S7 ..., S7a, S7b, S7d, D-CTG, ... S8") and the proof is one sentence: *"Every clause of Q is discharged by the *Invariant preservation* paragraph above — every invariant except S8 directly, and post-state S8 by that paragraph's *Foundation-S8 transport* step."*
**Problem**: The full invariant audit is already performed in the "Invariant preservation" paragraph. R-SP restates the same conclusion in wp clothing and a use-site inventory of every invariant, then back-references the audit. This is two passages asserting the same result; the wp(REARRANGE_K, Q) framing computes nothing new — it resolves "trivially true" by pointing upward. The review standard against trivial wp analysis applies directly.
**Required**: Either delete R-SP and let the "Invariant preservation" paragraph stand as the sufficiency statement, or make R-SP carry genuine wp content (e.g. demonstrate a *non-trivial* clause where R-PRE is load-bearing — the R-PRE(iv) bound on ord(c_{n−1}) ≤ N+1 is the obvious candidate, and is currently deferred to an Open Question).

### Issue 2: Four sections defer to the same "Foundation-S8 transport" step
**ASN-0084, Invariant preservation / Canonical decomposition / R-BLK / R-SP**: "Foundation-S8 transport" is established in the Invariant-preservation paragraph and then re-cited in "Canonical decomposition" ("its application to the post-state M'(d) is the *Foundation-S8 transport* established above"), in R-BLK ("The S8-unique maximal partition of M'(d) exists by the *Foundation-S8 transport* established above"), and again in R-SP ("post-state S8 via *Foundation-S8 transport*").
**Problem**: This is the flagged accretion pattern — multiple paragraphs in different sections deferring to one downstream/upstream location. The reader meets the same pointer four times.
**Required**: State the transport once where post-state S8 is genuinely consumed (R-BLK), and drop the redundant re-citations.

### Issue 3: ℕ-addition cancellation is derived through shift lemmas where the NAT axioms suffice
**ASN-0084, "Identification of singleton tumblers with natural numbers"**: *"Cancellation of ℕ-addition, where used below, is likewise discharged through the identification: `a + c = b + c ⟹ a = b` by TS2 (ShiftInjectivity...) and `c + a = c + b ⟹ a = b` by TS5 (ShiftAmountMonotonicity...) ... supplemented by TS4 (ShiftStrictIncrease...) for the zero case..."*
**Problem**: Cancellation of ℕ addition is elementary from the foundation's own NAT axioms (NAT-order trichotomy + NAT-addcompat monotonicity). Routing it through three shift lemmas (TS2/TS4/TS5) on the tumbler image is a defensive detour that obscures a standard fact — over-justification in a definition slot.
**Required**: Replace the shift-lemma derivation with a one-line appeal to NAT-order/NAT-addcompat, or simply state ℕ cancellation as standard and cite the NAT axioms.

### Issue 4: Forward-reference framing around "Width positivity"
**ASN-0084, RegionPartition / R-PRE**: "Their identification with cut-ordinal differences, and their positivity, depend on R-PRE(iv) and are derived once in the *Width positivity* consequence of R-PRE below"; and in R-PRE: region non-degeneracy "is *derived* ... rather than imposed as a separate precondition; the derivation is recorded as the 'Width positivity' consequence below."
**Problem**: Two forward pointers to the same "Width positivity" consequence, each carrying justificatory meta-prose ("derived once," "rather than imposed as a separate precondition") explaining the document's structure rather than advancing the argument.
**Required**: Keep a single bare forward reference (or none) and let the Width-positivity consequence speak for itself; drop the "derived once / rather than imposed" framing.

## OUT_OF_SCOPE

### Topic 1: Necessity/minimality of R-PRE(iv)
The last Open Question ("what does R-PRE(iv) guarantee beyond what D-SEQ already supplies") is the right place for the wp-minimality analysis; R-PRE(iv) is in fact non-redundant (it bounds ord(c_{n−1}) ≤ N+1), but a full necessity treatment belongs in a future revision rather than as a correctness defect here.

### Topic 2: k-cut generalization and composition of rearrangements
The Open Questions on k > 4 cuts and composition of multiple REARRANGE operations are genuinely new territory, not gaps in this ASN.

VERDICT: REVISE
