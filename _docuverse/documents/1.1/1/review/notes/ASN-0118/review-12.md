# Review of ASN-0118

## REVISE

### Issue 1: Stated effect/frame clauses do not vacate pre-shift positions — S2 (functionality) is not established by the postconditions in the displacing case

**ASN-0118, "The COPY operation" (CP2, CP3a, CP3b, CP6)**: The operation is introduced as "the transition Σ → Σ' with the following effect ... and the frame conditions that say what it leaves alone," with CP2 binding `Σ'.M(d)(p + i) = cᵢ` and CP3a binding `Σ'.M(d)(v + W) = Σ.M(d)(v)` for `v ≥ p`.

**Problem**: In the displacing case (`p ≤ max`), the placement positions `[p, p+W)` overlap the *ordinals of the pre-state positions* `p, …, min(p+W−1, max)`. CP2 binds position `p` to `c₀`. Nothing in CP2/CP3a/CP3b/CP6 removes the pre-state binding `p ↦ Σ.M(d)(p)` — CP3a only asserts a *new* binding at `p+W`, CP3b frames only `v < p`, and CP6 frames only `subspace(v) ≠ s_C`. Taken as the operation's definition, the stated clauses therefore admit a post-state in which `p` is bound to both `c₀` (CP2) and the un-vacated `Σ.M(d)(p)` — a double binding that violates S2 (ArrangementFunctionality). Functionality is in fact established *only* by the separately-exhibited K.μ⁻ + K.μ⁺ composite (where K.μ⁻ removes the `≥ p` positions before K.μ⁺ re-adds them), not by the effect/frame clauses that purport to define the transition. ASN-0082 faces exactly this and states an explicit vacating clause (I3-V, PostInsertionVacating) plus a domain characterization (D-DOM); ASN-0118 omits the analogue.

**Required**: Either add an explicit vacating / domain-closure postcondition for the text subspace (e.g., that the only `s_C` bindings of `Σ'.M(d)` at ordinals `≥ p` are the placement positions `[p, p+W)` and the shifted positions `{v+W : v ∈ V_{s_C}(d), v ≥ p}`, with the pre-state positions in `[p, max]` vacated), or state explicitly that COPY *is defined* as the exhibited composite with CP2/CP3 as its derived net effect. As written, S2 cannot be discharged from the postconditions alone.

### Issue 2: CP8 range-new characterization is internally contradictory

**ASN-0118, ProvenanceRecording (CP8)**: "For each `cᵢ` that is *range-new* — newly in the content-subspace range of `M(d)` at `Σ'`, which the placement (CP2) makes every placed address not already in that range — ASN-0047's coupling J1★ ... demands the membership ..."

**Problem**: The parenthetical asserts "the placement (CP2) makes every placed address" range-new, i.e., that *every* `cᵢ` is newly in the range. The very next paragraph then treats the case "For each `cᵢ` that is *not* range-new — already in the content-subspace range of `M(d)` in the pre-state," and the worked example's re-COPY variant exhibits exactly a placed address (`x₁`) that is not range-new. The clause therefore contradicts the ASN's own subsequent handling. A reader cannot tell whether range-new is being *defined* (placed and not already in the pre-state range) or *claimed universal* (all placed addresses).

**Required**: Rewrite the parenthetical to define range-new unambiguously (placed by CP2 *and* not already in the pre-state content-subspace range), removing the assertion that placement makes *every* placed address range-new.

### Issue 3: Empty-destination depth uses `m_{s_C}(d)` before it is defined

**ASN-0118, displacing/append decomposition (empty sub-case)**: "`p` is a valid insertion position, so `#p = m_{s_C}(d)` (ValidFirstInsertionPosition (a)) ... every placement position has depth `m_{s_C}(d)`."

**Problem**: When `V_{s_C}(d) = ∅`, the common depth `m_{s_C}(d)` is undefined (ASN-0047, LinkSubspaceDepth: `m_S(d)` is well-defined only while `V_S(d) ≠ ∅`). ValidFirstInsertionPosition fixes `#p = m` for a *chosen* parameter `m ≥ 2`, not for a pre-existing `m_{s_C}(d)`. Writing `#p = m_{s_C}(d)` in the empty sub-case is circular — it names a depth the operation has not yet established. The ASN partly acknowledges this ("establishing it, in the empty sub-case") but still equates `#p` with `m_{s_C}(d)`.

**Required**: In the empty sub-case, state `#p = m` for the chosen `m ≥ 2` and note that this *defines* `m_{s_C}(d)` for the post-state, rather than equating `#p` with an as-yet-undefined `m_{s_C}(d)`.

## OUT_OF_SCOPE

(none — the ASN confines INSERT/DELETE/REARRANGE/MAKELINK interactions to its Open Questions rather than defining claims for them, which is the correct treatment.)

VERDICT: REVISE
