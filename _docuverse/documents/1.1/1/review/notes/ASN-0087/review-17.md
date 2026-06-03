# Review of ASN-0087

## REVISE

### Issue 1: First-link V-position depth is not determined by the current state, contradicting the "computed from state" claims

**ASN-0087, Inputs**: "The caller does not — and cannot — specify the link's address or its V-position in the home document. Both are determined by the system from the current state."

**ASN-0087, Effect**: "The caller does not supply `v_ℓ`; the substrate computes it from the link subspace's current cardinality and depth."

**Problem**: These two positive claims are false in the first-link boundary case. The same Effect section states: "The depth `m_L(d)` of the link subspace is *not* fixed by the substrate to any particular value: when `V_{s_L}(d) = ∅`, K.μ⁺_L's `ValidFirstLinkPosition(d, v_ℓ, m)` admits any chosen `m ≥ 2`." When `V_{s_L}(d) = ∅`, the cardinality is `0` and `m_L(d)` is *undefined* (m_L(d), ASN-0047, is "well-defined only while V_S(d) ≠ ∅"). So `v_ℓ` cannot be "computed from the link subspace's current cardinality and depth" — its depth is a free parameter. The ASN both asserts `v_ℓ` is state-determined and acknowledges it is not, an internal contradiction. The contradiction propagates to M-Pre, M-Alloc, and M-Effect, all of which present `v_ℓ` (and its depth `m_L(d) ≥ 2`) as substrate-determined without exposing the first-link free choice.

**Required**: Reconcile the determinism claims with the free-`m` case. Either (a) add `m` as an explicit MAKELINK input for the first-link case, (b) fix `m` by convention (e.g., minimal `m = 2`) and state that convention normatively, or (c) revise the Inputs/Effect/M-Pre/M-Alloc/M-Effect prose to state that when `V_{s_L}(d) = ∅` the first link's V-position depth is a free parameter not determined by `Σ`, and specify what supplies it. The worked example silently makes this choice ("We choose the minimal admissible depth `m = 2`"), which underscores that the choice is exogenous to the state.

## OUT_OF_SCOPE

### Topic 1: `dom(M)` vs `E_doc` reconciliation discharging K.μ⁺_L's `d ∈ E_doc` precondition

The ASN discharges K.μ⁺_L's load-bearing `d ∈ E_doc` precondition (ASN-0047) by `d ∈ dom(M)` (ASN-0093) "under the standing assumption that the combined substrate maintains the coupling," explicitly deferring to "a not-yet-written substrate-reconciliation ASN."

**Why out of scope**: The two foundations use different notations for the allocated-document set, and reconciling them affects every operation in the combined model, not MAKELINK specifically. This is genuine framework-level territory for a future ASN, not an error introduced here. (Noted only so the gap is on record; the ASN flags it itself.)

### Topic 2: Who selects the first-link-subspace depth as a policy matter

The Open Questions already gesture at deferred-consistency and movement of V-positions; the *policy* for choosing `m` when a subspace is first populated (as opposed to the *specification gap* flagged in Issue 1) is a sequencing/authoring-layer concern.

**Why out of scope**: Issue 1 requires the ASN to stop *claiming* `v_ℓ` is state-determined; the broader question of an optimal depth-selection policy across operations is future territory.

VERDICT: REVISE
