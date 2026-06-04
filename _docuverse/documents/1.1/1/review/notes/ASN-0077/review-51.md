# Review of ASN-0077

This is a large, largely rigorous note carrying the `review-mode.anti-bloat` classifier. The core mathematics (O0–O14, the singleton-span edge case, the multi-step inductions) checks out on the cases I traced. The findings below are predominantly forward-reference accretion and claim proliferation, plus one structural redundancy.

## REVISE

### Issue 1: Defensive "no transition-vocabulary closure" prose restated four times
**ASN-0077, "Where origin already lives" / O0(b) and the paragraph after the derivation**: the same disclaimer appears at least four times —
- "two foundation facts compose directly, with no appeal to a transition-vocabulary closure";
- "established from L1c and the Allocator hierarchy alone, with no K.λ-event closure and no vocabulary-completeness assumption";
- "The semantic correspondence above rests on L1c and the Allocator hierarchy alone; it needs no statement about which transition placed `ℓ` into `dom(L)`";
- "No transition-vocabulary closure over `dom(L)` is required anywhere in this ASN."

**Problem**: Meta-prose explaining what the proof does *not* rely on, repeated. The reader must skip past it to follow O0(b). One statement of the citation basis suffices.
**Required**: Cite L1c + Allocator hierarchy + SubAllocatorBundle once in the derivation; delete the three echoing disclaimers.

### Issue 2: Transition-vocabulary inventories enumerated, then disclaimed
**ASN-0077, paragraph before O11★ and O11★★ sub-case (iii)**:
- "Among the foundation vocabulary (ASN-0047) the `M(d)`-fixing transitions include K.α, K.λ, K.δ, K.ρ, and any K.μ⁺/K.μ⁻/K.μ~/K.μ⁺_L acting on a document `d' ≠ d`; but the proof never relies on this list being complete…"
- "(Concretely, among the foundation vocabulary of ASN-0047, this class comprises every `M(d')`-modifying step for `d' ≠ d` … K.α, K.λ, K.δ, K.ρ; any transition a richer vocabulary might add falls into sub-case (i)/(ii)…)"

**Problem**: The inductions rest only on the binary modifies-`M(d)` / leaves-`M(d)`-fixed partition (correctly stated). The enumeration is then explicitly declared non-load-bearing — exactly the defensive-exhaustiveness pattern. It advances no reasoning.
**Required**: Keep the binary partition; delete the vocabulary inventories and their "but we don't rely on this list" hedges.

### Issue 3: Downstream-consumer justifications for stating claims separately
**ASN-0077, O11' intro and O11★★ intro**:
- "We state its parallel claim separately rather than as a parenthetical note, so that downstream proofs needing arrangement-extension preservation under K.μ⁺_L can cite a labeled result."
- "Downstream ASNs that reason about origin preservation across mixed extension activity therefore need a labeled lemma for this combined case. We supply it here."

**Problem**: Use-site inventory / rationale for a claim's existence. Whether a claim is labeled is an editorial fact; the prose justifying it belongs nowhere in the argument.
**Required**: Delete both justifications. State the claim.

### Issue 4: Repeated deferral to the worked example and to LP10/LP11
**ASN-0077, O13, O14, and the bridging sentence**:
- O13 "Witness (exhibited concretely in the worked example)."
- O14 "Witness (exhibited concretely in the worked example)."
- "Both failure modes are exhibited concretely in the worked example below."

Additionally, the "projection-level counterpart is LP10 / LP11 (ASN-0098)" correspondence is restated in O13, in O14's failure mechanism, and twice again in the worked example.

**Problem**: Multiple paragraphs deferring to the same downstream location, and the same LP10/LP11 cross-reference duplicated ~4×. The witness is in the worked example; one pointer is enough, and the LP-counterpart remark needs stating once.
**Required**: Single deferral per negative claim; state the LP10/LP11 correspondence once.

### Issue 5: O11★ and O11'★ are strict special cases of O11★★
**ASN-0077, O11★ / O11'★ / O11★★**: "O11★ and O11'★ together close the multi-step gap for pure-K.μ⁺ and pure-K.μ⁺_L extension chains. A combined chain … is *not* covered by either O11★ … or O11'★ … We supply it here."

**Problem**: O11★★ (mixed K.μ⁺/K.μ⁺_L chain) subsumes both pure-kind chains; O11★ and O11'★ are then redundant labeled theorems whose retention is justified only by the use-site prose flagged in Issue 3. Three near-identical inductions where one suffices.
**Required**: Prove O11★★; derive O11★ and O11'★ as one-line specializations or drop them. Do not justify the narrower lemmas by appeal to future citation.

### Issue 6: O2 derivation explains a citation choice instead of arguing
**ASN-0077, Equivalence chain (F2)=(F3)**: "O2 — not M16a alone — is what discharges this step uniformly across content and link blocks; M16a applies only when `aⱼ ∈ dom(C)`, while O2 also handles the link case via CL-OWN bridged by M-int."

**Problem**: Commentary on *why O2 rather than M16a* is cited, rather than the collapse step itself. The collapse follows from O2 directly; the comparison with M16a is meta-justification.
**Required**: "By O2, `{origin(aⱼ + i) : 0 ≤ i < nⱼ}` collapses to `{origin(aⱼ)}`." Delete the M16a contrast.

## OUT_OF_SCOPE

### Topic 1: Origin reporting for cross-subspace I-spans (link origins from an I-span)
**Why out of scope**: The I-span lift restricts to `dom(C)` by definitional choice; reporting link origins from an I-span is correctly deferred to the ASN's own Open Question 1. This is future territory, not an error here.

### Topic 2: Historical-containment operation over `Σ.R`
**Why out of scope**: The "Not historical containment" exclusion and the corresponding Open Question correctly defer a complementary provenance operation. It belongs in a future ASN.

META: The note specifies a well-formed observation operation (state, postconditions, frame, permanence invariant) and stays in specification territory; the issues are prose accretion and claim proliferation, not drift.

VERDICT: REVISE
