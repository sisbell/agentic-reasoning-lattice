# Review of ASN-0118

This ASN is in strong shape: the resolution/placement split is cleanly grounded in ASN-0058's machinery, the composite decomposition is exhibited rather than asserted, the tiling argument is explicit, the wp analysis is non-trivial, and the worked example actually exercises the provenance branches. The remaining findings are precision and prose-discipline issues, not structural ones.

## REVISE

### Issue 1: Misstatement of what J1'★ forbids in the worked example
**ASN-0118, "A worked assembly from two sources", final CP8 bullet**: "The membership `(x₁, d) ∈ Σ'.R` holds without a redundant record — the P4★/P2 branch firing exactly where J1'★ would forbid a fresh K.ρ."
**Problem**: J1'★ constrains the *net* new pairs `R' ∖ R`, not steps. A K.ρ recording `(x₁, d)` when that pair already stands in `Σ.R` (which P4★ guarantees here) is a no-op on `R` — it contributes nothing to `R' ∖ R` and J1'★ is indifferent to it; nothing is forbidden. The sentence is also in tension with the main text's parallel branch ("The COPY operation", range-new-yet-already-recorded case), which calls a redundant K.ρ "J1'★-admissible." The two passages assign opposite J1'★ verdicts to the same kind of no-op recording. The counterfactual reading ("if the pair were *not* in `Σ.R`, recording it would violate J1'★") is the only sense in which "forbid" is right, and the text does not say that.
**Required**: Align both passages with J1'★'s actual content: a K.ρ whose pair is already in `R` adds nothing to `R' ∖ R` and is constrained by nothing; J1'★ bites only on pairs genuinely new to `R`, which it confines to range-new addresses. State the worked-example branch as "no K.ρ is needed, and a redundant one would be a no-op," dropping the "forbid" claim.

### Issue 2: Range equality and CP4 exactness cite only the lower-bound clauses; the closure clauses they need go uncited
**ASN-0118, "Survival of links anchored to the reused content"**: "`ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {c₀, …, c_{W−1}}` (CP2 adds the placed addresses; CP3a/CP3b move prior positions but preserve their I-addresses, so the prior range is retained)" — and **"Shared identity across documents"**: "COPY adds `W` new `(document, V-position)` references (one per placement, CP2), so the total number of references into the placed set … increases by exactly `W`."
**Problem**: Both are equalities, and CP2/CP3a/CP3b only give one direction. For the range equality's `⊆` direction you need CP3c (the text-subspace domain is *exactly* left ∪ placement ∪ shifted — otherwise an unconstrained extra text position could carry an arbitrary address into the range) and CP6's domain-equality conjunct (the non-text range is pinned to its pre-state value). For CP4's "exactly `W`" you need the same closure: without CP3c/CP6, nothing cited rules out additional references being created or destroyed. The ASN *has* exactly these clauses — indeed it added CP3c for this purpose — but the two derivations don't invoke them, so as written they are claims, not proofs.
**Required**: Add CP3c and CP6 (domain-equality conjunct) to the premises of the range-equality parenthetical, and note in the CP4 paragraph that exactness rests on the same closure (shifted bindings replace, rather than add to, their pre-state reference pairs; CP3c/CP6 exclude any other change).

### Issue 3: Garbled sentence in the entity-frame paragraph
**ASN-0118, "The COPY operation", *Frame — entity set***: "This is the standard CP3c sets for the arrangement domain: dischargeable from the postconditions alone, not only through the exhibited composite."
**Problem**: The sentence does not parse. It reads as a mangled relocation of CP3c's closure-role sentence ("…are dischargeable from the postconditions alone, not only through the exhibited composite") — the same point stated a few paragraphs earlier under domain closure, now duplicated in broken form. This is the reviser-drift pattern: prior content relocated rather than removed.
**Required**: Delete or rewrite. If the intended content is "CP12 and CP8's `⊆` direction play, for `E` and `R`, the closure role CP3c plays for the arrangement domain," say exactly that, once, grammatically — and verify the preceding "why the clause is needed" sentence still earns its place after the rewrite.

### Issue 4: The placement-position S8a/S8-depth discharge is stated twice, nearly verbatim
**ASN-0118, "The COPY operation"**, append-or-empty case ("These placement positions `{p + i : 0 ≤ i < W}` are well-formed by S8a-validity of `p` and OrdShiftHom(b) … with `p + 0 = p` S8a-valid directly. They also carry the subspace common depth…") and displacing case ("…instead `p` is itself S8a-valid (a valid insertion position), and each `p + i = shift(p, i)` preserves S8a by OrdShiftHom(b) (ASN-0036), with `p + 0 = p` S8a-valid directly. The same gap-fill positions also carry the subspace common depth… `#(p + i) = #shift(p, i) = #p = m_{s_C}(d)`…").
**Problem**: The discharge is case-independent — it depends only on `p` being an S8a-valid insertion position of depth `m_{s_C}(d)` (or the chosen `m` in the empty sub-case) — yet it is derived in full in both case paragraphs, with the same citations and the same `p + 0 = p` remark. Two paragraphs saying the same thing in different words is the duplication pattern the anti-bloat classifier targets, and it will keep accreting if each case carries its own copy.
**Required**: Factor it once — a short standalone observation before the case split ("for a valid insertion position `p`, every `p + i`, `0 ≤ i < W`, is S8a-valid with depth `m_{s_C}(d)`, by ValidInsertionPosition (a) / ValidFirstInsertionPosition and OrdShiftHom") — and have both case paragraphs cite it. Keep only the genuinely case-specific remark (that I3-VP/I3-VD cover the shifted positions but not the gap-fill) in the displacing case.

### Issue 5: The composite-validity proof interrupts the operation contract
**ASN-0118, "The COPY operation"**: the multi-paragraph exhibition of COPY as a valid composite (append/empty case, displacing case, coupling discharge) sits inside the *Effect — provenance* clause, between CP8 and the operation's frame conditions (CP3b, CP1, CP12, CP7a, CP6).
**Problem**: A reader following the operation's contract must wade through roughly nine paragraphs of decomposition-and-validity argument before reaching the frame clauses that complete the operation's definition. The proof is substantive and should stay — this is a placement finding, not an existence finding. As placed, the contract's clause list is no longer readable as a contract.
**Required**: Complete the operation definition first (all effects, then all frames, uninterrupted), and move the composite exhibition — decomposition, intermediate-state invariants, J0/J1★/J1'★ discharge — to its own section immediately after, referenced from CP8 with a single sentence.

## OUT_OF_SCOPE

### Topic 1: Nominal-extent vs. placed-width guarantee under partial binding
**Why out of scope**: The operation is fully determined without it (`W` is defined by resolution), and the ASN correctly flags the C2 shortfall as an Open Question; what COPY should *promise* about the gap between a span's named extent and its smaller resolved width is new territory, not an error here.

### Topic 2: Link-subspace transclusion and post-COPY undiscoverability under later removal
**Why out of scope**: Placing links by reference, and the conditions under which a link inherited via COPY becomes undiscoverable again when the destination later contracts the transcluded positions, belong to the link-operation and DELETE-interplay ASNs; both are properly listed as Open Questions rather than specified here.

VERDICT: REVISE
