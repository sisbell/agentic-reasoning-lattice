# Review of ASN-0129

The note is in strong shape — the trace is genuinely computed, the ceiling theorem is honest about its relativization, and the dynamics classification is grounded per rule. Four issues remain: one completeness gap in QD-audit's own coverage argument, one transfer-citation that skips a hop, and two anti-bloat findings (a near-verbatim internal duplication in PC6, and an unproven excluded-case aside in PD0 whose one-phrase proof is also mislabeled).

## REVISE

### Issue 1: QD-audit's surface-check expressibility argument covers only one disjunct of P-tgt
**ASN-0129, QD-audit (BaseReadAudit)**: "a gating discipline written in PL must be able to state what the surface checks; V-DOC admits exactly that test, as `is_doc`. The link store's analogous surface check, `Nullify_Binary`'s P-tgt residence clause `a ∈ A_rel^Σ` (S3), needs no atom of its own: it is already PL-expressible as membership in the reflected `L_dom`."

**Problem**: P-tgt (S3, ASN-0128) is a disjunction: `a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr)`. The audit's stated principle is that a PL-written gating discipline "must be able to state what the surface checks," and it then presents only the residence disjunct as "the surface check." The self-emit disjunct is *not* PL-expressible, and not incidentally so: `a_emit(Σ, d) = chain_d(f_d^Σ)` requires the homed-set (`home(a') = d`, which PC6 itself says prefix testing cannot characterize and which no atom exposes) and `inc(·, 0)` arithmetic (excluded from V-PRIM by design). So the surface's actual target check is only partially statable in PL, and QD-audit neither says so nor says why that is acceptable — by the audit's own standard, this is a silently elided gap in the very paragraph whose job is to be the exhaustive accounting.

**Required**: Scope the sentence to the residence disjunct explicitly and add the acknowledgment: the self-emit disjunct reads the frontier address, an emit-side quantity PL deliberately does not expose (consistent with V-PRIM admitting no address arithmetic and PC6's atom granularity), so a PL gate can state P-tgt's residence clause but not its self-emit clause — a deliberate exclusion, stated. (Alternatively, argue that a gating discipline never needs the self-emit disjunct, and say why.)

### Issue 2: PC6 states the same granularity point twice; the internal-iteration point appears three times
**ASN-0129, PC6 (ExpressiveClosure)**, base-fixing prose: "The stopping point is forced by the converse below, whose proof method is normalization — a PL spelling per leaf — and a raw arithmetic leaf, `t ⊕ w` on a query argument, has none: V-PRIM admits the comparisons and no address arithmetic."
Then, same section, costs paragraph: "The *granularity* restriction is priced where the base is fixed: an exposed arithmetic leaf (`t ⊕ w` on a query argument) has no PL spelling — V-PRIM admits comparisons, never address arithmetic — so the converse's normalization fails at it…"

**Problem**: These are the same point — same example, same reason, same consequence — stated twice within one section in nearly identical words. This is the anti-bloat duplication pattern. Secondarily, the internal-iteration point is stated three times across the note: V ("Atoms may be *internally iterative*… the composition primitives below add none"), PC6 ("internal iteration permitted only here, behind the atom's own termination bound: `chain` is a bounded-iteration combinator…"), and PC6a ("atoms' internal iteration (the `chain` walk) is bounded behind its own termination proof and contributes a leaf, not an unrolling").

**Required**: State the `t ⊕ w` point once — the natural home is the costs paragraph, which adds the paired-admission remedy; the base-fixing sentence can carry a bare pointer or nothing. Consolidate the internal-iteration point to one full statement (PC6's evaluation-class definition is where it bears weight) with at most a parenthetical citation at the other two sites.

### Issue 3: PD0's excluded-case parenthetical asserts an unproven stability claim, and "the same witness argument" is not the same argument
**ASN-0129, PD0 (AuditMonotonicity)**: "(the guarded lower bound `if max_{T1}(D) is some m then m ≥ a₀ else ⊥` over grow-only `D` is ⊤-stable by the same witness argument, but we keep the class to the enumerated forms)"

**Problem**: Two defects. First, this asserts a stability theorem for a form the classification explicitly excludes — a case the class's enumeration already rules out, the anti-bloat pattern of imagining an excluded case. Second, the one-phrase proof is wrong as labeled: the existential rule's argument is witness persistence — the witness stays in the domain and is re-read. Here the term does not re-read the witness; it reads the *new* maximum of the grown domain. The actual argument needs two steps the witness argument does not contain: the old maximum `m` remains a member of `[D]_{Σ'}`, so `max_{T1}([D]_{Σ'}) ≥_{T1} m` (maximum dominates members), and T1 transitivity then carries `≥ a₀`. A claim outside the class, proven by a mislabeled "similarly," is exactly the kind of aside the standards forbid.

**Required**: Either delete the inner parenthetical (the exclusion sentence before it stands on its own), or admit the guarded form into ST's enumeration and give the two-line proof (non-emptiness persists; new max dominates the old by membership; transitivity).

### Issue 4: R3's transfer to extended-record steps cites RP-b alone, skipping the B2 hop
**ASN-0129, PD0, grow-only definition**: "per-type slice growth is R3, ASN-0086, carried across extended-record steps by RP-b"

**Problem**: RP-b (ASN-0128) is stated for ASN-0126 claims — its proof reads "the ASN-0126 claim applied there constrains ρ(Θ)." R3 is an ASN-0086 transition lemma quantified over ASN-0086's `→`-steps; its route to extended-record `→_sh` steps is ASN-0126's B2 (which carries ASN-0086 transition invariants across genuine `→_sh` steps) composed with RP-b. The note knows this — every other ASN-0086 transition-invariant transfer in the document cites the full chain ("L12a per step and L12, both carried across extended-record steps by ASN-0126's B2 with RP-b, ASN-0128"). This one citation omits the B2 hop, breaking the note's own per-step citation convention at a load-bearing point (the grow-only definition is what PD0's entire ⊤-stability theorem rests on).

**Required**: Cite "B2 with RP-b" — or drop the R3 citation entirely and rest on the step effects, which the same parenthetical already cites (GatedTransitionRelation's frames plus the fresh-key adjunction give per-type slice growth directly).

## OUT_OF_SCOPE

### Topic 1: A frontier-address read atom
Issue 1 asks only that the inexpressibility of P-tgt's self-emit disjunct be acknowledged. Whether the read surface *should* expose the frontier (`a_emit`/`chain_d(f_d)`) as an atom — enabling gates that state the full P-tgt, or RangeSterilization-aware gates ("the next deposit homed at d lands sterilized") — is a vocabulary-design question for a future ASN, with its own footprint and dynamics consequences.

**Why out of scope**: Admitting a new atom changes the base, the ceiling (PC6), and the footprint classification (FP/PD2) together; that is a deliberate extension in the sense of PC6's "paired admission," not an error in this note.

### Topic 2: Completeness of the PD0 classification
PD0's classes are syntactic and sufficient, not complete: the audit-view membership atom `is_K` is extensionally ⊤-stable (it equals an existential over grow-only `L_K` with a step-constant body, per PC3's cross-view lemma) but is not in ST's enumerated forms — a user must use the spelled-out existential, as the note's own `ever_res` does. A classifier that closes ST under the cross-view lemmas, or certifies stability for terms mixing views and polarities, is Open Question 5's territory.

**Why out of scope**: The note acknowledges the enumeration boundary explicitly and records the mechanical-certification question as OQ5; an incomplete-but-sound classification is a design choice, not a defect.

VERDICT: REVISE
