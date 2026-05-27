# Review of ASN-0069

## REVISE

### Issue 1: Forward reference in K.δ subcase A verification reads as backward reference

**ASN-0069, "The Fork Composite" verification, K.δ sub-case A**: "Outer-precondition `¬IsElement(d_new)` follows directly from `IsDocument(d_new)` already established"

**Problem**: `IsDocument(d_new)` is not yet established at this point in the verification flow — it appears two paragraphs later ("By KDeltaZerosK01, `zeros(d_new) = zeros(d_src) = 2`, so `IsDocument(d_new)`"). Sub-case B handles the same situation correctly with the phrase "(established below)" acknowledging the forward reference. The mismatch between sub-cases obscures whether the reader is following a circular chain or a forward reference.

**Required**: Either change sub-case A to "(established below)" to match sub-case B, or restate `¬IsElement(d_new)` derivation directly from `zeros(d_new) = 2 ≠ 3` (which can be established at this point from `d_src ∈ E_doc` + KDeltaZerosK01 without first naming IsDocument).

### Issue 2: V8a's "as long as" clause is incongruent with K.α-only scope

**ASN-0069, V8a**: "V8's correspondence between `d_src` and `d_new` over the V-positions present at fork time is preserved across every K.α step as long as those V-positions remain in both arrangements."

**Problem**: V8a is scoped specifically to K.α steps (per its opening "Subsequent K.α allocations…"). K.α's frame condition `(A d :: M'(d) = M(d))` means V-positions cannot be removed by K.α — the contingency "as long as those V-positions remain" never bites within the lemma's scope. The clause either (i) reads as if K.α could affect V-position presence (false) or (ii) silently widens the scope to interleaved sequences (in which case V8a duplicates V8b without saying so). V8b is the place that handles cross-operation evolution.

**Required**: Drop the "as long as those V-positions remain in both arrangements" clause from V8a, since K.α-only persistence is unconditional. Cross-operation behavior belongs to V8b.

### Issue 3: Worked example sentence on sibling-fork distinctness is unparseable

**ASN-0069, "Worked Example", subsequent-fork paragraph**: "V10(a) holds concretely: `d_new = inc(d_src, 1)` differs from `d_new² = inc(d_new, 0)` in length when contrasted with `d_src` (both share length `#d_src + 1`) and in the trailing component when contrasted with each other (TA5(c) at the subsequent fork modifies position `sig(d_new) = #d_new` only — incrementing `d_new`'s final `1` to `2` — so `(d_new²)_{#d_new} = 2 ≠ 1 = (d_new)_{#d_new}`)."

**Problem**: The clauses "differs from `d_new²` … in length when contrasted with `d_src`" and "(both share length `#d_src + 1`)" contradict each other under any natural reading. The intent appears to be "both have length `#d_src + 1` (sharing length, not differing) and differ in the trailing component", but the surface text says they "differ in length". A reader checking V10(a) here will be stalled.

**Required**: Rewrite to make the two siblings' length agreement and trailing-component disagreement explicit and non-contradictory.

### Issue 4: V5a(a) labels K.δ as "non-arrangement-modifying" while K.δ initialises M for new entities

**ASN-0069, V5a clause (a)**: "if the transition is M-targeted at some `d_target ≠ d*`, or is any non-arrangement-modifying elementary transition (K.α, K.λ, K.δ, K.ρ)"

**Problem**: K.δ on `IsDocument(e)` sets `M'(e) = ∅`, which is an arrangement modification at the freshly created entity. The clause's correctness rests entirely on the parenthetical that follows ("K.δ frames `(A d' : d' ≠ d_new : M'(d') = M(d'))` … `d_new ≠ d*` because …"), but the umbrella label "non-arrangement-modifying" misclassifies K.δ. A reader who only consumes the headline label will miss that K.δ requires the freshness/distinctness step that the parenthetical supplies.

**Required**: Either re-label this group as "preserves arrangements of all pre-existing documents" (which is what the parenthetical actually proves) or split K.δ out from the umbrella with its dedicated frame condition stated up front.

### Issue 5: V11a recovery argument relies on suffix-chain transitivity without re-running induction

**ASN-0069, V11a recovery, "Prefix identity" clause**: "For each `0 ≤ i ≤ k`, the chain `dⁱ_new ≼ d^k_new` (from the prefix-chain derivation above, instantiated at the suffix segment `dⁱ_new ≼ dⁱ⁺¹_new ≼ ... ≼ d^k_new` and composed via the established transitivity of `≼`)…"

**Problem**: The "prefix-chain derivation above" established `d_src ≼ d^k_new` by induction from `d_src = d⁰_new`. For arbitrary `i`, the suffix segment `dⁱ_new ≼ … ≼ d^k_new` requires its own induction starting at `i`, not a "composition". The shorthand "instantiated at the suffix segment" papers over the need to re-run the inductive argument with a different start point. The result is correct, but the citation is hand-waved.

**Required**: Make the inductive step explicit — either by stating a generalized "for any starting index `j`, `dʲ_new ≼ d^k_new` by induction on `k - j`" lemma and instantiating it twice, or by walking through the suffix induction once.

## OUT_OF_SCOPE

### Topic 1: A_v sub-allocator activation axiom

**Why out of scope**: The ASN consistently uses `A_v(d_src)` and cites ASN-0047's Allocator hierarchy as the basis. ASN-0047's SubAllocatorAxiom explicitly activates only `A_C(d)` and `A_L(d)` on K.δ; `A_v(d)` is defined in the Allocator hierarchy but its activation is not separately axiomatized. This is an ASN-0047 gap, not an ASN-0069 defect; ASN-0069 correctly uses the foundation as written.

### Topic 2: Snapshot vs. living fork semantics

**Why out of scope**: V11's "transitive identity along unedited fork chains" and V10a's "time-sensitivity of derivation" together commit the ASN to snapshot semantics — the fork inherits source state at fork-time and propagates no further. Whether a "living" variant exists is a design alternative, not a gap in this ASN.

### Topic 3: Permission and discoverability model

**Why out of scope**: Whether a user is authorised to fork `d_src`, whether the source's owner can enumerate descendants, and whether fork events are observable from the source's vantage all belong to a separate access/registry layer that the abstract transition system does not specify.

VERDICT: REVISE
