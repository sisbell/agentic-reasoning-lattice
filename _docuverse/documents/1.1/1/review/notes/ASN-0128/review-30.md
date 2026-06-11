# Review of ASN-0128

The load-bearing arguments were checked in detail and hold: I0's single-span-determined-by-coverage argument (T1-least start, endpoint separation, TA-LC cancellation) is complete and correctly preconditioned; I0a's two inclusions are proven, not asserted; I1a's induction covers every step kind, including the K ~ R wrapper instantiation and the born-nullified deposit; I6's wp equivalence is established in both directions with the attainability convention doing exactly the work claimed; DR's C3-emptiness derivation (distinctness at the pre-state, antichain at the constructed post-state via RP-c) is sound, and its hit branch correctly re-establishes each postcondition at the unchanged state rather than concluding it from a step; BH2's termination bound and BH4's totality of `age` both check out. The transfer bookkeeping (RP-a vs RP-b vs RP-c) is applied correctly at every crossing I traced, including the subtle RangeSterilization-by-RP-b case in I2. Two issues remain.

## REVISE

### Issue 1: BH1's Effect line states denotation-level exclusion while `is_filtered` is coverage-level
**ASN-0128, BH1 (read-filter), Effect; restated in S1 (Retired)**: "Addresses carrying an active tuple of this type are excluded from the *result sets* of the default view's two enumeration surfaces on every other registered type" and S1's "the default view on every other type excludes it from enumeration *results*."
**Problem**: The formal rewrite drops a result element `x` iff `¬is_filtered(x)` fails, and `is_filtered(addr)` tests `addr ∈ coverage(F)` — a membership predicate, per AD a subtree test. So retiring `t` excludes not only `t` but every extension `t.x` from every other type's default-view enumerations. The Effect line and S1 both state the strictly weaker denotation-level reading ("addresses carrying an active tuple," "excludes it"). The note polices exactly this denotation/coverage distinction everywhere else — AM's two matching regimes, D2's bridge, I0a's separating pair — yet here the normative summary and the formal predicate disagree, and the subtree-wide reach of a Unary filter mark (retiring a document-level address filters its entire subtree from default enumerations) is nowhere stated as intended behavior, only derivable from the displays.
**Required**: Align the prose with the predicate: state in BH1's Effect (and S1) that exclusion is coverage-scoped — an extension of a filtered address is also dropped from default-view results — and that this is the AD assertion doctrine applied to the filter mark. Alternatively, if denotation-level filtering was the intent, redefine `is_filtered` as a denotation test and remove it from the membership regime; the current text commits to both readings at once.

### Issue 2: The attainability-convention sentence is duplicated verbatim in I6 and DR
**ASN-0128, I6 ("The wp, assembled") and DR (immediately after the wp display)**: "The equivalence is read as ASN-0126's WP lemma reads its own wp — the attainability convention `wp(g → S, R) ≡ g ∧ wp(S, R)` is in force: on a rejected call nothing fires and the wp is false outright." — word-for-word identical in both sections.
**Problem**: This is the anti-bloat duplication pattern at its purest: the same convention statement, in the same words, in two sections. The two *necessity arguments* that follow each instance are genuinely different (I6's convention guards a no-instance-of-POST case; DR's guards a postcondition-true-at-the-unchanged-state case) and both must stay — but the convention itself needs stating once.
**Required**: State the convention once at its first use (I6, or a one-line reading convention where the note's wp displays are introduced) and have DR cite it in a clause ("read under I6's attainability convention"). Each site keeps its own necessity argument; only the shared statement is deduplicated.

## OUT_OF_SCOPE

### Topic 1: Wrapper-level concurrency contract
I4 fixes the race semantics for `Emit_K` under both idem flags, and the wrapper's behavior follows compositionally (`Nullify_Binary ≡ Emit_R` with idem=⊤: a same-document, same-target race dedups via I1; cross-document races deposit redundant-but-harmless tuples, per BH4's case split). But no single place states the wrapper's race contract.
**Why out of scope**: The result is derivable from I4 + I1 + S3 as committed; consolidating it is successor material, not an error here.

### Topic 2: App-facing naming of registered coverage classes
The three shipped classes get surface names (`retired`, `supersedes`, `R` — Standard registrations), but app-registered classes have no naming or presentation story: `targets_keyed` returns a "map K → addr" keyed by coverage classes with no committed serialization of the keys.
**Why out of scope**: This belongs to the registration/declaration protocol, adjacent to Open question 8's multi-app composition — new territory, not a defect in this note's semantics.

VERDICT: REVISE
