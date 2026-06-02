# Review of ASN-0086

I checked the proofs for R0, R0a, R1–R6c, R-Scope, and the wp Case 2 derivation, plus the worked-sketch arithmetic. The core correctness is solid: the cross-home/same-home antichain split in R0a is complete, R-Scope's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` follows correctly from the R0a antichain at both Σ and Σ', and the wp Case 2 biconditional (`a ∉ nullified(Σ') ⟺ K ≁ R ∨ a_emit ∉ coverage(G)`) is derived in both directions with the unit-depth restriction shown load-bearing. The Worked Sketch tumbler values check out.

The findings below are the accreted meta-prose this note's anti-bloat classifier flags, plus one scoping note.

## REVISE

### Issue 1: Citation-handle meta-commentary in the Working-domain paragraph
**ASN-0086, "Working domain — `→*`-reachable states"**: "We name this fact **RT-closure** and cite it below by name, without restating the reasoning."
**Problem**: The clause "without restating the reasoning" is commentary about the document's own citation practice, not reasoning that advances the claim. Naming the fact is fine; narrating that you will cite it by name is scaffolding the reader must skip.
**Required**: Drop the self-referential clause. State the closure fact once; later uses can cite it without the meta-announcement.

### Issue 2: Use-site inventory / forward reference embedded in a structural slot
**ASN-0086, "Working domain"**: "Two ASN-0043 invariants — L14 (DualPrimitive) and L14a (NonTranscludability) — are *not* published by ASN-0093's K.λ contract; this note carries them across each K.λ-step separately via the FreshLinkKeyDisjointness sub-lemma."
**Problem**: This is bookkeeping about which invariants flow through which contract, planted early and pointing forward to a sub-lemma defined much later (in "Tuple Identity"). It is an inventory of what gets discharged where, not a step in any argument at this location. The substantive fact — L14/L14a hold at the fresh key — belongs at FreshLinkKeyDisjointness, where it is actually proved and used.
**Required**: Move the L14/L14a carry-across statement to the FreshLinkKeyDisjointness sub-lemma (or to R0, its consumer). Leave the Working-domain paragraph to state the invariant-preservation fact without the per-invariant forward inventory.

### Issue 3: Repeated deferral to the Worked Sketch
**ASN-0086, R6c Consequence**: "(The Worked Sketch below exhibits both failures concretely.)" — and again at **wp Case 2** ("illustrated by Step 4 of the Worked Sketch") and the wp load-bearingness paragraph.
**Problem**: Three separate sites defer to the same downstream Worked Sketch. Each claim is already established by its own derivation (R6c by induction; the wp by the biconditional). The parenthetical forward pointers add navigation overhead without advancing reasoning, the compounding-across-cycles pattern the classifier targets.
**Required**: Keep at most one pointer to the Worked Sketch (e.g., a single note that the sketch instantiates R6a/R6b/R6c and the wp false branch). Remove the redundant parentheticals; the abstract claims already stand alone.

### Issue 4: CoverageEqualityDecidable proof is at implementation-procedure granularity
**ASN-0086, Lemma CoverageEqualityDecidable**: the proof sorts endpoints into cells, partitions into points and open gaps, and decides gap-emptiness via the immediate successor `c_k.0`.
**Problem**: The decidability *guarantee* is the system-level content; the cell/gap/successor decision procedure is implementation mechanics that exceeds the abstraction level of every other lemma in the note (the rest cites T2/T12/PrefixSpanCoverage and stops). The gap-emptiness sub-argument re-derives the standard immediate-successor characterization that ASN-0034's TA5 note already supplies.
**Required**: Compress to the guarantee plus the load-bearing reduction (finite endpoint set ⇒ finitely many constant cells, each decided by T2 comparisons), citing the existing immediate-successor fact rather than re-deriving it inline.

## OUT_OF_SCOPE

### Topic 1: Retraction semantics restricted to standard-triple links
`nullified(Σ)` quantifies over `L_R^Σ`, which requires `|Σ.L(b)| = 3`. A higher-arity link whose slot-3 coverage equals `coverage(R)` and whose slot-2 covers `a` therefore does *not* nullify `a`. This is internally consistent (the relational layer's Nullify only emits arity-3 retractions), but the limitation — "type-R" retraction is inert at arity > 3 — is unstated.
**Why out of scope**: Higher-arity typed relations are explicitly deferred (Open Questions: "be regarded directly as elements of higher-arity typed relations"). Pinning down retraction semantics for `|Σ.L(a)| > 3` belongs to that future ASN, not this one.

### Topic 2: Cross-layer retraction-stability discipline
The final Open Question — what discipline a higher-layer operation must satisfy for R6a/R6c to survive its transitions — is correctly deferred. This note's R6a/R6c are proved against `→ ≡ K.σ ∪ K.α ∪ K.λ` only, and that scope is stated.
**Why out of scope**: New territory above the K-operation substrate; not an error in the present invariants.

VERDICT: REVISE
