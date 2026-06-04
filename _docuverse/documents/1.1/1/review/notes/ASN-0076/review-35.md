# Review of ASN-0076

## REVISE

### Issue 1: The structural-vs-semantic caveat is restated in five places

**ASN-0076, §The Composite / §The Supersession Relationship / E4 / worked-example E4**: the same disclaimer — "this is only a structural witness; identification as supersession rests on the external `τ_sup` convention, deferred to a future ASN" — appears at the `τ_sup` definition ("deferred to a future ASN on type-endset conventions"), in the Supersession Relationship intro ("the link model establishes only a structural witness ... rests on the external `τ_sup` convention, not on the structure"), in E4's interpretation ("its reading as a supersession rests on the external `τ_sup` convention fixed at §The Composite"), and again in the worked example ("Structural witness only; semantic identification ... §The Composite").

**Problem**: This is precisely the anti-bloat pattern of "multiple paragraphs in different sections defer to the same downstream location" and "two paragraphs say the same thing in different words." The reader must skip past the same caveat four or five times to follow the claims. The distinction is load-bearing exactly once.

**Required**: State the structural-vs-semantic distinction once (it belongs at the `τ_sup` definition where the convention is introduced). Remove the restatements in §The Supersession Relationship intro, E4's interpretation, and the worked example. E7 already carries the rigorous version of the distinction (covers vs. discoverable_from) and need not be preceded by prose previews elsewhere.

### Issue 2: §The Composite previews E0's ValidComposite★ discharge

**ASN-0076, §The Composite**: "EDITLINK as a valid composite. EDITLINK satisfies ValidComposite★ (ASN-0047); both its clauses — K.λ's elementary preconditions at each intermediate state and the J0/J1★/J1'★ coupling constraints — are discharged in E0 below."

**Problem**: Forward-reference accretion. This paragraph announces what E0 will prove and is fully duplicated by E0's "ValidComposite★ discharge" subsection. It advances no reasoning; it is a use-site preview of a downstream claim.

**Required**: Delete the preview paragraph. E0 itself establishes the ValidComposite★ status.

### Issue 3: Redundant `#τ_sup ≥ 1` conjunct with inconsistent justification

**ASN-0076, §The Composite (precondition) and E0**: the precondition lists `τ_sup ∈ T ∧ #τ_sup ≥ 1`, and E0 discharges the `E_type` span length "by the precondition of the composite," whereas the `E_from`/`E_to` lengths are discharged "by T0."

**Problem**: T0 (CarrierSetDefinition) guarantees `#t ≥ 1` for every `t ∈ T`, so `#τ_sup ≥ 1` is vacuous once `τ_sup ∈ T` is stated. The precondition carries a redundant conjunct, and E0 then justifies the three structurally identical span-length facts two different ways (T0 for two, "the precondition" for the third) when T0 covers all three.

**Required**: Drop `#τ_sup ≥ 1` from the precondition (keep `τ_sup ∈ T`), and discharge `#τ_sup ≥ 1` by T0 uniformly with `#ℓ_old` and `#ℓ_new` in E0 and the worked example.

### Issue 4: Redundant defensive justifications

**ASN-0076, E2 and E0**: E2 proves pairwise distinctness via L11a, then adds a parenthetical second proof — "(K.λ's freshness precondition ... independently guarantees the same distinctness at each step.)" E0's "We must observe two things about the order. First, ..." paragraph defends against a concern (whether ordering is a *precondition*-level constraint) that K.λ's preconditions plus L4 already exclude.

**Problem**: Both are defensive belt-and-suspenders prose. E2's parenthetical re-proves a fact already established. E0's "First" point imagines a precondition coupling that the carrier (K.λ + L4) excludes, then argues it away.

**Required**: Remove E2's redundant parenthetical. In E0, retain only the load-bearing semantic observation (that the chosen ordering makes `E_to`'s span denote an existing entity rather than a forward declaration) and the "Second" atomicity point that the maximum-of-initial-segment argument depends on; drop the defense that ordering "is not a precondition-level constraint."

## OUT_OF_SCOPE

### Topic 1: Supersession-type recognition convention and chain/cycle semantics
**Why out of scope**: The conventions by which a reader identifies `τ_sup` as a supersession marker, traverses supersession chains, detects cycles, or computes "current" successors are correctly deferred to the Open Questions and a future type-endset/link-search ASN. These are new territory, not errors here.

### Topic 2: Authorization of `d_new` selection
**Why out of scope**: E6's deferral of who may publish a supersession (authorization/capability layer) is legitimately outside the link model, which carries no executor field.

VERDICT: REVISE
