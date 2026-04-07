# Review of ASN-0042

## REVISE

### Issue 1: O3 is falsified by delegation

**ASN-0042, Permanence**: "The argument is clean: ownership is determined by pfx(π) and a (by O0). The address a is permanent (by T8). The prefix pfx(π) is permanent... Since the ownership computation takes immutable inputs, it cannot yield a different result in any future state."

**Problem**: The argument is wrong. `ω(a)` is not a function of `(pfx(π), a)` alone — it is `argmax` over all `π' ∈ Π` where `pfx(π') ≼ a`. The set `Π` grows through delegation (O7 says "creates a new sub-prefix... assigns it to a new principal"). When delegation introduces a principal `π'` with `pfx(π') ≼ a` and `#pfx(π') > #pfx(π)`, then `ω(a)` changes from `π` to `π'`.

Concrete counterexample: State `Σ₀` has principal `π₁` with `pfx(π₁) = [1, 0, 2]`. Address `a = [1, 0, 2, 0, 3, 0, 1]`. Then `ω_{Σ₀}(a) = π₁`. Now `π₁` delegates to `π₂` with `pfx(π₂) = [1, 0, 2, 0, 3]`, producing state `Σ₁`. Then `ω_{Σ₁}(a) = π₂` (longer match). O3 asserts `ω_{Σ₁}(a) = π₁`. Contradiction.

The ASN's own text confirms this reading: "Delegation permanently transfers effective ownership of the subdomain" and "New ownership domains are created through delegation." O8 itself states `ω(a) = π'` after delegation for `a ∈ dom(π')` — this is a change of `ω`, which O3 forbids.

**Required**: Either (a) restrict O3 to non-delegation transitions: "Among state transitions that do not introduce new principals, `ω` is invariant," or (b) reformulate O3 as monotonic refinement: "Delegation can only narrow a parent's effective domain, never reassign addresses outside the delegate's domain, and is the sole mechanism by which `ω(a)` can change," or (c) define a two-phase model where delegation precedes allocation and O3 applies only after the principal hierarchy for a given prefix region is established. Whatever the fix, the argument must acknowledge `ω`'s dependence on `Π`.

---

### Issue 2: O1a is false for finer-than-account prefixes, creating cascading inconsistencies

**ASN-0042, The Account-Level Boundary**: `(A p, a ∈ T : pfx(π) ≼ a  ≡  acct(pfx(π)) ≼ a)`

**Problem**: This biconditional fails when `pfx(π)` is finer than account level. Let `pfx(π) = [1, 0, 2, 0, 3]` (document-level, `zeros = 2`). Then `acct(pfx(π)) = [1, 0, 2]`. Consider `a = [1, 0, 2, 0, 5, 0, 1]`:

- `pfx(π) ≼ a`: component 5 of `a` is 5, component 5 of `pfx(π)` is 3. `5 ≠ 3`. FALSE.
- `acct(pfx(π)) ≼ a`: `[1, 0, 2] ≼ [1, 0, 2, 0, 5, 0, 1]`. TRUE.

The biconditional is violated. O1a is only valid when `pfx(π)` has `zeros ≤ 1`.

Yet O7 explicitly permits finer delegation. Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers" (LM 4/17). This includes document-level and version-level delegation, producing principals with `zeros ≥ 2` in their prefix.

This creates cascading problems:
- **O6** claims `acct(a)` "identifies the allocating principal." If the allocator is a document-level principal (`pfx = [1, 0, 2, 0, 3]`), then `acct(a) = [1, 0, 2]` identifies the account-level ancestor, not the actual allocator.
- **O10(b)** states `acct(a') = pfx(π)`, which requires `pfx(π)` to be at account level (`zeros = 1`). If `pfx(π)` has `zeros ≠ 1`, this equality cannot hold.
- **acct itself** is defined only for tumblers with a user field (`zeros ≥ 1`). For node-level principals (`zeros = 0`), `acct(pfx(π))` is undefined, yet O1a quantifies over all principals.

Additionally, the English preamble ("if `acct(p) = acct(a)` then...") states a conditional, but the formal statement is an unconditional biconditional. These do not match.

**Required**: The ASN must resolve whether ownership is prefix containment at arbitrary levels (O1) or exclusively account-level (O1a). The cleanest resolution: add an explicit constraint that `pfx(π)` satisfies `zeros(pfx(π)) ≤ 1` for all `π ∈ Π`, then revise O7 to state that delegation at document/version levels creates subordinate allocators but not ownership principals. If finer-grained ownership is intended, drop O1a and revise O6 and O10(b) accordingly. Also define `acct(t)` for `zeros(t) = 0` or restrict its domain.

---

### Issue 3: Injectivity of pfx required but unstated

**ASN-0042, The Exclusivity Invariant**: "(iii) the longest among a linearly ordered finite set is unique"

**Problem**: This establishes that the longest *prefix* is unique — correct, since prefixes of the same tumbler are linearly ordered by length. But `ω(a)` maps from the unique longest prefix to a unique *principal*. If two distinct principals share the same prefix (`pfx(π₁) = pfx(π₂)`, `π₁ ≠ π₂`), both tie for longest match, and `(E! π :: ω(a) = π)` fails. The ASN never states that `pfx` is injective.

**Required**: Add an axiom: `(A π₁, π₂ ∈ Π : pfx(π₁) = pfx(π₂) ⟹ π₁ = π₂)`. This is load-bearing for O2.

---

### Issue 4: O2 well-definedness relies on an implicit coverage axiom

**ASN-0042, The Exclusivity Invariant**: "(i) at least one principal's prefix contains any allocated address (the address was baptized by someone who holds a containing prefix)"

**Problem**: This is asserted parenthetically, not proved or stated as an axiom. It is a non-trivial claim: every allocated address lives under some principal's prefix. This requires that the principal hierarchy covers the entire allocated address space — including at system bootstrap (who is the first principal? what prefix do they hold?). The argument implicitly assumes a root/node-operator principal exists before any allocation occurs.

**Required**: State explicitly as an axiom: "For every allocated address, at least one principal's prefix contains it." Optionally, note that this is guaranteed by O5 (only owners may allocate) — allocation only occurs within an existing principal's domain, so every allocated address is born under a covering prefix. But this derivation should be shown, not assumed.

---

### Issue 5: No concrete example

**ASN-0042, throughout**

**Problem**: The ASN provides extensive prose discussion with implementation evidence (Gregory's `tumbleraccounteq`, `docreatenewdocument`, etc.) but never constructs a concrete scenario with specific tumbler values and verifies O0–O2, O5, O6, O10 against it. A worked example would have caught Issue 1 (the O3/delegation contradiction) immediately.

**Required**: Add at least one scenario. For example: "Let `π₁` have `pfx = [1, 0, 2]`. `π₁` allocates document address `a = [1, 0, 2, 0, 3]`. Verify: O0 — `owns(π₁, a)` requires only `[1, 0, 2]` and `[1, 0, 2, 0, 3]`; O1 — `[1, 0, 2] ≼ [1, 0, 2, 0, 3]` holds; O2 — `ω(a) = π₁` (longest match, sole principal). Now `π₁` delegates `[1, 0, 2, 0, 3]` to `π₂`. Verify: O2 — `ω(a) = π₂` (longer match). Check O3..." This exercise would force the ASN to confront the delegation issue.

---

### Issue 6: O4 numbering gap

**ASN-0042, Properties Introduced table**: Numbering proceeds O0, O1, O1a, O2, O3, O5, O6, ...

**Problem**: O4 is absent from both the body and the properties table. If the gap is intentional (a property was removed during drafting), the numbering should be closed to avoid confusion. If unintentional, the missing property should be identified.

**Required**: Either renumber to close the gap or document why O4 is absent.

---

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism
**Why out of scope**: The ASN correctly identifies transfer as an open question. The current model (O3) asserts permanence; a transfer mechanism would require new machinery (external registry, deed concept) that this ASN is not attempting to specify.

### Topic 2: Cross-node identity federation
**Why out of scope**: O9 establishes node-locality. Federation would be a new specification layer building on O9, not a correction to it.

### Topic 3: Authentication and session binding
**Why out of scope**: O11 explicitly axiomatizes principal identity as external to the ownership model. The mechanism for establishing identity is a separate concern.

VERDICT: REVISE
