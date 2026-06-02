# Review of ASN-0047

## REVISE

### Issue 1: ExtendedReachableStateInvariants statement collapses the per-state / composite-boundary temporal distinction it is built around

**ASN-0047, *Extended reachable-state invariants***: "Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies the *per-state invariants* below; every state at a composite boundary (Σ or Σ' of a valid composite) additionally satisfies the *composite-boundary properties* below."

**Problem**: The preamble carefully distinguishes per-state invariants ("hold at **every** reachable state — ... every intermediate state within a composite") from composite-boundary properties (hold only at boundaries). But the theorem statement quantifies the *per-state* class over states "reachable by a finite sequence of valid composite transitions" — and such a state **is** a composite boundary. A mid-composite intermediate state is reached by [valid composites] followed by a *partial* composite, which is not itself a valid composite, so it is excluded by this quantifier. The statement therefore asserts the per-state class only at composite boundaries — the same scope it gives the boundary class — erasing the distinction the section exists to make, and asserting strictly less than (a) what the preamble claims and (b) what the Class (a) matrix proves (per-*elementary* preservation, which is exactly what is needed to cover intermediate states).

**Required**: Quantify the per-state class over all states reachable by a finite sequence of *elementary* transitions drawn from valid composites (i.e. every elementary-transition target, including mid-composite intermediates), and reserve the "composite boundary" quantifier for the Class (b) properties only. The proof already supports the stronger statement; only the quantifier needs aligning.

### Issue 2: The "link retention under clearance is forced" argument is stated redundantly

**ASN-0047, *Decomposition of K.μ~***: the bijection-equation paragraph (clause (v) discussion) states "The full-clearance decomposition cannot realise such a re-seating: K.μ⁺ writes only content-subspace positions and K.μ⁻ removes link positions only by suffix, so links are retained pointwise"; and the closing **Decomposition** paragraph restates "The retention of link-subspace mappings under the clearance is forced rather than incidental: K.μ⁺ (amended) is content-only and K.μ⁺_L only places at the contiguous min or max, so any link-subspace position removed by K.μ⁻ could not be restored."

**Problem**: Two paragraphs in the same section assert the identical fact (K.μ⁺ content-only + K.μ⁻ suffix-only ⟹ links retained pointwise) in different words. This is the duplication pattern the anti-bloat classifier flags; the reader who has parsed the clause-(v) version must re-verify that the Decomposition-paragraph version says nothing new.

**Required**: State the forced-retention fact once (it most naturally belongs in the clause-(v) / Step (A) Case `s_L` discharge where link-fixity is established) and have the other site reference it rather than restate it.

### Issue 3: P7a discharge carries a defensive sub-paragraph re-deriving ValidComposite★ structure rather than advancing the claim

**ASN-0047, *Class (b)* P7a discharge, "Temporal positioning of v"**: "the V-position v carrying the new I-address a is created by K.μ⁺ at the composite endpoint Σ', not at the post-K.α intermediate state — at the intermediate state immediately after K.α and before K.μ⁺, v does not yet inhabit dom(M(d)) ... J0's existential is realised only after K.μ⁺ has fired ... which is the composite endpoint by ValidComposite★'s structure."

**Problem**: The load-bearing content of the discharge is only that `v` and `a` co-exist at Σ' (so S3★ + L14 force `subspace(v) = s_C`). The quoted sub-paragraph instead narrates the intra-composite timeline and re-explains ValidComposite★'s structure — meta-prose about *when* steps fire, not advancing the P7a derivation. A reader must skip past it to reach the substantive S3★/L14 step that follows.

**Required**: Reduce to the single load-bearing sentence ("`v` and `a` both inhabit Σ', so S3★ + L14 + S3★-aux force `subspace(v) = s_C`"); drop the timeline narration, which restates ValidComposite★ rather than using a fact P7a needs.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
The ASN's K.μ⁻ models only suffix removal on the link subspace; the implementation's interior `DELETEVSPAN` compacts-and-renumbers. This is already correctly carried as an open question, and `DELETEVSPAN` is named-operation territory excluded by scope.

### Topic 2: Concurrency / serialization of allocation under a shared home document
The carried open questions about concurrent allocation and address-space exhaustion are genuinely new territory (the SequentialTransitionAxiom forecloses concurrency in this ASN by assumption), not errors here.

VERDICT: REVISE
