# Review of ASN-0097

## REVISE

### Issue 1: Π11's "single closed form" is just `iproj`'s definition
**ASN-0097, §"Behavior Under State Transitions" (after Π11(c))**: "Pulling these into a single closed form, in every reachable state and every transition: `a ∈ iproj(d, e, Σ') ⟺ a ∈ cov(e) ∧ a ∈ ran(Σ'.M(d))` — a single-state characterization, which falls out of the definition of `iproj`."

**Problem**: This is literally the definition of `iproj` at state `Σ'`. It is not a "closed form" of any transition — it makes no claim about how `iproj(d, e, Σ')` relates to `iproj(d, e, Σ)`. The text acknowledges it "falls out of the definition," which is the giveaway.

**Required**: Either remove the alleged closed form, or state and prove an actual transition-level closed form (e.g., `iproj(d, e, Σ') = iproj(d, e, Σ) ∪ (cov(e) ∩ Δran) ∖ (cov(e) ∩ Δran⁻)` with `Δran`/`Δran⁻` as additions/removals in `ran(M(d))`).

### Issue 2: Mode II asserts `ran(M(d_v)) ⊆ ran(M(d))` without derivation
**ASN-0097, §"Three Modes of Displacement" (Mode II)**: "Forking a document `d` to a version `d_v` (via the `K.δ` + `K.μ⁺` composite J4 in ASN-0047) places `d_v` in `E_doc` and arranges `d_v` such that `ran(M(d_v)) ⊆ ran(M(d))` — sharing I-addresses with the source."

**Problem**: This inclusion is the entire load-bearing claim of Mode II. It is stated as a property of J4 but never derived. Without it, the conclusion that "any link whose endsets reach `ran(M(d))` may also reach `ran(M(d_v))`" does not follow. The ASN must establish this rather than assert it.

**Required**: Either (a) derive `ran(M(d_v)) ⊆ ran(M(d))` from J4's contract (with the contract restated, since J4 in another ASN is not self-contained), (b) state it as an explicit Π-claim and prove it, or (c) condition Mode II on a versioning assumption explicitly labeled as such.

### Issue 3: `iproj = Σ.M(d)(proj)` asserted but not derived
**ASN-0097, §"The Projection"**: "the two are connected by the arrangement: `iproj(d, e, Σ) = Σ.M(d)(proj(d, e, Σ))`."

**Problem**: This equality is subsequently used as a working identity (e.g., in the wp derivation step `def of ran` → `def of proj`). It is a non-trivial set equality between two differently-quantified definitions and should be proved once. A reader cannot assume it is a definition — both `proj` and `iproj` are independently defined above this line.

**Required**: One-line bidirectional proof immediately after the definition.

### Issue 4: Π6 has no proof, only a restatement
**ASN-0097, §"Projection Properties" (Π6)**: The justification given is "A single link projects into many documents simultaneously; each projection is determined by that document's arrangement alone."

**Problem**: This is the claim restated as its own proof. The actual argument — that `proj(d, e, Σ)` and `proj(d', e, Σ)` reference disjoint state components (`M(d)` and `M(d')` respectively) and are therefore each computable without consulting the other — is missing. Under the prompt's rule "No proof by checkmark," a one-sentence restatement is not a proof.

**Required**: Explicit derivation from Π5 + the disjointness of `M(d)` and `M(d')` as state components.

### Issue 5: `K.μ⁺_L` listed in Π12 but never defined or analyzed
**ASN-0097, §"Behavior Under State Transitions" (Π12)**: "`K.α`, `K.λ`, `K.δ`, `K.μ⁻`, `K.μ⁺`, `K.μ⁺_L`, `K.μ~`, and `K.ρ` all carry such a frame on documents other than their target..."

**Problem**: `K.μ⁺_L` appears in this list but is never defined, analyzed, or distinguished from `K.μ⁺` in the ASN's projection analysis (Π8 covers `K.μ⁺` generically). If it is link-subspace extension, its effect on `M(d)` and on link-subspace projections requires separate treatment; if it is subsumed by Π8, the ASN must say so.

**Required**: Either remove `K.μ⁺_L` from Π12 with the note that it is subsumed by `K.μ⁺`, or add a sentence specifying its scope and how Π8 applies.

### Issue 6: Π12's enumeration confuses "frame on other documents" with "no document target"
**ASN-0097, §"Behavior Under State Transitions" (Π12)**: "`K.α`, `K.λ`, `K.δ`, `K.μ⁻`, `K.μ⁺`, `K.μ⁺_L`, `K.μ~`, and `K.ρ` all carry such a frame on documents other than their target..."

**Problem**: `K.α` (content allocation) and `K.λ` (link allocation) do not have a "target document" — their frame is universal (they modify no `M(d)`). Lumping them with document-targeted operations under "frame on documents other than their target" is imprecise. Π13 and Π14 already handle these cases separately, which suggests the unified framing in Π12 is wrong.

**Required**: Either restrict Π12 to operations with a document target (`K.μ⁻`, `K.μ⁺`, `K.μ~`, etc.) and let Π13/Π14 handle the others, or restate the frame condition uniformly (e.g., "operations whose write set does not include `M(d)`").

### Issue 7: Π13's claim does not match Π13's proof scope
**ASN-0097, §"Behavior Under State Transitions" (Π13)**: The claim is `(A d, e, ℓ ∈ dom(Σ.L) : proj(d, e, Σ) = proj(d, e, Σ'))`.

**Problem**: The quantifier is over `ℓ ∈ dom(Σ.L)` but `ℓ` does not appear in the projection arguments — only `e` does. Either the quantifier should be over endsets (and pulled from `Σ.L(ℓ)` for some `ℓ`), or `ℓ` should be removed. As stated, `ℓ` is unbound on the right-hand side.

**Required**: Fix the quantifier — either `(A d, ℓ ∈ dom(Σ.L), i :: proj(d, ℓ, i, Σ) = proj(d, ℓ, i, Σ'))` or `(A d, e :: proj(d, e, Σ) = proj(d, e, Σ'))`. Same issue applies to Π14.

### Issue 8: Worked example does not test cross-document or reverse-orphaning claims
**ASN-0097, §"A Worked Example"**: The example traces a single document `d` through K.μ⁻, K.μ~, and a counterfactual K.μ⁺.

**Problem**: The example exercises Π9, Π10, Π11. It does not verify Π6 (cross-document independence), Π12 (cross-document frame), Π15a/b (reverse orphaning), Π16/17 (reach), or any CCR-dependent behavior. Per the prompt's "concrete example" requirement, the example should verify key postconditions — but several of the more subtle R-guarantees (R10 cross-document, R11 reverse orphaning, R12 discovery) get no concrete witness.

**Required**: Extend the example with a second document `d'` to witness R10, and a reverse-orphaning step to witness R11. At minimum, add one scenario where `proj(d, e, Σ) = ∅` but `proj(d', e, Σ) ≠ ∅`.

### Issue 9: Π11's transition claim and "transition content" sentence contradict each other
**ASN-0097, §"Behavior Under State Transitions" (after Π11(c))**: "The transition content of Π11 is the monotonicity above: K.μ-class transitions move `iproj` only in the direction the operation moves `ran(M(d))`."

**Problem**: This "transition content" is just Π11(a)+(b)+(c), already stated and proved. Calling it the "transition content" *after* labeling the prior line a "closed form" suggests the author is trying to make Π11 sound stronger than it is. The redundancy obscures rather than clarifies.

**Required**: Either collapse the redundant framing into the original Π11 statement, or articulate a genuinely new synthesis claim (e.g., a single composed inequality covering all three K.μ cases under unification).

## OUT_OF_SCOPE

### Topic 1: Composition of operations and path-independence of cumulative projection changes
**Why out of scope**: The open questions raise this directly. A theory of composite transitions over `M` belongs in a future ASN on operation composition, not in the per-operation projection analysis here.

### Topic 2: Endset algebra (union, intersection, complement) and projection distribution
**Why out of scope**: Listed in open questions. This is a generalization belonging to a future ASN on the algebra of endsets.

### Topic 3: Resolution of the CCR axiom
**Why out of scope**: The ASN correctly identifies CCR as an open structural choice and conditions R13 accordingly. Settling CCR is the work of ASN-0094's successor consultation, not this ASN.

### Topic 4: Single-valuedness of projection across all reachable states
**Why out of scope**: Listed in open questions. The projection function is single-valued by construction (set-builder definition), but the question of whether `M(d)` remains a function under all reachable transitions is a state-invariant question for a separate ASN on `M`'s well-formedness.

VERDICT: REVISE
