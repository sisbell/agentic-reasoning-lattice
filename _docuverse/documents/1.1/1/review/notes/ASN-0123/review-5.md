# Review of ASN-0123

This is a careful, deeply-worked note. The core apparatus (SA, VN-B1, nextv) is sound, the ownership theorems (V8, V9) are airtight, and the foundation usage is conscientious — re-proving B1 as VN-B1 rather than citing it across transition systems is exactly the right move. I checked the proofs of SA, VN-B1 (all four K.δ cases), V8, V9(a)/(b), V10, V13, and V-WF's coupling discharge; they hold. Two precision defects remain.

## REVISE

### Issue 1: The forker is named `π` in the operation and `π'` in V9 — the symbol for the central parameter is swapped between sections.

**ASN-0123, Operation (cross-owner clause) vs. V9**: The operation's identity clause reads "`v := a fresh document identity that π allocates`" with maximality "`(A π'' ∈ Π : pfx(π'') ≼ v ⟹ #pfx(π'') ≤ #pfx(π)) (O5(ii))`" — here **`π` is the forker**, and O5 bounds by `#pfx(π)`. V9 then reads "`Let ω(d_src) = π ≠ π', and let v be the identity π' allocates — allocated_by(π', v)`" with maximality bounding by `#pfx(π')` — here **`π'` is the forker and `π` is the owner**.

**Problem**: The operation's forker `π` *is* V9's forker `π'`; the operation's (unnamed) owner *is* V9's `π`. A reader who carries the operation's convention into V9 — natural, since V9 is the operation's own correctness theorem — reads every `pfx(π)`/`pfx(π')` in the severance proof with the roles reversed. The math is locally self-consistent within each section (V9 re-binds both symbols), so this is not a soundness error, but reusing `π` for two different roles on the operation's defining parameter is exactly the kind of inconsistency that propagates into errors when later ASNs build on V9's statement.

**Required**: Use one symbol for the forker throughout. Keep `π` as the forker (matching the operation signature `VERSION(π, d_src)`) and name the owner explicitly — e.g. `π_o := ω(d_src)` — in V9. Then V9's severance reads "`Let π_o := ω(d_src) ≠ π`, `v` allocated by `π`," and the O5(ii) bound is `#pfx(π)`, consistent with the operation.

### Issue 2: V-WF's cross-owner realizability silently presupposes an account-tier forker.

**ASN-0123, V-WF**: "VERSION is realizable as a valid composite at every reachable Σ with d_src ∈ E_doc: the step sequence is **one K.δ**, then — when n ≥ 1 — one K.μ⁺ and |A| K.ρ steps." And: "In the cross-owner branch the K.δ instance draws from **the forker's account document sub-allocator** (a k = 2 descent or k = 0 sibling there — in vocabulary, its detail out of scope)."

**Problem**: P-prin is only "`π ∈ Π`," and by O1a (`zeros(pfx(π)) ≤ 1`) the foundation admits **node-tier** principals (`zeros(pfx(π)) = 0`) into Π. Such a forker has no account, hence no "account document sub-allocator" to draw from: producing a fresh document (`zeros = 2`) under a node prefix requires first baptizing an intermediate account (`zeros = 1`), so the identity allocation is *not* "one K.δ" but at least two entity-creation steps. The owned branch has no analogous gap — it allocates in `d_src`'s own pre-existing version namespace in one K.δ regardless of the forker's tier — so V-WF is rigorous for the owned case and for account-tier cross-owner forkers, but its uniform "one K.δ" and its "the forker's account document sub-allocator" carry an unstated hypothesis on `π`. The *validity* conclusion (couplings hold initial-to-final) survives a multi-step identity allocation, but the asserted step structure does not, and the realizability of the cross-owner branch genuinely depends on this hypothesis.

**Required**: State the presupposition. Either tighten the cross-owner branch's precondition to an account-tier forker (`zeros(pfx(π)) = 1`, or "π possesses an account-level document sub-allocator"), or qualify V-WF to read that the clean "one K.δ" structure holds for the owned case and for account-tier cross-owner forks, with the general cross-owner identity allocation a (possibly multi-step) out-of-scope document-creation composite whose only consumed contract is `Document(v) ∧ v ∉ E ∧` O5. The mechanics of how a non-account principal reaches a document are correctly out of scope; the unstated dependency on having an account is not.

## OUT_OF_SCOPE

(none — the note's deferrals to document creation, version comparison, content/link operations, and the serialization/windowing/withdrawal open questions are all appropriately scoped.)

VERDICT: REVISE
