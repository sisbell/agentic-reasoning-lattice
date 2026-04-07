# Review of ASN-0029

## REVISE

### Issue 1: D0 missing actor constraint
**ASN-0029, The Document as Position**: D0 specifies `pre: a ∈ AccountAddr` but no constraint on who may create documents under account `a`.
**Problem**: D5(d) states "only the owner may allocate new tumblers extending d's prefix" and D10a includes `account(d) = actor(op)` in its precondition. D0 has no parallel constraint. As written, any actor may create documents under any account — the formal spec does not prevent it. (`AccountAddr` is also used without a standalone definition, though its meaning is recoverable from `account(d)`.)
**Required**: Add `actor(op) = a` to D0's precondition, matching the pattern established by D10a and D15.

### Issue 2: D12 precondition incomplete — no access check, no constraint on a_req
**ASN-0029, Versioning**: D12 specifies `pre: d_s ∈ Σ.D` and nothing else. The parameter `a_req` appears in postconditions (via D13) but is unconstrained in the precondition.
**Problem**: Two gaps. (a) `a_req` is not required to be a valid account address. (b) No accessibility check. D5(c) says only the owner and designees may access a private document. Yet D12 allows CREATENEWVERSION on a private document by any `a_req`. A non-owner could version a document they cannot access. D16 reinforces this: it describes non-owner forking as the resolution for modification requests, implying the non-owner can see the document — but D12 doesn't enforce this.
**Required**: `pre: d_s ∈ Σ.D ∧ a_req ∈ AccountAddr ∧ (Σ.pub(d_s) ∈ {published, privashed} ∨ account(d_s) = a_req)`

### Issue 3: D2 derivation hand-wave
**ASN-0029, Address Allocation**: "This mirrors P1 (ISpaceMonotone, ASN-0026) at the document level."
**Problem**: P1 says `dom(Σ.I)` never shrinks. D2 says `Σ.D` never shrinks. These are independent properties — one does not follow from the other. The analogy is suggestive but is not a derivation. D2 is an invariant over all operations; the ASN should verify it against each defined operation.
**Required**: State D2 as an independent invariant with an explicit verification sketch: D0 adds to Σ.D (frame preserves existing members); D10a preserves V-space hence Σ.D membership; D12 adds to Σ.D (frame preserves existing members); ASN-0026 operations (INSERT, DELETE, COPY, REARRANGE) modify V-space within documents but never remove a document from Σ.D (P7 preserves non-target documents; target documents retain V-space).

### Issue 4: Σ.pub frame not established for ASN-0026 operations
**ASN-0029, Publication**: D10 claims `[Σ.pub(d) = published ⟹ Σ'.pub(d) = published]` for every state transition.
**Problem**: The ASN verifies D10 against D0, D10a, and D12. It does not address ASN-0026 operations (INSERT, DELETE, COPY, REARRANGE, and the partial CREATENEWVERSION). Since Σ.pub is introduced in this ASN, ASN-0026 naturally says nothing about it. D10's universality requires establishing that these pre-existing operations have the extended frame `Σ'.pub(d) = Σ.pub(d)` for all `d ∈ Σ.D`. Without this, D10 is ungrounded for the majority of state transitions.
**Required**: Add a brief statement: operations defined in ASN-0026 do not modify Σ.pub; their frame conditions extend to include `(A d : d ∈ Σ.D : Σ'.pub(d) = Σ.pub(d))`.

## OUT_OF_SCOPE

### Topic 1: Link operations and the ownership/publication boundary
D5(b) claims the owner controls outgoing links; D11(b) claims publication surrenders control over incoming links. No formal invariant governs link creation, and the incoming/outgoing distinction is not formalized.
**Why out of scope**: Link semantics is a separate domain. This ASN correctly defers to a future links ASN.

### Topic 2: Privashed state transitions
The ASN defines `private → published` and `private → privashed` but defers `privashed → private` and `privashed → published`. The interaction matters (e.g., `privashed → private → published` would allow a previously privashed document to gain D10 monotonicity).
**Why out of scope**: The ASN explicitly lists this as an open question and limits D10a's scope accordingly.

### Topic 3: FINDDOCSCONTAINING access control
D17 ranges over all `d ∈ Σ.D`. Whether private documents should be discoverable is an access-control question.
**Why out of scope**: The ASN lists this as an open question. The formal definition is correct for the query semantics; the access filter is a separate concern.

### Topic 4: Concurrent enforcement of D15
D15 requires `account(d) = actor(op)` for modifications. Multiple sessions under the same owner or the trust model for `actor(op)` are concurrency/enforcement concerns.
**Why out of scope**: The ASN correctly identifies these as implementation mechanism and lists concurrent access as an open question.

VERDICT: REVISE
