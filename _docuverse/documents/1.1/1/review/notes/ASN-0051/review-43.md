# Review of ASN-0051

## REVISE

### Issue 1: K.μ~ listed as "elementary transition" in SV7

**ASN-0051, SV7 (DiscoveryInvarianceUnderLFrame)**: "For every elementary transition Σ → Σ' that holds L in frame — K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, and K.ρ"

**Problem**: K.μ~ is identified in ASN-0047 as a "distinguished composite," not an elementary transition. ASN-0047's elementary set is {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}. The SV7 wording conflates the two categories. The proof itself remains sound (K.μ~ decomposes to K.μ⁻ + K.μ⁺, both L-frame), but the terminological imprecision propagates: a reader tracing "every L-frame elementary" through the body cannot match the seven listed against ASN-0047's six elementaries.

**Required**: Rephrase as "every elementary transition or distinguished composite that holds L in frame" or list elementaries and K.μ~ separately. Apply the same fix in SV13(e) where K.μ~ is similarly conflated.

### Issue 2: SV11 biconditional proof wording omits "overlap"

**ASN-0051, SV11 (PartialSurvivalDecomposition)**, biconditional (⇒) proof: "equality with m · p therefore forces ... (ii) each non-empty term to be itself a maximal fragment, ruling out condition (b)'s adjacency or overlap of distinct non-empty terms within a block (**any adjacency would coalesce two terms into one fragment**, dropping the count below m · p)."

**Problem**: The parenthetical justifies only the adjacency half. Two non-empty decomposition terms that *overlap* (share an I-address) within a block also coalesce into a single fragment, and the biconditional explicitly covers this case ("adjacent or overlap"). The proof needs to discharge both halves.

**Required**: Change to "any adjacency *or overlap* would coalesce two terms into one fragment" and add the one-line argument that overlapping terms, being individually contiguous within I(β_k), share an extremum position and therefore form one ordinal-contiguous region.

### Issue 3: discover_through_s(d) lacks a formal SV claim

**ASN-0051, Link Discovery section**: introduces `discover_through_s(d) = discover_s(ran(M(d)))` as "the document-derived specialisation of discover_s," noting that unlike discover_s(A) on a fixed A, it varies with M(d). The behaviour under K.μ⁺/K.μ⁻ is then described only informally in the "Caveat — document-derived discovery is not permanent" remark.

**Problem**: discover_through_s is a named operator that downstream consumers will use (it is *the* natural query when reading "what links target this document?"). The ASN proves SV2–SV5 for π/locate and SV7–SV9 for discover_s, but the parallel survivability statements for discover_through_s are left as exercises in the reader's derivation. Specifically: monotonicity under K.μ⁺/K.μ⁺_L (analogue of SV2), reduction under K.μ⁻ (analogue of SV3), document-isolation (analogue of SV4), and the non-permanence caveat all deserve labelled status. Without these, downstream proofs about discover_through_s cannot cite this ASN.

**Required**: Add an SV claim (or a small group) stating: (a) discover_through_s(d) ⊆ discover_through_s(d) under K.μ⁺/K.μ⁺_L; (b) the reverse inclusion under K.μ⁻; (c) cross-document isolation; (d) the explicit witness of strict shrinkage when contraction removes the last contributing V-position. Each follows from the corresponding π-claim applied per-link to coverage(Σ.L(a).s).

### Issue 4: SV5 worked example is degenerate; non-degenerate case appears only in the SV5 discussion

**ASN-0051, Worked Example, "After reordering" subsection**: "A K.μ~ step swaps v₂ and v₃: M''(d)(v₂) = a₄, M''(d)(v₃) = a₂... locate(F, d) = {v₂, v₃} — the V-positions happen to be the same set, because the swap exchanges two V-positions that both belong to the locate set"

**Problem**: The Worked Example, which a reader naturally consults to *see* SV5 in action, only exhibits the case where the locate set is preserved (ψ permutes within the locate set). The general behaviour — locate set *changing* — is exhibited in the SV5 proof's witness paragraph but is buried in the discussion of the formal relationship. A reader who skips the SV5 prose and goes straight to the Worked Example will see "ψ-permutation leaves locate alone" and may misread SV5 as a *locate*-invariance claim. The degeneracy note acknowledges this but doesn't repair the pedagogical gap.

**Required**: Extend the Worked Example with a third subsection ("Reordering that changes locate") exhibiting a swap that crosses the locate boundary — e.g., from the post-removal state M'(d) = {v₁↦a₁, v₂↦a₂, v₃↦a₄, v₄↦a₅}, swap v₁ and v₂ to demonstrate that locate({(a₂,ℓ)}, d) shifts from {v₂, v₃} to {v₁, v₃} while π is unchanged.

### Issue 5: "Resolution" used informally throughout without definition

**ASN-0051, Endset Projection section onward**: The text uses "resolution" repeatedly — "resolution of the from-endset in d," "resolution is arrangement-dependent," "discovery-resolution distinction" — without ever defining the term. The closest is "Resolution gives the positions a reader would see; projection gives the underlying content identities."

**Problem**: SV10 is titled "DiscoveryResolutionIndependence" and SV13(e) is "Resolution is arrangement-dependent." These claims rest on a term the ASN never pins down. Compare to the careful definitions of π, locate, discover_s, vitality. Without a formal definition tying resolution to locate(e, d), readers must reverse-engineer the intent.

**Required**: Add an explicit definition at the head of the Endset Projection section: "*Resolution* of endset e in document d is the function locate(e, d) — the set of V-positions in d whose content is part of e." Then SV10's name and SV13(e)'s wording become precise references rather than informal glosses.

### Issue 6: SV6 proof's "Restricting to element-level t" step lacks an explicit boundary check

**ASN-0051, SV6 proof**: "*Restricting to element-level t.* For element-level t — those with zeros(t) = 3 — the inequality is tight. The three zeros at p₁, p₂, p₃ already account for all zero components of t, so t has *exactly* three zeros and they sit at exactly the positions p₁, p₂, p₃."

**Problem**: The "inequality is tight" claim depends on zeros(t) ≤ 3, which the proof gets from "zeros(t) ≥ 3 + (zeros in [k, #t])" plus "zeros(t) = 3." But the boundary case t_{k-1} = 0 (i.e., p₃ = k-1) and t_k vs. the field-separator structure of t needs one more line: when k-1 = p₃, position k is the first position of t's element field (i.e., field-component, not separator), and the proof relies on this in the T4-validity ("If t_{k-1} = 0 — i.e., k − 1 is one of p₁, p₂, p₃ — then t_k lies in the element field and is nonzero") but does not explicitly enumerate the cases k-1 = p₁ (impossible since k > p₃ > p₁) and k-1 = p₂ (impossible since k > p₃ > p₂). The proof should make clear that only k-1 = p₃ is the live boundary case, with the others ruled out by k > p₃.

**Required**: Add one clarifying sentence: "Among the three cases k-1 ∈ {p₁, p₂, p₃}, only k-1 = p₃ is possible, since k > p₃ > p₂ > p₁."

### Issue 7: K.μ~-induced intermediate states not addressed in projection invariance claim

**ASN-0051, SV5 proof and SV13(e)**: SV5 establishes π_{Σ'}(e, d) = π_Σ(e, d) under K.μ~, citing "ran(M'(d)) = ran(M(d))" directly. SV13(e) restates this.

**Problem**: ASN-0047 defines K.μ~ as a distinguished composite that "expands into two consecutive elementary steps (K.μ⁻ + K.μ⁺), each satisfying its own precondition at the respective intermediate state" when dom_C(M(d)) ≠ ∅. So between Σ and Σ', there is an intermediate state Σ_int where K.μ⁻ has executed but K.μ⁺ has not. At Σ_int, ran(M_int(d)) ⊊ ran(M(d)), so π_{Σ_int}(e, d) may be strictly smaller than π_Σ(e, d). A reader expecting SV5 to be a per-step claim would be misled. The ASN should explicitly note that SV5 is a composite-level claim, with the intermediate K.μ⁻ step covered by SV3 and the intermediate K.μ⁺ step covered by SV2, jointly composing to the equality.

**Required**: Add a sentence after SV5's proof: "Note that K.μ~ as a distinguished composite passes through an intermediate state where K.μ⁻ has executed but K.μ⁺ has not; at that intermediate state SV3 applies (shrinkage), and the K.μ⁺ step recovers via SV2 (enlargement). The composite-level equality π_{Σ'}(e, d) = π_Σ(e, d) is the consequence; per-step invariance of π is not claimed."

### Issue 8: NewLinkEvaluationDefinedness corollary lacks an explicit proof

**ASN-0051, SV13(e) caveat**: "*Corollary (NewLinkEvaluationDefinedness).* For a link a_new allocated by K.λ ... every slot s ∈ {from, to, type} and every document d ∈ dom(Σ'.M) yield well-defined values `locate(Σ'.L(a_new).s, d)` and `discover_s(A)` (with a_new admissible to enter) immediately at Σ'..."

**Problem**: The corollary is stated and motivated but not proved. Specifically, the well-definedness of `locate(Σ'.L(a_new).s, d)` requires that Σ'.L(a_new) is defined at Σ' (immediate from K.λ's effect), that .s is well-defined for s ∈ {from, to, type} (immediate from L3's |Σ'.L(a_new)| ≥ 3), that coverage(Σ'.L(a_new).s) is a well-defined set of T (immediate from L4), and that Σ'.M(d) is well-defined for d ∈ dom(Σ'.M) (immediate from K.λ's frame). Each step is one line. The corollary deserves at least a bulleted derivation.

**Required**: Provide a four-line derivation showing each component of `locate(Σ'.L(a_new).s, d)` and `discover_s(A)` is well-defined immediately at Σ', citing K.λ's effect and the relevant L-properties.

## OUT_OF_SCOPE

### Topic 1: Survivability under composite transitions other than K.μ~

The ASN treats K.μ~ as a special distinguished composite but does not address general composite transitions (e.g., K.α + K.μ⁺ + K.ρ as required by J0/J1★). Each elementary step is analyzed, and a reader can compose, but no claim states "for any ValidCompositeExtended Σ → Σ', survivability properties X, Y, Z hold."

**Why out of scope**: ASN-0047 defines composite validity, and downstream ASNs on specific composites (fork via J4, transclusion patterns, etc.) are the natural place for composite-level survivability theorems.

### Topic 2: Link semantics and the type endset's downstream interpretation

The ASN treats Θ purely structurally — as the "third slot" excluded from vitality predicates. The full semantics of types (matching policy, type hierarchy enforcement, ghost type addresses' acquisition behavior) is deferred to a future ASN.

**Why out of scope**: This is explicitly flagged in the Scope block ("Link type semantics and interpretation").

### Topic 3: Survivability across server boundaries (replication)

The ASN reasons about a single conceptual state. Replication, cross-server link discovery, and BEBE-style propagation are not addressed.

**Why out of scope**: Explicitly flagged in the Scope block.

### Topic 4: Broader-level span survivability (k ≤ p₃ case)

The ASN explicitly scopes SV6 to k > p₃ (element-field action point) and defers broader-level spans to ASN-0034's allocator and address-hierarchy machinery.

**Why out of scope**: The ASN acknowledges this restriction and explains its rationale; broader spans are a future ASN concern.

### Topic 5: Quantitative bounds on fragment counts across composite edits

SV11's m · p bound is per-state. The ASN notes that p varies with composite edits but does not characterize how p changes, nor bound the worst-case growth of p across a transition sequence.

**Why out of scope**: A worst-case fragment analysis is appropriate for an editing-cost or storage-bound ASN, not a survivability foundation note.

VERDICT: REVISE
