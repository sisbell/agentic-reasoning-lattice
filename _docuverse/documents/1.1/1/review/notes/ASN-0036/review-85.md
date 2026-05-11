# Review of ASN-0036

## REVISE

### Issue 1: Worked example violates the ASN's own notation reservation for `+`

**ASN-0036, Worked example § "After creating d₁ with 'hello'"**: 

> "Verify: `M(d₁)(1.1 + k) = 1.0.1.0.1.0.1.1 + k` for `k = 0, 1, 2, 3, 4`."

**Problem**: Earlier in the "Span decomposition" section, the ASN explicitly states: "We reserve the symbol `+` for NAT addition on components and indices throughout this ASN; tumbler ordinal displacement is always written as `shift(v, k)` (equivalently `v ⊕ δ(k, m)` per ASN-0034) — never as `v + k`." The worked example then uses `1.1 + k` and `1.0.1.0.1.0.1.1 + k` — `+` on tumblers — directly contradicting the reservation. A future reader who applies the reservation strictly cannot disambiguate whether `1.1 + 2` is NAT addition (yielding `1.3`, which happens to be the right tumbler by accident) or genuine displacement (formally `shift(1.1, 2) = 1 ⊕ δ(2, 2) = [1, 3]`). The text doesn't say which.

**Required**: Rewrite as `M(d₁)(shift(1.1, k)) = shift(1.0.1.0.1.0.1.1, k)` for `k = 0, 1, 2, 3, 4`. This is the only `+`-on-tumbler instance I found; the Σ₂ and Σ₃ S8 checks already use prose rather than the offending formula, so the fix is local.

### Issue 2: S7c's load-bearing role in S8 is overstated

**ASN-0036, S7c discussion**: "S7c, stated here for architectural completeness, is load-bearing for S8's correspondence run definition for I-address shifts below — specifically the well-definedness argument that the action point of `δ(k, #a)` falls strictly after the subspace identifier — not for S7 itself."

**Problem**: S8's existence proof constructs *singleton* runs (`nⱼ = 1`), so conjunct (b) is checked only at `k = 0`, where `shift(aⱼ, 0) = aⱼ` is convention-identity and no displacement computation occurs. S7c's `#E(a) ≥ 2` bound is only consumed by the auxiliary lemma's `k ≥ 1` case, which the existence proof's construction never invokes. The lemma explicitly notes this: "For k ≥ 1 — which is vacuous for the singleton decomposition…". So S7c is load-bearing for the postcondition's *subspace-preservation* clause when that clause is applied to non-singleton runs (as in the Σ₂ worked example with `n = 3` and `n = 2`) — not for S8's existence claim itself.

**Required**: Replace "load-bearing for S8's correspondence run definition" with something like "load-bearing for the subspace-preservation clause of S8's postcondition when applied to non-singleton correspondence runs; S8's existence proof via singleton runs does not consume it, but operational refinements that coarsen the decomposition do."

### Issue 3: Awkward prose in the D-CTG-depth intermediate construction

**ASN-0036, D-CTG-depth proof**: "wᵢ = 1 for j + 2 ≤ i ≤ m (if any such positions exist; since j ≤ m − 1, at least the m-th component exists at position j + 1 or beyond)."

**Problem**: The parenthetical "at least the m-th component exists at position j + 1 or beyond" is confused: the m-th component is *at* position m (by definition), not "at position j + 1 or beyond." The intent is to defend that the range `j + 2 ≤ i ≤ m` may be empty when `j = m − 1`, but the phrasing inverts the relationship between component-index and position-index.

**Required**: Replace with: "wᵢ = 1 for j + 2 ≤ i ≤ m (the range is empty when j = m − 1, in which case wⱼ₊₁ = wₘ = n is the last component; for j ≤ m − 2 the range is nonempty)."

### Issue 4: S5's within-document construction silently extends consistency beyond S0–S3

**ASN-0036, S5 Formal Contract**: "S0–S3 are the only invariants checked. The constructions are minimal — single I-address, trivial arrangements — to isolate the consistency claim from other architectural properties."

**Problem**: The within-document construction with `vₖ = [1, k]` for `k = 1, ..., N + 1` also satisfies D-CTG (the k-values form a contiguous range), D-MIN (`min = [1, 1]`), D-SEQ, S8a, S8-depth, and S8-fin. The cross-document construction with all `vᵢ = [1, 1]` also satisfies these. The Frame clause claims to isolate the construction from "other architectural properties," but the constructions happen to satisfy nearly all of them. This isn't an error, but it weakens the claim's framing: a reader cannot tell from the construction *what* finite multiplicity actually depends on, because the constructions also witness consistency with the full strand model.

**Required**: Either acknowledge that the constructions satisfy more than S0–S3 (strengthening the claim — multiplicity is unbounded even under the full strand model), or construct a witness that genuinely isolates S0–S3 (e.g., one that violates D-CTG by having gaps).

## OUT_OF_SCOPE

None — the ASN explicitly scopes out node ontology, operation effects, links, version semantics, enfilade internals, and replication. The deferred items (subspace alignment, operation preservation of D-CTG/D-MIN, run consolidation, sharing-inverse computability) are correctly identified as open questions for downstream ASNs rather than gaps in this one.

VERDICT: REVISE
