# Review of ASN-0126

## REVISE

### Issue 1: The born-nullified analysis stops one inference short of the consequence its own setup establishes

**ASN-0126, Worked illustration ("Born nullified") / Weakest precondition**: "By ASN-0086's `nullified`/`A_K` machinery the citation is born nullified: `a ∈ nullified(Σ₂)`, hence `(a, [c₁], [c₂] ∪ [c₃]) ∉ A_citation^{Σ₂}`. The gate did not reject this call — all of (0), (i), (ii) held — the wp's inherited third conjunct did."

**Problem**: The example exhibits one poisoned slot and stops, but the machinery already on the page yields a strictly stronger and app-critical consequence. `coverage(G_rng)` contains the chain addresses `...2.4`, `...2.5`, `...2.6`; `a_emit` advances strictly sequentially (subsequent-emission branch), and L-ContiguousPrefix — which the note itself transfers via B2 — forbids skipping. So *every* emission homed at `d` landing in those slots — Step 2's and the next two after it, **of any registered type**, since `nullified` and wp conjunct C3 read only `L_R` and the address — is born nullified. And the condition is permanent: the retraction tuple remains in the audit slice forever (L12/L12a, R3), `nullified` reads `L_R` not `A_R` (R6b — nullifying `a_R` lifts nothing), and R6c bars restoration. One gate-clearing Binary range retraction therefore irreversibly sterilizes a contiguous block of its home document's future emission slots; active emission at `d` resumes only after the block is exhausted by sacrificial born-nullified emits. This is precisely the kind of derived consequence the note's standards demand ("postconditions established but consequences not explored"), and it is the framework-level hazard an app registering a Binary retraction type must know.

**Required**: State and derive the corollary (a short paragraph in the wp section or the born-nullified subsection — every premise is already in play), and reference it from the app-obligation discussion in "Retraction as an attributed Binary". Whether the substrate should prevent it can remain open.

### Issue 2: The bridge section's intro claims more than B2 proves

**ASN-0126, The projection bridge**: "We now show it is a *bridge*: it carries this framework's gated dynamics onto ASN-0086's ungated dynamics, so that every ASN-0086 result holds, suitably projected, here."

**Problem**: "Every" is contradicted three sentences later by B2's own carve-outs: only conclusions that are single-state C/M/L predicates transfer directly; existence-of-successor conclusions do not; transition invariants transfer only across genuine `→_sh`-steps. Worse, some ASN-0086 results fail outright under projection: `π(Σ)` is `→*`-reachable but in general **not layer-reachable** — a `→_sh` run containing a range-G `Emit_R` (the worked illustration's Step 1) projects to a `→`-derivation that violates ASN-0086's discipline commitment (an `L_R`-growing step that is not a `Nullify`). So layer-scoped results (the disciplined-domain wp simplification, the unit-depth-discipline discharge) do not hold "suitably projected" at all. The note never *relies* on them — it correctly keeps C3 live — but the intro asserts a transfer the section then carefully refuses to deliver.

**Required**: Replace the intro sentence with B2's actual scope, and state explicitly that projected runs need not be layer-reachable, so layer-scoped ASN-0086 results are outside transfer range.

### Issue 3: The wp inheritance is misattributed to B2, and the guard rule's semantics is unstated

**ASN-0126, Weakest precondition of the shape-gated emit**: "— and applies to this note's `→_sh*`-reachable Σ by the projection bridge, which sends Σ to the `→*`-reachable `π(Σ)` where wp Case 2 holds (B2), Σ and `π(Σ)` agreeing on the C/M/L components the wp reads (B1)"

**Problem**: Two defects. (a) wp Case 2's conclusion is not "a predicate over the C/M/L components of a single `→*`-reachable state" — it is a per-state equivalence whose left side quantifies over the operation's post-state, which is exactly what B2 disclaims ("B2 yields no `→_sh`-successors"). Case 2 holds *at* `π(Σ)` by its own quantification once ProjectionBridge gives reachability; carrying the equivalence to the gated step at Σ needs effect-identity plus B1 (enabledness and post-state read only shared C/M/L). The section's subsequent derivation uses those pieces, but the headline citation attributes to B2 a transfer B2 excludes — inconsistent with the note's own care elsewhere ("This is R-Scope at its native transition, *not* a B2 transfer"). (b) The rule "`wp(g → S, R) ≡ g ∧ wp(S, R)` when the postcondition requires the operation to fire" leans on an unstated wp semantics. Under a blocking/partial-correctness reading, a disabled guard yields no post-state and the postcondition holds vacuously, making wp = ⊤ on `¬g` and falsifying the equivalence; the rule is sound only under the attainability/total-correctness reading the note silently assumes. The gloss "the tuple is never deposited and `(a, F, G) ∉ A_K^{Σ'}`" even imagines a post-state `Σ'` that does not exist when the guard blocks.

**Required**: Justify the inheritance by ProjectionBridge + effect-identity + B1 (or add an explicit deterministic-operation transfer clause to the bridge), and state the wp convention (attainability reading: wp requires the step to fire and the postcondition to hold) under which the guard-conjunction rule is valid.

### Issue 4: "Precondition L3 only" contradicts the note's own P5 lift

**ASN-0126, The shape-gated emit**: "ASN-0086's `K.λ` step has precondition L3 only (arity ≥ 3, non-empty type slot); it does not inspect span counts"

**Problem**: P5's proof discharges, for the lifted step, "the inherited L3 and `d ∈ dom(Σ.M)`" — if `K.λ` truly carried L3 only, the home-allocation discharge would be unnecessary. The "only" is also untenable against the foundation: L1a requires `home(a) ∈ dom(Σ.M)` for every link address, so a `K.λ` step at an unallocated home would break an invariant; the step's contract must carry home allocation (as `Emit_K`'s precondition does) plus key freshness. The note thus gives two inconsistent inventories of the inherited precondition set that `K.λ_sh` extends.

**Required**: State `K.λ`'s inherited precondition set once (L3, home allocation, fresh key per its contract) and use it consistently; the intended contrast — `K.λ` inspects no span counts — survives without "only".

### Issue 5: RegisteredAdmissible cites C0 for a premise C0 does not state

**ASN-0126, Gate realizability**: "By C0 (RegistryWellFormedness, The registry) the registry stores, for K's coverage class, a finite representative endset `K_j ∈ T_admissible`"

**Problem**: C0's well-formedness, as defined, says only that shape values lie in `{Unary, Binary, Multi}` and coverage-class keys are unique (plus finiteness). The premise `K_j ∈ T_admissible` comes from the registry's *type declaration* ("stored concretely as a representative `K_j ∈ T_admissible`", The registry), not from C0. Since this premise carries RegisteredAdmissible, which in turn carries P5's discharge of `K ∈ T_admissible` and L3's non-empty type slot, the citation must be exact.

**Required**: Cite the registry typing, or fold "every stored representative lies in `T_admissible`" into C0's well-formedness clause and keep the citation as is.

### Issue 6: The span-count-vs-coverage point is stated in full twice; P1's conclusion is pre-stated

**ASN-0126, Single-source ∥ Shape-conformance**: "but a source presenting one *contiguous* extent as two abutting spans is `|F| = 2` and excluded just the same, though its coverage equals that of a conformant one-span F" and "Conversely, a source presenting one contiguous extent as two abutting spans `(a, ℓ₁)`, `(a ⊕ ℓ₁, ℓ₂)` has `|F| = 2` and fails every shape even though its coverage equals that of the conformant one-span F"

**Problem**: The same point — the gate measures span count, not coverage; abutting spans fail despite coverage-equality — is made in full in both sections, with "the gate measures span count, not coverage" appearing nearly verbatim in each. This reads as a prior cycle's clarification landing in two places rather than one (the anti-bloat pattern: two paragraphs saying the same thing in different words). The same pattern appears in The registry, whose clause "so the registry is a fixed *input* carried in `Σ` that no reachable state revises (P1, Registry permanence)" pre-states the conclusion that Registry permanence then proves as P1.

**Required**: Give the divergence discussion one home — Shape-conformance, which owns the gate and already carries the unit-depth-coverage direction; Single-source keeps the bare rule, the disjoint-passages motivation, and the Open Question 6 pointer. Trim The registry's clause to the definitional commitment plus the P1 pointer.

## OUT_OF_SCOPE

### Topic 1: A discipline commitment for the gated layer
ASN-0086's RelationalLayer commits every `L_R`-growing step to be a `Nullify`; this note's operation set admits generic Binary `Emit_R` (the worked illustration uses it), so that commitment lapses along with its layer-scoped guarantees. Whether the gated layer should adopt a successor commitment — e.g., all `L_R` growth via `Nullify_Binary` with P-tgt-valid targets, restoring single-tuple scope and the disciplined wp simplification as layer guarantees and closing Issue 1's embargo hazard at the layer level — is commitment design for the successor note. **Why out of scope**: the note handles the discipline's loss correctly case-by-case; designing its replacement is new territory, not an error here.

### Topic 2: Registry lifecycle beyond Σ_init
Runtime registration, deregistration, migration, and composition of registries from multiple apps are all foreclosed by the immutability design; a future ASN could relax P1 to per-epoch stability with versioned registries. **Why out of scope**: immutability is this note's deliberate commitment, not an oversight, and the relaxation would be a new framework, not a fix.

VERDICT: REVISE
