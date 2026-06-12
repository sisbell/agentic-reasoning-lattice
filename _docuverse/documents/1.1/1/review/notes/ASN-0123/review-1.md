# Review of ASN-0123

## REVISE

### Issue 1: The necessity half of G2 has an unproven step
**ASN-0123, "G2: links must carry through… — the transcription clause"**: "For that link to be discoverable from the version `v`, LP12 requires `coverage ∩ ran(Σ'.M(v)) ≠ ∅`; since the construction works uniformly for every `a ∈ A`, the guarantee forces A ⊆ ran(Σ'.M(v)) — range preservation is *necessary*."
**Problem**: By PrefixSpanCoverage, `coverage({(a, δ(1, #a))}) = {t : a ≼ t}` — the entire subtree of `a`, not `{a}`. LP12 therefore only forces `subtree(a) ∩ ran(Σ'.M(v)) ≠ ∅`. The conclusion `a ∈ ran` needs an additional fact: no element of `ran(Σ'.M(v)) ⊆ dom(C') ∪ dom(L')` (S3★) can be a *proper extension* of `a`. That fact is true — by LP-Sub every stored address has form `[d, 0, s, k]` with `zeros(d) = 2`, and a proper extension of `a = [d₀, 0, s_C, k]` would require a document prefix equal to `d₀.0` (trailing zero, not T4-valid) or `d₀.0.s_C` (`zeros = 3 ≠ 2`) — but it is nowhere stated or proved. Since this is the load-bearing step behind "the operation may not allocate content," the necessity claim does not follow as written.
**Required**: State and prove the stored-address prefix-antichain lemma (`subtree(a) ∩ (dom(C) ∪ dom(L)) = {a}` for stored `a`, derivable from LP-Sub's structural form), and cite it at this step.

### Issue 2: The ownership-model bridge is asserted, not established — ω may be undefined at the guard
**ASN-0123, "The Operation" / "State and Local Apparatus"**: "if ω(d_src) = π → v := nextv(E, d_src)"; "Ownership is the prefix model of ASN-0042: … effective owner ω(a) the unique most-specific covering principal (O2)…"; "we treat each entity-creating step as the baptism of its address, so E plays the registry role of ASN-0040's B for document-level addresses."
**Problem**: ω's totality and uniqueness on the registry is a *derived* property of ASN-0042's own reachable states — O2 rests on O4 (DomainCoverage), which rests on O14's bootstrap and the O12–O17b delegation dynamics. This ASN runs ASN-0047's transition system with ASN-0042's vocabulary, but never states which of those facts are assumed to hold of the hybrid (E as registry, K.δ as baptism, `allocated_by` attached to K.δ). Nothing stated guarantees every `d_src ∈ E_doc` has a covering principal, yet the operation's branch guard `ω(d_src) = π` is undefined otherwise. V8 and V9 likewise apply O2, O5, and O15 over hybrid states.
**Required**: A standing-assumptions paragraph: the docuverse states carry an ASN-0042-conforming principal structure (O4-coverage of E — derivable from an O14-analog plus NodeLineage and prefix transitivity, O12/O13/O15 dynamics, `allocated_by` attaching to K.δ); or add definedness of `ω(d_src)` to the preconditions.

### Issue 3: Contiguity of the version namespace (the B1-analog) is proved by parenthesis
**ASN-0123, "nextv (VersionFrontier)"**: "The realized children E ∩ S(d, 1) form a contiguous prefix {c₁, …, c_m} of the stream (ASN-0040's B1, maintained here because every allocation into the stream is a K.δ step on the stream's frontier: the k = 1 sub-case fires only when the namespace is empty and the k = 0 sub-case extends its maximal member — FrontierEquivalence, ASN-0047)".
**Problem**: B1 is an invariant of ASN-0040's transition system (Bop + B0a closure + seed conformance), not automatically of ASN-0047's K.δ vocabulary; transferring it needs an induction with three obligations, none shown: (i) the base case at Σ₀ (vacuous, but should be said); (ii) that the *only* K.δ outputs landing in `S(d, 1)` are `inc(d, 1)` and `inc(c_j, 0)` with `c_j ∈ E` — in particular that no `k = 2` output (which carries a zero where stream members carry `d`'s nonzero final component) and no other document's increment can produce a member of `S(d, 1)`; (iii) that freshness plus operand-membership force the frontier (`inc(c_j, 0)` already exists for `j < m`). FrontierEquivalence covers only the `(t, 0)` branch. This invariant carries G1's minimality, B2's `hwm + 1` form, V5(a–c), and V7's "enumeration terminates at the first absentee."
**Required**: State the contiguity invariant as a named claim and give the preservation argument — or route it through ASN-0034's AllocatedSet realized-prefix structure for the activated `A_v(d)` via ActivatedEmission and T10a.6.

### Issue 4: V3 is cited and tabled but never stated or proved
**ASN-0123, claims table**: "V3 | source frame: every d_src-indexed state component is unchanged; the fork is strictly additive and writes no forward pointer" — cited in V7 ("by V3 no d_src-indexed state mentions v"), V10 corollary (i), V12, and the evidence section.
**Problem**: There is no claim-site for V3 in the body. G3 derives the *demand* and the Effect clause *stipulates* the frame, but nothing shows the stipulated net frame is what the K.δ + K.μ⁺ + K.ρ step sequence actually produces (E-membership, `M'(d_src)`, C, L values, and the `d_src` provenance row — the last needing the observation that R grows only by `(a, v)` pairs).
**Required**: Add V3 as a stated claim with its short discharge from the composite's step frames.

### Issue 5: V5(a) conflates "k-th fork" with "k-th namespace allocation"
**ASN-0123, V5 (ChronologicalRank)**: "the k-th fork of d_src (counting forks performed in the owned branch, in commit order) receives v = d_src·k, the k-th stream member".
**Problem**: This holds only if forks are the namespace's *only* allocations. ASN-0047's own J4 fork composite also allocates on `A_v(d_src)`, and K.δ `k = 1`/`k = 0` steps are available to other composites; one interleaved non-VERSION allocation gives the k-th fork rank > k. The proof offered ("each fork takes the frontier, so rank = hwm + 1 = creation order") proves the namespace-relative statement. The missing hypothesis is VD — which the ASN introduces only later, explicitly as a discipline whose enforcement is deferred to Open Question 1.
**Required**: Restate (a) as "the k-th allocation into `S(d_src, 1)` receives `d_src·k`," or condition it explicitly on VD.

### Issue 6: V11(a) fails at the boundaries
**ASN-0123, V11 (EditIndependence)**: "every arrangement transition's structural precondition is satisfiable on v at Σ' with no further allocation".
**Problem**: False as quantified. For an `n = 0` fork, K.μ⁻ (strict contraction) and K.μ~ (requires the content image to take ≥ 2 distinct values) are unsatisfiable; for `n = 1`, K.μ~ is unsatisfiable; and when `dom(C) = ∅`, K.μ⁺ has no admissible image, so no arrangement transition is enabled at all. The intended point — no *v-specific* setup is needed — survives, but the universal claim does not. The ASN elsewhere takes pride in admitting the empty source; this clause must survive that same boundary.
**Required**: Weaken to the correct statement: `v ∈ E'_doc` with `ω'(v)` the forker stands under the same enabling conditions as any document — K.μ⁺ enabled whenever `dom(C) ≠ ∅`, K.μ⁻ whenever `n ≥ 1`, K.μ~ whenever the content image is non-constant — with nothing specific to `v` outstanding.

### Issue 7: V10 corollary (ii) states its key sentence backwards
**ASN-0123, V10, corollary (ii)**: "The guarantee extends, by the same equation evaluated at later states, to links created *after* the fork against the shared addresses: the version did not exist when such a link is conceived, yet the link reaches it."
**Problem**: For a link created after the fork, the version *does* exist when the link is conceived. The intended statement is the converse: the link did not exist when the version was forked, yet it reaches the version. Additionally, "the same equation evaluated at later states" is conditional on the version still arranging the shared addresses at that later state (no intervening contraction); corollary (iii) covers contraction but (ii)'s extension does not reference the condition.
**Required**: Fix the direction of the sentence and add the standing-arrangement condition (or a pointer to corollary (iii)).

### Issue 8: The atomicity remark claims more than the foundations supply
**ASN-0123, Remark (atomicity)**: "there is no observable state in which the version exists without its snapshot."
**Problem**: The composite has an intermediate state — post-K.δ, pre-K.μ⁺ — in which `v ∈ E_doc` with `M(v) = ∅`. SequentialTransitionAxiom grants atomicity per *atomic* transition, not per composite, and nothing in ASN-0047 forbids another composite from beginning at that intermediate state. "Observable" is doing unsupported work; the ASN's own Open Question on concurrent-fork serialization concedes this neighborhood is unresolved.
**Required**: Restate as a boundary-level fact — no composite boundary of a valid VERSION exhibits `v` without its snapshot — or state the assumed composite-isolation convention explicitly.

## OUT_OF_SCOPE

### Topic 1: Enforcement of VD across the full operation vocabulary
**Why out of scope**: Which future operations may allocate into a version namespace, and under what invariant, is exactly the ASN's first Open Question; it belongs to the document-creation and operations ASNs. (Within this ASN it surfaces only as the conditioning gap flagged in Issue 5.)

### Topic 2: Cross-owner identity allocation mechanics
**Why out of scope**: The forker's document-creation namespace (K.δ `k = 2` descent / `k = 0` sibling under the account, and the realizability of that step) is CREATENEWDOCUMENT territory; the ASN's three stated constraints plus O5 carry V9, so deferring the mechanics is legitimate.

### Topic 3: Derivation-direction recovery and supersession semantics
**Why out of scope**: What could orient a cross-ownership derivation when only symmetric shared-content provenance survives, and whether withdrawal semantics can coexist with permanence, are correctly parked as Open Questions — new guarantees, not errors here.

VERDICT: REVISE
