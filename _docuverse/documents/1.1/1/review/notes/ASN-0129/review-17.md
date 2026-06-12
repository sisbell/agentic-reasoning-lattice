# Review of ASN-0129

## REVISE

### Issue 1: Self-emit inexpressibility asserted at theorem strength the note elsewhere refuses
**ASN-0129, QD-audit**: "The self-emit disjunct is *not* PL-expressible, deliberately: `a_emit(Σ, d) = chain_d(f_d^Σ)` (FrontierUnification, ASN-0126) reads the frontier of the home's chain — an emit-side quantity assembled from the homed-set (`home(a') = d`, which no atom exposes and prefix testing cannot characterize: PC6's base granularity) and the chain arithmetic `inc(·, 0)` that V-PRIM excludes — so a PL gate can state where a retraction's target *resides*, never where the surface's next emission *lands*."

**Problem**: This is a semantic inexpressibility claim discharged by a blocked-route argument — precisely the argument form C-reach declares unsound ("an earlier framing argued it from… that argument is unsound") and PC6 explicitly fences ("Whether some extensionally equal PL term exists is an inexpressibility question of C-reach's kind"). Under PC6's own statement, "not PL-expressible" means *no* syntax-directed computation over the base denotes the test `a = a_emit(Σ, d)`; establishing that requires an invariance argument over every atom denotation, and the paragraph rules out only the direct assembly route (`home` decomposition plus `inc(·, 0)`). It is silent on the indirect routes the vocabulary actually opens: BH4's `age` is *defined from* the very frontier quantity `f_d^Σ` (FP records its home-wide footprint), so frontier-derived data reaches PL terms as numbers; and `L_dom` is reflected into term position (QD-refl), so the full link-domain data of which `a_emit(Σ, d)` is a function is PL-visible — what remains open is whether the admitted operations compute the function, which is an invariance question of exactly the kind the note demotes to conjecture for `reach` and hedges for the parity candidate ("no evident expression"). The flat "never" breaks the note's own calibration, in a load-bearing design paragraph.

**Required**: Restate at the strength the note's standard licenses: the grammar/vocabulary fact (no atom exposes `home`, prefix testing fails on sub-document homes, V-PRIM admits no address arithmetic — so PL has no *spelling* of the frontier), with the extensional claim explicitly given C-reach's epistemic status (conjectured, obligation recorded), or supply the invariance proof — which must in particular handle BH4's `age` atoms and reflected `L_dom`. The design conclusion that follows ("a gate… states the residence clause and leaves the self-emit clause to the operation that owns it") needs only the vocabulary-level fact and survives the demotion unchanged.

### Issue 2: PC6's parity candidate argues against a fragment smaller than the one V-PRIM ships
**ASN-0129, PC6 (What the relativization costs)**: "the candidate witness that an unrestricted class strictly exceeds PL is the parity of `count(L_dom)` — a one-bit accumulator over the enumerated domain, computable without feedback, with no evident expression in PL's ℕ fragment (comparisons and `+` against literals)."

**Problem**: The parenthetical misdescribes the admitted fragment. V-PRIM admits "the comparisons (`=`, `≤`) and addition (`+`) **on ℕ-valued terms**" — term-to-term comparison and term-level addition, so e.g. `count(D₁) + count(D₂) = count(D₃)` between arbitrary set-valued terms is well-typed PL. "Against literals" is PD0's deliberate polarity restriction on the *aggregate stability rules*, not the vocabulary's bound; PC6 has imported the narrower phrasing into the expressiveness discussion. The candidate is therefore argued against the wrong fragment: the load-bearing question is whether parity escapes Boolean combinations of `=`/`≤` between *sums of counts* and literals (it plausibly does — no doubling or modular operator, no ℕ quantifier — but `count(L_dom) = count(D) + count(D)` is the kind of term the current phrasing wrongly excludes from consideration).

**Required**: State the fragment as V-PRIM defines it — comparisons between ℕ-valued terms, term-level `+`, ℕ literals — and assess the parity candidate against that fragment, keeping the "no evident expression" hedge.

## OUT_OF_SCOPE

### Topic 1: Predicate dynamics under the arrangement-layer transition vocabulary
**Why out of scope**: PD0–PD2 are proven over R-TR's `→_sh` (K.σ ∪ K.α ∪ K.λ_sh), and the note correctly fixes `S` to that relation. A deployment whose substrate also takes ASN-0127-layer steps (K.δ, K.μ⁺/μ⁻/μ~, K.ρ) needs the classification re-grounded against the composed relation — likely benign, since PL footprints touch nothing outside the link store except `dom(Σ.M)`, but `is_doc`'s ⊤-stability (PD0) rests on no step ever removing a document key, which only the composed system's frame inventory can certify. That is a future composition note, not an error here.

### Topic 2: Formal separation proofs for the costs-paragraph candidates
**Why out of scope**: A proof that parity-of-`count(L_dom)` separates the unrestricted-fold class from PL, and (after Issue 1's recalibration) the invariance argument for frontier/`a_emit` inexpressibility, are open theory of the same family as Open Question 6 — counting-plus-order invariance arguments. The note's job is to state the candidates honestly, not discharge them; the proofs belong to the open-questions track.

VERDICT: REVISE
