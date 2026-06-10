# Review of ASN-0119

This is a careful, largely sound note. I checked the imported postconditions against ASN-0084, re-derived both worked examples (pivot `ABCDE ↦ ACDEB` and swap `ABCDEF ↦ AEFCDB`) ordinal-by-ordinal, verified the π-tables, confirmed the J-coupling vacuity arguments and the subspace-preservation that closes J1★. The mathematics holds. The defects are in how the note grounds and classifies the ASN-0047 composite machinery it leans on, plus one redundancy.

## REVISE

### Issue 1: Composite-boundary properties — miscategorized, ungrounded, and P4a discharged too cheaply

**ASN-0119, invariant-discharge paragraph ("What is preserved: I-address correspondence")**: "The remaining ExtendedReachableStateInvariants conjuncts (P6, P7, P8, P7a, P4a, the E-family NodeLineage/ActivatedEmission, the L-family, the C-family) are preserved by the C/E/R/L frame."

**Problem**: Three distinct faults converge on the composite-boundary handling.

(a) *Mislabel.* ASN-0047 partitions its invariants: `ExtendedReachableStateInvariants` lists the **per-state** conjuncts (S2 … CL-UNIQ), and `P4★ ∧ P4a ∧ P7a` are the separately-stated **composite-boundary properties**. The note knows this — two sentences earlier it correctly writes "The one composite-boundary invariant that reads the mutated arrangement, P4★." Yet here it sweeps P4a and P7a into "the remaining ExtendedReachableStateInvariants conjuncts," contradicting its own classification. P4a and P7a are composite-boundary properties, not per-state invariants.

(b) *Ungrounded composite status.* The note imports REARRANGE as "an atomic arrangement-rearrangement primitive … distinct from … K.μ~," and then invokes composite-level predicates on it: the J-couplings "for the composite as a whole" and the composite-boundary properties P4★/P4a/P7a at Σ'. But ASN-0047's `ValidComposite★` defines valid composites over a **closed** atomic vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` that does not contain REARRANGE. The J-couplings and composite-boundary properties are defined relative to valid composites; until REARRANGE is explicitly admitted into that vocabulary (equivalently: stated to be, as a single atomic step, a one-step valid composite, so that Σ' is a composite boundary), the appeals to "the composite as a whole," "between Σ and Σ'," and the composite-boundary properties at Σ' have no formal referent. The verification work is done; the framing sentence that admits REARRANGE is missing.

(c) *P4a discharged as "by frame," but P4a is a trace property.* P4a (TraceWitnessing) quantifies over all valid traces to the state and asserts, for each `(a,d) ∈ R`, the existence of a *trace state* `Σ_k` where `a` sat in `d`'s content-subspace range. `R' = R` (frame) gives that the *set* of provenance entries is unchanged, but it does not by itself supply the *witness*. The actual argument is: a trace to Σ' is a trace to Σ extended by the REARRANGE step; Σ is a composite boundary at which P4a held, so each `(a,d) ∈ R = R'` already has a witness `Σ_k` in the prefix; that witness persists in the extended trace. "Preserved by the C/E/R/L frame" omits this trace-prefix reasoning entirely. (P7a, by contrast, genuinely *is* trivial by frame — `dom(C)` and `R` both frozen — so for P7a only the category label (a) is wrong.)

**Required**: (a) Classify P4a/P7a as composite-boundary properties, matching the note's own P4★ treatment. (b) Add an explicit sentence admitting REARRANGE into ASN-0047's transition vocabulary as a new atomic primitive constituting a single-step valid composite, so that "Σ' is a composite boundary" and the J-couplings are well-defined. (c) Give P4a its real discharge: R frozen *plus* content-subspace-range invariance *plus* persistence of the pre-state's trace witnesses along the trace prefix.

### Issue 2: The RA6 paragraph states "not inherited from ASN-0084" twice

**ASN-0119, "Links" section**: "ASN-0084's REARRANGE_K frames only the content store and the arrangement; its frame R-FRAME-P/R-FRAME-S **says nothing about the link store L**. … This is a **fresh frame commitment of the lifted operation, not a consequence inherited from the import**."

**Problem**: The first clause ("says nothing about the link store L") and the closing sentence ("a fresh frame commitment … not … inherited") carry the same content — that RA6 is new, because ASN-0084 is silent on `L`. The intervening sentence states RA6 itself. One of the two framings suffices; the closing sentence is a restatement of the opening premise. (This is the only clear same-content-twice instance the anti-bloat scan turned up — the LP3/LP11 caveat and the per-subspace S3★ aside both clarify genuine subtleties and should stay; the foundation recap in "The two streams" is statements of what things are, not meta-prose.)

**Required**: Keep "ASN-0084's frame says nothing about L, so we add `Σ'.L = Σ.L` (RA6)"; drop the closing "fresh frame commitment … not inherited" restatement, or fold it into the opening clause.

## OUT_OF_SCOPE

### Topic 1: REARRANGE outside depth 2 / outside the text subspace
**Why out of scope**: The note explicitly scopes itself to `s_C` at `#v = 2` ("We make no claim about other subspaces or other depths"), matching ASN-0084's CutSequence CS3/CS4. Higher-depth transposition, link-subspace reordering, and ≥5-cut permutations are new territory, correctly deferred (and partly captured in the Open Questions), not a gap in this ASN.

### Topic 2: Cross-document boundary-hood, lock-free concurrent rearrangement, discovery-index invariants, prior-arrangement recovery, displacement-arithmetic boundary guards
**Why out of scope**: These are exactly the note's five Open Questions. Each is a relationship to a future operation or a refinement layer, not an obligation REARRANGE itself must discharge.

META: (none) — the ASN defines an operation on the arrangement and the system guarantees (content permanence, extent conservation, link survival, isolation) any conforming implementation must meet; the implementation evidence (`diff[2]`, the collision bug) motivates the abstract tiling guarantee rather than specifying mechanics, so the note is on-track.

VERDICT: REVISE
