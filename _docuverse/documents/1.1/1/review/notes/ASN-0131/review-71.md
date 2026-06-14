# Review of ASN-0131

I checked the substantive machinery and found it sound. The biconditional RE-DEF and its soundness/completeness reads (RE-SND, RE-CMP) are faithful; the worked instance computes correctly (the width-2 span reaches `a₄` so `{a₂,a₃} ⊆ coverage(e₁)`, the `θ`-vs-content field-agreement argument is valid, the answer `{(1,e₁)}` reads off every distinctive claim); the union/intersection laws are correct, including the two independent `⊇`-counterexamples and the necessary-and-sufficient touch-implication characterization; RE-ADDR's antichain argument and RE-RET's R-Scope-bounded backward direction are both rigorous; and RE-CWP's weakest precondition derivation (including the `R = ∅` boundary collapsing to `RE = ∅`) is exact. No logic defect found.

The findings below are all the anti-bloat patterns the classifier targets — forward-reference accretion around the retraction machinery. They are prose to trim, not arguments to re-prove.

## REVISE

### Issue 1: Duplicated retraction-deferral announcement
**ASN-0131, "The unit of the answer" preamble vs. "Fresh emissions" opener**:

Preamble: *"The retraction *discipline* — which constrains the way the withdrawn set grows — bears only on two later questions: what a fresh emission, and what a retraction step, each leave addressable. We set it up where the first arises (RE-ADDR, 'Fresh emissions' below) and draw on it again under 'Stability' (RE-RET)."*

Opener: *"We now set up the retraction machinery deferred from the definition. It is needed only here (RE-ADDR) and under 'Stability' (RE-RET) — the two points where addressability depends on *how* the retraction slice grows, rather than on its present contents alone."*

**Problem**: These two passages, in different sections, say the same thing in different words — both announce that the retraction discipline is needed at RE-ADDR and RE-RET. This is precisely the flagged pattern (two paragraphs deferring to the same downstream locations; document-ordering justification "we set it up below / we now set it up"). The reader meets the same deferral twice and has skipped past meta-prose before any retraction content is delivered.

**Required**: Keep the machinery setup once, at its point of use (the Fresh-emissions section). Delete the preamble's deferral sentences ("We set it up where the first arises … and draw on it again …") and the opener's "deferred from the definition / needed only here and under Stability" framing. The substantive content — that the discipline bears only on what an emission and a retraction step leave addressable — survives in the setup itself.

### Issue 2: Consumer-inventory in the `addressable` preamble
**ASN-0131, "The unit of the answer"**: *"So `addressable`, the definition RE-DEF we are about to give, and everything we read off them through soundness, completeness, composition, selection, and contraction depend on `Σ.L` and the present arrangement, never on *how* a retraction was performed."*

**Problem**: The sentence forward-references RE-DEF (given two paragraphs later in the same section) and enumerates five downstream sections as consumers. This is the "definition's introduction enumerates downstream consumers … rather than advancing the definition's meaning" pattern. The real point — `addressable` and `RE` are history-independent, depending only on present `Σ.L` — does not need the roll-call of section names to land.

**Required**: State the history-independence point plainly and drop both the "RE-DEF we are about to give" forward pointer and the "soundness, completeness, composition, selection, and contraction" enumeration.

### Issue 3 (minor): Use-site recap tail on the `Σ.L`-evolution bridge
**ASN-0131, "Fresh emissions"**: *"So importing unit-depth is licensed by the standing assumption, not by the bare `→*` inclusion that carries the note's other ASN-0086 `Σ.L`-lemmas — those cited 'via the `Σ.L`-evolution bridge' at their use sites."*

**Problem**: The distinction between the two import strengths (unit-depth needs layer-reachability via the standing assumption; R0a/R-Scope need only `→*`) is correct and load-bearing. But the tail — "those cited 'via the bridge' at their use sites" — is a use-site inventory of where the other lemmas get cited, which adds no reasoning. Naming the bridge once and citing it later is fine; cataloguing the citations here is the accretion.

**Required**: Keep the two-route distinction tersely; drop the use-site-pointer tail.

## OUT_OF_SCOPE

### The link-subspace region (OQ7), type-slot/content semantics (OQ6), cross-server completeness (OQ5)
**Why out of scope**: These are correctly deferred to the note's own Open Questions rather than half-answered. The `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis carried for RE-RET's forward direction, and the `W ⊆ s_C` caller obligation, are both disclosed as conditions rather than smuggled in — appropriate scoping, not errors.

### The conservative-lift modelling assumption for ASN-0082 insert/delete
**Why out of scope**: ASN-0082 models its shift primitives only over `(C, M)`; whether they frame `Σ.L, Σ.E, Σ.R` in the full `(C,L,E,M,R)` state is genuinely another layer's question. The note handles it by an explicitly-labeled modelling assumption rather than an unstated leap, which is the honest way to bridge the model mismatch — not a defect in this ASN.

VERDICT: REVISE
