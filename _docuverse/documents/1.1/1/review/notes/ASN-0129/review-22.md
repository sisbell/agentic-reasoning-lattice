# Review of ASN-0129

I checked the vocabulary generation (V through COD) against the ASN-0128 records, the QD/PC machinery including QD-fin's induction and PD0's stability ground, the PC6 converse leaf-by-leaf, and recomputed the five-state worked trace (both view sequences, the C3 discharge at Σ₄, and the chain indices) — all of which hold. Three issues remain, none structural.

## REVISE

### Issue 1: PC2's binder guard leaves the else-branch untyped, and the worked example leaves it uninstantiated

**ASN-0129, PC2 (ValueComposition) and Worked composition**: "compose only through the *binder guard* `if f(s) is some y then g(y, s) else c_default`" … "`head_live(t) ≡ if tip(t) is some h then ¬is_retired(h) else ⊥-case`"

**Problem**: PC2 types the condition (V-PRIM's `def`), the binder (`y` at the narrowed base type), and the then-branch (`g`, state-indexed, same Σ and view) — but says nothing about what `c_default` may be. Two readings are open: a V-PRIM constant only, or an arbitrary PL term of codomain C₂ (possibly state-reading). The two readings give different languages: the binder guard is PL's *only* conditional former (V-PRIM ships no general if-then-else), so for Boolean codomain a state-reading else is reconstructible through PC0 (`(def(f) ∧ …) ∨ (¬def(f) ∧ Q)`), but for `T`- or ℕ-valued results it is not — under the constant-only reading, value-codomain functions expressible under the term-reading are lost. PC6's ceiling statement and its converse quantify over the exact grammar ("a combinator from the admitted vocabulary … PC2's binder guard"), so the ambiguity propagates into the ceiling claim itself. The worked composition compounds it: `head_live` is exhibited with the metavariable "⊥-case" in the else slot, so what is shown is a term schema, not a PL term — the claimed reading "t's current head is unretired" is unrealized at the ⊥ branch, and the term's dynamics classification is undetermined by the exhibit.

**Required**: One sentence in PC2 fixing the else-branch's admissible forms (constant only, or any PL term of codomain C₂ evaluated at the same Σ and view), and an instantiated `head_live` (e.g., `else ⊥`, with the remark that the choice is the author's decision point retained).

### Issue 2: PC6's parity assessment surveys an incomplete ℕ fragment

**ASN-0129, PC6 (What the relativization costs)**: "Assessed against that fragment: a parity term would be a Boolean combination of comparisons among sums of counts and literals…"

**Problem**: The assessment narrows from "no PL term computes parity" to a survey of "PL's ℕ fragment as V-PRIM ships it" — counts, literals, `+`. But PL's ℕ-valued leaves are not exhausted by `count`: `age` (BH4 family) is an ℕ∪{⊥}-valued *state-reading* atom whose narrowed values enter ℕ position through PC2's binder, including inside quantified bodies over `L_dom` — `(∃ a ∈ L_dom :: age(a) = c ∧ …)` is an admitted Boolean term that is not "a comparison among sums of counts and literals." Whenever the registry attaches BH4 to any class, the claimed normal form for parity candidates excludes admitted terms without argument; and `age` is built from precisely the chain-index arithmetic (`f_d^Σ`) the granularity restriction otherwise fences off. The note's own standard makes the gap visible: Open Question 6's *self-emit* entry explicitly names the frontier-derived routes a proof must handle ("BH4's `age` is defined from the very quantity `f_d^Σ`"; the reflected `L_dom`), while the *parity* entry — resting on this same assessment — names none. The conjecture may well still stand; the assessment's inventory must match the vocabulary it assesses.

**Required**: Either scope the parity assessment to BH4-free registries explicitly (consistent with the ceiling being registry-pinned), or extend the survey to age-bearing terms, and record the route in OQ6's parity entry as is done for self-emit.

### Issue 3: Duplicated deliberateness/deferral prose across PC6a, C-reach, and Open Question 4

**ASN-0129, PC6a, C-reach, Open Question 4**: C-reach: "an app computes closure by iterating `succs` at agent time, and the substrate cannot be handed the loop. Mutually-recursive predicate definitions … must be unrolled at agent time — a deliberate exclusion, not an oversight; the successor that would consciously raise the ceiling is Open Question 4's." OQ4: "PC6a excludes recursion deliberately. If a forcing case arrives … the conscious extension is a bounded least-fixed-point operator … raising the ceiling by a named primitive rather than by accident."

**Problem**: The same content — the exclusion is deliberate, the conscious extension lives in OQ4 — is stated in C-reach and restated in OQ4's framing prose, and the agent-time point appears twice within C-reach's own closing paragraph ("iterating `succs` at agent time" / "unrolled at agent time"). PC6a additionally closes with a forward pointer to C-reach ("what the *semantics* can nonetheless express is the separate question C-reach addresses") on top of the intro bullet covering the same division. This is the accretion pattern the note carries a classifier for: defensive justification ("a deliberate exclusion, not an oversight") and multiple sites deferring to the same downstream slot.

**Required**: State the grammar fact once (PC6a), the conjecture status once (C-reach), and let OQ4 pose its measure-discipline question without re-asserting deliberateness; cut one of C-reach's two agent-time sentences.

## OUT_OF_SCOPE

### Topic 1: Evaluation atomicity relative to concurrent transitions
PC4 guarantees agreement of two evaluators *at the same Σ*; what discipline ensures a protocol's trigger evaluation is not interleaved with a `→_sh` step (snapshot semantics, fire atomicity) is scheduler machinery. **Why out of scope**: the note explicitly defers protocol constructions and their scheduler disciplines to the application layer; the sequential-state model makes per-state evaluation well-defined here, and the concurrency question is new territory, not an error.

### Topic 2: Cost model for PL evaluation
PC5 establishes termination, not bounds; a complexity account (per-atom costs over `|dom(Σ.L)|`, fold nesting depth) would be needed before any protocol latency argument. **Why out of scope**: the note's guarantees are purity and decidability; quantitative bounds are a separate, future layer over the same grammar.

VERDICT: REVISE
