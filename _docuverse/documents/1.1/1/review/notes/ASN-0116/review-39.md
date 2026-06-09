# Review of ASN-0116

This is a careful, thorough note. The two-layer split (content identity vs. arrangement), the K-atomic decomposition (`K.α`×n → `K.μ⁻` → `K.μ⁺` → `K.ρ`×n), the block-disjointness interval arithmetic, the I3-reconciliation, the coupling discharges (J0/J1★/J1'★), and the non-trivial discoverability wp (IP6, containment-not-emptiness) all check out. The four boundary cases (suffix-present, append, empty subspace, front-insertion `J=1` with `n'_{s_C}=0`) are covered, and the worked example exercises the postconditions concretely. The cross-references are all to foundation ASNs, so rule 7 is satisfied.

My findings are confined to the prose-accretion patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Process-rationale prose in the provenance discharge
**ASN-0116, "The document remains one coherent sequence" (provenance paragraph)**: "The consultation settles that this coupling is intrinsic to insertion — the inserting document's identity is minted into the address as content enters (4/11, theory answer: "the origin IS the address"), and the implementation makes the binding concrete by writing a DOCISPAN provenance record per inserted I-span (KB synthesis; theory answer "provenance follows creation, and for native insertion creation and placement are the same act")."

**Problem**: This sentence references the *consultation / KB-synthesis / theory-answer* process and argues *why* the provenance coupling exists. It is meta-prose: to follow the actual argument (the J0/J1★/J1'★ discharge that immediately follows and stands entirely on its own) the reader skips past it. The phrase "The consultation settles that this coupling is intrinsic" is exactly the reviser-drift pattern of new prose justifying *why* a clause is needed rather than establishing it.

**Required**: Cut the process rationale. Retain at most the bare evidence citation (4/11; the DOCISPAN record) as grounding for I-PROV, and let the formal J0/J1★/J1'★ discharge carry the weight.

### Issue 2: `J=1` sub-case duplicated across the composite section and the worked boundary
**ASN-0116, "INSERT as a valid composite," K.μ⁻ bullet**: "At the front-insertion extreme `J = 1` this branch still fires with `n'_{s_C} = 0`: the content subspace clears entirely … so the whole suffix is vacated and re-installed `n` higher by the following K.μ⁺ — distinct from the append case … and the empty subspace …"

**Problem**: The dedicated "Boundary — front insertion into a non-empty document (`J = 1`)" passage later re-walks this same `n'_{s_C}=0` strict-contraction case in concrete form. Since `J=1` already lies inside the general `1 ≤ J ≤ N` argument, the inline digression and the worked boundary say the same thing twice (general words, then concrete numbers). One of the two is doing the work; the inline digression is the trimmable one.

**Required**: Reduce the inline K.μ⁻ digression to a single clause noting that the bound `J−1 < N` holds down to `J=1` (so K.μ⁻ fires throughout `1 ≤ J ≤ N`), and let the dedicated front-insertion boundary carry the concrete `n'_{s_C}=0` walkthrough.

### Issue 3: "What INSERT does not do" lodged in the precondition
**ASN-0116, INSERT precondition**: "Link placement is a distinct operation drawing on K.λ, not K.α."

**Problem**: This is a statement of what the operation does not do, sitting mid-precondition where the reader is tracking the conjuncts that constrain `p`, `n`, and `d`. Per the placement guidance it is not meta-prose, but its location interrupts the precondition.

**Required**: Move it out of the precondition list (e.g. to the surrounding prose where the content/link subspace split is introduced), or drop it.

## OUT_OF_SCOPE

None. The note correctly confines link-discoverability discussion (IP4, IP6) to *consequences* of INSERT's arrangement effect via foundation lemmas (LP12, LP18), rather than specifying link discovery as an operation, and it defers transclusion / DELETE / concurrency to its Open Questions rather than claiming them.

VERDICT: REVISE
