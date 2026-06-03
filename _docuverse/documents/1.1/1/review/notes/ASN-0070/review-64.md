# Review of ASN-0070

I worked through the F-canonical proof (Steps 1–5), the F-subspace correspondence, the inverse-image definition, the contiguity claim, and all six worked configurations. The core mathematics is sound: the inverse-image relation is well-defined, the per-subspace canonical form's existence and uniqueness arguments are complete (including the acyclicity/partition argument in Step 2 and the right/left-closure arguments in Step 4), and the worked examples correctly exercise F-multi, F-slot, F-contig, F-multidoc, and the vacuous-subspace convention. My findings are narrow.

## REVISE

### Issue 1: Concurrency open question presupposes a model state the foundation excludes
**ASN-0070, Open Questions**: "What concurrency semantics must `follow` guarantee when the queried document is being modified by another transition concurrently?"
**Problem**: SequentialTransitionAxiom (ASN-0047) fixes that "Transitions Σ → Σ' are atomic, uninterruptible, and totally ordered." Within this ASN's model there is no concurrent transition — a document cannot be "modified by another transition concurrently." The question imagines a case the foundation already excludes. As written it implies `follow` carries a concurrency obligation, but the operation is a pure query (Frame `Σ' = Σ`) evaluated against a single serialized state; concurrency would only arise in the replication/inter-server (BEBE) regime, which is out of scope for this ASN.
**Required**: Remove the question, or reframe it explicitly as deferring to a future replication/multi-server model and drop the framing that `follow` itself must "guarantee" concurrency semantics — otherwise it reads as an obligation on an operation whose model is sequential by axiom.

### Issue 2: Forward-reference accretion in the worked-example verification bullets
**ASN-0070, A Worked Example (Configuration 1, F-multi bullet)**: "Not exercised in this example ...; exercised by the cross-subspace straddle configuration below, whose content branch resolves `a₀` to the two V-positions `[1, 1]` and `[1, 6]`."
**Problem**: The bullet defers to a downstream configuration and pre-states that configuration's result inside Configuration 1's verification. The forward pointer and the spoiled result do not advance Configuration 1's check; they are the "defer to the same downstream location" accretion pattern. The reader must carry a later configuration's content to read an earlier one.
**Required**: Trim to "not exercised here" (the property is fully exercised at its own configuration, where the verification belongs). Apply the same trim wherever a verification bullet pre-states a later configuration's outcome.

## OUT_OF_SCOPE

### Topic 1: Cross-document resolution coherence under shared homes
**ASN-0070, Open Questions (first question)** — the relationship that must hold between `follow(ℓ, d, i)` and `follow(ℓ, d', i)` when `d` and `d'` transclude overlapping homes is genuinely new territory (cross-document resolution coherence), not a defect in this ASN. F-multidoc correctly establishes only that no document is privileged; comparing resolutions across documents is future work.

VERDICT: REVISE
