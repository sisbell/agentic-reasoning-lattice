# Review of ASN-0115

I checked the substrate citations, the Confinement lemma, and each of R0–R11 against the foundation contracts. **The mathematics is sound** — I found no correctness error. The Confinement proof (T5 with `p ≼ s`, `p ≼ reach(σ)`, `s ≤ t ≤ reach(σ)`) is valid; the R6 gap analysis correctly pins the canonical start from `act ≠ ∅` and reduces "no interior hole" to D-SEQ★ contiguity; the R8 subspace-dispatch (contrapositive of S3★ + S3★-aux + SD) and CL-OWN/CL-UNIQ link-vacuity are correct; the five worked instances check out arithmetically (I verified `δ(5,2)=[0,5]`, `reach=[1,7]`, `act={[1,2],[1,3],[1,4]}`, and `[1,2,1]∈⟦σ⟧`). The findings below are accretion/placement (the active `review-mode.anti-bloat` patterns) plus one mis-targeted proof citation.

## REVISE

### Issue 1: R8's boxed claim has absorbed its own proof

**ASN-0115, "What co-delivery reveals: transclusion" (R8 box)**: the boxed claim statement contains, verbatim, a multi-step derivation —

> "To run store membership *back* to subspace we need that each of subspace(v), subspace(v') is one of s_C, s_L to begin with — supplied by S3★-aux ... whereupon the contrapositive of the off-store S3★ branch closes the step: were subspace(v) = s_L while a ∈ dom(Σ.C), S3★ would force a ∈ dom(Σ.L), contradicting SD; so a ∈ dom(Σ.C) fixes subspace(v) = s_C ..."

— followed by the full CL-OWN/CL-UNIQ vacuity proof, all inside the `> **R8**` block.

**Problem**: R1–R5 establish this ASN's own convention — the box states the obligation, the prose below proves it. R8 (and, more lightly, R9, whose box carries the content/link `origin`/`home` dispatch) breaks that convention by embedding proof in the claim slot. To extract what R8 actually obligates ("content positions co-resolving to one address deliver identical, shared-origin material, one item per position; link co-resolution is impossible, so the guarantee is content-only") a reader must wade past the derivation. This is essay/proof content in a structural slot — exactly the accretion the anti-bloat mode flags, and it compounds if left.

**Required**: Reduce the R8 box to the obligation statement (matching R1–R5's clean form). Move the subspace-dispatch derivation and the CL-OWN/CL-UNIQ vacuity argument into the prose that follows the box. Apply the same trim to R9's box.

### Issue 2: R7's repeatability proof mis-cites immutability for link items

**ASN-0115, R7 proof**: "Over the intervening transitions `Σ →* Σ'`, content immutability (S0) and link immutability (L12) hold the stored entry fixed, giving `Σ.C(a) = Σ'.C(a)` (resp. `Σ.L(a) = Σ'.L(a)`)."

**Problem**: For a link position the delivered item is `⟨ref, a⟩` — it carries the *address* `a`, never the link value `Σ.L(a)`. So `Σ.L(a) = Σ'.L(a)` is the wrong equality: it is neither needed nor consulted. The link item's stability already follows from the step proven two sentences earlier ("`act` and the resolved addresses agree position-for-position"), which gives `a = a'` and hence `⟨ref,a⟩ = ⟨ref,a'⟩`. The conclusion holds, but the cited justification (L12 / `Σ.L(a)`) targets a value the item does not deliver — and L12 does no work here. The genuine asymmetry (content items need S0; link items need only arrangement-equality) is silently lost.

**Required**: For the link case, justify item-stability by the already-established agreement of resolved addresses; reserve S0 (and drop L12) for the content case, where value-persistence is actually load-bearing.

### Issue 3: Standing-precondition paragraph carries a use-site inventory and a why-justification

**ASN-0115, "The substrate we build on" (Standing precondition)**: "Throughout this ASN, every state `Σ` — including the states named in the V-spec and `deliver` definitions and in every claim R0–R11 — ranges over states *reachable from the initial state `Σ₀`* ... This scoping is load-bearing: the per-state invariants the claims below cite are established by ASN-0047 ... only of reachable states, and may fail otherwise."

**Problem**: Two of the named accretion patterns appear in one short paragraph: a use-site inventory ("including the states named in ... every claim R0–R11") and prose explaining *why* the scoping is needed ("load-bearing ... may fail otherwise") rather than just stating it. The necessary content is one sentence: every state `Σ` ranges over states reachable from `Σ₀`.

**Required**: Trim to the bare scoping statement; drop the R0–R11 enumeration and the "load-bearing / may fail otherwise" justification.

## OUT_OF_SCOPE

### Topic 1: inline provenance, hard-fail policy, straddling spans, channel faithfulness
**Why out of scope**: These are correctly deferred by the ASN itself (Open Questions; the R2 frame-limit and the OQ on a single boundary-crossing span). The ordinal-level restriction + Confinement lemma legitimately push a single straddling span to a future ASN, and R6's authorization/existence caveat correctly separates "unbound position" from "unconsultable document." No gap in *this* ASN — the boundary is drawn well. Raising none of these as REVISE.

META: not applicable — the ASN defines an abstract pure-query operation over state with state-component invariants (precedent: ASN-0086 Observe); implementation references are cited as evidence, not as the specification.

VERDICT: REVISE
