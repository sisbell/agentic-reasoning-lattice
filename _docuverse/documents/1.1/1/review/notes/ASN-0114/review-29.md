# Review of ASN-0114

I checked each claim's derivation, the boundary cases, the worked example's arithmetic, and the wp analysis. I also applied the `review-mode.anti-bloat` lens for meta-prose around the claims. Findings below.

## REVISE

(none)

I verified the load-bearing arguments rather than taking them on faith:

- **The two collapses.** `coverage(R) = ∅ ⟺ R = ⟨⟩` (first) and `coverage(e) = ∅ ⟺ e = ∅` (second) are sound: `⟸` is immediate, `⟹` is the contrapositive of ASN-0053 S2, and every member of a span-set/endset is a *well-formed* span (T12), so S2 applies to each. No degenerate empty-coverage span can sneak in. The slot-3 guarantee (`followlink(Σ, a, 3) ≠ ⟨⟩` via L3 + both collapses + F1) follows.

- **F2 (DiscontiguityFaithfulness).** The two-step argument is airtight: `R ≠ ⟨⟩` from non-empty coverage + first collapse gives `|R| ≥ 1`; the singleton case `R = ⟨σ⟩` forces `{p, r} ⊆ ⟦σ⟧`, then S0 convexity puts `q ∈ ⟦σ⟧` while F1 demands `q ∉ ⟦σ⟧` — contradiction, so `|R| ≠ 1`. Hence `|R| ≥ 2`.

- **F7 (EmptyVersusInvalid) and its wp.** The non-trivial wp `wp(followlink(a,i), R = ⟨⟩) ≡ a ∈ dom(Σ.L) ∧ 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = ∅` chains correctly through definedness + F1 + both collapses. The empty/invalid distinction is a genuine operation invariant, and the divergence the implementation evidence flags (empty-end → `putrequestfailed`) is exactly what F7 forbids — a well-chosen obligation an abstract spec exists to surface.

- **Worked instance.** Arithmetic verified end to end: `zeros(d) = 2`; `aₖ = 1.0.1.0.5.0.1.k` with `zeros = 3`, `E₁ = s_C`; `a₃ ⊕ δ(2,#a₃) = a₅` by OrdinalShift; the interval `[a₃, a₅)` genuinely contains the non-emittable `a₃.1`; `coverage(e₁) ∩ F = {a₃,a₄,a₇,a₈}` via LP-Fin Corollary; disconnectedness witnessed by `a₃ < a₅ < a₇` with `a₅ ∉ coverage(e₁)`; single-span impossibility by convexity. F7 checks (`followlink(Σ,a,2)=⟨⟩`, `followlink(Σ,a,4)=⊥`, `followlink(Σ,a,0)=⊥`) are correct.

- **Honesty of the confinement claim.** F6 is correctly scoped to coverage, and the ASN explicitly concedes representation-level non-exposure of other ends is *not* a contract guarantee (an admissible `R` could split `eᵢ`'s coverage at a position chosen by inspecting `eⱼ`). The partial home-document disclosure is precisely bounded to the T4-valid, `zeros ≥ 2` slice — non-T4-valid interior tumblers and node/user-level targets are correctly excluded from the "region is documents" reading. These are the "what does the postcondition *not* establish" derivations the standard rewards, not over-claims.

No improper cross-ASN references (every citation — ASN-0034/0036/0043/0047/0053/0093/0098 — is a foundation). No out-of-scope operations are given claims. wp analysis includes a non-trivial case. Concrete example present and correct.

**On bloat:** I did not have to skip meta-prose to follow any claim. The prose is dense but does work — the disclosure discussion answers the stated question, the "boundary we must respect" section performs genuine scope delineation (separating the recorded end from its resolution, which the implementation conflates), and the implementation citations corroborate rather than specify mechanics. No "Why the axiom is needed" sub-paragraphs, no use-site inventories, no document-ordering justifications, no duplicate body paragraphs. The Synthesis is a legitimate compression of the body, not redundancy.

## OUT_OF_SCOPE

### Topic 1: Resolution of the recorded endset against a document's arrangement
The ASN correctly defers this to the "boundary we must respect" section and Open Question 2. FOLLOWLINK's contract is with the *recorded* end (exact by F1, permanent by F5); the implementation's projection-and-filter step (shrinkage per Q15, document-relative results per Q11) is a separable operation. Properly excluded — not a defect here.

### Topic 2: Normal form for the returned span-set (Open Question 1)
Coverage underdetermines the span decomposition (F3 makes this explicit). Whether a canonical/normalized form should be mandated is a future concern; binding the contract at coverage is the right choice for *this* ASN.

### Topic 3: Wire-level re-encoding of the `⟨⟩`/`⊥` distinction (Open Question 3)
F7 establishes the distinction abstractly; preserving it across a serialization boundary is a protocol concern belonging to a transport ASN, not to the read operation.

VERDICT: CONVERGED
