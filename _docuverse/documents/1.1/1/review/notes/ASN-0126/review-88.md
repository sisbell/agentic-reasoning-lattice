# Review of ASN-0126

The framework is technically sound: the projection bridge, P5's manual lift, the three-move single-tuple-scope argument for the Binary wrapper, and the born-nullified worked example all check out, including the address arithmetic (`a_R = ...2.3`, `a = g = ...2.4 ∈ coverage(G_rng) = [...2.4, ...2.7)`). The C3-liveness observation and its concrete witness are correct and genuinely illuminating. The remaining findings are forward-reference residue (the note carries the anti-bloat classifier) plus one imprecise wp justification.

## REVISE

### Issue 1: The Nullify-fate caveat in "The registry" is a downstream preview

**ASN-0126, The registry**: "The inherited `Nullify` comes with a caveat the listing must flag: ASN-0086 defines it as an empty-from `Emit_R`, which has no `→_sh` image (The shape-gated emit), so under the gate the bare `Nullify` is unreachable — the framework's retraction is instead re-expressed as a from-filled `Emit_R`, itself a use of `Emit_K` (Retraction as an attributed Binary)."

**Problem**: This caveat establishes nothing where it sits. The "no `→_sh` image" fact is not derivable until "The shape-gated emit" (which it forward-references), and the re-expression is not given until "Retraction as an attributed Binary" (which it also forward-references). "The shape-gated emit" then states the same thing properly — it *derives* that the empty-from `Nullify` has no `→_sh` image from the `|F| = 1` rule, and points forward once to the re-expression. So the conclusion appears twice and is justified only downstream. The opener "a caveat the listing must flag" is itself meta-prose. This is exactly the "multiple paragraphs defer to the same downstream location" / "definition's introduction enumerates downstream consumers" pattern.

**Required**: In "The registry," list the inherited operation set `{Emit_K, Observe_K, Nullify}` without the caveat. Let "The shape-gated emit" — where the empty-from-has-no-image fact is proved — carry the `Nullify` consequence and the single forward pointer to "Retraction as an attributed Binary."

### Issue 2: The wp's reason for omitting precondition (0) is wrong, and clashes with the L3 claim two sentences later

**ASN-0126, Weakest precondition of the shape-gated emit**: "(the arity guard (0) is omitted from `g_sh` because the postcondition's arity-3 slice `|Σ.L(a)| = 3` already forces it)"

**Problem**: A guard conjunct appears in `wp(g → S, R) = g ∧ wp(S, R)` precisely when it can fail and block the step; a postcondition cannot "force" a guard away. The real reason (0) drops out is that the vehicle is `Emit_K`, which always constructs the triple `(F, G, K)` — so (0) is *vacuously true* for this operation (a value-condition, not a state-precondition) and contributes ⊤. The stated reason also contradicts the next paragraph, which says L3 is "discharged by precondition (0)": (0) cannot be both omitted-because-the-postcondition-forces-it *and* the live fact discharging L3's arity clause. The two statements reconcile only through the unstated fact that `Emit_K` always deposits an arity-3 triple.

**Required**: State that fact directly — (0) is vacuously satisfied because `Emit_K` constructs `(F, G, K)` with arity 3, hence adds no wp conjunct, and the same arity-3 fact discharges L3's arity clause. Then "omitted" and "discharges L3" stop conflicting.

### Issue 3 (minor): (0) and (i) are glossed twice in adjacent sentences

**ASN-0126, The shape-gated emit**: "...three added preconditions: (0) *the emitted value is a standard triple* — arity 3, so it carries exactly the two content slots `(F, G)` that `Sh-conf` reads; (i) *K is registered* — the registry records a shape for K; and (ii) `Sh-conf(K, F, G)`. Precondition (0) makes the value the standard triple ..., fixing `F = e₁` and `G = e₂` as its only two content slots, and (i) supplies `shape(K)` ... — so `Sh-conf(K, F, G)` ... is well-defined wherever (ii) is reached."

**Problem**: The two sentences gloss the same premises twice — "carries exactly the two content slots `(F, G)`" ≈ "fixing `F = e₁` and `G = e₂` as its only two content slots"; "the registry records a shape for K" ≈ "(i) supplies `shape(K)`." Only the well-definedness conclusion of the second sentence is new.

**Required**: List (0)/(i)/(ii) tersely in the first sentence; let the second sentence carry the partiality/well-definedness argument without restating the premises.

## OUT_OF_SCOPE

### Topic 1: G-cardinality shapes between Binary and Multi
The catalog offers `|G| = 0`, `|G| = 1`, and `|G| < ∞` (any). An app needing "at least one target" or "at most k" cannot express it — Multi admits 0 and is otherwise unbounded. Finer G-cardinality shapes are a future-catalog question (OQ6 covers F-arity and N, not G cardinality), not an error here.

### Topic 2: Dynamic registration
The registry is written only at `Σ_init` (P1 fixes it forever). An app needing to register or retire a type at runtime is outside this framework's immutable-registry design — a successor concern, consistent with the note's deliberate static-registration guarantee.

VERDICT: REVISE
