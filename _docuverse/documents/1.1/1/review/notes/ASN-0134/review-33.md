# Review of ASN-0134

The logical core is sound — I checked the conflict analysis (H0–H2), the per-home-suffices confluence (G1, including the H3 lift), the operation-level non-confluence families (§4), and the verdict soundness chain (V0/V2/V1) against their grounding traces, and found no hole. The frontier arithmetic in §7 and §8 checks out. My findings are one misleading justification and a set of anti-bloat redundancies the carried classifier asks me to surface at source.

## REVISE

### Issue 1: The nesting-homes justification for the origin argument is a red herring

**ASN-0134, H1 / W1 / §7**: W1 — "the origin argument of H1, which needs no anchor incomparability and is therefore **immune to the nesting homes** (`d ≼ d'`) the ASN-0093 stack admits". H1 introduces the same thread: "we argue by *origin*, not by anchor position, because the two documents need not be prefix-incomparable — the ASN-0093 stack admits *nesting* homes (`d = [1.0.1.0.1]` and `d' = [1.0.1.0.1.1]`)".

**Problem**: The framing implies nesting is a hazard for anchor-incomparability arguments (`CrossDocumentDisjointness`). It is not, for *documents*. Two distinct documents have `zeros = 2`; if `d ≼ d'` with `d' = d.x`, then `zeros(d') = zeros(d) + zeros(x) = 2` forces `zeros(x) = 0`, hence `x₁ ≠ 0`. The anchors then diverge at the position immediately after `d`: `b_C(d) = [d.0.s_C]` carries `0` there, `b_C(d') = [d.x.0.s_C]` carries `x₁ ≠ 0`. The ASN's own example proves it — `b_C([1.0.1.0.1]) = [1.0.1.0.1.0.1]` versus `b_C([1.0.1.0.1.1]) = [1.0.1.0.1.1.0.1]` diverge at the sixth component (`0` vs `1`), prefix-incomparable. So `CrossDocumentDisjointness`'s anchor incomparability holds for nesting documents; "needs no anchor incomparability *therefore* immune to nesting" is a non-sequitur built on a manufactured hazard. (H1's narrower phrase — a "*document-level divergence* argument would be false" — is defensible, since the document *tumblers* are comparable; W1's escalation to anchors is what overreaches.)

The genuine reason to prefer origin is already stated in both H1 and W1: it "settles the cross-document, cross-subspace `S ≠ S'` case [`CrossDocumentDisjointness`'s] single-`·` statement leaves unnamed." That reason carries the choice alone.

**Required**: Rest the origin choice on cross-subspace generality; delete the nesting claim in W1 (anchors are immune to nesting too, for documents) and the gratuitous nesting echoes in H1 and §7 (whose example is sibling homes anyway).

### Issue 2: §9 MIC clauses and §5 W-claims re-derive their source claims instead of citing them

**ASN-0134, MIC clause 4 vs V0**: V0 — "The discriminator is *access count*, not type-confinement: ... its lone access lands on one index, whether that access reads a type's active view or a home's cross-type frontier." Clause 4 — "The discriminator is *access count*, not `Observe_K`-grade-ness (V0): one bounded access lands on one index, whether it reads a type's active view or a home's cross-type link frontier." Clause 4 cites V0 *and* repeats its discriminator sentence (and its `age` argument) near-verbatim.

**ASN-0134, MIC clause 7 vs V2**: V2's "global ... not per-home" plus the "type-scoped for a cross-type join, and home-scoped over the member homes for a `stale` enumeration" distinction, and "strictly stronger than soundness alone needs," are all restated in clause 7 under a `(V2)` citation.

**ASN-0134, §5 W1/W2/W3 vs H1/H2/ChainMembership**: W1 re-runs H1's origin argument (with the same nesting overstatement), W2 re-runs H2's frontier-collision, W3 re-runs `ChainMembershipForOrigin`.

**Problem**: A collecting section (the contract) and a classifying section (the partition) should *name* the claim and add the one delta they contribute, not re-explain the claim. The reader who already has V0/V2/H1/H2 must read the same derivation twice to confirm it is the same derivation.

**Required**: In §9, reduce clauses 4/7/8 to "claim + delta" — e.g. clause 4: "single-bounded-access reads are per-call snapshots (A3/V0), age included"; clause 7: "multi-read verdicts adopt the one-index construction (V2) — global, not per-home." In §5, let W1/W2/W3 cite H1/H2/`ChainMembershipForOrigin` and carry only the model-intrinsic / serialization-borne label, which *is* their contribution.

### Issue 3: The literal-vs-operative `I1a` argument is developed three times

**ASN-0134, §4 instance (i) / MIC clause 8 / SAFE(b)(ii)**: §4 instance (i) develops, at length, that the both-miss derivation is `K`-surface-emitted only *literally*, that `I1a`'s induction needs a miss-against-its-own-pre-state, and that clause 8 restores the coincidence. Clause 8 restates it ("making each `idem = ⊤` deposit a genuine miss against its own pre-state restores the *operative* `K`-surface-emittedness `I1a`'s induction needs"). SAFE(b)(ii) restates it a third time ("the both-miss interleaving leaves the two coverage-equal emits `K`-surface-emitted only *literally*, so `I1a`'s induction breaks ... follows not from per-home MIC but from clause 8").

**Problem**: This is the note's subtlest argument, and it earns one careful development — but only one. Clause 8 and SAFE(b)(ii) re-prove it rather than discharging it by reference.

**Required**: Develop it once in §4 instance (i). Clause 8 and SAFE(b)(ii) should assert the conclusion "by §4 instance (i)" and stop.

### Issue 4: "regardless of home" is asserted at six sites

**ASN-0134, intro / §4 instance (i) (×3) / §4 family summary / SAFE(b) / clause 8**: the point that the `idem=⊤` duplicate arises whether or not the racing emits share a home is stated in the abstract ("regardless of whether the two racing emits share a home"), then "it opens *regardless of home*," "a duplicate per-home MIC permits regardless of home," "carries the same-home pair (`d = d'`) verbatim," and again in SAFE(b) and clause 8.

**Problem**: The intro names this "the load-bearing correction," which warrants *one* emphatic statement — the place where the same-home case is actually derived (§4 instance (i), via clause 2's slot-spacing `φ, φ+1`). Five further restatements are the accreted-emphasis pattern the classifier targets.

**Required**: Keep the derivation and one "regardless of home" at §4 instance (i); let the intro, the family summary, SAFE(b), and clause 8 cite it.

### Issue 5 (minor): A1's rejection sub-list reads exhaustive but omits two causes

**ASN-0134, A1**: "a *rejected* call, one whose precondition fails at the state it is evaluated against — a gate failure, a `P0` failure, or a `P-tgt` failure (ASN-0128 S3, I6)."

**Problem**: The list omits the `Emit_K` *miss-branch* home-validation rejection (`d ∉ dom(Σ.M)`, ASN-0128 I6) and `Nullify_Binary`'s `P-reg` rejection. The five zero-step *cases* stay exhaustive (all fall under "rejected call"), so the exhaustiveness claim survives — but the parenthetical reads as a complete enumeration of rejection causes and is not.

**Required**: Mark the sub-list illustrative ("e.g., a gate, `P0`, or `P-tgt` failure") or drop it — either is bloat-neutral or bloat-reducing.

## OUT_OF_SCOPE

### Topic 1: Tightening `I1a`'s statement to its operative notion

The gap §4 exploits — `I1a`'s literal "deposit branch of an `Emit_K`" versus its proof's "miss against the step's own pre-state" — is a looseness in ASN-0128's `I1a` *statement*, not a defect here. ASN-0134 identifies it correctly and patches it locally with clause 8. Hardening the `I1a` statement so future concurrent consumers don't re-discover the gap belongs to ASN-0128, a foundation; nothing to do in this note.

**Why out of scope**: It is a refinement of a foundation ASN, and ASN-0134 already handles the consequence soundly.

VERDICT: REVISE
