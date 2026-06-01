# Review of ASN-0047

This is a carefully constructed ASN; the core mathematics (the K.δ case discharge, the D-SEQ★ derivation, the K.μ~ admissibility/fixity argument, GlobalLineage) is rigorous, with concrete worked examples discharging the key postconditions. My findings are confined to meta-prose accretion (the note carries `review-mode.anti-bloat`) and one precision point. I found no soundness gap.

## REVISE

### Issue 1: S8★ carries a downstream-consumer inventory and a "no consumer" essay
**ASN-0047, *Amendments to existing transitions*, S8★**: "S8★ has no consumer within this ASN: no property here takes it as a premise … S8★ is carried as a per-state invariant solely to *provision the downstream INSERT/DELETE operation ASNs*, whose run-mechanics … take the per-subspace correspondence-run decomposition as their working substrate. Within this ASN, S8★ discharges no obligation beyond its own preservation…"

**Problem**: This is precisely the anti-bloat pattern flagged: a definition's prose enumerating downstream consumers (INSERT/DELETE run-mechanics) and explaining its own lack of an in-ASN consumer, with a forward reference to out-of-scope operation ASNs. It explains future provisioning rather than advancing the invariant's meaning, and a precise reader must skip the entire passage to reach the actual preservation argument. The legitimate content (S8★ is a per-subspace decomposition state property, established by two routes, preserved by each transition) survives without it.

**Required**: State S8★, its two-route establishment, and its preservation. Delete the "no consumer within this ASN" essay and the downstream INSERT/DELETE provisioning inventory.

### Issue 2: Defensive parenthetical in K.μ~ Step (A) imagines a case the stipulation already excludes
**ASN-0047, *Decomposition of K.μ~*, Step (A)**: "(this is exactly why S3★-aux is stipulated by clause (i): without it a candidate image such as `π(v) = [7, 1, 1]` would satisfy S8a yet have first component `7 ∉ {s_C, s_L}`, leaving S3★(Σ')'s two implications vacuous at `π(v)` and the exhaustiveness below unestablished)."

**Problem**: Reviser-drift pattern — a parenthetical that conjures a case (`[7,1,1]`) which the stipulated S3★-aux(Σ') already excludes, then explains *why the stipulation exists* rather than advancing the derivation. Clause (i) already names S3★-aux as a hypothesis; the proof consumes it directly in the very next sentence ("With both source and image subspaces confined to `{s_C, s_L}`…").

**Required**: Drop the parenthetical. The clause-(i) stipulation and its use suffice.

### Issue 3: Defensive justification accretion around the Bridging lemma and K.σ subsumption
**ASN-0047, *The state model***: (a) "(†) is a definitional consequence, not a tracked per-state invariant … Hence (†) carries no separate preservation obligation and is not enrolled in ExtendedReachableStateInvariants."; (b) the *Notational convention* M2 paragraph "In ASN-0047 M2 holds only at the registration event … it is deliberately superseded by the arrangement-extension transitions."; (c) K.δ Frame "This is exactly ASN-0093 K.σ's effect `dom(M') = dom(M) ∪ {e}`, made visible at the operation rather than only through the Bridging lemma."

**Problem**: These passages explain *why* facts are not enrolled, *why* an inherited invariant is not inherited, and *why* an effect is shown at one location rather than another — defensive/document-organization meta-prose rather than statements of what the model does. Each can collapse to a single clause without losing content.

**Required**: Reduce to terse statements: (a) "(†) holds by the lockstep K.δ effect and the default-value convention"; (b) "M2 holds at registration but is superseded by K.μ⁺/K.μ⁺_L"; remove (c)'s presentation-justification clause entirely.

### Issue 4: K.μ⁺ relies on a content-depth concept defined later, under the link-subspace heading
**ASN-0047, *Elementary transitions*, K.μ⁺**: "The content-subspace depth `m_C(d)` is governed by the live-depth re-pinning rule stated once under *V-position depth (operational)*."

**Problem**: `m_C(d)` is used in K.μ⁺'s precondition, but the governing rule lives several sections downstream under *Link-subspace extension* and is framed primarily for `m_L(d)` (with a parenthetical that it "governs both subspaces uniformly"). A content-subspace transition deferring its depth semantics to a link-section forward reference forces the reader to jump forward to follow the precondition.

**Required**: Either state the live-depth rule once at first use (the K.μ⁺ precondition) and reference it from the link section, or move the rule to a subspace-neutral location preceding both K.μ⁺ and K.μ⁺_L.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: J4 correctly leaves a forked document's link subspace empty and the ASN flags a link-inheritance mechanism as future work. This is new territory (a future operations/version ASN), not a defect here.

### Topic 2: Address-space exhaustion of a document's link/content sub-allocator
**Why out of scope**: The open questions raise whether allocation can fail. Allocation-availability is governed by the foundation (T0 unboundedness) and downstream operation ASNs, not by this transition model.

VERDICT: REVISE
