# Review of ASN-0036

## REVISE

### Issue 1: S8 run-corollary asserted in the summary table but never derived
**ASN-0036, Properties Introduced (S8 row)**: "corollary (via ShiftPreservation applied pointwise) preserves subspace identifier, zero-count (= 3, S7b), and element-field depth (#E(aⱼ) ≥ 2, S7c) across each run"
**Problem**: The S8 proof establishes existence using *only* the singleton decomposition (every `nⱼ = 1`), where conjunct (b) "reduces to the base case `M(d)(vⱼ) = aⱼ` at `k = 0`." For singleton runs, `shift(·, 0)` is the identity, so ShiftPreservation (which requires `k ≥ 1`) is never invoked. The preservation-across-runs corollary has content only for runs of length `> 1` — exactly the coalesced runs the proof defers. Yet the corollary is asserted as an established result in the table, and the S8 formal contract lists S7b, S7c, and ShiftPreservation under *Depends* while its own postconditions ((a) existence, (b) the run identity) do not need them. The contract even concedes this: "S7b and S7c are preconditions of the run-corollary (via ShiftPreservation), *not* of the existence claim." A corollary that is neither a stated postcondition nor derived in the proof body should not appear as a settled guarantee.
**Required**: Either (a) state the run-corollary explicitly as an S8 postcondition and give the one-step derivation (apply ShiftPreservation to each `k` in each run of length `> 1`), accepting that this only bites once coalescing is established; or (b) strike the corollary from the table and remove S7b/S7c/ShiftPreservation from S8's *Depends*, since the established (singleton) existence claim does not use them.

### Issue 2: Repeated use-site deferrals to S7b ("rationale at S7b")
**ASN-0036, S7a / S7d / S7 (Depends lines)**: "T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation (rationale at S7b)"
**Problem**: The note carries the `review-mode.anti-bloat` classifier. The phrase "(rationale at S7b)" recurs verbatim across the *Depends* lines of S7a, S7d, and S7 — three different structural slots all pointing the reader to the same downstream location for a justification rather than discharging it in place. This is the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: State the T10a.4 role once where it first matters and let the later citations stand without the back-pointer, or inline the half-sentence of rationale so the reader need not navigate to S7b.

### Issue 3: Coalescing deferral repeated in three locations
**ASN-0036, S8 intro / S8 postcondition / Open Questions**: "a separate question" … "(Coalescing deferred — see open questions.)" … "Must the span decomposition of an arrangement have a unique maximal form…"
**Problem**: The same deferral (whether runs can be coalesced into maximal form) appears in the S8 introductory paragraph, again in the S8 formal-contract postcondition, and again as an Open Question — the "multiple paragraphs defer to the same downstream location" accretion pattern. The Open Questions entry is the legitimate home; the two upstream restatements are noise the reader must reconcile.
**Required**: Keep the deferral at one site (Open Questions) and drop the duplicate forward pointers from the S8 prose and postcondition, or reduce them to a single neutral note.

## OUT_OF_SCOPE

### Topic 1: V-position ordinal decomposition (ord, vpos, w_ord, OrdAddHom, OrdAddS8a, OrdShiftHom)
**Why out of scope**: This entire section builds within-subspace displacement arithmetic — explicitly "the mechanism by which arithmetic stays within a subspace" — but none of its lemmas is consumed by any invariant established in this ASN. S8, D-CTG, D-SEQ, and ValidInsertionPosition all use `shift`/TumblerAdd directly; ShiftPreservation handles I-address structure without OrdAddHom. The only downstream references to `ord`/`w_ord` are the Open Questions on the subtraction homomorphism and the round-trip `(ord(v) ⊕ w_ord) ⊖ w_ord`. That places this machinery with the operation-layer arithmetic (INSERT/DELETE displacement), which is out of scope here — it is tooling for a future operations ASN, not a state invariant of the strand model. The lemmas themselves appear correct; the concern is purely that they have no in-ASN consumer.

### Topic 2: Subspace alignment `subspace(v) = subspace_I(M(d)(v))`
**Why out of scope**: The ASN correctly notes (Open Questions) that alignment between a V-position's subspace and its mapped I-address's subspace is an operations-layer preservation obligation, not a state invariant. Leaving this unconstrained in the arrangement model is appropriate; it belongs with the operations that must establish it.

VERDICT: REVISE
