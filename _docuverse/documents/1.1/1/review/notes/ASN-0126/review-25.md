# Review of ASN-0126

## REVISE

### Issue 1: The gate-vs-landing distinction is restated five times in abstract prose

**ASN-0126, The shape-gated emit / P4 / P6 / Registration**: the same point — "the gate enables (safety, P4) but a gate-enabled emit may still fail to land in the active subset (the stronger wp)" — is stated as abstract prose in at least five places:
- The shape-gated emit: "So the proper statement is: the gate rejects exactly the unregistered/non-conforming... the *active-subset* wp is a separate, strictly stronger condition..."
- Gate realizability intro: "P4 and the wp above are the *safety* half of the gate; neither closes the converse..."
- P6 closing: "A conforming emit always *fires* (P6), but may still be born nullified... The two halves bracket the gate exactly..."
- Property P4: "P4 is the gate's *enablement* half only; active-subset landing is the separate, stronger condition..."
- Property P6: "P4 and P6 together fix the gate to fire on *precisely* the conforming triples."

**Problem**: Pattern 7 (two paragraphs saying the same thing in different words), here compounded fivefold. The Worked illustration's "Born nullified" example legitimately concretizes the distinction; the five abstract restatements do not advance reasoning past the first.

**Required**: State the gate/landing separation once where the wp is derived (The shape-gated emit), let the Worked illustration concretize it, and reduce the P4/P6 property statements to the bare claim plus a single back-pointer. Delete the redundant abstract restatements.

### Issue 2: Repeated downstream deferrals to "The shape-gated emit"

**ASN-0126, P4 / P6 / Worked illustration**: "(The shape-gated emit)" is cited as the deferral target in P6's derivation (twice), in P4, and in the Worked illustration ("exactly as The shape-gated emit argues is attainable").

**Problem**: Pattern 4 — multiple paragraphs in different sections deferring to the same downstream location. The repeated pointer signals that the content was split across sites rather than stated once.

**Required**: Consolidate the wp argument in one place; remove duplicate "see The shape-gated emit" pointers, keeping at most one.

### Issue 3: The "Gate realizability — the liveness dual of P4" lead paragraph is motivational meta-prose

**ASN-0126, Gate realizability**: "P4 and the wp above are the *safety* half of the gate; neither closes the converse — that a conforming triple *can* fire at all. The central promise of this note... is unusable if the gate could spuriously block a conforming emit. We therefore owe a realizability lemma dual to P4..."

**Problem**: This paragraph explains *why P6 is needed* rather than stating or proving anything. It is the "why the axiom is needed" pattern applied to a lemma. P6's statement is self-justifying — a liveness claim needs no three-sentence apologia.

**Required**: Open the section with P6's statement directly. One clause ("the liveness dual of P4") suffices to relate it; drop the motivational framing.

### Issue 4: "dom(Σ.L) carries only conforming tuples" rests on an unstated initial condition

**ASN-0126, Single-source**: "`→_sh` is the *complete* transition relation of a framework-governed substrate... so within such a substrate `dom(Σ.L)` carries only conforming tuples and there is no off-gate path into the link store."

**Problem**: This conclusion holds only if `Σ_init.L` contains no non-conforming tuples. P1 *freezes* whatever `Σ_init` contains and explicitly admits ill-formed initial registries; by the same token nothing in the note forbids a non-conforming `Σ_init.L`. The "only conforming tuples" claim quietly assumes `Σ_init.L = ∅` (inherited from ASN-0086's base state) but never states it. The Registry permanence section states the base case `Σ = Σ_init` for the registry but says nothing about the link store's initial contents.

**Required**: State explicitly that `Σ_init.L = ∅` (or that `Σ_init.L` is shape-conforming) as the base condition the inductive "only conforming tuples" argument requires — parallel to how C0 raises initial registry well-formedness to an explicit commitment.

### Issue 5: Defensive authority-citations accreted around the |F|=1 design choice

**ASN-0126, Single-source**: "an exclusion Nelson's 'no free-floating materials' rule already endorses..."; "matching Nelson's single-target intent, his DELETEVSPAN command taking 'the given span' (singular)"; and in the coalescing paragraph, "This is forced by implementation ground truth — Gregory confirms..." plus "Nelson's span/span-set distinction agrees..."

**Problem**: The single-source commitment and the app-side-coalescing rule stand on their own structural arguments (the lattice usage is single-source; the coverage-singleton measure is unsatisfiable). The stacked Nelson/Gregory appeals are defensive justifications endorsing each micro-decision rather than content advancing the claim — essay content the precise reader must skip past. One evidentiary anchor per decision is enough.

**Required**: Reduce to a single supporting citation per claim (e.g. one Gregory reference for "udanax-green performs no coalescing"); drop the redundant "Nelson's rule already endorses" / "Nelson's intent agrees" endorsements.

### Issue 6: The coalescing-divergence paragraph duplicates its own resolution

**ASN-0126, Shape-conformance**: The paragraph beginning "One edge follows from counting spans rather than coverage..." states the span-count-vs-coverage divergence, resolves it ("single-source means a single span as emitted"), then a later sentence restates the identical rule generalized — "This divergence and its coalescing rule fall on *any* single-span slot... coalescing abutting spans to the canonical one-span form before emit is the app's responsibility wherever a shape constrains a slot to one span."

**Problem**: Pattern 7 within one section — the coalescing-is-the-app's-responsibility rule is stated for F, then restated verbatim-in-substance for "any single-span slot." The generalization adds one fact (it applies to G too) buried in a full restatement.

**Required**: State the rule once, generalized to any single-span slot from the start; cut the F-specific restatement.

## OUT_OF_SCOPE

### Topic 1: Idem flag semantics

The registry stores an `idem` flag and P3 asserts its stability, but the flag has no operational role in this note (correctly deferred to Open Question 1). Defining the registry field here is acceptable; giving it meaning is future work.

### Topic 2: Multi-source / higher-arity emit paths

The note restricts the gated fragment to `|F| = 1`, N = 3, and points to ASN-0086's ungated `→` for everything else. The actual mechanics of multi-source relations belong to a successor note (Open Question 6).

VERDICT: REVISE
