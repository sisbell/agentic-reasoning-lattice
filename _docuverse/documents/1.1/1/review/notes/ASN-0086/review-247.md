# Review of ASN-0086

## REVISE

### Issue 1: (UZ) introduced as "used throughout" but never used
**ASN-0086, Allocator Structure → *Derived chain facts***: "We use two `S(p, d)` postconditions throughout, both holding along the whole `inc(·, 0)` chain: **(UL) uniform length** ... and **(UZ) uniform zero-count** — `zeros(cₙ) = zeros(c₁)`..."

**Problem**: (UL) is genuinely used (R0a Case 2: `#a = #t_i = #t_1 = #a'`; the worked example's element-field-length check). (UZ) is never referenced anywhere after its introduction. Every zero-count argument in the note is done directly — R0a Case 1 reasons by zero-count addition along concatenation, the worked example computes `zeros(a₁) = 3` by inspection, and chain-element zero structure comes from ChainElementT4Validity (foundation), not (UZ). The "we use two ... throughout" framing is false for the second item; (UZ) is provisioned and abandoned.

**Required**: Delete (UZ) (and adjust "two postconditions" to "one"), or cite the actual site that needs it.

### Issue 2: Phantom precondition "P2" introduced only to be dismissed (wp Case 1)
**ASN-0086, Weakest-Precondition Analysis, Case 1**: "The scope condition P2 (`|Σ.L(a)| = 3`) is consequently absent from the wp, by R-Scope's arity-independence..."

**Problem**: Nullify's preconditions are P0, P1, and P-tgt — there is no P2. "P2" appears nowhere else in the note. Naming a never-defined "scope condition P2" purely to announce its absence from the wp is reviser-drift residue: it asks the reader to track a precondition the operation never carried. The underlying fact (R-Scope is arity-independent, so arity does not enter the wp) is real and worth one clause, but the P2 label invents the very condition it dismisses.

**Required**: State the arity-independence directly ("the wp does not constrain `|Σ.L(a)|`, by R-Scope's arity-independence") without introducing a labeled phantom precondition.

### Issue 3: R3 proof skips the `|Σ'.L(a)| = 3` conjunct
**ASN-0086, R3 proof**: "...The membership test for `L_K^{Σ'}` is `coverage(Σ'.L(a).e₃) = coverage(K)` ... Therefore `(a, F, G) ∈ L_K^{Σ'}`."

**Problem**: Membership in `L_K^{Σ'}` (Definition — TypedRelation) requires four conjuncts including `|Σ'.L(a)| = 3`. The proof establishes the slot equalities and the coverage test but never states that the arity conjunct is preserved. It is trivially preserved (R2 gives `Σ'.L(a) = (F,G,K'')`, a triple), but per the "every invariant conjunct addressed" standard the closure on the arity conjunct should be made explicit rather than left silent.

**Required**: Add one clause: `|Σ'.L(a)| = |Σ.L(a)| = 3` by R2, since the stored value is preserved exactly.

### Issue 4: Discipline-discharge induction lists Observe_K among transition cases
**ASN-0086, Three Operations, discipline discharge**: "...split by the kind of step. ... `Observe_K` is state-preserving — either way the discipline carries over. By the commitment, every transition that grows `L_R` is a `Nullify`..."

**Problem**: The induction is over `→`-steps (`→ ≡ K.σ ∪ K.α ∪ K.λ`). `Observe_K` is a pure read, not a `→`-step, so it is not a case in this induction; including it is a category slip. Separately, the load-bearing reason "every transition that grows `L_R` is a Nullify" relies on `L_R` being triple-restricted (a higher-arity K.λ emission cannot enter `L_R`), which the argument leaves implicit — without it, a raw K.λ could in principle grow `L_R` outside Emit_K.

**Required**: Drop Observe_K from the case split (it does not transition state), and add the one clause noting that only triple emissions can grow `L_R` (so every `L_R`-growing step is an Emit_K at `K ~ R`, hence a Nullify by the commitment).

## OUT_OF_SCOPE

### Topic 1: Cross-layer type-address collision (Open Questions)
**Why out of scope**: Whether two layers independently choosing colliding type addresses under L9 causes interference is a multi-layer coordination question; this note fixes a single relational vocabulary over one substrate and correctly defers it.

### Topic 2: Concurrency/atomicity of Emit vs. Observe
**Why out of scope**: The consistency model under concurrent Emit/Observe is genuinely new territory (the note's transitions are sequential per ASN-0093's SequentialTransitionAxiom); belongs in a future concurrency ASN.

VERDICT: REVISE
