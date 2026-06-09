# Review of ASN-0126

## REVISE

### Issue 1: The standard-triple shape of every stored value is presupposed but never established

**ASN-0126, "Properties established" (P6) and "The shape-gated emit" (P3)**: P6 reads "the stored tuple `Σ.L(a) = (F, G, K)`" for every `a ∈ dom(Σ.L)`, and its induction "carries the *predicate* 'K registered ∧ `Sh-conf(K, F, G) = ⊤`'" — both referencing `F, G`. P3 likewise quantifies over "a tuple `(F, G, K)`."

**Problem**: Both P6's statement and its IH presuppose that every stored value decomposes as a standard triple `(F, G, K)` of arity exactly 3 — that is what licenses extracting `F = e₁`, `G = e₂` so `Sh-conf` can be read at all. But the derivation P6 spells out is meticulous about citing a premise for *every other* conjunct — value persists by L12, registration persists by P1, conformance persists by P4, new tuples handled by P3 — while never establishing the triple shape. That shape comes solely from precondition (0) ("the emitted value is a standard triple — arity 3") on `K.λ_sh`, the only depositing step, together with `Σ_init.L = ∅`. P3's proof says only "(i), (ii) are among its preconditions" and never isolates (0)'s contribution; P6's proof never invokes (0). The omission is conspicuous because the wp section *does* handle arity-3 carefully ("the postcondition's arity-3 slice `|Σ.L(a)| = 3` already forces it") — yet P6, the audit-level closure that "a consuming app relies on," silently drops it. This is not merely notational: "every link in the gated store has arity 3" is itself a guarantee apps depend on, and P6 understates what it actually proves.

**Required**: State the standard-triple closure explicitly. Add to P3 that every `→_sh`-deposited value is a standard triple (immediate from (0)), and have P6 carry "stored value is a standard triple ∧ K registered ∧ `Sh-conf = ⊤`," citing (0) for the first conjunct alongside L12/P1/P4 for the rest.

### Issue 2 (anti-bloat): the no-image conclusion is derived twice in Single-source

**ASN-0126, Single-source, paras 2–3**: Para 2 establishes the general fact — "the `|F| = 1` rule ... excludes *every* empty-from emit ASN-0086 admits ... `Emit_K(Σ, d, ∅, G)` is a legitimate ASN-0086 invocation with no `→_sh` image" — and closes with the connective "Retraction is simply the named operation where this bites." Para 3 then re-walks the identical argument for the specific case ("Nullify ≡ Emit_R(…, ∅, …) with an *empty* from-set; under `|F| = 1` that form fails every shape, so the literal `F = ∅` Nullify has **no** `→_sh` image") before reaching its actual new content, the Binary wrapper recipe.

**Problem**: The empty-from → fails-`|F|=1` → no-`→_sh`-image chain is stated generically, then re-instantiated for Nullify, which is an immediate instance of the general claim; plus the "Retraction is simply…" sentence is connective filler announcing the next paragraph. This is the same-thing-twice / essay-in-structural-slot accretion the anti-bloat pass targets.

**Required**: Keep para 2's generality claim (it usefully shows the rule is not retraction-specific). In para 3, cite that result rather than re-deriving the Nullify no-image conclusion, and drop the connective sentence — proceed directly to the wrapper.

## OUT_OF_SCOPE

### Topic 1: a unit-depth-constrained Binary shape

The note honestly discloses (Single-source) that registering R as Binary is strictly weaker than ASN-0086's unit-depth retraction discipline — a single *non-unit* G-span is Binary-conformant, so R-Scope's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` holds only when the app voluntarily routes through the unit-depth wrapper. A shape that gates G by span *shape* (unit-depth), not merely span *count*, would recover the single-tuple guarantee at the gate itself.

**Why out of scope**: the catalog here is deliberately classified by G span count; a span-shape-classified variant is a new catalog entry, and the disclosure shows this is a known, intended limitation rather than a hidden gap.

VERDICT: REVISE
