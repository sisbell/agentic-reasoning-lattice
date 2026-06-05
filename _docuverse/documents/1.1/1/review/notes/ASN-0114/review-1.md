# Review of ASN-0114

## REVISE

### Issue 1: No concrete worked example verifying the postconditions

**ASN-0114, throughout**: The note states F0–F8 and derives F2 from F1, but never instantiates any claim against a specific link.

**Problem**: The review standard requires that an ASN "verify its key postconditions against at least one specific scenario." Every claim here is stated and discharged abstractly. The two claims that most need a witness — F2 (a disconnected end forces `|R| ≥ 2`) and F7 (valid-empty `⟨⟩` vs invalid `⊥`) — are exactly the ones a reader cannot check without a concrete instance. Gregory's evidence supplies candidates (the `orglinks.c:412–413` multi-region endset for F2; the `sporgl.c:93` empty-end path for F7), but no worked instance is given.

**Required**: Add at least one concrete scenario, e.g. a link `a` with `e₁ = {(s₁,ℓ₁), (s₂,ℓ₂)}` whose coverage is disconnected and `e₁`-request checked against F1/F2, plus an empty-slot request checked against F7 (returns `⟨⟩`) versus an out-of-range selector (returns `⊥`).

### Issue 2: `followlink(Σ, a, i)` is used both as a non-deterministic relation and as a determinate value

**ASN-0114, F0/F3/F7**: F0 says "the returned span-set `R`"; F3 says "any two span-sets `R, R'` each satisfying F1 ... are denotationally equal" (i.e. the result is *not* unique as a span-set); yet F7 writes `followlink(Σ, a, i) = ⟨⟩` as a literal equality of values, and F5/F6/F8 write `followlink(...)` as a single term.

**Problem**: Three distinct gaps follow from leaving the operation's status (function vs. relation) unfixed:
1. **Realizability never established.** F0 asserts a satisfying `R` exists but never shows one. (It is trivial — `eᵢ ∈ Endset = 𝒫_fin(Span)` is already a finite set of well-formed spans, so any ordering of `eᵢ` is a span-set with identical coverage — but this one line is the basis of the entire wp claim and is omitted.)
2. **F7's `= ⟨⟩` presupposes determinism F3 denies.** For a non-empty end the result is not a unique span-set, so writing `followlink(...) = ⟨⟩` as plain equality (not under `coverage(·)`) only makes sense for the empty case.
3. **Uniqueness of `⟨⟩` for the empty end is unjustified.** That `⟨⟩` is *the* answer for an empty end (not merely *an* answer with coverage `∅`) depends on ASN-0053 S2 (every well-formed span denotes a non-empty set), which forbids any nonempty span-set with empty coverage. S2 is never cited.

**Required**: State whether `followlink` is a relation (claims read "for any `R` satisfying F1") or a function returning a canonical/normalized span-set. Note the trivial realizability of `R` from `eᵢ`. Justify F7's `= ⟨⟩` by citing S2 to show `⟨⟩` is the unique coverage-`∅` span-set.

### Issue 3: F5's derivation overstates which premises are load-bearing

**ASN-0114, "Determinism over time"**: "This composes two distinct facts, and it is worth seeing that both are load-bearing. ... Remove either fact — make link values mutable, or bind ends to positions rather than to content identity — and F5 fails."

**Problem**: F5 as formally stated is a *coverage-equality* claim: `coverage(followlink(Σ', a, i)) = coverage(followlink(Σ, a, i))`. Its derivation uses only L12 (`Σ'.L(a) = Σ.L(a)` ⟹ equal endset ⟹ equal coverage). Content-identity addressing is **not** load-bearing for this claim: if ends were bound to V-positions instead of I-addresses, L12 would still fix the recorded spans, so the coverage would still be constant and F5 would still hold — only the *semantic* reading ("same material") would change. The claim "bind ends to positions ... and F5 fails" is therefore false for F5 as written; content-identity is load-bearing for a stronger material-permanence statement that F5 does not formally make.

**Required**: Either restrict the prose to "L12 is what F5 needs; content-identity addressing is what makes coverage-permanence mean material-permanence — a separate, stronger reading," or promote F5 to an explicit material-permanence claim and then show content-identity in the derivation chain. As written the derivation and the prose disagree on what F5 guarantees.

## OUT_OF_SCOPE

### Topic 1: Resolution of the recorded endset against a document's arrangement
**Why out of scope**: The note's "boundary" section correctly identifies projecting the recorded end into a document's live arrangement (shrinkage, per-document variation) as a separable concern and defers it. This is properly handled, not an error — flagged only to confirm the boundary is respected.

VERDICT: REVISE
