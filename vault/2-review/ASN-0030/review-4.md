# Review of ASN-0030

## REVISE

### Issue 1: A3 note contradicts the qualification for transition (c)

**ASN-0030, Accessibility Transitions**: "Transitions (a) through (e) are each achievable by a single operation."

**Problem**: The same section subsequently establishes that transition (c) — unreferenced to active — is "not achievable by any currently defined operation" for truly unreferenced addresses (refs(a) = ∅). If refs(a) ≠ ∅ the address was never in state (ii); it was active in another document. So no single operation takes an address from state (ii) to state (i). The note and the qualification contradict each other.

**Required**: Revise the note to exclude (c) from the single-step list. Something like: "(a), (b), (d), (e) are each achievable by a single operation. (c) is permitted by the invariants but not achievable by any currently defined operation for truly unreferenced addresses. (f) is composite."

---

### Issue 2: A4a missing frame condition

**ASN-0030, REARRANGE**: A4a specifies `pre`, `post (a)-(c)` but no frame condition.

**Problem**: A4 includes `(f) (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))`. A5 includes `(f)-(g)`. A4a, which is also a "specification requirement," omits the corresponding frame. Since REARRANGE targets a single document, P7 (CrossDocVIndependent) should apply — other documents' V-spaces are preserved. Without stating this, A4a is an incomplete specification.

**Required**: Add a frame condition:

    (d)  (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d'))

---

### Issue 3: A5(f) contradicts postconditions when d_s = d_t

**ASN-0030, COPY**: "(f) Σ'.V(d_s) = Σ.V(d_s)" and the precondition does not require d_s ≠ d_t.

**Problem**: Self-transclusion is valid (P5, ASN-0026). When d_s = d_t, the target's V-space changes by (a)-(e) — it gains k positions. But (f) asserts the source (= target) V-space is unchanged. This is a direct contradiction. Concrete case: d has V-space [a, b, c]. COPY(d, 1, 1, d, 3) should produce [a, b, a, c] by (a)-(e), but (f) requires [a, b, c].

**Required**: Either condition (f) on d_s ≠ d_t, or remove (f) entirely since (g) already covers d_s when d_s ≠ d_t. The narrative ("the source and other documents are unchanged (f)–(g)") should note the self-copy case.

---

### Issue 4: A8 ghost analysis cites wrong inc invocation

**ASN-0030, The Ghost Domain**: "Child allocation `inc([1], 1)` produces exactly `[1, 0, 1]` by TA5(d)."

**Problem**: TA5(d) says `#t' = #t + k`. For t = [1] and k = 1: #t' = 1 + 1 = 2, with k − 1 = 0 intermediate zero-positions, and position 2 set to 1. Result: [1, 1], not [1, 0, 1]. To produce [1, 0, 1] requires k = 2: #t' = 1 + 2 = 3, position 2 is the intermediate zero, position 3 is 1.

**Required**: Change `inc([1], 1)` to `inc([1], 2)`.

---

### Issue 5: A8 ghost permanence argument has a vacuous premise

**ASN-0030, The Ghost Domain**: "Ghost addresses at the *same level* as existing allocations — between siblings — remain ghosts permanently."

**Problem**: T10a (AllocatorDiscipline, ASN-0001) requires each allocator's sibling stream to advance exclusively by `inc(·, 0)` — sequential increment by 1 at the last significant position. If siblings t₁ and t₃ were produced by the same allocator with t₁ < t₃, then every address between them at the same level was necessarily produced by the sequential stream (the allocator passed through each value). Combined with T8/P1 (addresses are never freed), same-level ghosts between siblings of the same allocator cannot exist. By T10 (PartitionIndependence), same-level addresses under the same parent prefix come from the same allocator. The premise — a ghost t₂ between allocated siblings t₁ and t₃ at the same level — is unreachable under the allocation model. The two-case argument (sibling allocation can't fill it, child allocation can't fill it) is formally correct but proves a vacuously true statement.

**Required**: Either (a) acknowledge that T10a's sequential discipline prevents same-level gaps between siblings, making the permanence claim vacuously true, and reframe in terms of where ghosts actually exist (beyond the allocation frontier, in unestablished subtrees); or (b) define the ghost permanence claim for the scenarios that actually arise — frontier ghosts (above the highest sibling in each allocator's stream) are permanent because T9 (ForwardAllocation) ensures all future allocations exceed them.

---

## OUT_OF_SCOPE

### Topic 1: MAKELINK operation specification

**Why out of scope**: The ASN derives link integrity consequences (A7, A7a, A7b) from address permanence applied to endset I-addresses. The derivations are sound given the definitions. But MAKELINK — the operation that creates links and populates endsets — is not formalized in any foundation ASN. The link-related properties here are consequences of A0 applied to I-addresses, not link-specific machinery. Formalizing link creation, link state (Σ.links), and link operations belongs in a future links ASN.

### Topic 2: Historical backtrack mechanism

**Why out of scope**: The ASN correctly identifies that recovering truly unreferenced content (transition (ii)→(i)) requires a mechanism not yet specified and records it as an open question. Formalizing this mechanism and its invariants is new territory.

### Topic 3: Publication constraints on reachability loss

**Why out of scope**: The open question "can published content become unreferenced?" identifies a real design tension (D10 monotonicity of publication vs. D5 owner modification rights), but resolving it requires policy decisions beyond this ASN's scope.

VERDICT: REVISE
