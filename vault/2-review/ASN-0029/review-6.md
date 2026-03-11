# Review of ASN-0029

## REVISE

### Issue 1: D7 — `home(a) ∈ Σ.D` not established

**ASN-0029, Document Identity**: "No additional metadata, no lookup table — the address IS the provenance record. Nelson: 'You always know where you are, and can at once ascertain the home document of any specific word or character.'"

**Problem**: D7 defines `home(a) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ a}` as a pure address computation — this is sound. But the semantic claim that this function identifies "the home document of any specific word or character" requires that `home(a) ∈ Σ.D` for every allocated I-address `a ∈ dom(Σ.I)`. This depends on an unstated assumption: that INSERT on document `d` allocates I-addresses under `d`'s tumbler prefix (so that `home(fresh) = d`). Neither ASN-0001 nor ASN-0026 formally states that I-space allocation is prefix-scoped to the creating document. ASN-0026 P9 says fresh addresses satisfy `fresh ∩ dom(Σ.I) = ∅` — a uniqueness constraint — but not WHERE in the address space they fall.

The derivation chain needed is: (i) INSERT(d, ...) allocates I-addresses with prefix `d`, so `home(fresh) = d`; (ii) `d ∈ Σ.D` by precondition; (iii) `d` persists by D2. Link (i) is missing from the formal model.

**Required**: Either add a lemma `(A d ∈ Σ.D, p : 1 ≤ p ≤ n_d : home(Σ.V(d)(p)) ∈ Σ.D)` with an explicit statement of the prefix-allocation assumption it rests on, or note the dependency as an open assumption pending a future ASN on I-space allocation mechanics.

### Issue 2: Privashed state — prose claims unsupported by formal model

**ASN-0029, Publication**: "The `privashed` state does not have this monotonicity property — a privashed document can freely revert to private at any time, with the understanding that anyone who linked to it has no recourse."

**Problem**: Within the formal model as specified, `privashed` is terminal. The only operation that modifies `Σ.pub` is D10a, whose precondition requires `Σ.pub(d) = private`. ASN-0026 operations preserve `Σ.pub` by the frame extension. D0 and D12 set new documents to `private` and preserve existing `pub` via their frames. D17 is a pure query. So no defined operation can transition a document OUT of `privashed`. The prose claim that privashed "can freely revert to private" describes design intent for future operations, but within the current formal model, D10's monotonicity holds for `privashed` just as it does for `published` — vacuously, since no operation changes either.

The ASN partly acknowledges this: "The transitions from `privashed` to `private` and from `privashed` to `published` are permitted but deferred to open questions." But then it states as a present-tense property that privashed "does not have this monotonicity property." Within the current model, it does — by the same argument that establishes D10 for `published`.

**Required**: State clearly that within the current formal model, `privashed` is also permanent (no operation transitions out of it), and that the intended non-monotonicity will be realized by operations in a future ASN. Alternatively, define a WITHDRAW or UNPUBLISH operation with appropriate preconditions to make the privashed-specific behavior formal.

### Issue 3: ASN-0026 frame extension for Σ.pub is unnamed

**ASN-0029, Publication**: "We extend their frame conditions: operations defined in ASN-0026 do not modify publication status, i.e., `(A d : d ∈ Σ.D : Σ'.pub(d) = Σ.pub(d))`."

**Problem**: This cross-ASN frame extension is used in the verification of D10 across all operations, making it load-bearing. But it is embedded in the D10 discussion prose rather than being a named property. Every other property in the ASN (D0–D17) has a label. This one — arguably the most important for the D10 verification — does not.

**Required**: Elevate to a named property (e.g., "D10-ext" or similar), or fold it into the Σ.pub definition as an explicit frame axiom for pre-existing operations.

## OUT_OF_SCOPE

### Topic 1: Associate access model for private documents
**Why out of scope**: D5(c) references "designated associates" who may access private documents. The mechanism for designating associates — what state tracks it, which operations establish or revoke it — is explicitly deferred. This is new state and new operations, not an error in the current ASN.

### Topic 2: Privashed transition operations
**Why out of scope**: The formal operations for `privashed → private` and `privashed → published` are explicitly listed as deferred. These require new operation definitions with their own preconditions, postconditions, and frame conditions — new territory.

### Topic 3: FINDDOCSCONTAINING accessibility filtering
**Why out of scope**: D17 quantifies over all of Σ.D regardless of publication status, meaning a query on a published document's I-addresses could reveal private documents that transclude from it. Whether D17 should be restricted to accessible documents is a design question the ASN correctly lists as open.

### Topic 4: Concurrent access and D15 enforcement
**Why out of scope**: D15 is stated as a design requirement on correct participants. The properties that concurrent access must satisfy to ensure D15 holds (locking, token-based access, session ordering) are implementation-layer concerns that the ASN correctly defers.

### Topic 5: Cross-account version provenance without structural ancestry
**Why out of scope**: When D12 Case 2 creates a version under a different account, the source-version relationship exists only through shared I-addresses — no structural ancestry in the address. What the system must preserve about this implicit relationship is a legitimate open question that doesn't affect the correctness of D12's formal specification.

VERDICT: REVISE
