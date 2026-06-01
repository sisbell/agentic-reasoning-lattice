# Review of ASN-0086

## REVISE

### Issue 1: The unit-depth retraction discipline is claimed equivalent to "reached by relational-layer operations," but Nullify can target non-A_rel addresses

**ASN-0086, Definition — Unit-depth retraction discipline**: "A layer satisfies the *unit-depth retraction discipline* iff every `L_R^Σ` tuple ... has a to-endset of the form `{(b, δ(1, #b))}` for some target `b ∈ A_rel^Σ` — equivalently, every `L_R^Σ` tuple was produced by a `Nullify(Σ, d_retr, b)` call."

And the wp domain restriction, Case 2: "every *pre-existing* `L_R^Σ` tuple has a unit-depth to-span `{(b, δ(1, #b))}` with coverage `{t : b ≼ t}` for some `b ∈ A_rel^Σ`; the fresh `a` is prefix-incomparable with every such `b` by K.λ's emission rule together with R0a."

**Problem**: The stated equivalence is false. The Definition of Nullify explicitly says P1 (`a ∈ A_rel^Σ`) "neither gates execution ... the underlying Emit_R executes and produces a Σ' even when `a ∉ A_rel^Σ`" and that off the P1 path `a` may be "a content, document, or ghost address." So a `Nullify` call — a published relational-layer operation — can produce an `L_R^Σ` tuple whose to-span target `b` is **not** in `A_rel^Σ`. Hence "produced by a Nullify call" does **not** entail "target `b ∈ A_rel^Σ`," and a state reached using only relational-layer operations need not satisfy the discipline as written.

This breaks the wp Case 2 derivation. The step "the fresh `a` is prefix-incomparable with every such `b` ... together with R0a" invokes R0a, whose antichain covers only `dom(Σ.L) = A_rel`. If a pre-existing retraction targets a document-level ghost `b` (zeros = 2) — a well-formed `Nullify(Σ, d_retr, b)` call, since `(b, δ(1,#b))` is T12-valid for any `b` with `#b ≥ 1` — then `coverage({(b, δ(1,#b))}) = {t : b ≼ t}` can contain a *future* fresh link address `a` allocated under that document (`b ≼ a` holds when `b = home(a)`). Then `a ∈ nullified(Σ')` and `(a,F,G) ∉ A_K^{Σ'}` even though both wp disjuncts may hold — falsifying the weakest-precondition claim over the domain the ASN says is relational-layer-reachable.

**Required**: Reconcile the two. Either (a) restrict the relational layer's `Nullify` usage so targets must lie in `A_rel^Σ`, and state that restriction as the layer commitment that makes the "equivalently produced by Nullify" gloss true; or (b) drop "target `b ∈ A_rel^Σ`" from the discipline and re-derive the wp Case 2 "no pre-existing retraction nullifies `a`" step without R0a — i.e., establish `b ⋠ a` for arbitrary (possibly document-level/ghost) unit-depth targets, which the current argument does not do.

### Issue 2: Defensive meta-prose justifying the `↝` definition's existence

**ASN-0086, State transition relation / `↝`**: "This categorical relation is required by R7a, whose decomposition theorem quantifies over *every* transition a higher-layer operation may issue against `Σ.L` — a generality the concrete `→` (fixed to the three K-ops) cannot express. The deliberately open-ended range is the content of R7a's universal claim, not an imprecision."

**Problem**: This is forward-reference accretion: the definition explains *why it is needed* (and defends against a charge of "imprecision") rather than stating what `↝` is. The operative content — `↝` is the union of `→` with any higher-layer transition — is already given in the preceding sentence. The justification belongs to R7a, not to the definition slot.

**Required**: Delete the defensive sentences; keep only the definitional content. R7a can state its own quantification requirement at its own site.

### Issue 3: Use-site inventory plus defensive justification in the state-local-conforming definition

**ASN-0086, Definition — state-local-conforming state**: "We attach no reachability requirement: the lemmas quantifying over state-local-conforming states — R0, R5, Emit_K — discharge their post-state obligations from the catalog invariants holding *at* Σ and never consult how Σ was reached, so a reachability conjunct would add nothing they use."

**Problem**: This enumerates downstream consumers (R0, R5, Emit_K) to justify an *omission* — the "use-site inventory" and "explains why needed rather than what it says" anti-bloat patterns. The definition's content is "preserves the state-local catalog, need not satisfy chain discipline or R0a"; the inventory does not advance that meaning and will rot as consumers change.

**Required**: Reduce to the definitional statement plus, if needed, a single clause noting the absence of a reachability requirement. Drop the R0/R5/Emit_K enumeration.

## OUT_OF_SCOPE

### Topic 1: Cardinality/ratio bounds on `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Raised as an Open Question; quantitative retraction bounds are new territory, not a defect in this note's qualitative invariants.

### Topic 2: Higher-arity typed relations `L_K^{(n)}` and binary projections
**Why out of scope**: The note explicitly restricts to standard-triple links; multi-arity relational structure is a future ASN.

VERDICT: REVISE
