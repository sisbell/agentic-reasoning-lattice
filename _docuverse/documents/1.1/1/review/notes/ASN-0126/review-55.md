# Review of ASN-0126

This is a strong note: P1, P3, P5, P6 have crisp statements with real derivations, the wp analysis is genuinely non-trivial (the C3-becomes-live observation), the projection bridge to ASN-0086 is sound, and the worked illustration checks the key postconditions against concrete addresses (including a born-nullified witness that exercises the gate-vs-landing separation). The findings below are localized; none invalidates the core results, but each is real.

## REVISE

### Issue 1: The C2 self-nullification example names the wrong operation and omits a gate conjunct

**ASN-0126, "The shape-gated emit" (wp, C2 paragraph)**: "C2 … fails for a *self-nullifying retraction* … this is ASN-0086's supported self-emit Nullify (its `P-tgt` branch `a = a_emit(Σ, d_retr)`), and it clears the gate because R is Binary and the unit-depth wrapper `G = {(a, δ(1, #a))}` is one Binary-conformant span."

**Problem**: Two defects, both pointing the same way.

1. *Wrong referent.* ASN-0086's self-emit Nullify is `Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` with `F = ∅`, so `|F| = 0`. By Binary's `Sh-conf` (`|F| = |G| = 1`) this fails the gate — and the note's own Single-source section says so emphatically: the `|F| = 1` rule "excludes *every* empty-from emit," and ASN-0086's Nullify "has **no** `→_sh` image." So "ASN-0086's supported self-emit Nullify … clears the gate" directly contradicts the note's earlier claim. What actually clears the gate is the *Binary re-expression* of the self-emit retraction, with the canonical from-fill `F = {r}`.
2. *Incomplete justification.* Binary requires `|F| = 1` **and** `|G| = 1`. The gate-clearing reason cites only G ("the unit-depth wrapper `G` … is one Binary-conformant span") and never establishes `|F| = 1`. Since the relevant F here is `{r}` (not `∅`), the conjunct does hold — but the note doesn't say so, leaving the gate-clearing argument missing half its premise.

**Required**: Replace "ASN-0086's supported self-emit Nullify" with the Binary-wrapped self-emit retraction (canonical from-fill `F = {r}`, `|F| = 1`; `G = {(a_emit, δ(1, #a_emit))}`, `|G| = 1`), and state both span-count conditions as the gate-clearing fact. Reconcile explicitly with Single-source's "no `→_sh` image" claim for the empty-from form.

### Issue 2: P2 is given two distinct meanings under one label

**ASN-0126, "Registry permanence"**: "`shape(K)` depends only on the P1-invariant registry, hence is constant on `→_sh*` (P2)"
**ASN-0126, "Registration entries"**: "This is what makes `shape(·)` a function of the type-as-coverage-class … — the well-definedness P2 asserts."

**Problem**: "P2 (ShapeStability)" is invoked for two different properties with two different premises:
- *State-stability* — `shape(K)` is constant across reachable states; premise is P1 (registry invariance). This is the reading P4's derivation actually uses ("`shape(K)` is registry-determined and the registry is invariant").
- *Coverage-class well-definedness* — `shape(K) = shape(K')` whenever `K ~ K'`; premise is C0 (unique coverage-class keys).

These are not the same claim, and C0 — the premise for the second reading — is stated in a later section than where P2 is "stated and derived." P2 never receives a single precise statement, yet it is cited by number in three places (and underpins P4 and P6).

**Required**: Give P2 one crisp statement. If it is meant to cover both facts, state both conjuncts and attribute premises correctly (state-stability ← P1; coverage-class well-definedness ← C0), and acknowledge the forward dependence on C0 at the point P2 is derived.

### Issue 3: Meta-prose flagged by the note's own anti-bloat classifier

**ASN-0126, "The shape-gated emit" (wp)**:
- "The conjunct accounting is then complete: every named gate component is either present in the wp or shown absorbed." — an exhaustiveness/closure claim that advances nothing; the reader can already see which conjuncts appear. This is the clearest offender.
- "The first two conjuncts are this note's contribution; the remaining three are inherited verbatim." — a provenance inventory that does not advance the wp computation.

**Problem**: These are precisely the "exhaustiveness claims" and "use-site inventories" the `review-mode.anti-bloat` classifier targets. The two absorption arguments preceding the closure sentence (for `K ∈ T_admissible` and for L3) do real work — they discharge why those guards do not surface in the wp — but the closure sentence on top of them is redundant self-certification.

(Lesser instance, not separately required: the "Properties established" section lists P1–P5 as pure redirections while stating P6 in full — a hybrid index/content slot. If kept, prefer making it a uniform index.)

**Required**: Delete the completeness-closure sentence; drop or inline the provenance annotation.

## OUT_OF_SCOPE

### Topic 1: Empty-registry degeneracy
If `Σ_init.registry = ∅`, precondition (i) never holds, so no `K.λ_sh`-step ever fires and `dom(Σ.L)` is permanently empty. This is a consistent (if useless) configuration, and Open Question 4 ("Does the substrate ship any types pre-registered?") is the right home for whether `Σ_init.registry` may be empty.
**Why out of scope**: A consequence for the successor note on standard registrations, not an error here.

### Topic 2: Homogeneity of Multi tuples
A Multi registration accepts `G = ∅`, `|G| = 1`, and `|G| ≥ 2` tuples under the same type, so "what a Multi tuple means" is not pinned by shape alone.
**Why out of scope**: This is the behavior/predicate semantics deferred to Open Questions 2 and 3.

VERDICT: REVISE
