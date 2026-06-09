# Review of ASN-0126

## REVISE

### Issue 1: The shape-gated emit's wp does not coincide with `K.λ_sh`'s precondition

**ASN-0126, The shape-gated emit**: "This weakest precondition *coincides with `K.λ_sh`'s own precondition*. ... The added guards introduce no slack between 'enabled' and 'achieves the postcondition': every legal `→_sh` emit attains active-subset membership of its tuple, and the gate rejects exactly the calls whose tuples are unregistered/non-conforming or, by the inherited conjuncts, would fail to land active."

**Problem**: This is the note's central depth artifact, and the coincidence claim is false — it contradicts the note's own next paragraph.

`K.λ_sh`'s precondition is, by definition, `K.λ`'s precondition (L3 / `d ∈ dom(Σ.M)`) plus the three *added* guards (0), (i), (ii). It does **not** contain ASN-0086's second conjunct `(K ≁ R ∨ a_emit ∉ coverage(G))` nor the third `¬(∃ (b,F',G') ∈ L_R^Σ :: a_emit ∈ coverage(G'))`. Those are *landing* conditions the wp derives for the postcondition `(a,F,G) ∈ A_K^{Σ'}`; they are not enablement conditions. ASN-0086 itself is careful here: it asserts wp/precondition coincidence only for Case 1 (Nullify), and pointedly does **not** for Case 2 (active-subset emit). This note re-introduces the coincidence claim that ASN-0086 declined to make.

The note's own *Disciplined-domain simplification (conditional)* paragraph then states the opposite: at a general `→_sh`-reachable (non-layer-reachable) state the third conjunct "cannot be dropped" and "the full inherited wp ... all three ASN-0086 conjuncts intact ... stands." If the third conjunct is genuinely non-vacuous there, then there exist legal `→_sh` emits whose tuples do **not** land in `A_K^{Σ'}` — directly falsifying "every legal `→_sh` emit attains active-subset membership."

Concrete counterexample, built from a retraction form the note explicitly permits: at a `→_sh`-reachable state, register R Binary and emit a *non-unit-depth* Binary retraction `(b, [r], {(ℓ_prev, δ(2, #ℓ_prev))})` — Binary-conformant (`|F|=1, |G|=1`), and the note stresses a single Binary span "of non-unit length ... is equally Binary-conformant." Its coverage `{t : ℓ_prev ≤ t < shift(ℓ_prev,2)}` contains `inc(ℓ_prev,0) = a_emit(Σ,d)`. Now any subsequent shape-conforming `Emit_K(Σ',d,F,G)` is a legal `→_sh`-step (satisfies (0),(i),(ii)) yet deposits its tuple at a pre-nullified address, so `(a,F,G) ∉ A_K^{Σ''}`. The gate did not reject it; the wp's third conjunct did.

**Required**: Drop the coincidence claim and "every legal `→_sh` emit attains active-subset membership." State precisely that the wp for active-subset landing is *strictly stronger* than `K.λ_sh`'s precondition: the gate (`g_sh` + L3) enables the emit, but the two inherited ASN-0086 conjuncts are landing conditions a legal emit may still violate. P4 (the `Sh-conf` enablement half) is the only "by construction" claim the gate supports; reserve the active-subset wp as a separate, strictly stronger condition. Make this consistent with the conditional-simplification paragraph, which already states the correct position.

### Issue 2: Registry well-formedness omits the condition P2/P3 depend on

**ASN-0126, Registration entries**: "A registry is well-formed when shape values lie in `{Unary, Binary, Multi}`, idem values lie in `{⊤, ⊥}`, and names are unique within the registry."

**Problem**: P2 (ShapeStability) and P3 (IdemStability) assert `shape(K)` and `idem(K)` are *well-defined* functions of the coverage class `[K]`. For that, the registry must hold **at most one entry per coverage class** — otherwise two entries with `~`-equal keys but differing shapes would make `shape(K)` multivalued. The well-formedness conditions list *name*-uniqueness (not load-bearing for P2/P3) but omit *coverage-class-key* uniqueness (which is). The prose "the registry assigns `~`-equal endsets one and the same entry" asserts this property, but it is never made a well-formedness requirement, leaving an admissible-looking registry — `{([K],"a",Unary,⊤), ([K'],"b",Binary,⊥)}` with `K ~ K'` — that satisfies every stated condition yet makes `shape(K)` ambiguous and P2 false.

**Required**: Add to the well-formedness conditions that coverage-class keys are unique — no two entries have `~`-equal keys (equivalently, define the registry as a partial function `T_admissible/~ ⇀ (name, shape, idem)`). Then P2/P3 well-definedness follows; as written it rests on prose the well-formedness predicate does not enforce.

## OUT_OF_SCOPE

### Topic 1: Multi-with-`G=∅` versus Unary collision under idem
A Multi registration admits `|G|=0` tuples structurally indistinguishable from Unary tuples (the note notes Multi subsumes Unary/Binary). Whether such a tuple inherits Unary or Multi default predicates, and how `idem` resolves across the overlap, is genuine new territory — correctly deferred to the operational successor (Open questions #1–#3), not an error here.

### Topic 2: Standardized registration of R
Whether R ships pre-registered Binary or each app registers its own retraction type (Open question #4) is left open with explicit Nelson rationale. The expressibility claim is correctly stated conditionally ("when R is registered Binary"), so this belongs to a successor.

VERDICT: REVISE
