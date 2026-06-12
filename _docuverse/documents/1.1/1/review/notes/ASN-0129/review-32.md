# Review of ASN-0129

## REVISE

(none)

I verified the note at three depths before reaching this verdict.

**Claim-level checks.** The worked trace was recomputed step by step: gate verdicts (Sh-conf at cmt/res/retired), dedup branches (I5 for idem=⊥, I1 misses against empty active classes), landing conditions (C2/C3 at each deposit, including the DR/R0a discharge at Σ₄), the nullification scope at Σ₃ (subtree(a₂) ∩ A_rel = {a₂}, a₁ untouched), and all three value sequences — active ⊤⊥⊤⊥⊥, default ⊤⊥⊤⊥⊤, and `ever_res` ⊥⊥⊤⊤⊤ — come out exactly as written, including the vacuous-⊤ boundary case at the empty store, which the note flags with the activity-witness caveat rather than hiding. The four spotlight compositions (OPEN, quiescent's three spellings, under_cap/out_capped, head_live, targets_under, the Reg universal) all type under WT's rules as stated, and the Reg universal's body is core-family-only, so V-IDX's instance-wise condition holds at every registry as claimed.

**Proof-level checks.** QD-fin's induction is complete (base R-VAL, step by the frame clauses, slice finiteness via ASN-0086's address injectivity). PD0's ground was checked rule by rule: filter grow-only-ness genuinely needs both base growth and ST-body persistence and the proof supplies both; the aggregate polarity rules are each one-directional and the note correctly places `count = c` in neither class and excludes T1-extrema rather than hand-waving them in. PD2's active-view clause names all three cross-type leaks (retraction, BH4's home-wide footprint, `targets_keyed`'s cross-type join) — I could construct no fourth: the footprint table in FP is exhaustive against the atom inventory. PC6's converse was checked at its one non-trivial leaf (the Observe_K filter spelling matches ASN-0086's matching-set definition exactly, with V-TUP supplying the per-tuple conjuncts) and at the registry-lookup leaf (constant-folding is sound because the statement quantifies over *functions*, not terms). The two conjectures are correctly held at conjecture status, and the C-reach caveats against citing FO-inexpressibility are accurate — the out-degree-≤-1 observation that `is_in_chain` *is* `reach` on thin graphs is a real obstruction, not rhetoric. C-emit's grammar fact was independently confirmed: expressing `a_emit(Σ, d)` needs address construction (`inc`, excluded) and a home-grouping atom (absent), and `age` exposes frontier-relative indices, never the frontier address.

**Anti-bloat pass.** The flagged accretion patterns were searched for specifically. The dense rationale paragraphs (the `age` totalization, PC2's else-branch reading, the `Reg`-restriction grounding, UV's reconciliation of ASN-0128's two sentences) each fix a semantic commitment a builder needs, not defensive meta-prose — UV's reconciliation in particular is the place where an upstream ambiguity ("does not rewrite the walk" vs. the open default-view question) gets a binding reading, which is content, not justification. The three deferrals to Open Question 6 are the status lines of three distinct conjectures, not relocated findings. The "additions are six, each fenced" inventory is load-bearing for the extension-language claim (composition is the only mechanism, so the new-atom census must be exact). Nothing rose to a finding.

## OUT_OF_SCOPE

### Topic 1: Trace-level (temporal) predicates
**Why out of scope**: PL is single-state by design (PC6 excludes temporal operators), and cross-state properties — "P held before Q," "P stable for k steps" — are recoverable only obliquely through PD0's stable classes and BH4's per-home ordinal time. A protocol-layer temporal language with proof rules for convergence arguments is new territory; the note correctly fences protocol constructions out rather than gesturing at them.

### Topic 2: Cost semantics for evaluation
**Why out of scope**: PC5 delivers termination, deliberately not bounds. Which QD filters and folds admit index-accelerated evaluation (enfilade-backed), and what cost contract the substrate should expose for trigger evaluation at scale, is a future ASN — nothing in this note's guarantees depends on it.

### Topic 3: Evaluation interleaved with transitions
**Why out of scope**: PC4 covers two evaluators at the *same* Σ. What an evaluation in flight across a →_sh step observes — snapshot atomicity of a single term — is an isolation discipline belonging to the scheduler/protocol layer the note defers, not to the predicate foundation.

### Topic 4: Rounding out V-PRIM's set fragment
**Why out of scope**: V-PRIM ships membership, equality, and emptiness but no set literals or binary union. The common cases have PL spellings (pointwise disjunction for union membership; count-of-union via a complement filter), and PC6 already frames vocabulary gaps as deliberate, individually closable admissions — with the caveat, worth carrying forward, that any admission interacts with the parity candidate's normal-form argument, so rounding out the fragment is a ceiling-affecting design decision for a future note, not an omission here.

VERDICT: CONVERGED
