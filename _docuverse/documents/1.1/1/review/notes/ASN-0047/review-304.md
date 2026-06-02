# Review of ASN-0047

## REVISE

### Issue 1: K.μ⁻ worked example contradicts the K.μ⁻ definition on what is a precondition vs. a derived consequence
**ASN-0047, *Worked example: interior content replacement*, Step 1**: "K.μ⁻'s explicit preconditions are: (a) `d ∈ E_doc` ...; (b) `dom(M(d)) ≠ ∅` ...; (c) the contracted post-state `M_int(d)` must satisfy the per-state arrangement invariants S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, and D-MIN★".

**Problem**: The K.μ⁻ definition states the opposite on both points. On (b): "The strict-contraction constraint forces `n_S ≥ 1` ... hence ... `dom(M(d)) ≠ ∅`, discharging the effect clause's satisfiability" — i.e. non-emptiness is *derived*, not an explicit precondition. On (c): "The per-state arrangement invariants S2, S3★, ... at M'(d) are *derived consequences* of this constructive form, **not separate preconditions**." The link worked example (Step 5) gets this right: "(`dom(M(d)) ≠ ∅` is not a separate check — strict contraction forces it, per K.μ⁻'s definition)." So one worked example treats as "explicit preconditions" exactly what the definition and the other worked example call derived consequences. A reader cannot tell which characterization governs.
**Required**: Rewrite Step 1's "Precondition discharge" to match the definition: the only explicit preconditions are `d ∈ E_doc` and the constructive per-subspace retention choice; non-emptiness and the per-state invariants are derived. Align it with the Step 5 phrasing.

### Issue 2: ValidComposite★ is partially restated with a forward pointer to its own full statement
**ASN-0047, *Coupling and isolation***: "A composite transition `Σ →* Σ'` is *valid* (ValidComposite★) iff (1) each elementary step satisfies its own precondition ... and (2) the couplings J0, J1★, J1'★ hold for the composite as a whole ... The full statement ... is in *Scoped coupling constraints* below."

**Problem**: Clauses (1) and (2) are then stated in full again under ValidComposite★ in *Scoped coupling constraints*. This is a partial restatement paired with a forward pointer to the same content — the "multiple paragraphs defer to the same downstream location" pattern. The reader reads the definition twice and must reconcile the two phrasings.
**Required**: Replace the partial restatement here with a bare forward pointer ("validity is defined as ValidComposite★, *Scoped coupling constraints* below"), or move the full definition here and drop the duplicate. Keep one authoritative statement.

### Issue 3: The "K.μ⁺ transiently violates P4★, restored by J1★" fact is stated three times
**ASN-0047**: P4★ definition box — "P4★ is a Class (b) composite-boundary property: K.μ⁺ alone may transiently violate it ... with restoration at the composite boundary governed by J1★." *Composite-boundary verification matrix* — "After K.μ⁺ before K.ρ: `(a, d) ∈ Contains_C(M_post)` but not yet in R." Class (b) proof — "Only K.μ⁺ may transiently violate P4★ ...; J1★ supplies the co-occurring K.ρ ... restoring the bound."

**Problem**: The same transient-failure-and-restoration claim appears in three slots. The matrix (index) plus the proof (detail) already cover it; the third statement in the definition box is redundant essay in a structural slot.
**Required**: Drop the transient/restoration sentence from the P4★ definition box (keep only the property statement and its scoping), leaving the matrix and proof to carry the discharge.

### Issue 4: P4a definition box carries discharge-mechanism essay that belongs in the proof
**ASN-0047, P4a definition box**: "*Discharge mechanism.* P4a is discharged by induction along the witnessing trace, not by a per-state check. For a freshly recorded entry ... the witnessing trace state is the composite endpoint Σ' itself ... It forbids a composite that both places `a` (K.μ⁺) and removes it (K.μ⁻) before its endpoint ...".

**Problem**: The Class (b) proof's P4a row then says only "discharged by its definition box" — the proof defers its discharge to the definition, inverting the normal structure (definitions state *what*, proofs establish *how*). The multi-paragraph discharge argument is essay content lodged in a definition slot. Combined with the preceding classification essay ("P4a is *not* a state-local invariant ... We classify it explicitly as a *trace property*"), the box is doing the proof's job.
**Required**: Keep the formal P4a statement and the trace-property typing in the definition box; move the "Discharge mechanism" argument into the Class (b) proof where the other composite-boundary properties are discharged inline.

### Issue 5: J4 step (ii) carries enfilade/POOM implementation-mechanics evidence that the scope excludes
**ASN-0047, J4, step (ii)**: "Gregory's `docreatenewversion` reads the source document's full live POOM via `doretrievedocvspanfoo` — the entire `cwid.dsas[V]` content-subspace width ... retrieving leaf crums in ascending V-order (the `incontextlistnd` insertion-sort by V-address) and re-seating them ... (`isanextensionnd` merges only naturally I-adjacent segments) ...".

**Problem**: This paragraph descends into POOM structure, crum-level enfilade internals, and named C routines — material the Scope section lists as OUT OF SCOPE ("POOM structure and V-stream mechanics," "enfilade implementation internals"). The abstract content J4 needs (a complete, order- and multiplicity-preserving copy of the content subspace) is already captured by the φ-bijection statement immediately above it; the crum/POOM detail is over-grounded evidence, not a system guarantee.
**Required**: Compress the implementation evidence to the level that grounds the φ-copy semantics (full content subspace copied in source order, duplicates retained, link subspace excluded), and drop the POOM/crum/routine-internal mechanics.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
The ASN already routes this to an Open Question ("Must the system guarantee ... an interior link can be withdrawn ... preserving D-CTG★ / D-MIN★ ... the implementation's interior `DELETEVSPAN` ... compacts-and-renumbers"). This is correctly deferred — DELETEVSPAN is a named operation and out of scope here.
**Why out of scope**: Interior compaction/renumbering is a future operation-level concern; the current suffix-only K.μ⁻ is a complete elementary primitive in its own right.

VERDICT: REVISE
