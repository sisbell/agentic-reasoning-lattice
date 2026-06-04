# Review of ASN-0099

## REVISE

### Issue 1: Summary sentence after F9-λ restates and forward-points without advancing the argument
**ASN-0099, "Arrangement Independence" (after F9-λ derivation)**: "F9 and F9-λ together exhaust V's single-step impact on `findlinks(I, ·)`: F9's invariance across V ∖ {K.λ} and F9-λ's controlled increment at K.λ. F19 below confirms the multi-step closure is monotone."
**Problem**: This paragraph proves nothing. It restates what F9 and F9-λ already establish, makes an exhaustiveness gesture ("together exhaust"), and forward-defers to F19. A reader following the chain must skip it. This is exactly the accreted summary-with-forward-reference pattern the anti-bloat classifier targets.
**Required**: Delete the sentence. F9 and F9-λ stand on their own; F19 is reached in due course.

### Issue 2: ComprehensionInvariantUnderΣL is introduced with meta-prose about document structure
**ASN-0099, "Determinism and Comprehension Invariance"**: "F8 is one instance of a structural pattern that recurs throughout this ASN: every claim of the form 'the comprehension is unchanged when `Σ.L = Σ'.L`' rests on the same derivation chain. We name it once as a discrete step."
**Problem**: Naming a reused lemma is fine, but this framing sentence explains *why the lemma exists in the document* ("recurs throughout this ASN," "We name it once") rather than stating its content. It is an authorial use-site gesture, not reasoning. The lemma body that follows is self-justifying.
**Required**: State the lemma directly. Drop the "one instance of a structural pattern that recurs… We name it once" preamble.

### Issue 3: F4's headline claim is tautological; the framing inflates illustrative witnesses into an exhaustiveness theorem
**ASN-0099, F4 (MatchIndividuation)**: "Any predicate disagreeing with F1 on a realizable (a, I) pair defines a different operation, not an alternative implementation of FINDLINKS."
**Problem**: As stated, F4's headline is a tautology — any total function that disagrees with another on some input *is* a different function. The substantive content lives entirely in the five witness constructions (which genuinely disambiguate overlap from containment/cardinality semantics and are legitimate object-level content). But the "three strengthenings and two weakenings" framing presents an *illustration* as if it were an exhaustive individuation result; five examples do not establish that no other predicate coincides with F1. The witnesses are worth keeping; the theorem-shaped wrapper around a tautology is the bloat.
**Required**: Restate F4 to claim what it actually demonstrates — that natural alternative match designs (coverage-containment either direction, cardinality threshold, I-independent slot tests) yield operations distinct from FINDLINKS, with the witnesses below — and drop the tautological "any predicate disagreeing… defines a different operation" formulation and the exhaustiveness count.

## OUT_OF_SCOPE

### Topic 1: Time bound between K.λ commit and FINDLINKS visibility
**Why out of scope**: The note correctly defers this to an Open Question; latency/consistency semantics are genuinely future territory, not a defect here.

The mathematics checks out: A1a's per-operation `L'=L` citations against ASN-0047's amended frames are correct; the V∖{K.λ} vocabulary is exhaustively covered (A1a atomic + A1 for K.μ~); F13/F20/F20a distribution chains are valid; the worked example (Queries 1–6) is internally consistent; F11's I-side persistence and its disclaimed V-side non-analogue are sound.

VERDICT: REVISE
