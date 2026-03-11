# Review of ASN-0029

## REVISE

### Issue 1: D1 and D12(g) — per-account monotonicity is false

**ASN-0029, D12 postcondition (g)**: "`(A d' : d' ∈ Σ.D ∧ account(d') = account(d_v) : d' < d_v)`"

**ASN-0029, D1**: "Within any account `a`, documents are allocated with strictly increasing addresses"

**Problem**: Both claims are false when own-account versioning (D12 Case 1) interleaves with root document creation. Consider: account `1.0.1` creates documents `1.0.1.0.3`, then `1.0.1.0.5`, then versions `1.0.1.0.3` producing child `1.0.1.0.3.1`. By T1, `1.0.1.0.3.1 < 1.0.1.0.5` (diverge at position 5: 3 < 5). Yet `account(1.0.1.0.5) = account(1.0.1.0.3.1) = 1.0.1`, and `1.0.1.0.5` was allocated before `1.0.1.0.3.1`. D1 requires `1.0.1.0.5 < 1.0.1.0.3.1` — false.

D12(g) is wrong for Case 1 specifically: the child `d_v = 1.0.1.0.3.1` does not exceed all documents under the account — only children of `d_s`. T9 (ForwardAllocation) is per-allocator, not per-account. T10a distinguishes the root allocator (sibling stream via `inc(·, 0)`) from child allocators (spawned via `inc(·, k')` with `k' > 0`). Each allocator is independently monotonic. Different allocators under the same account are not jointly monotonic.

**Required**: Split D12(g) by case and restate D1 as per-allocator:

- D12(g) Case 1: `(A d' : d' ∈ Σ.D ∧ parent(d') = d_s : d' < d_v)` — exceeds existing children of `d_s`
- D12(g) Case 2: `(A d' : d' ∈ Σ.D ∧ account(d') = a_req : d' < d_v)` — exceeds all docs under `a_req` (this holds because root allocation gives a document number exceeding all prior roots, and children of lower-numbered roots are lexicographically smaller)
- D1: restate as per-allocator monotonicity, aligning with T9's `same_allocator` predicate

The worked example does not expose this bug because its pre-state contains only `d_s` under account `1.0.1`. Add a second root document (e.g., `1.0.1.0.5`) to the pre-state and the violation becomes visible.

---

### Issue 2: account(d) uniqueness claim is false

**ASN-0029, account definition**: "`account(d) = the unique a ∈ AccountAddr with a ≼ d`"

**Problem**: Uniqueness fails when the user field of `d` has more than one component. For `d = 1.0.2.3.0.4` (node `[1]`, user `[2,3]`, document `[4]`), the AccountAddr prefixes are:

- `1.0` — zeros = 1, user field empty
- `1.0.2` — zeros = 1, user field `[2]`
- `1.0.2.3` — zeros = 1, user field `[2,3]`

All three satisfy `a ∈ AccountAddr ∧ a ≼ d`. The "unique" quantifier is unsatisfied. This affects every property that uses `account(d)`: D0, D1, D3, D4, D5, D12, D13, D15.

The intended account is the *longest* AccountAddr prefix — the full N.0.U from T4's decomposition. The prose says this correctly ("the N.0.U portion of d's tumbler") but the formal definition does not.

**Required**: Either (a) define `account(d) = max≼ {a ∈ AccountAddr : a ≼ d}` and show the max is well-defined (prefixes of a fixed tumbler are totally ordered under ≼, so the set is a chain with a maximum), or (b) define `account(d)` directly via `fields()` extraction. In either case, state that the result is the full N.0.U — the account whose user field matches T4's decomposition of `d`.

---

### Issue 3: D14 closure assumes D0 creates root documents, unstated

**ASN-0029, D14**: "non-root documents in Σ.D are created only by D12 Case 1"

**Problem**: This claim requires that D0 (CREATENEWDOCUMENT) produces only root documents — documents with single-component document fields, i.e., `parent(d)` undefined. But D0's specification says only that the new `d` satisfies `account(d) = a` and exceeds all existing documents under `a`. It does not constrain the document field to be single-component. If D0 could produce a multi-component document field (a non-root document), then non-root documents could be created by D0 as well, and the closure argument for `parent(d) ∈ Σ.D` would fail.

The implicit reasoning is that D0 uses the account's root allocator (T10a sibling stream), which produces single-component extensions. But this is never stated.

**Required**: Add an explicit postcondition to D0: `parent(d) is undefined` (equivalently, `d`'s document field is single-component). Or add a clause stating that D0 allocates via the root allocator for account `a`, producing a sibling in the root document stream. This is also needed to make D0's monotonicity postcondition correct — a root document with the next sequential number exceeds all existing documents under the account (including children of lower-numbered roots), but a child document would not.

---

### Issue 4: D4 cites T8 for document address permanence, but T8 governs I-space

**ASN-0029, D4**: "Since a document's tumbler address is permanent (T8, AddressPermanence, ASN-0001)"

**Problem**: T8 states: "If tumbler `a ∈ T` is assigned to content `c` at any point in the system's history, then `a` remains assigned to `c`." This governs `dom(Σ.I)` — I-space address-to-content bindings. Document addresses live in `Σ.D`, not `dom(Σ.I)`. Documents have `zeros(d) = 2`; I-space addresses have `zeros = 3`. T8 does not apply to document membership.

The conclusion of D4 is correct — `account(d)` is a pure function of the value `d`, and since `d` is a mathematical value (not a mutable reference), `account(d)` cannot change across state transitions. But this follows from the immutability of values, not from T8. The permanence of `d ∈ Σ.D` across transitions is D2, not T8.

**Required**: Replace the T8 citation with the correct justification: `account(d)` is a pure function of the value `d`, and `d` is immutable as a member of `Σ.D` (whose membership is permanent by D2). No mutable state is consulted, so the result cannot vary.

---

### Issue 5: D13 Case 1 does not verify the child allocation produces a document-level address

**ASN-0029, D13**: "This follows from T10a (AllocatorDiscipline): the parent allocator spawns a child via `inc(·, k')` with `k' > 0`"

**Problem**: T10a with `k' > 0` spawns a child allocator, but different values of `k'` produce different results. By TA5(d), `inc(d_s, k')` produces a tumbler with `k' - 1` intermediate zeros and a final component of 1. For `d_s` with `zeros(d_s) = 2`:

- `k' = 1`: no new zeros, `zeros(d_v) = 2` — document-level address. Correct.
- `k' = 2`: one new zero, `zeros(d_v) = 3` — element-level address. Wrong level.
- `k' = 3`: two new zeros, `zeros(d_v) = 4` — invalid (exceeds T4's maximum of 3 zeros).

D13 must constrain `k' = 1` to ensure the child is a document, not an element. Without this, the claim that `d_v` is a document address (in `Σ.D`, parseable by `fields()`, satisfying T4 with `zeros = 2`) is unjustified.

**Required**: State explicitly that own-account version allocation uses `k' = 1` in T10a, and verify that `zeros(inc(d_s, 1)) = zeros(d_s) = 2`, preserving document-level structure.

---

### Issue 6: D0's monotonicity depends on D0 being root-only (circular with Issue 3)

**ASN-0029, D0**: "`(A d' : d' ∈ Σ.D ∧ account(d') = a : d' < d)`"

**Problem**: This postcondition — `d` exceeds ALL existing documents under account `a` — is correct only if `d` is a root document. A root document `a.0.K` with `K` exceeding all existing root document numbers will exceed all children of lower-numbered roots (since children like `a.0.K'.x` satisfy `a.0.K'.x < a.0.K` when `K' < K`). But if `d` were a child document, this would fail for the same reason as D12(g) in Issue 1.

This is the same gap as Issue 3 — the correctness of D0's monotonicity postcondition depends on D0 producing root documents, which is assumed but not stated.

**Required**: Same fix as Issue 3 — make root-only allocation explicit in D0.

---

## OUT_OF_SCOPE

### Topic 1: Associate access model for private documents
**Why out of scope**: D5(c) acknowledges "designated associates" but explicitly defers the mechanism. A future ASN should formalize what state tracks designations and which operations establish them. This doesn't affect the properties stated here, since all operations require ownership.

### Topic 2: Privashed state transitions and semantics
**Why out of scope**: The ASN correctly defers privashed → private and privashed → published transitions to future work. The current ASN only specifies private → published and private → privashed via D10a. The open questions appropriately flag the outstanding issues (retroactive binding, withdrawal semantics).

### Topic 3: Concurrent access guarantees
**Why out of scope**: D15 is a design requirement on correct participants. The abstract properties of concurrent access (session isolation, token semantics) belong to a separate ASN on the concurrency model, as the ASN itself notes.

### Topic 4: FINDDOCSCONTAINING access filtering
**Why out of scope**: Whether D17 queries all of Σ.D or only accessible documents is a policy decision that interacts with the access model (not yet formalized). The current formulation over all of Σ.D is the mathematically clean baseline; access filtering would narrow the result set.

VERDICT: REVISE
