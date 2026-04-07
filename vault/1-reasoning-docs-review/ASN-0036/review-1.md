# Review of ASN-0036

## REVISE

### Issue 1: S5 formal statement does not match its intent

**ASN-0036, Sharing**: "`(A a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| is unbounded)`"

**Problem**: As written, this universally quantifies over addresses in a fixed state and asserts each has unbounded sharing multiplicity. In any fixed state, the multiplicity of each address is a definite finite number (possibly zero — orphaned content per S6 has multiplicity exactly zero). The predicate "is unbounded" is not well-formed when applied to a definite natural number.

The intended claim is an architectural anti-constraint: no finite constant caps sharing across all reachable states. That is: `(A N ∈ ℕ :: (E Σ reachable, a ∈ dom(Σ.C) :: |{(d, v) : ...}| > N))`. This quantifies over the state space, not within a single state.

**Required**: Reformulate S5 as a statement about the state space — for every natural number N, there exists a reachable state in which some I-address has sharing multiplicity exceeding N. Alternatively, state it negatively: the model imposes no finite upper bound on `|{(d, v) : M(d)(v) = a}|`.

### Issue 2: S7 derivation from T4 has two gaps

**ASN-0036, Structural attribution**: "`origin(a) = fields(a).document`" — "S7 follows from T4 (ASN-0034)"

**Problem (a)**: T4 defines how to parse a tumbler into fields. It does not establish that I-space addresses are allocated under the originating document's tumbler prefix. The claim that `fields(a).document` identifies the document that allocated `a` requires an additional architectural premise: that I-space allocation scopes addresses beneath the allocating document's prefix. This premise is load-bearing (it is what makes attribution structural rather than metadata) but unstated. Neither T4 nor T9/T10/T10a guarantee this — they describe tumbler structure and allocation mechanics, not the convention binding I-address prefixes to documents.

**Problem (b)**: `fields(a).document` is well-defined only when `zeros(a) ≥ 2` (per T4's field correspondence: zeros = 0 is node-only, zeros = 1 is node+user, zeros ≥ 2 has a document field). The ASN defines `Σ.C : T ⇀ Val` without restricting `T` to element-level tumblers. S7 applies `fields(·).document` to every I-address, but nothing prevents an I-address with `zeros(a) < 2` — for which the document field is undefined.

**Required**: (a) State the architectural premise that I-space allocation uses the allocating document's tumbler as a prefix. (b) Either restrict `dom(Σ.C)` to tumblers with `zeros(a) ≥ 2` (or ≥ 3 for element-level), or qualify S7 as applying only to addresses with a document field.

### Issue 3: S8 correspondence run displacement is underspecified

**ASN-0036, Span decomposition**: "`(A k : 0 ≤ k < ℓ : Σ.M(d)(v ⊕ k) = a ⊕ k)`"

**Problem**: The variable `k` has no declared type. Three readings, each with problems:

(i) *k is a natural number.* Then `v ⊕ k` overloads `⊕` (ASN-0034 defines tumbler addition on two tumblers, not a tumbler and a natural number). The quantification `0 ≤ k < ℓ` treats ℓ as a natural number, conflicting with T12 where ℓ is a tumbler displacement.

(ii) *k is a tumbler.* Then `0 ≤ k < ℓ` ranges over all tumblers in the interval `[0, ℓ)` under T1. This set is infinite — for any non-trivial ℓ, tumblers of arbitrary length populate the interval (by T0b). The quantification demands `M(d)` be defined at every such tumbler, which contradicts a finite document model.

(iii) *k is an element-level displacement tumbler (same depth as v, action point at the last significant position).* This is the intended reading — consecutive positions differ only at the element ordinal — but it is not stated.

Furthermore, the appeal to the degenerate decomposition ("each V-position forms a run of length one") assumes that a T12 span `[v, v ⊕ ℓ)` can isolate a single element of `dom(M(d))`. But by T1 and T0b, the interval `[v, v ⊕ ℓ)` contains tumblers of all lengths between `v` and `v ⊕ ℓ`. Whether these are in `dom(M(d))` depends on unstated constraints on address depth. The partition claim S8(a) — that V-spans cover exactly `dom(M(d))` without overlap — is not established.

Finally, `dom(M(d))` finiteness is used ("S8 follows from the finiteness of `dom(M(d))`") but never established as a property. The type `T ⇀ T` permits infinite domains.

**Required**: (a) Specify k's type — either restrict to element-level displacements or introduce a counting abstraction for span membership. (b) Establish that dom(M(d)) is finite (or derive S8 without finiteness). (c) Show the degenerate decomposition actually partitions dom(M(d)) given the structure of T12 spans.

### Issue 4: S8 run-count monotonicity claim is false

**ASN-0036, Span decomposition**: "The number of runs is monotonically non-decreasing over the editing history."

**Problem**: Deleting content from a document removes V-positions from `dom(M(d))`. If an entire correspondence run's V-span is deleted, the run count decreases. The claim confuses I-space allocation events (which are monotonically non-decreasing per S0/S1) with V-space arrangement runs (which fluctuate with editing — insertions split runs, deletions remove them).

**Required**: Either retract the monotonicity claim, or restate it precisely as: the number of distinct I-space allocation events underlying a document's history is monotonically non-decreasing (which follows from S1 but is a different quantity from the current arrangement's run count).

### Issue 5: No concrete example

**ASN-0036, throughout**

**Problem**: The ASN introduces nine properties (S0–S8), proves one theorem (S9), and derives several consequences, but never instantiates the state model with specific tumblers. A worked example would ground the abstractions and expose edge-case interactions. For instance: two documents, one transcluding a span from the other, with specific tumbler addresses for V-positions and I-addresses. Verify S0 (content unchanged across a transition), S3 (all V-references resolve), S7 (origin traced through I-address), S8 (decomposition into runs with explicit spans).

**Required**: Add at least one concrete scenario with specific tumblers, showing the state `(C, M)` before and after a transition, with each relevant property checked against the instantiated state.

## OUT_OF_SCOPE

### Topic 1: Operation-specific preservation of S0–S9
**Why out of scope**: The ASN establishes invariants. Proving that INSERT, DELETE, COPY, and REARRANGE each preserve these invariants requires operation definitions, which the scope explicitly excludes.

### Topic 2: Link survival through I-space identity
**Why out of scope**: The ASN notes that links point to I-addresses (preserved by S0), but formalizing link behavior requires the link model, which is out of scope.

### Topic 3: Sharing-inverse query cost
**Why out of scope**: S5 establishes that sharing is structurally represented. The efficiency of computing "which documents reference I-address a" is an implementation concern, not an invariant.

VERDICT: REVISE
