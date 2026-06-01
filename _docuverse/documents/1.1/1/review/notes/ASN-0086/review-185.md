# Review of ASN-0086

## REVISE

### Issue 1: Unused leftmost-strictness justification (defensive exhaustiveness)
**ASN-0086, Definition — state-local-conforming state**: "the containment `{→*-reachable} ⊆ {substrate-conforming} ⊆ {state-local-conforming}` holds with *both* inclusions strict. The leftmost is strict because conformance-preserving `↝`-steps that are not K-op `→`-steps — e.g. a direct K.λ caller respecting the substrate clauses — reach substrate-conforming states that are not `→*`-reachable..."

**Problem**: Only the *rightmost* strictness is load-bearing downstream — NestedLinkWitness drives the wp Case 1 PC-load-bearingness counterexample and the "discipline alone insufficient" wp argument. The *leftmost* strictness (that conforming `↝`-steps reach non-`→*`-reachable states) is never consumed by any later proof. The clause is a defensive exhaustiveness claim that the precise reader must skip. This is exactly the anti-bloat pattern of a justification that does not advance reasoning.

**Required**: Drop the leftmost-strictness clause, or move it to wherever (if anywhere) it is actually cited. State only the rightmost strictness, which is used.

### Issue 2: Citation-convention meta-prose
**ASN-0086, Definition — state-local-conforming state**: "Downstream uses of either strictness cite this definition rather than re-arguing the inclusion."

**Problem**: This sentence advances no object-level reasoning; it narrates a citation protocol. It is the flagged pattern "prose justifies document ordering / citation convention." It also overstates: per Issue 1, one of the two strictnesses has no downstream user.

**Required**: Delete the sentence.

### Issue 3: Use-site inventory in the worked sketch
**ASN-0086, Worked Sketch, Step 1 ("L-invariant verification at b₁")**: "The lemma-consequences L2, L11a, L12b are not step-preserved state-local invariants and so lie outside R0's preservation argument; they hold automatically — L2 from the `home` definition, L11a as GlobalUniqueness (ASN-0034) instantiated at `b₁`, L12b from L12a together with L1a."

**Problem**: This is a defensive enumeration of which foundation consequences do/don't fall under R0's preservation scope, inserted into a concrete worked example whose purpose is to exhibit R0–R6 against specific tumblers. It is the flagged "use-site inventory" pattern — it catalogues consumers/non-consumers rather than verifying the step. The example already discharges L0/L1/L1a/L1b/L1c by inspection; the L2/L11a/L12b catalogue adds no verification.

**Required**: Remove the inventory sentence. If a reader needs to know these consequences hold, that belongs (once) in R0's statement of scope, not re-litigated per worked step.

### Issue 4: Relational-layer "protocol rationale" prose
**ASN-0086, Definition — relational layer**: the three labelled commitments ("*Nullify-as-sole-`R`-producer discipline:*", "*P1-confinement of Nullify targets:*", and the surrounding "this meets the target-membership requirement... Together these three commitments make the layer satisfy that discipline...").

**Problem**: The substantive content — the layer's operation set and that every `R`-typed emission routes through the unit-depth `Nullify` form — is one sentence. The remainder explains *why* each commitment is needed and re-asserts that the conjunction yields the discipline, which is the flagged "Protocol rationale / why the axiom is needed" expansion rather than statement of what the layer is.

**Required**: Collapse to the operation set plus the single discipline commitment; drop the per-commitment rationale, which restates the Unit-depth-retraction-discipline definition in different words.

## OUT_OF_SCOPE

### Topic 1: Concurrency, atomicity, and Observe ordering
**Why out of scope**: The Open Questions on Emit/Observe atomicity, the consistency model for `A_K` transitions, and Observe result ordering concern a concurrency layer the substrate does not yet specify. These are new territory, not defects in the single-authority, sequential-transition model this ASN proves over.

### Topic 2: Multi-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note explicitly confines `L_K` to standard-triple links and defers higher-arity relational structure. Building `L_K^{(n)} ⊆ A_rel × ℘(A)^n` is a future ASN, not a correction here.

VERDICT: REVISE
