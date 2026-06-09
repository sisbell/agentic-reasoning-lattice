# Review of ASN-0126

The formal core is strong. I checked the worked illustration's address arithmetic (`a_R = inc(ℓ₂,0) = ...2.3`, `a = g = ...2.4 ∈ coverage(G_rng) = [...2.4, ...2.7)`), the gated-emit wp derivation, the projection-bridge transfer of ASN-0086 lemmas (all quantified over `→*`-reachable, so valid without the unit-depth discipline), and the P5 lifting proof. These hold up. The born-nullified witness correctly demonstrates that the inherited third wp conjunct stays live under Binary-gated retraction. My findings are almost entirely the meta-prose accretion the note's own `anti-bloat` classifier flags.

## REVISE

### Issue 1: Essay content in "App-side obligations"
**ASN-0126, Single-source**: "R is not a framework-guaranteed type — the substrate ships the typed-link mechanism, not a fixed catalog ... an app needing multi-source relations drops to a different substrate, ASN-0086's ungated →, whose K.λ admits arbitrary arity directly."
**Problem**: This paragraph advances no reasoning the surrounding claims need. It restates "the app registers R" (already said one paragraph up), forward-references P6, and editorializes about which substrate an app "drops to." A reader chasing the `|F|=1` consequence must skip past it.
**Required**: Delete the paragraph; if the "app, not substrate, registers R" obligation is load-bearing, fold it into a single clause where R is first introduced.

### Issue 2: "Why the precondition is needed" prose around arity-3
**ASN-0126, The shape-gated emit**: "The arity restriction is not because higher-arity values are unreadable — F = e₁ and G = e₂ project at any arity N ≥ 3 — but because at N > 3 there are content slots beyond e₁, e₂ ... only arity 3 makes {e₁, e₂} exhaustive over content."
**Problem**: The preceding sentence already states what (0) does (forces the standard triple so `Sh-conf`'s two-slot test is exhaustive). This "not because X but because Y, e.g. e₄ in a 5-endset" elaboration justifies *why* the precondition exists rather than stating it — the named "domain-discharge ordering" device is invoked twice in the same passage to the same end.
**Required**: Keep the one-sentence statement that (0) forces arity 3 so `{e₁,e₂}` is content-exhaustive. Cut the counterfactual ("not because unreadable") and the e₄ excursus.

### Issue 3: Philosophical closer in Registry permanence
**ASN-0126, Registry permanence**: "Distinct registries yield distinct substrates: the registry is not state the substrate evolves through but a parameter that individuates which substrate one is in."
**Problem**: This adds nothing P1 has not already established (`Σ.registry = Σ_init.registry` for all reachable Σ). It is interpretive essay content in a structural slot.
**Required**: Remove.

### Issue 4: Span-count-vs-coverage explained twice, plus app-responsibility prose
**ASN-0126, Single-source** ("`|F| = 1` counts spans, not addresses reached") **and Shape-conformance** ("A single unit-depth span ... is one span ... yet its coverage is ... generally infinite ... Span-count, not coverage, is the measure").
**Problem**: The same point — span count is the measure, not coverage — is made in both sections. Shape-conformance then spends a full paragraph on app responsibility ("coalescing any multi-span presentation ... is the app's responsibility ... not the substrate's at the gate"), which is a use-site/responsibility inventory wrapped around the one genuine technical fact (span-count is coverage-variant, so two abutting same-coverage spans fail). The fact is worth one sentence; the responsibility framing is not.
**Required**: State the measure once. In Shape-conformance, reduce the coalescing paragraph to the single coverage-variance observation; drop the "whose responsibility" attribution.

### Issue 5: Multiple deferrals to the same downstream proof
**ASN-0126, wp section**: "the full discharge is in P5's proof, Gate realizability" — and **Properties established, P5**: "Derived in The shape-gated emit (Gate realizability)."
**Problem**: The wp paragraph (itself inside "The shape-gated emit") defers the `K ∈ T_admissible` discharge forward to P5, which lives in the same section; P5's summary then points back. This is a deferral loop within one section that makes the reader hop to follow a one-line fact (`coverage(K) = coverage(K_j) ≠ ∅ ⟹ K ∈ T_admissible`).
**Required**: State the `K registered ⟹ K ∈ T_admissible` discharge inline at first use (it is a single line) and drop the forward pointer.

## OUT_OF_SCOPE

### Topic 1: Operational semantics — idem, behavior catalog, default predicates, composition
**Why out of scope**: The Open questions list correctly defers these to a successor note. This ASN's job is the static shape catalog, gate, and immutable registry; layering read-filters/transitive-closure/idempotence on top is new territory, not a defect here.

### Topic 2: Arity beyond N=3 and multi-source (|F| > 1)
**Why out of scope**: Open question 6 names this as a separate path. The note's contribution is deliberately the `F=1, N=3` slice; richer arity belongs to a supplemental framework.

VERDICT: REVISE
