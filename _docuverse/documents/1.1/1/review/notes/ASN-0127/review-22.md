# Review of ASN-0127

## REVISE

### Issue 1: False slot enumeration in the cardinality-changing swing variant
**ASN-0127, Worked illustration, *Swing under K.μ~*, cardinality-changing variant**: "L_2' leaves the pre-state result untouched — its only non-empty coverage slot misses `{a_1}` (`coverage(e_1) ∩ {a_1} = subtree(a_2) ∩ {a_1} = ∅`, since `a_2 ⋠ a_1`), so `findlinks_disc(W₀, d, Σ) = {L_1}` still"
**Problem**: `L_2' = ({a_2}, ∅, Θ)` has **two** non-empty slots: `e₁ = {a_2}` and `e₃ = Θ = {a_θ}` — the same sentence's setup even emphasizes "`Θ = {a_θ}` mandatory" (L3 requires `e₃ ≠ ∅`). "Only non-empty coverage slot" is factually wrong. The conclusion survives only because `subtree(a_θ) ∩ {a_1} = ∅` (established in the shorthand paragraph), but that slot must be checked, not erased — every other match analysis in the illustration correctly enumerates the type slot.
**Required**: Replace with an enumeration of both non-empty slots, e.g. "its from-slot misses `{a_1}` (…) and its type slot misses (`subtree(a_θ) ∩ {a_1} = ∅`, as established above)."

### Issue 2: Five informal ASN-0098 analogy invocations, zero formal bridge to `discoverable_from`
**ASN-0127, F-IMG degenerate cases / F-V / D-CWP**: "This matches the boundary behavior ASN-0098 pins down for the analogous primitive `project`"; "This is the composite reading of the ASN-0098 `project` boundary precedent"; D-CWP statement: "(the **bridge**, the discovery analog of LP12a's `project(a, i, d, Σ') = project(a, i, d, Σ) ∩ R`, ASN-0098)"; D-CWP derivation: "the discovery analog, on the contraction side, of ASN-0098's LP12a … like LP12a it is stated purely over the pre-state"; D-CWP boundary: "This is the whole-set reading of LP12a's own `R = ∅` specialisation `wp ≡ false` … The difference is one of grain …"
**Problem**: The relationship to the foundation's established discovery predicate is asserted rhetorically five times but never once proven, even though the formal bridge is one line: for `W ⊇ dom(Σ.M(d))`, `image(W, d, Σ) = ran(Σ.M(d))`, hence by LP12 (ASN-0098) `findlinks_V(W, d, Σ) = {a ∈ dom(Σ.L) : discoverable_from(a, d, Σ)}`. The note formalizes the empty-region boundary (`findlinks_V = ∅`) but leaves the full-region boundary — the one that ties its new vocabulary to the foundation's — as commentary. Without it, two vocabularies for the same concept coexist unconnected, and "analog" carries the load a lemma should carry. This is also the worst accretion cluster: three of the five call-outs sit inside a single lemma (D-CWP).
**Required**: State and derive the full-region reduction as a numbered claim (premises: F-IMG, F-V, LP12), then cut the analogy commentary to at most one citation site.

### Issue 3: Undischarged standing conditions — `d ∈ dom(Σ'.M)` persistence and image finiteness
**ASN-0127, F-IMG-MONO/F-IMG-CONTR/F-IMG-SWING, D-NONMONO, D-CWP**: every cross-state claim evaluates `image(W, d, Σ')` or `findlinks_disc(W, d_q, Σ')`, both undefined when `d ∉ dom(Σ'.M)` (F-IMG, F-V). **ASN-0127, F-IMG-SWING**: "the pinned cardinality makes a moved image take two distinct equal-size values, and distinct equal-size finite sets cannot nest."
**Problem**: (a) Definedness at the post-state is a precondition of the very expressions written, and it is never discharged. It follows from M1 (ArrangementMonotonicity, ASN-0047) — and the foundation models exactly this discharge: LP4 (ASN-0098) carries "(with `d ∈ dom(Σ'.M)` lifted by M1)". (b) The cannot-nest step is load-bearing only for *finite* sets (equal-cardinality infinite sets can nest); finiteness of the image comes from `image(W, d, Σ) ⊆ ran(Σ.M(d))` and S8-fin (ASN-0036), and is uncited. The corpus's per-step citation convention requires both.
**Required**: One sentence citing M1 for post-state definedness (once, where cross-state claims begin), and one citation of S8-fin at the cannot-nest step.

### Issue 4: The K.λ-residual narrative is told three times, and names an induction that does not exist
**ASN-0127, stability keystone section**: (i) intro paragraph: "supplied by the `Σ.L`-preserving transitions (F-PRES) but failing on any path that admits K.λ, where the existence-anchoring claims rest instead on LP13's per-link value persistence (E-INV)"; (ii) pre-lemma sentence: "A weaker per-link form supports the inductive step for K.λ"; (iii) F-CIL-perlink derivation tail: "the weakening is load-bearing under K.λ, where `dom(Σ'.L) = dom(Σ.L) ∪ {ℓ_new} ≠ dom(Σ.L)` makes F-CIL's global hypothesis fail while per-link preservation still holds at each prior key … F-CIL-perlink is therefore not an instance of F-CIL but the residual per-link reasoning that survives the weaker hypothesis."
**Problem**: The same point — F-CIL's global hypothesis fails under K.λ; per-link preservation takes over — appears in three places, two of them forward-deferring to F-PRES, E-INV, and F-LAMBDA before any of those exist. This is the flagged accretion pattern (multiple paragraphs deferring to the same downstream content; role-narration around a lemma rather than its content). Additionally, "the inductive step for K.λ" promises an induction the note never performs: F-LAMBDA is a single-step result, and all path-level claims route through LP13 (E-INV) or per-step chaining (F-INERT), not through an induction with F-CIL-perlink as its step.
**Required**: Say it once — at F-CIL-perlink, where the hypothesis weakening is visible — and delete the other two occurrences; replace "supports the inductive step for K.λ" with the accurate role (per-link residual used by F-LAMBDA).

### Issue 5: Residual meta-prose and precision slips
**ASN-0127, several sites**:
- F-MATCH: "a link with a multi-slot endset that meets `I` in any one slot is matched" — type slip: links have slots; endsets do not. Should read "a multi-slot *link*."
- D-ZERO: "(its image drops by D-NONMONO)" — ambiguous antecedent ("its" = the link's? the region's?), and the image fact is F-IMG-CONTR; D-NONMONO's contraction clause is the *set* consequence. Cite the right claim.
- F-UDIST: "this is union-distribution of a set-valued operation, not a measure-style additive law over disjoint pieces" — defensive disclaimer against a misreading nothing in the statement invites; the statement's "no disjointness required" plus F-VDIST's substantive overlap remark already carry the point.
- F-IMONO: "it is the fact a shrinking resolved request needs in the discovery analysis (D-NONMONO)" — downstream-consumer inventory in a derivation tail.
- F-V: "This is a *definition*, not a derived theorem." — status already carried by `≡` and the table's "(definition)" label.
- F-INERT: "the single-step-to-closure lift that ASN-0098's Closure schema (★) names, here instantiated over the K.λ-free restriction of the step relation" — schema (★) is stated for membership-persistence/value-preservation conjunctions over the *unrestricted* step relation; F-INERT's property is a result-equality chained over a *restricted* path. The honest justification is a two-line induction on path length; cite it as that, not as a schema instance it doesn't fit.
**Problem**: Each is small, but together they are exactly the accretion the anti-bloat classifier targets: defensive justifications, consumer inventories, and citations stretched past their stated scope, sitting between a reader and the algebra.
**Required**: Fix the two precision slips; delete or fold the three meta-sentences; restate F-INERT's closure step as a direct induction.

## OUT_OF_SCOPE

### Topic 1: Region-scoped transclusion and fork discovery
LP16 (ASN-0098) gives two-document discoverability from shared coverage I-addresses; the region-scoped analogue — when does `findlinks_disc(W₁, d₁, Σ)` agree with `findlinks_disc(W₂, d₂, Σ)` for transcluded regions, and how does the discovery set behave across a J4 Fork composite, where the order-preserving bijection φ carries `d_op`'s arrangement into `d_new` — is new territory.
**Why out of scope**: The note deliberately fixes a single query document; cross-document and composite-transition discovery is a different theorem set, not a gap in the single-document algebra established here.

### Topic 2: Meta-link queries over link-subspace regions
F-IMG admits `W` containing link-subspace V-positions (S3★ routes their images into `dom(Σ.L)`), so `findlinks_disc` can ask which links reach *links* arranged in a document. The interaction with CL-OWN/CL-UNIQ (every document's link-subspace arrangement holds only its own links, injectively) is noted nowhere and would shape what such queries can return.
**Why out of scope**: The algebra is sound on arbitrary `W`; characterizing the link-subspace specialization is a follow-on, not an error here. (Q1–Q4 already self-defer the conjunctive matching, uniform wp, content-keyed, and projection-composition questions.)

VERDICT: REVISE
