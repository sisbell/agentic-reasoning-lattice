# Review of ASN-0036

## REVISE

### Issue 1: OrdAddS8a derives `rₖ ≥ 2` when the claim needs only `rₖ > 0`

**ASN-0036, OrdAddS8a proof, action-point component step**: "At `i = k`: `rₖ = vₖ + wₖ ≥ 1 + 1 = 2`. From `vₖ ≥ 1` (S8a on `v`) and `wₖ ≥ 1` (ActionPoint's minimum-nonzero clause...), NAT-addcompat (left and right order compatibility) and NAT-order's ≤-transitivity Consequence give the chain `1 + 1 ≤ vₖ + 1 ≤ vₖ + wₖ`: right compatibility at `(m, n, p) = (1, vₖ, 1)`... then left compatibility at `(m, n, p) = (vₖ, wₖ, 1)`... and ≤-transitivity closes the chain into `vₖ + wₖ ≥ 1 + 1 = 2`."

**Problem**: S8a requires only that every component be strictly positive (`rₖ > 0`). The value `rₖ ≥ 2` is never used anywhere in the proof — the conclusion rests solely on "components `r₁` through `rₖ` are unconditionally positive," and `vₖ ≥ 1` already delivers `rₖ = vₖ + wₖ ≥ vₖ ≥ 1 > 0`. The two NAT-addcompat instantiations plus the ≤-transitivity chaining are gratuitous citation accretion proving a stronger fact than the claim consumes. This is exactly the over-derivation the anti-bloat classifier targets. The same `wₖ ≥ 1` / NAT-addcompat / NAT-order citations propagate into the Depends list, where they have no work to do.

**Required**: Replace the chain with one line: `rₖ = vₖ + wₖ ≥ 1 > 0` from `vₖ ≥ 1` (S8a) and `wₖ ∈ ℕ`. Drop the now-unused `wₖ ≥ 1` ActionPoint clause and the NAT-addcompat instantiation citations from the proof body and Depends.

### Issue 2: Citation-bookkeeping meta-prose in S8 Depends

**ASN-0036, S8 Depends (final parenthetical)**: "(The NAT-discrete, NAT-closure, NAT-addcompat, and NAT-order roles that underwrite the run-corollary's `k ≥ 1` content are charged to ShiftPreservation, not duplicated here.)"

**Problem**: This sentence advances no part of the argument — it is accounting prose about *where* citations are charged. A reader following S8 gains nothing; it exists to explain the bookkeeping of a prior revision. This is the "prose that does not advance reasoning" the review mode flags at source.

**Required**: Delete. ShiftPreservation's own Depends already carries those citations; S8 need not narrate the non-duplication.

### Issue 3: S8's proof establishes only the trivial singleton decomposition; the motivating prose promises more

**ASN-0036, Span decomposition (opening) and S8 proof**: "contiguous V-ranges often correspond to contiguous I-ranges. This is what makes finite representation possible." / Proof: "For each such `v`, form the singleton run `(v, a, 1)`... The singleton decomposition witnesses existence; minimality is not claimed."

**Problem**: The section motivates correspondence runs as the mechanism of *compressed* finite representation (a single run capturing a transcluded span or a typed block), yet the proof exhibits only singletons — one run per V-position, which is not compression and makes the entire `(vⱼ, aⱼ, nⱼ)` apparatus with `n > 1` vacuous. The image-structure-preservation corollary even quantifies over `1 ≤ k < nⱼ`, an empty range for every singleton. The substantive claim — that a contiguous V-block mapping ordinally to a contiguous I-block *forms* a valid run satisfying conjunct (b) — is asserted in the worked example (runs of length 5, 3, 2) but never derived in the theorem. The postcondition is honestly weak ("there exists a finite decomposition"), but the prose oversells what is proven.

**Required**: Either (a) temper the motivating prose to state only that finitely many runs exist (since `dom(M(d))` is finite, this is near-trivial), explicitly deferring coalescing to the open question on maximal decompositions; or (b) prove the non-trivial claim that an ordinally-corresponding contiguous block satisfies conjunct (b), so the worked-example runs are backed by the theorem rather than by assertion.

### Issue 4: m = 1 necessity paragraph reasons about a case the predicate's precondition excludes

**ASN-0036, Valid insertion position**: "The lower bound `m ≥ 2` is necessary: at `m = 1`, `v = [1]` and `shift([1], 1) = [1] ⊕ δ(1, 1) = [1] ⊕ [1]`; the action point of `[1]` is `k = 1`, so TumblerAdd gives `r₁ = 1 + 1 = 2`, producing `[2]` — a position in subspace 2, not 1."

**Problem**: Both predicates fix `m ≥ 2` in their preconditions (and S8a already forces `#v ≥ 2` for every V-position). This paragraph constructs and analyzes the `m = 1` case that the carrier excludes — reviser drift of the "imagines a case the precondition already excludes" form. The conclusion ("subspace identifier preserved for `m ≥ 2`") is the only operative content and is already stated in the surrounding OrdinalShift discussion.

**Required**: Compress to the positive statement: for `m ≥ 2`, `δ(n, m)` has action point `m > 1`, so TumblerAdd copies component 1 unchanged and the subspace identifier is preserved. Drop the `m = 1` excursion or relocate it to S8a's definitional discussion if a necessity record is genuinely wanted.

### Issue 5: `subspace_I` defined twice

**ASN-0036, S7c prose then standalone definition**: S7c's prose states "we name the first component of the element field as the *I-address subspace identifier*: `subspace_I(a) = E(a)₁`," and the immediately following block re-states "**subspace_I (I-address subspace identifier).** ... `subspace_I(a) = E(a)₁`" with a full contract.

**Problem**: The same definition appears in two adjacent slots ("two paragraphs say the same thing in different words"). S7c's job is the depth axiom `#E(a) ≥ 2`; the naming belongs solely to the definition block.

**Required**: Remove the naming sentence from S7c's prose; let the standalone definition block own `subspace_I`.

### Issue 6: S9 carries no content beyond S0 yet is restated at length

**ASN-0036, The separation theorem**: "S9 (Two-stream separation), corollary of S0. ... S9 is the directional reading of S0" — and the Properties table: "named directional reading of S0 (no formal content beyond S0)."

**Problem**: S0's own prose already argues the directional reading ("This constrains every operation to either leave `C(a)` unchanged or to operate only on addresses not yet in `dom(C)`"). S9 re-derives the same implication with no added formal content. Naming Nelson's "architectural foundation" is defensible, but the paragraph duplicates S0's argument rather than simply pointing to it.

**Required**: Reduce S9 to a one-line named pointer ("S9 is S0 read directionally: arrangement-only transitions cannot alter `C`") and drop the re-derivation.

## OUT_OF_SCOPE

### Topic 1: Subtraction homomorphism and round-trip conditions for `ord`
**Why out of scope**: The conditions under which `ord(v ⊖ w) = ord(v) ⊖ w_ord` and `(ord(v) ⊕ w_ord) ⊖ w_ord = ord(v)` hold depend on TA7a's conditional S-membership for subtraction. These are correctly deferred to the Open Questions; the ASN need not prove them to be sound on its addition-side results.

### Topic 2: Uniqueness / minimality of the run decomposition
**Why out of scope**: Whether a canonical (fewest-runs) decomposition exists is a property of operations and representation strategy, already listed as an open question. The state-level existence claim does not require it. (Note: this is distinct from Issue 3, which concerns the *prose* overselling existence, not the missing minimality result itself.)

VERDICT: REVISE
