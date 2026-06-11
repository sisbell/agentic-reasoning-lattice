# Review of ASN-0129

## REVISE

### Issue 1: V-IDX's universal-attachment condition is unsatisfiable at every constructible registry, and the note reasons about it as a live case

**ASN-0129, V-IDX (IndexedFamilies)**: "a body applying a *class-indexed* behavior-family atom (`is_filtered`, `succs`, `tip`, `age`, `stale`, …) at the bound class is well-formed only when the behavior is attached at *every* registered class" and "Universal attachment forces with it, by R-C0's compatibility, whatever record component the behavior constrains — the shape for BH1/BH2/BH3 (Unary, Binary, Binary respectively), `idem = ⊥` for BH4."

**Problem**: ASN-0128's R-C1 makes the three designated entries mandatory in every constructible registry, with fixed records (S1: `retired` Unary, idem=⊤, {BH1}; S2: `supersedes` Binary, idem=⊤, {BH2}; S3: `R` Binary, idem=⊤, ∅). Check each behavior against these: BH1 requires Unary and fails at `supersedes` and `R`; BH2 and BH3 require Binary and fail at `retired`; BH4 requires idem=⊥ and fails at all three. So universal attachment is impossible for every behavior family at every registry that can exist — the clause admits no well-formed term, ever. The note presents the condition as live ("the condition bites") and the "Universal attachment forces with it…" sentence derives consequences (e.g., an all-Unary registry under universal BH1) of an antecedent the foundation's mandatory entries rule out. This is a derived consequence the note must state: as written, the effective rule for `Reg`-quantified bodies is "core family, fixed-view slices, the class-unindexed `targets_keyed`, and V-PRIM's `·[K]` lookup — nothing else," and a reader cannot tell that from the text.

**Required**: State the vacuity explicitly as a consequence of R-C1/S1–S3 (or rescope the rule), and say what survives for `Reg`-bodies — in particular that the `·[K]` lookup is the designed route to per-class behavior data under non-uniform attachment. Delete or recast the "Universal attachment forces…" sentence so it does not analyze an impossible configuration as realizable.

### Issue 2: PC6's evaluation class never places V-TUP — the leaf enumeration and the node vocabulary disagree

**ASN-0129, PC6 (ExpressiveClosure)**: the class's nodes are "a base call …, a combinator from the admitted vocabulary (PC0's connectives, PC2's binder guard, V-PRIM's operations), or a single-pass fold …"; the base is "`Observe_K` …, the active-subset machinery derived from it, domain membership …, the registry lookup …, and the state-independent primitives (V-PRIM)"; yet the closing sentence asserts "`V_atom` with V-TUP and V-PRIM enumerates the leaf forms."

**Problem**: V-TUP appears in neither the base enumeration nor the admitted-combinator list, but both directions of the theorem rely on it. The converse's one substantive leaf check normalizes `Observe_K` into a QD filter whose body is built from V-TUP's per-tuple coverage tests — so V-TUP must be a leaf form, as the closing sentence says. The forward direction must evaluate PL terms containing V-TUP atoms (e.g., `(∃ x ∈ L_K :: t ∈ coverage_F(x))`) *within the class* — and the class as defined gives no node kind that performs a per-tuple read. The note's own standard ("a ceiling claim is circular until 'evaluable' is defined, so we fix its two parameters explicitly") makes this an internal inconsistency in the theorem's defining text, not a pedantic quibble.

**Required**: Place V-TUP explicitly — either in the base (per-tuple reads of in-hand stored values are read primitives) or in the admitted-combinator vocabulary — so the class definition and the leaf-enumeration sentence name the same leaf set.

### Issue 3: PC6's forward direction — "atoms are base calls or bounded-iteration combinators over them" — is false for the base as enumerated

**ASN-0129, PC6 (ExpressiveClosure)**: "*Forward*: structural induction — a PL term's control tree is its syntax tree (PC6a), its atoms are base calls or bounded-iteration combinators over them …"

**Problem**: Three families of PL leaves are not derivable from the enumerated base.

(a) *Coverage-membership tests need TumblerAdd.* Testing `t ∈ coverage(F)` for a general span requires forming the upper bound `s ⊕ ℓ` and comparing — ASN-0086's CoverageEqualityDecidable is explicit that coverage decisions use "T2 comparisons **and TumblerAdd**." V-PRIM deliberately admits comparisons only, and `⊕` appears nowhere in the base. So `is_K`, the V-TUP tests, and the nullified computation are not "combinators over the base." (V-TUP's own decidability line — "decidable span-by-span via T2" — repeats the elision and should cite TumblerAdd as ASN-0086 does.)

(b) *`age` needs home identification and chain arithmetic.* Computing `age(a)` requires identifying the homed-at-`d` set — T4 field extraction or zeros inspection, since `d ≼ a'` does not characterize `home(a') = d` (a link homed at sub-document `5.3` also extends document `5`) — and walking or counting `chain_d` positions, which needs `inc(·, 0)`. Neither field extraction nor `inc` is in the base or V-PRIM.

(c) *`C_dom` and `M_dom` are fold domains, but the base gives membership only.* QD admits `C_dom` and `M_dom` as quantification and `count` domains, so `count(C_dom)` is a PL term; the base provides "domain membership against `dom(Σ.C)`/`dom(Σ.M)`/`dom(Σ.L)`" — a test, not an enumeration — and no membership oracle over the infinite carrier `T` recovers a finite domain's element list. (`dom(Σ.L)` is recoverable as `⋃_K Observe_K`'s hist slices by P6; nothing analogous enumerates the content or arrangement domains.)

Without these, the "exactly" in PC6 fails in the forward direction: there are PL terms not computable by syntax-directed evaluation over the base as enumerated.

**Required**: Enlarge the base to what the atoms' derivations actually consume — enumeration reads for the three store domains, and the tumbler-structural operations on in-hand values (`⊕` per CoverageEqualityDecidable, `inc(·, 0)`, T4 field extraction) — or alternatively declare `V_atom` itself the base layer and restate the forward direction so the leaf claim matches the definition. Either repair must keep the converse's leaf check in sync.

## OUT_OF_SCOPE

### Topic 1: Predicate dynamics over the arrangement-edit transition vocabulary
**Why out of scope**: PD0–PD2 are explicitly scoped to `→_sh` (K.σ/K.α/K.λ_sh), and the note fences ASN-0127's layer as a separate query algebra. A deployment running both layers takes arrangement-edit steps (K.μ⁺/K.μ⁻/K.μ~, K.ρ, K.δ) under which the grow-only status of `M_dom` and the frame analysis would need re-derivation. That is a combined-layer stability theory — new territory, not an error here.

### Topic 2: Evaluation cost model
**Why out of scope**: PC5 proves termination, not bounds. A complexity model for PL evaluation (per-atom costs, fold sizes, the `chain` walk's measure as a budget) is implementation-facing future work, and nothing in this note depends on it.

VERDICT: REVISE
