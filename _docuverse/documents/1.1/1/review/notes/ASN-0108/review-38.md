# Review of ASN-0108

This is a strong note. The windowed-retrieval laws are abstract (the key is a declared design parameter, the guarantees are key-property-conditional), the worked walks under W5/W6/W8/W9 are concrete and check out, and the weakest-precondition analysis in W2 (identity vs. offset cursor, with the strict nesting membership-identity ⟹ frozen-prefix ⟹ genuine `wp`) is genuinely deep. W9a's count formula `⌈m/N⌉ + [N divides m]` verifies against all four boundary walks (`m=4`, `m=5`, `m=0`, `N>m`), and foundation usage (D-NONMONO, F-V/F-FULL, LP12/13/17/18, T9, F-LAMBDA) is consistent. The findings below are precision and accreted-prose, not structural.

## REVISE

### Issue 1: The stated import boundary is contradicted by W6a

**ASN-0108, "State, the Matching Set..."**: "We import exactly two qualitative facts about `Match` and use nothing more: (M-fin)... (M-mut)..."

**ASN-0108, W6a**: the set-level bridge invokes "ASN-0127's F-LAMBDA," "a function of `Σ.M(d_q)` alone (F-IMG, ASN-0127)," and "`findlinks_V(W, d_q, ·) = findlinks(image(W, d_q, ·), ·)` (F-V)" to derive `Match(q, Σ') = Match(q, Σ) ⊎ ({ℓ_new}...)`.

**Problem**: W6a uses three further ASN-0127 results (F-V, F-IMG, F-LAMBDA) — a structural fact about how `Match` *changes* under `K.λ`, beyond M-fin (finiteness) and M-mut (non-monotonicity). "Exactly two... and use nothing more" is therefore an overstated exhaustiveness claim that the body exceeds. A precise reader who relies on the boundary to know what the windowing layer rests on is misled, and the claim is the kind of "exactly N" assertion the anti-bloat pass should not leave standing when it is false.

**Required**: Either drop "and use nothing more," or state the import honestly — M-fin, M-mut, plus (for W6a) the `K.λ`-increment structure of `Match` (the F-LAMBDA/F-V/F-IMG bridge). The bridge itself is correct and should stay; only the minimality claim is wrong.

### Issue 2: W5 states clause-1 sufficiency-not-necessity three times

**ASN-0108, W5 (claim)**: "Clause 1 is the natural per-cursor condition, and it is not necessary; coherence is inherently a whole-pass property, since a condition evaluated independently at each cursor's transition cannot witness one cursor's drop being offset by a later cursor's rise."

**ASN-0108, W5 (post-claim paragraph)**: "Sufficiency does not run backwards, and the reason is that a clause-1 failure is an *event* whereas a skip or a duplicate is an *outcome*. ... The events need not accumulate into either outcome (the cancellation walk below), so clause 1 at every held cursor implies coherence but is not implied by it."

**Problem**: The same result — clause 1 sufficient, not necessary, because per-cursor failures can cancel over the pass — is asserted in the claim ("coherence is inherently a whole-pass property"), re-cast in the post-claim "event vs. outcome" paragraph, and then *proven* by the cancellation walk. The walk is the load-bearing content; the two prose passes are interpretation of a result the walk already demonstrates. To reach the proof the reader skips two restatements.

**Required**: State non-necessity once, let the cancellation walk carry it, and remove the duplicate "event vs. outcome" framing (or compress it to the single sentence the walk needs). Keep the walk and the cut-point/tail-reorder walks intact.

### Issue 3: The three-key computability breakdown is re-derived in W8, W9, and W9b

**ASN-0108, W8**: "Both identity keys keep `κ(c)` computable through orphaning — the address key by value-totality..., the matched-content key (least covered I-address) by endset persistence (L12/LP13); only the content-position key fails."

**ASN-0108, W9**: "(which either permanent key supplies — the address key for free, the matched-content I-address key via endset persistence)"

**ASN-0108, W9b(i′)**: "supplied for free by either permanent key (a *value-total* address key... or Gregory's matched-content I-address key, whose cursor key persists by that same permanence)"

**Problem**: W8 is the home of the computability result and establishes the three-key breakdown there correctly. W9 and W9b(i′) then re-derive the identical breakdown (address: value-total; matched-content: endset persistence; position: fails) rather than citing it, and the "ladder of key conditions" paragraph supplies a fourth statement of the computability/value-totality vocabulary that W8 also defines inline. This is the same fact restated across four sites.

**Required**: Let W8 own the breakdown; have W9 and W9b reference it ("under cursor-key computability, W8") instead of re-deriving the per-key cases. Resolve the computability/value-totality definition to one site (the ladder paragraph *or* W8, not both).

## OUT_OF_SCOPE

The natural extensions — multi-document enumeration with independent allocators, delivery guarantees for non-allocation-monotone keys, cross-state completeness over a mutating set, the uncomputable-cursor protocol, and progress-query coordination — are correctly deferred to the note's own Open Questions rather than specified here. No additional out-of-scope coverage to flag; count-only retrieval (W10) and link creation (used only via the `K.λ` frame) are likewise correctly held outside.

VERDICT: REVISE
