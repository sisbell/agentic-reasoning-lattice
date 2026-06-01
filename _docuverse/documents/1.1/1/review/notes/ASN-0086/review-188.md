# Review of ASN-0086

## REVISE

### Issue 1: K-Step Conformance Preservation proof uses the wrong closure symbol for the witnessing trajectory

**ASN-0086, Lemma — K-Step Conformance Preservation (proof)**: "Substrate-conformance of Σ is witnessed by a trajectory `Σ_init →* Σ` of conformance-witnessing steps; appending the conformance-preserving step Σ → Σ' (resp. Σ ↝ Σ') extends that trajectory…"

**Problem**: `→*` is defined as the reflexive-transitive closure of `→ ≡ K.σ ∪ K.α ∪ K.λ` (K-ops only). But the note explicitly asserts `{→*-reachable} ⊊ {substrate-conforming}` is strict, witnessed by conformance-preserving `↝`-steps that are *not* `→`-steps (Remark — NestedLinkWitness; Definition — state-local-conforming state). For a substrate-conforming Σ that is *not* `→*`-reachable, no trajectory `Σ_init →* Σ` exists — so the proof's witness is unavailable for precisely the states that make the lemma non-trivial. Taken literally, the proof only covers `→*`-reachable Σ, collapsing the very distinction the document builds.

**Required**: Replace `→*` here with the generic conformance-witnessing closure (the reflexive-transitive closure of the conformance-preserving sub-relation of `↝`, per the Definition — substrate-conforming state), and state that symbol explicitly. The `→` arrow must not be reused for it.

### Issue 2: The Nullify definition and wp Case 1 state the P0/P1/PC load-bearingness twice

**ASN-0086, Definition — Nullify**: "The other two conditions are *not* execution gates… **P1**: `a ∈ A_rel^Σ`… and **PC**: Σ substrate-conforming… Nullify still executes when P1 or PC fails; what fails is only the guarantee that the emission's nullified-scope is exactly `{a}`…" — closing with the forward pointer "(The wp Case 1 analysis below confirms that P0, P1, and PC are each load-bearing…)".

**Problem**: The wp Case 1 paragraph then re-derives exactly this — that P0 gates execution while P1 and PC condition R-Scope, and that each is load-bearing — in different words. Two passages in different sections carry the same content, and the first defers forward to the second. This is the forward-reference accretion the note's anti-bloat classifier targets: the reader must hold the informal Nullify-definition version and the formal wp version side by side to confirm they agree.

**Required**: State the P0-gate / (P1,PC)-scope distinction once (the formal wp Case 1 derivation is the load-bearing site), and reduce the Nullify definition to the operation's effect plus a single cross-reference. Drop the "(The wp Case 1 analysis below confirms…)" pointer.

### Issue 3: Worked-example Step 4 justifies a pre-state property with an irrelevant fact about the call

**ASN-0086, Worked Sketch, Step 4**: "The call is admissible to a direct K.λ caller, and its to-span is unit-depth in shape, so Σ_3 stays within the wp's domain — substrate-conforming and unit-depth-disciplined…"

**Problem**: The wp Case 2 domain condition is on the *pre-state* Σ_3. Whether Σ_3 is unit-depth-disciplined depends on Σ_3's existing `L_R^{Σ_3}` tuples (targets `a₁`, `b₁`, both live links), not on the shape of the new Step-4 call's to-span. The stated reason ("its to-span is unit-depth in shape") does not entail the conclusion ("Σ_3 stays within the wp's domain"); the conclusion is true for an unrelated reason. This is a non-sequitur justification of the kind the reviser-drift checklist flags (prose that does not advance the reasoning).

**Required**: Justify Σ_3 ∈ domain by Σ_3's own properties: Σ_3 is `→*`-reachable (hence substrate-conforming) and its pre-existing retraction tuples target live links (hence unit-depth-disciplined). The new call's to-span shape is irrelevant to pre-state domain membership and should be dropped or recast as a separate observation (that the call does not itself break the discipline).

### Issue 4: Disjoint-union well-definedness of `L^Σ` asserts forward rather than deriving in place

**ASN-0086, Definition — TypedRelation**: "We will show (R1) that this disjoint union is well-defined: each tuple address belongs to exactly one coverage-class slice."

**Problem**: The disjointness of `L^Σ = ⨆ L_K^Σ` is a one-step consequence of `Σ.L` being a function (a single value at `a` fixes one coverage class `[Σ.L(a).e₃]`). The definition defers this to R1, but R1 is stated as address-injectivity, and the "exactly one slice" reading is only a parenthetical aside inside R1's proof. A definition that introduces a disjoint union should discharge disjointness where the union is formed, not forward-point to a lemma whose headline claim is a different property.

**Required**: Inline the one-line disjointness argument at the union's definition (function-ness of `Σ.L` ⟹ unique `[Σ.L(a).e₃]`), and keep R1 to its injectivity statement.

## OUT_OF_SCOPE

### Topic 1: Cross-store invariants between `L_K` and arrangements `Σ.M`
**Why out of scope**: Whether relational predicates over `L_K` must coordinate with arrangement visibility (`Σ.M`) is genuinely new territory — the note correctly defers it to its first Open Question. It is not an error in this ASN, which scopes itself to the `Σ.L` store.

### Topic 2: Concurrency/atomicity of Emit vs. Observe
**Why out of scope**: The consistency model under which `A_K` transitions are observed concurrently is a future ASN concern (already an Open Question). This note's `→`-step semantics are sequential by the SequentialTransitionAxiom inherited from ASN-0093, which suffices for the present claims.

META: The ASN remains within specification territory — it defines state (typed relations, active subset), operations (Emit/Observe/Nullify), and invariants (R0–R7) abstractly enough that an alternative implementation would have to satisfy them; the findings are precision and bloat, not drift.

VERDICT: REVISE
