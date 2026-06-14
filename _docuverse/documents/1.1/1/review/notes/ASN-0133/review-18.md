# Review of ASN-0133

This note is unusually rigorous and self-aware about its own hypotheses, and I traced the load-bearing chain — Q0 (the fixed-view-base rebuild is exhaustive over the eight view-sensitive forms), Q1, Q-EXT (X-DEF ∘ PD0 ⊥-stability gives at-most-once per argument, surviving environment steps by step-agnosticism), Q5 (injection by step index), Q5a (bounded growth ⟹ H-RF, strictly stronger than H-RF in the open model, equivalent in the closed one), and all three regimes of Q6 — and it holds up, including the worked Σ₀→Σ₂ walk-through. The foundation citations I spot-checked (A_K ⊆ L_K; I2/I3/I4; PD0/PD1/PD2; BH3 `target_of` "several"⟹⊥; FrontierUnification) are used correctly. The gaps I found are in the scope section (Q7–Q9), the least-developed part of the note.

## REVISE

### Issue 1: Q9's anti-monotonicity is stated generally but holds only for S-monotone scoping bodies
**ASN-0133, SC / Q9**: "the relation is the rule's to declare" … "**Q9** — quiescence is anti-monotone in the scope: `S' ⟹ S` gives `quiescent_S ⟹ quiescent_{S'}`."

**Problem**: SC admits *any* Boolean PL predicate as the scoping body `β_ρ^S` ("the relation is the rule's to declare"). Q9's anti-monotonicity is then asserted for all scopes, but its only justification is that `S' ⟹ S` shrinks the filtered domain `{x ∈ [D_ρ] : β_ρ^S(x)}` — which requires `β_ρ^S` to be *monotone in S*. The three canonical bodies (`S(addr(x))`, `(∃ y ∈ addrs_G(x) :: S(y))`, `(∃ y ∈ addrs_F(x) :: S(y))`) are all monotone, but showing three bodies are monotone does not establish that all rule-chosen bodies are. A permitted body where S occurs negatively breaks Q9: take a tuple-domained rule with `β_ρ^S(x) ≡ ¬S(addr(x))` and scopes `S = λa.⊤`, `S' = λa.⊥` (so `S' ⟹ S`). Then the `S`-filtered domain is `{x : ¬⊤} = ∅`, making `quiescent_S = ⊤` vacuously, while the `S'`-filtered domain is the full `[D_ρ]`, so `quiescent_{S'}` can be ⊥. The stated implication `quiescent_S ⟹ quiescent_{S'}` fails. The "anti-monotone nesting" framing inherits the same defect.

**Required**: Restrict the admissible scoping bodies to those monotone in S (equivalently, S occurs only positively) as a condition of the SC framework, or qualify Q9 explicitly to monotone bodies. Either way the premise must be named, not left to the canonical examples.

### Issue 2: the per-target body's domain is `addrs_G`, not `coverage_G` — the latter is not QD-admissible
**ASN-0133, SC**: "a tuple-domained rule reaches the per-target tier through the `addrs_G`/`coverage_G` body, never through `addr`" (and the summary's "per-target by the denoted-target coverage").

**Problem**: The formal per-target body is `(∃ y ∈ addrs_G(x) :: S(y))`, which is well-typed because `addrs_G(x) : ℘_fin(T)` is a finite, QD-admissible quantification domain (set-valued closure + QD-fin). But `coverage_G(x)` for an address-denoting endset is `⋃ {t : a ≼ t}` over the denoted addresses — an **infinite** union of subtrees — so it is *not* a QD domain (QD-fin requires finiteness), and `(∃ y ∈ coverage_G(x) :: …)` would be ill-formed. Presenting "the `addrs_G`/`coverage_G` body" as interchangeable options, and calling the result "denoted-target coverage" (which conflates the finite denoted set `addrs_G` with the infinite `coverage_G`), is a precision defect in a section that rests on QD-finiteness. The formal definitions are correct; the prose is not.

**Required**: Drop the `coverage_G` body option and the "coverage" phrasing for per-target; the per-target tier is reached only through `addrs_G(x)` (the finite denoted set). If a coverage-style scope is intended, it must be spelled as S realized via a coverage *test* on each finite `y ∈ addrs_G(x)`, not as a quantification over `coverage_G(x)`.

## OUT_OF_SCOPE

### Topic 1: coordination-correctness of the audit-slice spelling under retraction
The worked registry spells both triggers over audit slices (`L_cmt`, `L_res`) precisely to obtain SF and hence termination — the note owns this ("the design choice, made checkable"). A consequence is that a *nullified* comment still satisfies `T_P(t) = ⊥` (audit-read), so the producer never re-comments a target whose comment was retracted, and likewise a nullified `res` keeps a comment "resolved." This is a coordination-*correctness*/liveness property (does the system recover live handling after retraction?) orthogonal to the termination claims this note makes, and it belongs to a future treatment of coordination adequacy, not to a revision of the termination results here.

META: not invoked — the note defines abstract, recognizable-from-the-PL guarantees (quiescence as a single PL term, absorption, conditional termination with every hypothesis named) that any coordination layer over the substrate would have to satisfy, with bodies deliberately opaque; it has not drifted into implementation mechanics.

VERDICT: REVISE
