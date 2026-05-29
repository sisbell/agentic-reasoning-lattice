# Review of ASN-0036

## REVISE

### Issue 1: Two separate slots defer the same coalescing question downstream
**ASN-0036, Span decomposition (S8 prose and S8 Formal Contract postconditions)**: the prose says coalescing is "deferred to the open question on unique maximal decompositions," and the postcondition repeats "Structure-preservation of `shift` on images … is not a postcondition of this singleton-existence theorem; it is a standalone consequence … recorded with the deferred coalescing work in the open questions."
**Problem**: Two paragraphs in the same property defer the same future work to the same downstream location. This is the multiple-deferral accretion pattern — the second pointer adds no reasoning, only re-announces the deferral.
**Required**: State the deferral once (the prose sentence suffices). Drop the parenthetical from the postcondition or reduce it to "(coalescing deferred — see open questions)."

### Issue 2: The depth-locking transition is stated three times
**ASN-0036, Valid insertion position**: the sentence "once a position is placed, S8-depth fixes the depth at the chosen `m` … transitioning the document into the non-empty regime governed by `ValidInsertionPosition`" appears (a) in the `ValidFirstInsertionPosition` definition prose, (b) verbatim-in-substance in that contract's postcondition (d), and (c) again in the "empty case" worked example ("once chosen, S8-depth locks the subspace to depth 3 … subsequent validity is governed by `ValidInsertionPosition`").
**Problem**: Three paragraphs say the same thing in different words. Per the anti-bloat directive this is duplicate prose that the reader must repeatedly re-parse.
**Required**: Keep it in the contract postcondition (d), where it is normative; remove it from the definition prose and the example.

### Issue 3: Over-elaborated length bound in ShiftPreservation
**ASN-0036, ShiftPreservation, conclusion (ii) part (3)**: "(because `#a ≥ 7` — three field-separator zeros plus at least one non-separator component in each of the four fields, summing to 3 + 4 = 7; invoking S7c's `#E(a) ≥ 2` tightens this to `#a ≥ 8`, and either bound suffices for `#a > 1`)".
**Problem**: The step only needs position 1 to lie before the action point `#a`, i.e. `#a > 1`. The parenthetical computes two stronger bounds (`≥ 7`, then `≥ 8`) and then concedes neither was needed. This is bloat in a proof slot — the reader works past it to reach the trivial fact actually used.
**Required**: Replace with the minimal justification: position 1 is copied unchanged because `1 < #a` (immediate from `#a ≥ 2` via S7c).

### Issue 4: Spurious S0 dependency on S7b
**ASN-0036, S7b Formal Contract, Depends**: "S0 (content immutability) — fixes `a`'s components, so allocation-time structure persists."
**Problem**: A tumbler is a fixed sequence in `T`; `zeros(a) = 3` is an intrinsic property of `a` alone and is never state-dependent. S0 ensures `a` *remains in `dom(C)`*, not that its components are "fixed" — they were never mutable. The citation conflates address-persistence with a non-existent component-mutability concern, a defensive justification that does not advance the claim.
**Required**: Either drop the S0 citation from S7b, or restate it precisely ("S1/S0 keep `a ∈ dom(C')`, so the zero-count condition continues to hold on the same address across transitions").

### Issue 5: Use-site inventory phrasing on Nat-pos
**ASN-0036, ShiftPreservation, conclusion (i)**: "by **Nat-pos** — the elementary fact that for `n ∈ ℕ`, `n ≠ 0 ⟹ n ≥ 1` (immediate from NAT-discrete at `m = 0`), which we name here and cite at later sites."
**Problem**: "which we name here and cite at later sites" is a downstream-consumer inventory, not content that advances the step. The naming is fine; the forward inventory is meta-prose.
**Required**: Delete the clause "which we name here and cite at later sites." Later uses can simply say "by Nat-pos."

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG / D-MIN and subspace alignment
The questions of whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants, and whether `subspace(v) = subspace_I(M(d)(v))` is maintained, are correctly placed in Open Questions. These belong to a future operations ASN; their absence here is not an error.

### Topic 2: Maximal/unique run decomposition (coalescing)
S8 proves only singleton existence and honestly disclaims minimality. The maximal-run question is genuine future territory, properly deferred (see Issue 1 for the presentation problem, not the scope decision).

Note on substance: the mathematical content checks out. S1 follows from S0; S4 from GlobalUniqueness; the S8 partition proof factors the repetitive case-work into a clean within-subspace lemma and handles cross-subspace via T5/T10; the OrdAddHom / OrdAddS8a boundary regimes (`k = 2`, `k = m`) are correctly collapsed; ShiftPreservation's four conclusions and the worked-example `k = 3` computation are correct. The findings above are accretion and clarity issues, not correctness failures.

VERDICT: REVISE
