# Review of ASN-0047

## REVISE

### Issue 1: P4a discharge does not name the premise that the witness survives to the composite boundary

**ASN-0047, P4a definition box (*Discharge mechanism*)**: "a freshly recorded entry `(a, d) ∈ R' \ R` is witnessed by the post-state Σ' itself — the K.μ⁺ that fires somewhere in the composite places a content-subspace V-position `v` with `M'(d)(v) = a`."

**Problem**: P4a's witnessing existential is explicitly restricted to *composite-boundary* states `{Σ₀, …, Σ_n}`, not intra-composite intermediate states. If a composite both places `a` (via K.μ⁺) and removes it (via K.μ⁻) before its endpoint, the entry `(a, d)` would be recorded with no boundary witness. The discharge asserts "Σ' witnesses it" without showing the placed V-position survives to Σ'. The load-bearing fact is J1'★ (its trigger conjunct `(E v ∈ dom(M'(d)) : subspace(v) = s_C ∧ M'(d)(v) = a)` is evaluated at Σ' and forbids exactly the place-then-remove composite), but J1'★ is never named at this step.

**Required**: State that the witness-at-Σ' follows from J1'★ (the ValidComposite★ clause-(2) constraint forcing a content-subspace witness at the composite endpoint), so the discharge names its premise rather than asserting survival.

### Issue 2: The operand-tracking discriminator is restated four to five times within J4

**ASN-0047, *Coupling and isolation*, J4**: the rule "fork's transclusion source is the K.δ operand `d_op` (= `d_src` for k=1, `prev_version` for k=0), so a subsequent version inherits the prior version's edits" appears in the opening paragraph, again in "The uniformity is necessary…", again in the per-sub-case bullets of Definition (Fork), again in step (i), and again in step (ii) ("a subsequent version (k = 0) inherits the current edited content…").

**Problem**: Five restatements of one discriminator in a single section. This is the "two paragraphs say the same thing in different words" accretion pattern the review mode flags — the reader must re-read variants of the same claim to confirm they are identical.

**Required**: State the operand-tracking rule once (Definition (Fork)) and let steps (i)/(ii) reference it rather than re-derive it. Drop "The uniformity is necessary…" or fold it into the single statement.

### Issue 3: The `max`-greatest-element well-definedness derivation is duplicated across K.α and K.λ

**ASN-0047, K.α (*Subsequent emission*) and K.λ (*Subsequent emission*)**: both spell out "The `max` is well-defined: the set … is non-empty by the subsequent-emission predicate, finite as a subset of `dom(C)`/`dom(L)` by C-fin/L-fin (ASN-0093), and totally ordered by T1 (ASN-0034), so it has a unique greatest element."

**Problem**: The identical three-clause derivation is given twice in this ASN, and is itself inherited from ASN-0093's K.α/K.λ. Since K.α and K.λ are declared to "follow ASN-0093's K.α/K.λ", re-deriving the foundation's own max-well-definedness is accreted restatement of foundation content.

**Required**: State the derivation once (or cite the ASN-0093 emission cases) and remove the duplicate; the only delta this ASN adds to these transitions is the extended frame (`E'`, `R'`), which is what warrants restatement.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
Already correctly deferred by the ASN's own Open Question on renumbering-aware contraction; K.μ⁻'s suffix-only model is faithful to gap-free POOM for suffix deletions, and interior `DELETEVSPAN` is a named operation, out of scope.

VERDICT: REVISE
