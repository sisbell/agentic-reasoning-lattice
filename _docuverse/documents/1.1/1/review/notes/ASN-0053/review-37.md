# Review of ASN-0053

## REVISE

### Issue 1: S5 discharges TA-LC by appeal to "well-defined" rather than naming its preconditions

**ASN-0053, S5 (SplitWidthComposition)**: "To apply TA-LC (ASN-0034), both compositions must be well-defined: s ⊕ (d ⊕ d') by TA-assoc, and s ⊕ ℓ since it equals reach(σ) (TA0 on σ). TA-LC gives: d ⊕ d' = ℓ."

**Problem**: TA-LC's contract (ASN-0034) has explicit preconditions: `Pos(x)`, `Pos(y)`, `actionPoint(x) ≤ #a`, `actionPoint(y) ≤ #a`, in addition to `a ⊕ x = a ⊕ y`. The proof substitutes a blanket "both compositions well-defined" instead of discharging these. The substitution happens to be sound — well-definedness of `s ⊕ (d⊕d')` via TA0 *is* `Pos(d⊕d') ∧ actionPoint(d⊕d') ≤ #s` — but the chain is left implicit. This is also why the just-listed TA-assoc consequences (ii) `Pos(d⊕d')` and (iii) `actionPoint(d⊕d') = min(k_d,k_{d'})` appear unused: they are in fact exactly the facts TA-LC needs, but the proof never connects them. The same property discharges TA-assoc's four preconditions with explicit bullets immediately above, so the loose TA-LC discharge is inconsistent with the property's own standard.

**Required**: Discharge TA-LC's preconditions explicitly: `Pos(d⊕d')` and `Pos(ℓ)` (the latter from T12); `actionPoint(d⊕d') = min(k_d,k_{d'}) ≤ k_d ≤ #s` (using consequence (iii)) and `actionPoint(ℓ) ≤ #s` (T12); `a := s`. Then the (ii)/(iii) enumeration earns its place rather than reading as orphaned.

### Issue 2: "level-uniform" / level_compat used before S6 defines them

**ASN-0053, WR (WidthRecovery) and "The reach function" prose**: "For a level-uniform span σ = (s, ℓ) with #s = #ℓ: reach(σ) ⊖ start(σ) = width(σ)."

**Problem**: The term *level-uniform* (and the supporting `level_compat`) is formally introduced only in S6, which appears two sections later (after Convexity and SpanClassification). WR, and the surrounding reach-function discussion ("For equal-length endpoints with a < b and #a = #b…"), use the concept before it exists. WR papers over this by re-spelling the definition inline ("with #s = #ℓ"), which is itself the redundancy symptom — the qualifier restates S6's definition. A reader hitting WR cannot evaluate "level-uniform" against a definition.

**Required**: Move S6 (the level constraint) ahead of WR, or introduce `level_compat`/level-uniform at first use. Then drop the redundant "with #s = #ℓ" rider from WR's statement.

### Issue 3: Population-evolution caveat stated twice

**ASN-0053, S9 closing prose and Open Question 1**: S9's closing says the normalized form "is unique *at a given instant* but depends on the ambient population… a span-set that minimally covers a target set of positions may need revision as new addresses are allocated between existing ones." Open Question 1 then asks "What abstract property must a span-set satisfy to guarantee that its normalized form remains valid as new addresses are allocated in the tumbler space?"

**Problem**: The same concern (normalized form is fixed-instant; address allocation can invalidate it) is developed in the S9 closing and re-posed as Open Question 1. Carrying it in both places is the "two paragraphs in different sections say the same thing" pattern the anti-bloat pass targets.

**Required**: State the caveat once. Keep the Open Question (it is the actionable form) and trim the S9 closing to the Nelson confirmation of existence/uniqueness plus a one-clause pointer, rather than re-developing the population-evolution argument inline.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound

The general difference bound S11d covers single-span minus single-span. The tight bound on `|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|` for span-sets is new territory (correctly logged as an Open Question), not a gap in this ASN.

### Topic 2: Cross-level intersection and subspace-boundary behavior

Intersection of spans at different hierarchical levels, and span guarantees at subspace boundaries, require relaxing the level_compat precondition this ASN deliberately assumes. Correctly deferred to Open Questions; not an error here.

VERDICT: REVISE
