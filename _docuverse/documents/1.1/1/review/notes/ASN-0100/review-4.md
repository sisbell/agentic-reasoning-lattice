# Review of ASN-0100

## REVISE

### Issue 1: I3-C citation does not match INSERT's content frame

**ASN-0100, "Discovering the Three Effects" → Effect Three frame summary**: "The content store is unchanged outside the freshly allocated addresses (I3-C, PostInsertionContentFrame; ASN-0082)."

**Problem**: ASN-0082's I3-C states `dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a))` and explicitly notes "Exact equality, strictly stronger than S0." INSERT extends `dom(C)` by `n` new addresses, so `dom(C') ≠ dom(C)`. I3-C as defined in ASN-0082 is therefore *not* satisfied by INSERT — it applies to a shift-only operation, not to INSERT which combines shift with content allocation. The cited frame does not match what INSERT actually establishes; the wording "unchanged outside the freshly allocated addresses" is weaker than I3-C's "Σ'.C = Σ.C".

**Required**: Remove the I3-C citation or rephrase to clarify that INSERT's content frame is weaker than I3-C: existing `dom(C)` entries are preserved pointwise (matching S0), but `dom(C)` itself extends by `{a_0, …, a_{n−1}}`. The actual preservation comes from INS.C's third clause and S0/P0 directly, not from I3-C.

### Issue 2: Imprecise citations for shift last-component arithmetic in S2 disjointness proof

**ASN-0100, "Verifying the Invariants" → "Arrangement functionality (S2)"**: 

- "Insertion positions have last component in {p_m, p_m + 1, …, p_m + n − 1} (by shift's last-component arithmetic per OrdAddHom and ShiftPreservation, ASN-0036)."
- "Shifted-right positions image v with last component ≥ p_m to a position with last component ≥ p_m + n (by TS4, ShiftStrictIncrease; ASN-0034)."

**Problem**: 
- TS4 (ASN-0034) gives `shift(v, n) > v` — whole-tumbler strict increase under T1 — not the specific component arithmetic `(shift(v, n))_m = v_m + n`. The latter requires TumblerAdd applied to `shift(v, n) = v ⊕ δ(n, m)`, where TumblerAdd's piecewise definition at action point `m` directly yields last component `v_m + n`.
- ShiftPreservation (ASN-0036) is stated explicitly for I-addresses (`a ∈ dom(Σ.C)`) and concerns `zeros`, T4-validity, `#E`, and `subspace_I`. It does not address V-position last-component arithmetic. The V-position analog is OrdShiftHom, which yields subspace preservation, S8a preservation, and an ordinal-projection identity, but again not the last component directly.

**Required**: Tighten the citations. For Insertion last components: cite TumblerAdd (ASN-0034) directly via the OrdinalShift definition, or cite OrdAddHom (a) (ASN-0036) which gives `ord(shift(p, k)) = ord(p) ⊕ w_ord` from which the last-component identity follows. For Shifted-right last components: cite TumblerAdd, not TS4.

### Issue 3: Missing explicit Insertion-region carve-out for I3-VD, I3-VP, I3-fin, I3-S7

**ASN-0100, "Verifying the Invariants"**: The ASN explicitly carves out the Insertion region when citing I3-S2 ("does not cover the Insertion region") and I3-S3 ("the Insertion region's contribution is verified explicitly"), but does not similarly carve out for I3-VD (PostInsertionDepthUniformity), I3-VP (PostInsertionWellFormedness), I3-fin (PostInsertionFiniteness), and I3-S7 (PostInsertionAllocationInvariants) — which also apply to ASN-0082's smaller post-state and require separate verification on the Insertion region.

**Problem**: The verification of S8-depth, S8a, S8-fin on the post-state is folded into the D-CTG★/D-MIN★/D-SEQ★ section through indirect inheritance, but the ASN never names the Insertion-region verification of these properties explicitly. A reader has to reconstruct from scattered observations (e.g., the empty-case S8a verification) that the Insertion positions satisfy each predicate.

**Required**: For each of I3-VD, I3-VP, I3-fin (and S7 invariants), state explicitly that ASN-0082's coverage is over Left + Shifted-right + cross-subspace, and provide the Insertion-region verification — even if brief. The Insertion-region verification of S8a (zero-free, depth ≥ 2, positive components) is given for the empty case but not factored out as a general property.

VERDICT: REVISE
