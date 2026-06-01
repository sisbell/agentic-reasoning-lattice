# Review of ASN-0086

## REVISE

### Issue 1: M2 misattributed to ASN-0036

**ASN-0086, "State transition relation" → *Arrangement modification is out of scope***: "ASN-0036's M2 (EmptyArrangement) — `(A d ∈ dom(M) :: M(d) = ∅)` — is the invariant that results."

**Problem**: M2 (EmptyArrangement) is a claim of **ASN-0093**, not ASN-0036. ASN-0036 has no M2 (its catalog is S0–S5, S7*, S8*, D-*); the M0/M1/M2 family is introduced in ASN-0093. The cited statement `(A d ∈ dom(M) :: M(d) = ∅)` matches ASN-0093's M2 verbatim. A reader chasing the foundation will not find M2 in ASN-0036.

**Required**: Change the attribution to "ASN-0093's M2 (EmptyArrangement)."

### Issue 2: Working-domain paragraph overclaims "full L/S/M/C catalog" preservation, contradicting the FreshLinkKeyDisjointness sub-lemma

**ASN-0086, "Working domain — `→*`-reachable states"**: "Each `→`-step is a single K.σ/K.α/K.λ primitive, which preserves the full L/S/M/C invariant catalog (ASN-0036, ASN-0043, ASN-0093)..."

**Problem**: This is stated as unconditional preservation of the *full* catalog, citing ASN-0043. But L14 (DualPrimitive) and L14a (NonTranscludability) are ASN-0043 invariants that ASN-0093's K.λ contract does **not** publish — which is precisely why the note must supply the FreshLinkKeyDisjointness sub-lemma to discharge them at the fresh key. R0's own proof admits this: "RT-closure's preservation clause carries the full L/S/M/C invariant catalog to Σ' (with L14/L14a at the fresh key supplied by the FreshLinkKeyDisjointness sub-lemma, since ASN-0093's K.λ contract does not itself publish them)." So the headline claim citing ASN-0043 overstates what the K-primitive alone delivers; the summary prose and the actual proof obligation disagree.

Relatedly, the FreshLinkKeyDisjointness proof derives L14 at the fresh key via the `s_L ≠ s_C` argument and then parenthetically notes "SD ... delivers `dom(Σ'.L) ∩ dom(Σ'.C) = ∅` directly" — two routes to the same conclusion in one paragraph.

**Required**: Scope the Working-domain claim to ASN-0093's *published* K-contract catalog, and state explicitly that L14/L14a are carried by FreshLinkKeyDisjointness rather than by the primitive's contract. Drop the redundant second derivation in the sub-lemma (keep either the `s_L ≠ s_C` argument or the direct SD appeal, not both).

## OUT_OF_SCOPE

### Topic 1: Higher-arity retraction tuples and `nullified`

`nullified(Σ)` quantifies over `L_R^Σ`, which by construction admits only standard-triple (`|Σ.L(a)| = 3`) links. A retraction recorded as a higher-arity link with type-coverage equal to `coverage(R)` would not be collected. Since the relational layer's `Nullify` always emits arity 3, this cannot arise within the layer; higher-arity relations are explicitly deferred to Open Questions. Not an error in this ASN.

VERDICT: REVISE
