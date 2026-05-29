# Review of ASN-0040

## REVISE

### Issue 1: hwm precondition not updated to the B6 scoping
**ASN-0040, hwm(B,p,d) Formal Contract**: "*Preconditions:* B satisfies B1 for (p, d); p ∈ T, d ≥ 1; S(p, d) defined."
**Problem**: B1 was recently rescoped to B6-valid namespaces only (its invariant now reads `(A p, d : B6(p, d) : ...)`). The hwm *Justification* opens "By B1 (Contiguous Prefix), children(B, p, d) = {c₁, ..., cₘ}" — but B1 supplies nothing for a non-B6 `(p, d)`. B2's precondition was correctly tightened to "(p, d) satisfies B6"; hwm's was not. As written, hwm is licensed on `p ∈ T, d ≥ 1` namespaces where its load-bearing appeal to B1 does not hold.
**Required**: Add `B6(p, d)` to hwm's preconditions (and the *Invariant* line), matching the scoping already applied to B1 and B2.

### Issue 2: B1 statement carries a downstream-consumer inventory
**ASN-0040, §B1**: "Nothing downstream needs contiguity for a namespace baptism can never target — every consumer (hwm, B2, Bop's freshness clause, B8 Case 1, B9) invokes B1 only for B6-valid (p, d), so the invariant is scoped accordingly."
**Problem**: This enumerates B1's downstream call sites instead of advancing the invariant's meaning — the flagged "definition's introduction enumerates downstream consumers" pattern, accreted around the recent rescoping commit. The list rots the moment a new consumer appears, and the reader must skip it to reach the invariant.
**Required**: Delete the inventory. The invariant scope `(A p, d : B6(p, d) : ...)` already states the restriction; the consumer list is not needed to read it.

### Issue 3: B1 proof closes with defensive scope justification
**ASN-0040, §B1 proof**: "Because B1 is scoped to B6-valid namespaces, no non-B6 pair need be considered: the target reduces to (p₀, d₀) and every other case to a distinct B6-valid pair handled by B7."
**Problem**: This paragraph justifies *why the scoping is admissible* rather than discharging a proof obligation — reviser drift trailing the rescoping. B0a already restricts baptismal operations to B6-valid `(p₀, d₀)`, so the case split is forced by the operation vocabulary, not by an external scoping decision that needs defending here.
**Required**: Remove; the two-case structure (target vs. other B6-valid namespace) stands on its own.

### Issue 4: Bop body defers repeatedly to the Formal Contract
**ASN-0040, §Bop**: "STRUCTURAL (on Σ): B4 (Atomic Baptism, §B4 below). See the Formal Contract for its status as a Σ-invariant." and "The frame condition — only s.B is modified — is stated in the Formal Contract *Frame:* line below."
**Problem**: Multiple sentences in one definition point forward to the same downstream location rather than stating content — the "defer to the same downstream location" pattern. The reader bounces between the operation body and its contract to assemble one statement.
**Required**: State the frame and B4 status once, inline, or once in the contract — not as cross-pointing prose in both.

### Issue 5: B₀ conf. maps its conditions to downstream Base lines
**ASN-0040, §B₀ conf.**: "The three conditions are the Base lines of B_fin (finiteness), B1 (genesis contiguity), and B10 (seed T4-validity) respectively."
**Problem**: Use-site inventory — it indexes which downstream proofs consume each conjunct rather than advancing the seed condition. (The adjacent "Non-emptiness is not among them" sentence *is* useful clarification and should stay.)
**Required**: Drop the mapping sentence; the three conjuncts are self-explanatory and each downstream Base line already cites B₀ conf.

### Issue 6: Foundation name cited inconsistently for T0(a)
**ASN-0040, §B9 prose vs. proof**: prose says "T0(a) (UnboundedComponents)"; the proof says "T0(a) (UnboundedComponentValues)."
**Problem**: The foundation name is `UnboundedComponentValues`. Two spellings for one foundation claim in adjacent paragraphs.
**Required**: Use `UnboundedComponentValues` in both places.

## OUT_OF_SCOPE

### Topic 1: Content/Occupied relationship (B3)
**Why out of scope**: B3 names a future `Occupied` predicate and content storage. The ASN handles this correctly — as a parametric *forward requirement* that proves nothing here, not as an in-scope claim — so no revision is needed; flagged only to confirm the deferral is the right shape.

META: not applicable — the ASN defines state (s.B), an operation (baptize), and invariants (B0–B10) abstractly, with implementation references used only as grounding; it has not drifted into implementation mechanics.

VERDICT: REVISE
