# Review of ASN-0029

## REVISE

### Issue 1: D7 uniqueness claim is false
**ASN-0029, Document Identity (D7)**: "home(Σ.V(d)(p)) = the unique d' with zeros(d') = 2 and d' ≼ Σ.V(d)(p)"
**Problem**: Multiple document-level prefixes can satisfy this condition. Consider I-address `a = 1.0.1.0.3.1.0.1.2.3` (N=[1], U=[1], D=[3,1], E=[1,2,3]). Both `1.0.1.0.3` (D=[3]) and `1.0.1.0.3.1` (D=[3,1]) have zeros = 2 and are prefixes of `a`. The word "unique" is false — the home document is `1.0.1.0.3.1`, not `1.0.1.0.3`, but the characterization cannot distinguish them. The reasoning via T4's `fields()` is sound (T4 gives a unique decomposition); the formal definition fails to capture it.
**Required**: Define `home(a)` as the *longest* prefix with zeros = 2, i.e., `max≼ {d' : zeros(d') = 2 ∧ d' ≼ a}`. Equivalently, define it via `fields()`: the tumbler formed from the node, separator, user, separator, and document components of `fields(a)`.

### Issue 2: D12 parameter `a_req` not related to `actor(op)`
**ASN-0029, Versioning (D12)**: "CREATENEWVERSION(d_s, a_req) — where a_req is the requesting account"
**Problem**: D0 pre: `actor(op) = a`. D10a pre: `account(d) = actor(op)`. D15: `account(d) = actor(op)`. All three use `actor(op)` for authorization. D12 introduces `a_req` as a parameter without stating `a_req = actor(op)`. As written, D12 permits one account to create versions on behalf of another — severing the connection to D15 and D16, which resolve non-owner modification via `actor(op)`.
**Required**: State `a_req = actor(op)` in D12's precondition, or explain why the parameter may differ from the actor.

### Issue 3: Frame conditions do not bound Σ'.D from above
**ASN-0029, D0 frame, D10a frame, D12 frame**
**Problem**: All three frames establish `Σ.D ⊆ Σ'.D` (existing documents preserved) but not `Σ'.D ⊆ Σ.D ∪ {new}`. D0's existential `(E d : d ∉ Σ.D ∧ d ∈ Σ'.D : ...)` means "at least one" in classical logic. Nothing prevents PUBLISH from creating phantom documents as a side effect, or CREATENEWDOCUMENT from creating multiple. The D2 verification implicitly assumes `Σ'.D` is tightly bounded — make it explicit.
**Required**: Add `Σ'.D = Σ.D ∪ {d}` to D0 and D12 frames. Add `Σ'.D = Σ.D` to D10a's frame.

### Issue 4: D5(c) introduces undefined concept "designated associates"
**ASN-0029, Structural Ownership (D5)**: "only the owner and designated associates may access d"
**Problem**: "Designated associates" appears in D5(c) but the ASN provides no definition — no state component, no designation operation, no formal characterization. D12's precondition for private documents allows only the owner (`account(d_s) = a_req`), contradicting D5(c)'s promise that associates can also access. The gap creates internal inconsistency: D5(c) says associates exist, D12 acts as though they don't.
**Required**: Either note that associates are deferred and D5(c) is stated as design intent (not yet formalized), or add a note in D12 explaining that versioning requires ownership of private documents even though read access may extend to associates.

### Issue 5: D17 span well-formedness gap
**ASN-0029, Document Discovery (D17)**: "Each span (s, l) denotes the contiguous range {t : s ≤ t < s ⊕ l}"
**Problem**: D17 uses `s ⊕ l` without requiring `l > 0`. By TA0 (WellDefinedAddition, ASN-0001), `⊕` requires a positive displacement (`w > 0`). If `S` contains a span with `l = 0`, the expression `s ⊕ l` is undefined and D17 is ill-formed. T12 (SpanWellDefined) requires `ℓ > 0`, but D17 does not reference this.
**Required**: Add `(A (s,l) ∈ S : l > 0)` to D17's precondition, or state that S consists of well-formed spans per T12.

### Issue 6: D14 parent function undefined for root documents
**ASN-0029, Versioning (D14)**: "parent(d) = max≼ {d' : d' ≺ d}"
**Problem**: For a root document like `d = 1.0.1.0.3` (single-component document field), the set `{d' : d' ≺ d}` is empty — no tumbler with zeros = 2 is a proper prefix of `d` (the only shorter prefixes have zeros ∈ {0, 1}). `max` over the empty set is undefined. The prose correctly says "at most one immediate structural parent," but the formal definition does not handle the root case.
**Required**: State that `parent(d)` is a partial function, defined when `{d' : d' ≺ d} ≠ ∅`.

## OUT_OF_SCOPE

### Topic 1: Privashed state transitions
**Why out of scope**: The privashed → private and privashed → published transitions are acknowledged design intent, explicitly deferred to open questions. D10 is verified for all currently-defined operations without depending on these transitions.

### Topic 2: Concurrent access properties for D15
**Why out of scope**: The ASN correctly identifies that concurrent-session invariants are implementation mechanics belonging in a future ASN, not in this document lifecycle specification.

### Topic 3: D17 access filtering
**Why out of scope**: D17 ranges over all Σ.D including private documents, creating tension with D5(c). The open questions already flag this. Since D5(c) is normative (not formalized as an invariant), the tension is between an informal design requirement and a formal definition — resolving it requires formalizing the access model, which is future work.

### Topic 4: DELETE/REARRANGE/COPY postconditions for D2
**Why out of scope**: D2 verification for ASN-0026 operations relies on informal reasoning. Formal postconditions for DELETE, REARRANGE, and COPY belong in ASN-0026. The reasoning given (P7 for non-targets, V-space modification for targets preserving Σ.D membership) is sound given ASN-0026's structure.

VERDICT: REVISE
