# Review of ASN-0042

## REVISE

### Issue 1: O7(c) restates the same condition-classification three times with an intra-claim deferral

**ASN-0042, O7 postcondition (c)**: "the binding obligations being conditions (iii) and (v) of O15 (condition (i) is fixed by the choice of p'', and conditions (ii) and (iv) are auto-discharged at entry; see the proof and the Formal Contract)."

**Problem**: The classification of (i)–(v) into "fixed / auto-discharged / binding" appears verbatim in three places — the O7 header, the proof of (c), and the Formal Contract — and the header points forward to the other two ("see the proof and the Formal Contract"). This is exactly the forward-deferral / use-site-inventory pattern the anti-bloat classifier targets: the reader must skip between three locations to assemble one claim. The recent revision (`clarify binding vs auto-discharged conditions in O7(c)`) added prose rather than consolidating it.

**Required**: State the (iii)/(v)-binding, (ii)/(iv)-auto-discharged classification once (in the proof, where it is actually argued), and let the header and Formal Contract reference it without re-stating the breakdown.

### Issue 2: Condition (v) prose defers its content instead of stating it

**ASN-0042, O7 proof of (c)**: "Condition (v) is, by contrast, a genuine per-state obligation on the choice of p'' (its content is stated canonically in the Formal Contract)."

**Problem**: "its content is stated canonically in the Formal Contract" is a pointer in a slot that should carry reasoning. Either condition (v) matters to the proof of (c) (then state what it requires of p'') or it does not (then drop the sentence). A parenthetical deferral is noise.

**Required**: Either discharge/use (v) explicitly here, or remove the sentence.

### Issue 3: Fresh-baptism of a delegate prefix is encoded redundantly and near-circularly

**ASN-0042, O18 / O17b / Delegation condition (v) / Freshness-(v)**: O18 asserts (as an axiom) `pfx(π') ∈ Σ'.B ∖ Σ.B`; condition (v) asserts `pfx(π') = next(Σ.B, p, d)`; Freshness-(v) derives `pfx(π') ∉ Σ.B` from (v); O17b restricts registry changes to `Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}`.

**Problem**: These four overlap. Given O17b's baptism branch and condition (v) pinning `pfx(π') = next(Σ.B, p, d)` with `pfx(π') ∉ Σ.B`, O18's conclusion follows — *except* that nothing but O18 forces a delegation transition into O17b's baptism branch rather than its frame branch. So O18 is part-redundant, part-load-bearing, and the dependency is effectively circular (condition (v) names `next(Σ.B,p,d)` as the prefix; O18 says that prefix is freshly added; O17b says additions are `next(Σ.B,p,d)`). The structure does not declare which facts are primitive.

**Required**: Designate the primitive (e.g., "every transition introducing a principal takes O17b's baptism branch adding `next(Σ.B,p,d)`") and derive O18 (and Freshness-(v)'s freshness conjunct) from it, eliminating the circular triple-statement.

### Issue 4: A load-bearing invariant is buried as an inline one-line induction

**ASN-0042, O10 Construction**: "By O14's bootstrap-registry clause (base case) and O17b (BaptismalRegistryCoupling, inductive step), every reachable Σ.B is an ASN-0040-reachable registry, so hwm and next are well-defined on it."

**Problem**: The well-definedness of `hwm`/`next` (B1 and finiteness preconditions) on every reachable `Σ.B` is relied on by O10, by the entire worked example, and implicitly everywhere `next(Σ.B, ·, ·)` appears. Asserting it as a half-sentence induction inside one construction hides a system-wide invariant. A reader cannot cite it where else it is needed.

**Required**: Promote "every reachable `Σ.B` is an ASN-0040-reachable registry conforming to B₀ conf." to a named derived invariant with its base/step shown once, and cite it where used.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and provenance/owner divergence
**Why out of scope**: O3 fixes a refinement-only regime; transfer would change the transition vocabulary. The ASN correctly defers this (Open Questions) rather than smuggling a transfer operation in.

### Topic 2: Cross-node identity federation consistent with O9
**Why out of scope**: O9 establishes node-locality; federation is new state and new invariants, properly listed as an open question, not a gap in this ASN.

### Topic 3: Domain density / gaps between baptized siblings
**Why out of scope**: Whether `odom(π)` must be gap-free is an allocation-liveness question belonging to the baptism layer, already noted as open.

VERDICT: REVISE
