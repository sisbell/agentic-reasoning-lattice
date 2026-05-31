# Review of ASN-0093

This note is structurally sound — the sub-allocator construction, the T10/T7 freshness arguments, the ChainMembershipForOrigin contiguous-prefix induction, and the C1c/L1c chain exhibitions all check out, and the nine-step worked example computes correctly at every key (verified tumblers, zero-counts, origins, and the prefix-comparable/incomparable cross-document cases). My findings are confined to the forward-reference / meta-prose accretion the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Consecutiveness-dependency stated twice, once as a defensive recap

**ASN-0093, "Address sub-allocators under documents" and the FirstEmission proof**:

The anchors paragraph already establishes the dependency in its derivation — "yielding `[d.0.(s_C+1)] = [d.0.s_L]` once `s_L = s_C + 1` is supplied by SubspaceConventionAxiom" — and then closes with a recap sentence that adds nothing:

> "Both value identifications consume SubspaceConventionAxiom — the link anchor in particular is producible by a sibling `inc(·, 0)` off `b_C(d)` *only because* the two subspace identifiers are consecutive."

The same point is then made a third time inside the FirstEmission proof as a defensive justification:

> "The link case runs the same SiblingStream argument at `p = b_L(d)`, but is *not* a pure content↔link relabelling: reaching the link anchor `b_L(d) = inc(b_C(d), 0) = [d.0.s_L]` consumes `s_L = s_C + 1` (SubspaceConventionAxiom), where the content anchor reaches `b_C(d)` directly by `inc(d, 2)`."

**Problem**: Two paragraphs in different sections say the same thing in different words; the FirstEmission version is the "is *not* a pure relabelling" defensive-justification pattern — prose explaining why a case is being shown rather than advancing the case. The consecutiveness fact is load-bearing exactly once, in the anchor derivation where it is already discharged.

**Required**: Drop the anchors recap sentence and the "not a pure relabelling" clause. The FirstEmission link case can simply cite the anchor construction for `b_L(d)` and proceed.

### Issue 2: Event-local lemma paragraph carries a use-site inventory

**ASN-0093, "Discharge of stated invariants" → Simultaneous-induction framing**:

> "The FirstEmissionFreshness and SubsequentEmissionFreshness lemmas are *event-local*: each is a one-shot freshness obligation discharged at the K.α/K.λ binding precondition that commits the emission (and reused in the SD matrix row), not a state property carried in the per-state IH conjunction."

**Problem**: The parenthetical "(and reused in the SD matrix row)" is a downstream-consumer inventory — it enumerates where the lemma is cited rather than advancing the proof. This is the use-site-inventory pattern the classifier flags.

**Required**: Remove the parenthetical. The matrix rows already cite the lemmas at their own sites; the framing paragraph need only state that the two freshness lemmas are event-local, not where they recur.

### Issue 3: M2's vacuity rationale duplicates the Scope deferral

**ASN-0093, "Scope" and "M2 (EmptyArrangement)"**:

The Scope section states:

> "The substrate fixes `M(d)` at `∅` on registration ... so the arrangement-side invariants of ASN-0036 hold vacuously; the arrangement-extension primitives that would make them non-trivial are deferred to a higher-layer ASN."

M2 then restates the identical point:

> "M2 is the explicit ground on which the arrangement-side invariants of ASN-0036 (S2, S3, S8a, S8-depth, S8-fin, D-CTG, D-MIN) hold vacuously in the substrate."

**Problem**: Two sections assert the same fact (arrangement invariants vacuous because `M(d) = ∅`, mutation deferred). One of them is redundant.

**Required**: Keep the concrete enumeration once (M2 is the better home, since it names the invariants), and reduce the Scope mention to the bare deferral of `K.μ*` without re-deriving the vacuity.

### Issue 4: "Terminology" note restates M0

**ASN-0093, "State model" → Terminology**:

> "'Document' in this substrate means 'element of `dom(M)`' — a purely structural notion (a T4-valid tumbler with `zeros = 2` registered into the arrangement function's domain)."

**Problem**: The parenthetical "(a T4-valid tumbler with `zeros = 2` ...)" restates M0, which is stated in full two sections later. The structural reading of "document" is fine; the embedded re-statement of the M0 predicate is the redundant part.

**Required**: Trim the parenthetical to "element of `dom(M)`" and let M0 carry the well-formedness conditions.

## OUT_OF_SCOPE

Nothing to add — arrangement mutation, entity stratification, provenance, coupling, and link withdrawal are correctly declared out of scope and the substrate does not smuggle claims about them in.

VERDICT: REVISE
