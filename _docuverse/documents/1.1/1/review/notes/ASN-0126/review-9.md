# Review of ASN-0126

## REVISE

### Issue 1: Registry-entry count mismatch in the worked illustration
**ASN-0126, Worked illustration**: "Consider four registry entries:" — followed by five bullets (`approved`, `succession`, `citation`, `touched`, `retract`).
**Problem**: The prose says "four" but lists five entries. A reader auditing the example against P2/P3 (which the illustration is meant to exercise) is told to expect four and finds five; `retract` in particular is load-bearing for the "born nullified" trace, so the miscount is not cosmetic — it obscures which entries the subsequent paragraphs rely on.
**Required**: Change "four" to "five", or drop `retract` from this list and introduce it separately where the born-nullified trace needs it.

### Issue 2: The singleton-coverage characterization names an empty class
**ASN-0126, Shape-conformance**: "The only endsets with singleton coverage are those whose single span has unit length at a terminal (childless) address; the framework requires no such thing."
**Problem**: Coverage is taken over `T` (all tumblers), and `coverage({(a, δ(1, #a))}) = {t ∈ T : a ≼ t}` (PrefixSpanCoverage, ASN-0043). For any tumbler `a`, the extensions `a.0`, `a.0.1`, … all satisfy `a ≼ t`, so this set is infinite — and since every finite integer sequence can be extended, *no* tumbler in `T` is "childless." The class of singleton-coverage endsets the sentence describes is therefore empty, so the characterization is either vacuous or misleading: it implies childless addresses exist and that some unit-length span could yield singleton coverage, neither of which holds over `T`. The surrounding argument (count spans, not coverage) is sound and is in fact *strengthened* by the correct statement.
**Required**: Replace with the accurate claim — over `T` no endset has singleton coverage via a prefix-coverage span, which is precisely why a `|coverage(F)| = 1` measure would be unsatisfiable and is rejected in favor of span-count. Drop the "terminal (childless) address" clause.

## OUT_OF_SCOPE

### Topic 1: Mixed trajectories combining `→_sh` emits with direct link-store emits
The note offers direct link-store interaction (ASN-0043) as the escape hatch for arity > 3 and multi-source `F`, but a trajectory interleaving raw `K.λ` (direct) and `K.λ_sh` steps is not `→_sh*`-reachable, so P1–P5 are silent about the resulting states. Reconciling the registry invariants with substrates that mix gated and ungated emits is genuinely new territory.
**Why out of scope**: The note explicitly confines itself to `→_sh`-reachable states and defers multi-source to a supplemental note (Open Q #6); the interaction is that successor's concern, not a defect here.

### Topic 2: Vacuous (empty) initial registry
C0 admits `|Σ_init.registry| = 0`, under which every emit fails precondition (i) and `→_sh` extends `dom(Σ.L)` never. The framework is then well-formed but inert.
**Why out of scope**: This is a degenerate instantiation, not a correctness gap; no claim is violated. A one-line note that registries are expected non-empty would help but is not required for the spec to be sound.

The two REVISE items are precision/consistency fixes; the structural core — `→_sh` refinement, the wp derivation against the active-subset postcondition, the gate-vs-landing separation (born-nullified witness), the projection `π` bridging the four-component state to ASN-0086's three, and the C0/P1 two-premise grounding of P2/P3 — is rigorous and self-contained, citing only foundation ASNs.

VERDICT: REVISE
