# Review of ASN-0077

## REVISE

### Issue 1: Mixed V-spans citation error
**ASN-0077, edge case "V-span over link subspace"**: "Mixed V-spans (crossing both subspaces) are excluded by S8-depth: positions of different subspaces have different depths in `d`'s arrangement, and a single level-uniform V-span fixes a single depth `m`, hence a single subspace."
**Problem**: S8-depth does *not* assert that distinct subspaces have distinct depths — its own postcondition explicitly states "Distinct subspaces may have distinct depths." Combined with LinkVPositionDepthAxiom fixing `m_L = 2`, a document with `m_C = 2` would have both subspaces at depth 2, so a depth-2 V-span could in principle cover positions of both subspaces. The exclusion argument as written is unsound.
**Required**: Cite C0a (PrefixConfinement, ASN-0058): every `t ∈ ⟦σ⟧` satisfies `t_j = u_j` for `1 ≤ j < m`, so in particular `t_1 = u_1`. Combined with C0 (action point `= m ≥ 2`, hence `ℓ_1 = 0`, hence `reach(σ)_1 = u_1`), every position in `⟦σ⟧` shares `u`'s subspace identifier. This is what actually excludes mixed V-spans.

### Issue 2: O2 derivation — M-sub bridge missing or mis-ordered
**ASN-0077, O2 derivation (both cases)**: 
- *Content case*: "S3★ (ASN-0047) gives `aⱼ + i ∈ dom(C)`. This discharges M16a's precondition..."
- *Link case*: "S3★ gives `aⱼ + i ∈ dom(L)`. To apply CL-OWN at `vⱼ + i`, we need... `subspace(vⱼ + i) = s_L`. The subspace bridge: S8a ... discharges M-sub(a)'s precondition..."

**Problem**: S3★'s antecedent is `subspace(v) = s_C` (resp. `s_L`). To apply S3★ at `v = vⱼ + i` and conclude `aⱼ + i ∈ dom(C)` (resp. `dom(L)`), one must first establish `subspace(vⱼ + i) = s_C` (resp. `s_L`). In the link case, M-sub(a) is invoked, but for CL-OWN downstream — not for the upstream S3★ application that already required the same bridge. In the content case, M-sub is never invoked at all, leaving the subspace identification at `vⱼ + i` unjustified for the S3★ step.
**Required**: Reorder the link-case derivation: first apply M-sub(a) (precondition `#vⱼ ≥ 2` from S8a) to obtain `subspace(vⱼ + i) = subspace(vⱼ)`, then apply S3★, then CL-OWN. Apply the same explicit M-sub step in the content case before invoking S3★ to identify `aⱼ + i ∈ dom(C)`.

### Issue 3: Singleton I-span — length-preservation chain compressed
**ASN-0077, edge case "Singleton I-span", #b > #a sub-case**: "For non-zero extensions, K.α (ASN-0047) emits every content address by `inc(·, 0)` from a content sub-allocator whose first emission `[d.0.s_C.1]` has length `#d + 2` and whose subsequent emissions preserve length by TA5(c); since `b` would extend `a` and so share `a`'s origin document `d = origin(a)`, `b` and `a` would have the same length `#d + 2`, contradicting `#b > #a`."
**Problem**: The argument compresses several steps: (i) structural extension of `a` by `b` (forced by the T1 case analysis) combined with `zeros(b) = zeros(a) = 3` (S7b) implies `b`'s document-level prefix equals `a`'s, hence `origin(b) = origin(a)`; (ii) by SubAllocatorAxiom (ASN-0047), `d`'s content sub-allocator is T10a-conforming with first emission `[d.0.s_C.1]` of length `#d + 2`; (iii) by TA5(c) applied inductively along the sub-allocator's `inc(·, 0)` chain, every output has length `#d + 2`. The "same length" conclusion rests on SubAllocatorAxiom + T10a-conformance, not on K.α alone.
**Required**: Cite SubAllocatorAxiom (clauses (b), (c), (d)) for the first-emission length and sub-allocator discipline; cite TA5(c) explicitly for the inductive length-preservation. Spell out the chain "structural extension + S7b ⇒ same origin ⇒ same sub-allocator ⇒ same length" rather than collapsing it.

### Issue 4: O5 hypothesis redundant
**ASN-0077, O5 statement**: "For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable transition `Σ → Σ'`, if `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)`, then `origin'(a) = origin(a)`."
**Problem**: The conditional clause is implied by the antecedent: P0 (ContentPermanence, ASN-0047) gives `dom(C) ⊆ dom(C')` and L12 (referenced via P3) gives `dom(L) ⊆ dom(L')`, so `a ∈ dom(Σ.C) ∪ dom(Σ.L)` already implies `a ∈ dom(Σ'.C) ∪ dom(Σ'.L)`. The own derivation cites P3 to justify this consistency. Carrying the conditional both obscures the claim and signals that something might fail (which it cannot, given the monotonicity invariants the ASN itself relies on).
**Required**: Restate O5 without the conditional: "For any `a ∈ dom(Σ.C) ∪ dom(Σ.L)` and any reachable transition `Σ → Σ'`: `origin'(a) = origin(a)`." Use P3 in the derivation to discharge membership preservation rather than restating it as a hypothesis.

## OUT_OF_SCOPE

None. The Open Questions appropriately defer multi-origin link reporting, intermediate-chain surfacing, native-vs-transcluded distinction, unreachable-byte-fetch guarantees, historical-containment coupling, and intra-document sharing reporting to future ASNs — these are extensions of SHOWORIGIN, not flaws in this one.

VERDICT: REVISE
