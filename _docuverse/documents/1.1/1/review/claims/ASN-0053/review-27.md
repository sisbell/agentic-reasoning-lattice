I read the foundation contracts (the ASN-0034 cone) and then ASN-0053 as a system, tracing each constructed-span precondition back through WF/D1/D2/T12 to the foundation, and walking the case analyses in SC, S8, S9, S11, S11a–d. The arithmetic is sound: every worked example computes correctly, the WF/D1/D2 precondition chains are unbroken (the `divergence ≤ #s` obligation is discharged via the equal-length exclusion of T1 case (ii) each time, the carrier-membership of reach endpoints is routed through TumblerAdd's `a ⊕ w ∈ T` postcondition, and `#s = #r` is propagated through S6 from level-uniformity + level_compat). I found no correctness defect. What I have are framing/rigor observations.

### S11c Case 2 main-text element-chase drops a guard without justification
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder) transitivity; SC case (iii)
**ASN**: Main-text S11c Case 2: "if t ≥ reach(β), then t ∉ ⟦β⟧ ... Therefore ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}."
**Issue**: ⟦α⟧ \ ⟦β⟧ is literally `{t : start(α) ≤ t < reach(α) ∧ reach(β) ≤ t}`; the main text rewrites it as `{t : reach(β) ≤ t < reach(α)}`, silently discarding the lower guard `start(α) ≤ t`. The rewrite is valid only because the Case 2 hypothesis `start(α) < reach(β)` forces `start(α) < t`, but the main-text proof does not say so. The formal-contract twin of S11c spells this out with explicit ⊆/⊇ inclusions ("we recover the discarded guard ... start(α) < reach(β) ... composes transitively"). The two copies of the same claim therefore differ in rigor; the body should be brought in line with its twin.
**What needs resolving**: n/a (OBSERVE) — sound as written, conclusion correct; align the body proof with the formal-contract version.

### S2 proof and contract are padded with defensive meta-prose
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness) postcondition (b)
**ASN**: S2 (EmptyDistinction): "This second condition is a comparison of natural numbers ... not of the end offset s ⊕ ℓ, which is a tumbler" / "not the type-incoherent comparison of the tumbler s ⊕ ℓ against #s."
**Issue**: The actual content of S2 is one line: T12(b) gives `s ∈ span(s, ℓ)`, so the denotation is non-empty. Around it sit several paragraphs re-deriving the well-formedness preconditions and pre-empting a type error (`actionPoint(ℓ) ≤ #s` is naturals, not a tumbler comparison) that no reader would make. This is defensive justification occupying proof and Preconditions slots — the precise reader must skip past it to find the single load-bearing step.
**What needs resolving**: n/a (OBSERVE).

### S6 Depends entry explains why TumblerAdd is needed rather than what it supplies
**Class**: OBSERVE
**Foundation**: TumblerAdd result-length identity
**ASN**: S6 (LevelConstraint): "Drop a precondition — say Pos(ℓ) — and s ⊕ ℓ need not be defined, so the length identity has nothing to stand on"; and the Depends body "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub ...) and the round-trip identity (D1 ...), neither of which yields ..."
**Issue**: This is the "new prose around an axiom explaining why the axiom is needed rather than what it says" pattern, plus a use-site inventory of which other foundations *don't* supply the fact. The dependency is just: TumblerAdd gives `#(a ⊕ w) = #w` under its preconditions. The counterfactual ("drop Pos(ℓ)") and the exclusion survey do not advance the claim.
**What needs resolving**: n/a (OBSERVE).

### Formal-contract Depends entries carry large use-site inventories
**Class**: OBSERVE
**Foundation**: TumblerAdd (TumblerAdd, ASN-0034)
**ASN**: S11 formal-contract Depends → TumblerAdd (a ~200-word paragraph cataloguing each consumption site); similarly S8, S3, S4, S1 Depends → TumblerAdd.
**Issue**: These entries restate the proof body inside the dependency list — enumerating "consumed twice ... needed already in the boundary characterization ... and again in the ρ-construction ...". A dependency entry should name the imported fact and where it lands; the blow-by-blow re-narration is noise duplicated across every difference/merge claim.
**What needs resolving**: n/a (OBSERVE).

### D0 declared "cited" but not used by any proof
**Class**: OBSERVE
**Foundation**: D0 (DisplacementWellDefined)
**ASN**: Properties Introduced table: "D0 | Displacement well-definedness ... | cited."
**Issue**: WF consumes D1; WR consumes D2; S5 consumes D1; no proof in the ASN invokes D0's postconditions (`b ⊖ a ∈ T`, `Pos(b ⊖ a)`, `actionPoint(b ⊖ a) = divergence`, or the `#a > #b → ... ≠ b` clause). The "cited" status appears to be over-declared.
**What needs resolving**: n/a (OBSERVE) — confirm whether D0 is genuinely consumed somewhere or downgrade the table entry.

VERDICT: OBSERVE