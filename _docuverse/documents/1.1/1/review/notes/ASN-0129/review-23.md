# Review of ASN-0129

## REVISE

### Issue 1: PD0's certified classes cannot classify quantification through a bound tuple's endset members — the gap sits on the note's own recommended path
**ASN-0129, PD0 (AuditMonotonicity)**: "Call a domain expression *grow-only* iff it is `L_K` or `L_dom` … or `M_K` in an audit-view term … or a filter `{x ∈ D : P(x, ·)}` with `D` grow-only and `P(x, ·) ∈ ST`" together with "*Quantifiers*: `(∃ x ∈ D :: P) ∈ ST` when `D` is grow-only and `P(x, ·) ∈ ST`."

**Problem**: The quantifier rules fire only over grow-only domains, and the grow-only list omits step-constant domains — in particular the bound-tuple V-TUP sets `addrs_F(tup)`, `addrs_G(tup)` that QD's set-valued closure admits as domains. Take the audit-only term

`(∃ tup ∈ L_K :: x ∈ addrs_F(tup) ∧ (∃ y ∈ addrs_G(tup) :: is_K'(y)))`

— "some K-tuple from x has a target that was ever a K'-member," evaluated entirely against audit slices. The outer ∃ is over grow-only `L_K`; the first conjunct is a step-constant; the inner body `is_K'(y)` is ST by PD0's own audit-membership clause. But the inner existential's domain `addrs_G(tup)` is in no grow-only clause, so the inner ∃ gets no verdict, the conjunction gets none, and the whole term is unclassified — despite being genuinely ⊤-stable (the domain is constant once `tup` is bound, since the stored value is immutable, and a finite disjunction of ST terms is ST by PD0's own Boolean rules). I checked for certified re-spellings: quantifier inversion rescues only bodies whose y-condition is itself membership in a grow-only domain (`(∃ y ∈ M_{K'} :: y ∈ addrs_G(tup))` works); for coverage-test bodies like `is_K'(y)`, and for the ∀ duals ("every target of every K-tuple is ever-acknowledged"), no certified spelling exists — there is no grow-only domain carrying the targets. PD0 acknowledges spelling-level incompleteness, but the note added explicit clauses precisely where natural spellings needed them (the audit-membership and reflected-set clauses), and PD1 plus the closing paragraph make this class load-bearing advice: "a sound 'stop when Q' wants Q in PD0's class." Any audit-anchored Q that inspects endset members through a tuple falls outside the class as the rules stand.

**Required**: Extend the grow-only class with step-constant domains — any domain expression whose denotation is fixed once its parameters are bound (the V-TUP set terms; the ground is immediate: a constant set is contained in itself across steps, and L12 via B2/RP-b fixes the stored value the projection reads). Optionally also certify audit-view `targets_of` and `⋃(D, f)` with `D` grow-only and `f` step-constant, by the note's existing "atom whose definition is a certified spelling" method.

### Issue 2: C-reach narrates the document's revision history instead of stating the proof obligation
**ASN-0129, C-reach**: "An earlier framing argued it from the inexpressibility of transitive closure in fixed-quantifier-depth first-order logic over finite structures; that argument is unsound for PL as actually defined, on three counts."

**Problem**: This is reviser-drift in the named form — prose addressed to someone who read a prior version, explaining why removed content was removed. The three counts (i)–(iii) are substantive and should stay: they characterize what any future proof must overcome (walk atoms decide reach on out-degree-≤ 1 families; PC2a's counting exceeds plain FO; built-in total orders degrade locality bounds). The "earlier framing" archaeology is the noise; the next reader has no earlier framing.

**Required**: Restate as direct constraints on the obligation — e.g., "A proof cannot proceed by citing FO-inexpressibility of transitive closure, on three counts: (i)…" — and delete the reference to the prior version of this note.

### Issue 3: Three sections defer to Open Question 6, and Open Question 6 re-derives their content
**ASN-0129, QD-audit / PC6 / C-reach / Open Question 6**: QD-audit: "(whether some extensionally equal term computes the test anyway is Open Question 6's self-emit conjecture)"; PC6: "recorded in Open Question 6's parity entry"; C-reach: "we record the proof obligation as Open Question 6 rather than discharge it by citation."

**Problem**: This is the flagged multi-site-deferral pattern, and the duplication is two-way. PC6 already states the BH4 route in full ("A registry attaching BH4 anywhere adds the leaf this normal form omits: `age`'s narrowed values enter ℕ position through PC2's binder, quantified bodies over `L_dom` included…"); Open Question 6 then restates the same route in different words ("at a BH4-attaching registry `age`'s narrowed values are ℕ-valued leaves beyond counts and literals — entering quantified bodies over `L_dom` through PC2's binder — frontier-derived data again"). The self-emit assessment is likewise split between QD-audit's long passage and OQ6's restatement of the frontier-derived routes (`age` from `f_d^Σ`, `L_dom` via QD-refl). A reader following any one conjecture must read the same assessment in two places to confirm nothing differs.

**Required**: One site per assessment. Either the body sections (PC6, QD-audit, C-reach) carry the full assessments and OQ6 lists the three obligations with bare pointers, or OQ6 carries the assessments and the body sections carry one-clause pointers. Not both.

### Issue 4: Ownership and mechanics prose stated twice — the OQ1-closing claim and the `targets_keyed` join
**ASN-0129, V and UV; V and V-IDX**: V: "the behavior atoms' default-view readings are this note's own, fixed at UV — ASN-0128 left them open (its Open Question 1)"; UV: "ASN-0128 committed the collection rule for `members` and `targets_of` and left the behavior surfaces open (its Open Question 1); UV closes the question…" And V: "*class-unindexed*: a single global atom joining `target_of` across every BH3-attached Binary type (FP), which each BH3-attached class's family contributes identically, the union over K collapsing the contributions to one symbol"; V-IDX: "the class-*unindexed* `targets_keyed` — BH3's join across every BH3-attached Binary type, indexed by no single K (FP), occurring as the same closed atom in every expansion instance."

**Problem**: Two instances of the same-claim-twice pattern. The provenance claim ("ASN-0128 left it open; this note closes it") appears in V's fencing inventory and again as UV's opening; the `targets_keyed` collapse-to-one-symbol mechanics are explained in V and re-explained in V-IDX (and the cross-type *footprint* consequence is then legitimately re-stated at FP and PD2 — those sites do new work and are fine). The fencing inventory in V is the right single home for provenance; V-IDX needs only the fact that `targets_keyed` is the same closed atom in every expansion instance, not the re-derivation of why.

**Required**: Keep the provenance accounting once (V's inventory is the natural site; UV then just defines and cites V). Keep the join mechanics once (V); V-IDX cites them and states only its instance-wise consequence.

### Issue 5: The parity assessment denies an operator it exhibits two clauses later
**ASN-0129, PC6 (relativization-costs paragraph)**: "that fragment supplies no doubling or modular operator, no ℕ quantifier, and no evident domain expression denoting a half-sized witness — `count(L_dom) = count(D) + count(D)` is the right shape…"

**Problem**: `count(D) + count(D)` *is* doubling, built from V-PRIM's admitted `+` — the sentence's own continuation exhibits it. What the fragment actually lacks is a halving witness (a domain `D` with `2·|D| = |L_dom|` exactly at even states), an ℕ quantifier, and a modular operator. In a paragraph whose entire job is precision about what the normal form omits, claiming an absent operator that the next clause constructs is a flaw the conjecture's eventual prover will trip over.

**Required**: Drop "doubling" from the missing-operator list (or replace with "halving"); the surrounding argument already carries the correct content.

## OUT_OF_SCOPE

### Topic 1: PL's status at states reached by arrangement-edit transitions
The note's state class `S` is the `→_sh*`-reachable extended-record states — `K.σ ∪ K.α ∪ K.λ_sh` only. A substrate that also takes ASN-0127's arrangement-edit steps (`K.δ`, `K.μ⁺`, `K.μ⁻`, `K.μ~`, `K.ρ`) reaches states outside `S`, where PC4–PC6 and PD0–PD2 are formally silent even though every PL footprint (link store, `dom(Σ.M)`, registry) is plausibly preserved or extended by those steps.
**Why out of scope**: The note draws the ASN-0127 boundary explicitly and inherits ASN-0128's transition relation; unifying the two relations and re-proving the dynamics over the combined step vocabulary is integration work for a future ASN, not an error in this one.

### Topic 2: Evaluation cost model
PC5 proves termination; nothing bounds cost. A trigger-heavy runner evaluating PD2-classified terms on every fire needs per-term complexity guarantees (e.g., footprint-proportional evaluation, incremental re-evaluation under PD2's non-interference).
**Why out of scope**: Complexity and incrementality are a new commitment layer over the denotational language this note fixes; nothing here is wrong without them.

VERDICT: REVISE
