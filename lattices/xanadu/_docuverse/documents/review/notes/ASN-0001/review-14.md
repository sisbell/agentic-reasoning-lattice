# Review of ASN-0001

## REVISE

### Issue 1: Span length representation claim contradicts constructive definition

**ASN-0001, Spans (T12)**: "In practice, span lengths in the element subspace are single-component tumblers `[n]` denoting a count of `n` consecutive positions"

**Problem**: This claim is correct only when the start address is itself a single-component ordinal (V-space ordinal-only view). For full I-space addresses — which is where links reference spans and endsets are defined — a single-component length `[n]` has action point `k = 1`, and `s ⊕ [n]` replaces the entire hierarchical structure below position 1. Concretely: `[1, 0, 3, 0, 2, 0, 1, 5] ⊕ [2] = [3]` — a server-level address, not the intended `[1, 0, 3, 0, 2, 0, 1, 7]`. The correct element-level displacement for a full I-space address is `[0, 0, 0, 0, 0, 0, 0, n]`, which has action point `k = 8`. The formal definition T12 is sound (it imposes no restriction on `ℓ` beyond `ℓ > 0` and TA0's `k ≤ #s`), but the informal characterization will mislead any reader who attempts to compute `s ⊕ ℓ` for an I-space span using a single-component length.

**Required**: Either (a) state explicitly that "single-component tumblers" applies to within-subspace ordinals and that I-space spans require lengths whose action point matches the hierarchical level of the start address, or (b) give the concrete form of an element-level I-space span length (e.g., `[0, 0, 0, 0, 0, 0, 0, n]` for an 8-component address) alongside the single-component shorthand.

### Issue 2: TA7a formal statement underdetermined on representation

**ASN-0001, Subspace confinement (TA7a)**: "`(A a ∈ S₁, w element-local : a ⊕ w ∈ S₁)` and symmetrically for `⊖`"

**Problem**: The verification section establishes that there are two distinct representations (2-component V-position `[N, x]` with displacement `[0, n]`, and ordinal-only `[x]` with displacement `[n]`) and that these have materially different behaviors under `⊖`. In the 2-component view, `[1, 5] ⊖ [0, 2]` produces `[1, 5]` (a no-op) — the result is technically in `S₁`, so TA7a holds, but the subtraction has not performed the intended shift. The verification correctly resolves this by adopting the ordinal-only formulation, and the worked example confirms the issue and its resolution. But the formal statement of TA7a does not specify which representation `a ∈ S₁` and "element-local `w`" refer to. The phrase "symmetrically for `⊖`" suggests the property is uniform across both operations, when in fact the verification shows it holds for different reasons (genuine shift for `⊕`, vacuous closure for `⊖` in the 2-component view, genuine shift for both in the ordinal view).

**Required**: The formal statement of TA7a should declare the ordinal-only representation as canonical (consistent with the resolution in the verification) and note that "element-local displacement" means `w = [n]` applied to the within-subspace ordinal `[x]`, with the subspace identifier as structural context outside the arithmetic. The "symmetrically for `⊖`" should be replaced with the explicit ordinal-level statement for both operations.

### Issue 3: Worked example does not verify T12 for I-space spans

**ASN-0001, Worked example**: The example verifies T1, T4, T5, T6, T9, T7, TA7a, TA7b, TA1, and TA4, but does not construct an I-space span or verify T12 against a concrete case.

**Problem**: T12 is a central property — "spans are the fundamental unit of content reference" — yet the worked example never computes `s ⊕ ℓ` for an I-space start address `s`. Given Issue 1 (the action-point sensitivity of span lengths), an explicit I-space span example would both verify T12 and resolve the ambiguity about span length representation. The example has all the ingredients: five I-space addresses forming a natural span.

**Required**: Add a T12 verification to the worked example. For instance: the span `(a₂, ℓ)` covering `a₂, a₃, a₄` has `s = 1.0.3.0.2.0.1.2` and `ℓ = [0,0,0,0,0,0,0,3]` (three elements). Verify `s ⊕ ℓ = 1.0.3.0.2.0.1.5 = a₅`, so the span denotes `{t : a₂ ≤ t < a₅} = \{a₂, a₃, a₄\}`. This simultaneously demonstrates the correct form of an element-level I-space span length.

## OUT_OF_SCOPE

### Topic 1: Crash recovery and allocation counter durability

The ASN's open questions include "Must allocation counter durability across crashes be a global-history property or only a per-session property?" This is a liveness/recovery property that lies outside the algebraic framework established here. The algebra gives the invariant (T9: monotonic allocation); the recovery mechanism that restores the invariant after a crash belongs in an operational ASN about system lifecycle.

**Why defer**: T9 specifies the safety property; the recovery protocol is new territory requiring its own preconditions and proof obligations (e.g., what state is durable, what can be reconstructed from I-space content).

### Topic 2: Span intersection and splitting algebra

The formal summary notes that spans are "self-describing contiguous ranges" but no property addresses span intersection, splitting, or merging. These operations are needed by DELETE (which partially affects spans) and by the enfilade traversal (which must split spans at tree boundaries). The properties exist — they follow from T12 and the arithmetic — but deriving them is non-trivial and belongs in an ASN on editing operations.

**Why defer**: The tumbler algebra provides the foundation; span operations are the next layer up.

### Topic 3: V-space position representation convention

The ASN establishes that V-positions are "element-local 2-component tumblers" but also that the arithmetic operates on ordinals only (1-component). Whether the canonical V-position is `[N, x]` or `[x]`-with-context-`N` affects how editing operations are specified. This convention choice belongs in the POOM / editing operations ASN.

**Why defer**: The algebra supports both representations; the choice of convention is an operational decision that depends on how editing operations decompose their work.

VERDICT: REVISE
