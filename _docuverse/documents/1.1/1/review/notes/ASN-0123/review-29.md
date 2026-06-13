# Review of ASN-0123

I checked the derivations (G1–G3), the well-formedness proof, and the eighteen V-claims. The mathematics is sound: VN-B1's induction is airtight, the severance theorem V9(a) closes both comparability branches cleanly, SA's antichain argument is correct, and the unbounded-depth argument (depth-1 forks spend no separator) is exactly right. The note also satisfies the depth mandate — concrete worked instances for both the owned and cross-owner forks, a non-trivial wp-style necessity argument for P-bdy in V9w, and explicit derivations rather than checkmarks throughout.

What it does not satisfy is the `review-mode.anti-bloat` mandate. Three cross-section duplications and a layer of defensive meta-prose have accreted around the forward references, and two citations are imprecise. The load-bearing content (notably V9's O5(ii) discharge — which I did *not* find trimmable) must stay; the *restatements* of it are the accretion.

## REVISE

### Issue 1: The cross-owner identity derivation is stated three times

The same structural argument — *v* is one document-level K.δ in `A_doc(pfx(π)) = S(pfx(π), 2)`, frontier-fresh by ChildSpawnFreshness/FrontierEquivalence, with `Document(v)`, O5(i), and O5(ii)-via-O1a+Z-mono — appears in full in three places.

**ASN-0123, Identity clause (cross-owner branch)**: "v := the document identity π allocates in it as a single document-level K.δ … whence Document(v) and pfx(π) ≼ v (O5(i)), and — proved structurally at V9 from that form with O1a and Z-mono … — the maximality … (O5(ii)). Freshness v ∉ E … fresh by ChildSpawnFreshness … or FrontierEquivalence …"

**ASN-0123, V-WF, Clause 1**: "In the cross-owner branch … π allocates the identity as one document-level K.δ at the frontier of its account document sub-allocator A_doc(pfx(π)) = S(pfx(π), 2) … inc(pfx(π), 2) ∉ E by ChildSpawnFreshness … and inc(c, 0) ∉ E by FrontierEquivalence … the produced v then satisfies Document(v) and — established structurally at V9 from that stream form … — pfx(π) ≼ v (O5(i)) with #pfx(π) maximal … (O5(ii))"

**ASN-0123, V9 preamble**: the actual proof of all three.

**Problem**: The frontier-freshness discharge (ChildSpawnFreshness / FrontierEquivalence / `parent(v) ∈ E`) is given in full in both the Identity clause and V-WF Clause 1; the O5(i)/O5(ii) "proved at V9" deferral appears in the Identity clause and twice in V-WF. The clause "Which document number k … stays out of scope … the form [pfx(π), 0, k] for any k ≥ 1" is in both the Identity clause and V-WF. This is the forward-reference-accretion pattern: two paragraphs deferring to the same downstream location (V9) while each re-deriving the thing deferred.

**Required**: Keep the discharge in exactly one place. V-WF Clause 1 is the natural home for the frontier-freshness argument (it is the validity proof); V9 is the home for the O5(ii) derivation (do not trim it). The Identity clause should state `v`'s *definition* and cite V-WF/V9, not re-run either argument.

### Issue 2: The node-tier exclusion is re-argued in three sections

**ASN-0123, P-tier comment**: "A node-tier non-owner (zeros(pfx(π)) = 0, which O1a admits into Π) satisfies neither disjunct and lies outside the domain — it must establish an account first, an out-of-scope prior act VERSION does not cover."

**ASN-0123, Identity clause**: "A node-tier principal (zeros(pfx(π)) = 0, which O1a admits into Π) holds no such namespace: reaching a document from a node prefix would first baptize an intermediate account, a second permanent entity (P1), breaking the single-mint guarantee — so such a principal must establish an account first …"

**ASN-0123, V-WF**: "a node-tier forker (zeros(pfx(π)) = 0, which O1a admits into Π) has no account document sub-allocator, and reaching a document … from a node prefix … would first baptize an intermediate account … a second entity, which P1 makes permanent … We therefore exclude that path from VERSION."

**Problem**: P-tier already excludes the node-tier non-owner from the operation's domain. The note then re-derives *why* (intermediate account → second permanent entity → breaks single mint) three times. This is the reviser-drift pattern "a paragraph imagines a case the precondition already excludes," compounded across sections.

**Required**: State the exclusion and its one-line rationale once (P-tier is the natural anchor). The Identity clause and V-WF should cite it, not re-derive it.

### Issue 3: Defensive meta-prose around assumptions and alternative proof routes

**ASN-0123, PS**: "And it is load-bearing, not decorative: the implementation does not enforce it (deviation 4 in the evidence section), so a conforming implementation must supply what udanax-green leaves to front-end cooperation." — explains *why the assumption is needed* rather than what it says.

**ASN-0123, V9w**: "(A monotonicity route via J1★ and P2 also closes — but only at a boundary, where every earlier range-entry composite has terminated and fired J1★; it is the boundary, not the bare monotonicity of R, that the argument turns on.)" — anticipates and rebuts a proof route the note does not take.

**ASN-0123, Remark (atomicity)**: "Two boundary assumptions must be kept apart. P-bdy … we do adopt … The interior-unobservability convention … is strictly stronger … and is one we do not lean on; the foundations do not state it …"

**Problem**: These advance no claim. The V9w proof uses P4★ directly; the monotonicity parenthetical is a dead alternative. The atomicity remark's "two assumptions kept apart" is genuine the first time the distinction is drawn, but the "one we do not lean on" framing is defensive padding. (The V9w *counterfactual* showing P-bdy is load-bearing — the "Were Σ to lie inside a predecessor composite…" sentence — is legitimate necessity-demonstration; keep that, cut the parenthetical after it.)

**Required**: Delete the monotonicity parenthetical and the "load-bearing, not decorative" sentence; compress the atomicity remark to the P-bdy-vs-interior distinction without the "we do not lean on … foundations do not state it" justification.

### Issue 4: Definitions enumerate their downstream consumers

**ASN-0123, PS**: "so O2, O5, O15 are available to V8 and V9."
**ASN-0123, nextv**: "We note now, for use later (V5), the shape of the argument list: nextv consults the set of allocated identities and the source's address, and nothing else."
**ASN-0123, SA**: "(G2 uses SA to convert subtree coverage into address identity.)"

**Problem**: A definition's introduction listing where it will be consumed is the use-site-inventory pattern; it does not advance the definition's meaning. Separately, "whole-request serialization; see the evidence section" appears in both the P-bdy comment and the atomicity remark — two paragraphs deferring to the same downstream location.

**Required**: Drop the consumer enumerations (the consuming claims already cite their premises). Keep nextv's *content* fact (registry-purity) — it is real — but state it as a property of `nextv`, not as a note "for use later (V5)." Collapse the duplicate "see the evidence section" deferrals to one.

### Issue 5: B-Seq is cited for serialization against the note's own non-transfer discipline

**ASN-0123, V5(a)**: "(a) is VN-B1 and the nextv frontier identity … under serialized commits (B-Seq): every arrival in the namespace is a frontier arrival …"

**Problem**: The note's entire VN-B1 apparatus exists *because* ASN-0040's transition-system facts (B1, B2, B8-same-namespace) do not transfer to ASN-0047's K.δ vocabulary — and V0 explicitly avoids serialization ("The same-allocator argument needs no serialization assumption, so this distinctness is unconditional on commit order"). Yet V5(a) reaches back for B-Seq, ASN-0040's serialization axiom about its *own* commit paths. ASN-0047's SequentialTransitionAxiom already totally orders all transitions — strictly more than B-Seq supplies — and is what V5(a) actually needs. The claim is correct; the citation is inconsistent and unnecessary.

**Required**: Cite ASN-0047's SequentialTransitionAxiom for the serialized-arrival fact, not ASN-0040's B-Seq.

### Issue 6: Single-step coverage lemma cited for the composite (V10)

**ASN-0123, V10 proof**: "L' = L and each link's slot coverage is transition-invariant (LP2, LP3), so the right-hand side may be read at Σ."

**Problem**: `Σ → Σ'` here is the whole VERSION composite (multi-step). LP2/LP3 (ASN-0098) are stated per single atomic transition; the multi-step form is LP3★. Since `L' = L` holds across the entire composite (V1), `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` follows from V1 alone with no coverage lemma at all.

**Required**: Justify coverage invariance from V1's `L' = L` directly, or cite LP3★ rather than the single-step LP3.

## OUT_OF_SCOPE

### Topic 1: Serialization of concurrent forks under one authority
The atomicity remark correctly flags that ASN-0047 supplies no whole-composite atomicity and that interior states are reachable; the note declines to assume interior-unobservability and routes the question to Open Question 4. This is the right disposition — a serialization guarantee for concurrent forks is a future obligation, not a defect in this ASN. No change needed beyond the trim in Issue 3.

META: (none — the ASN defines an operation on state with abstract invariants an alternative implementation must satisfy; the implementation section is properly framed as evidence with enumerated deviations.)

VERDICT: REVISE
