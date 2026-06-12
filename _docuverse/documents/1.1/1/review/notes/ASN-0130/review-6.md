# Review of ASN-0130

## REVISE

### Issue 1: Free-variable set of a referent overclaimed as "exactly" its parameters

**ASN-0130, PR3 (Expansion layer)**: "The renaming is total — a referent's free variables are exactly its parameters (PR-SIG), and all of them are renamed — and capture-free by construction"

**ASN-0130, PR3a (Referent step)**: "WT-α … yields `⟨y₁ : C₁, …, y_k : C_k⟩ ⊢ u : C_r`, where `u` is the renamed term, whose free variables are exactly the `yⱼ` and whose binders are fresh expansion names."

**Problem**: Both "exactly" claims are false universals, and PR3 mis-cites its own foundation for the first: PR-SIG establishes only inclusion — "A body well-types under its own `Γ_D` alone, so its free variables are *among* its parameters." Nothing in PR-ENC's domain (deliberately syntax-only) or in PR0's validation requires every parameter to *occur* in the body. Counterexample, constructible end-to-end: the signed term `(⟨x : T⟩, ⊤)` — `⊤` a V-PRIM constant — is in the encoding's syntactic domain (PR-ENC), parses, and well-types (`⟨x : T⟩ ⊢ ⊤ : Bool`, no WT-ref nodes, condition (iv) vacuous), so it registers under PR0. Its body's free-variable set is `∅ ≠ {x}`. After WT-α in PR3a, the renamed `u` for such a referent has free variables `∅ ⊊ {y₁}`.

The damage is confined to the statements, not the proofs: totality of the renaming needs only `free(body) ⊆ params` (renaming all parameters then covers all free variables); the Weaken step's provisos ("neither free in it nor binders of it") and the Substitute step's non-interference ("every `Eⱼ`'s free variables lying in `dom(Γ)`") consume only the inclusion. But a lemma chain of this precision — built specifically to discharge capture-freeness — cannot rest narrative weight on a false set-equality, and PR3's parenthetical attributes to PR-SIG a claim PR-SIG does not make.

**Required**: Replace both occurrences of "exactly" with the inclusion: PR3 — "a referent's free variables are among its parameters (PR-SIG), and all parameters are renamed, so every free variable is"; PR3a — "whose free variables are among the `yⱼ`". Verify no downstream step silently strengthens the inclusion back to equality (none does on my reading — the substitution for an unused `yⱼ` is vacuous and PC2 discharges it the same way).

## OUT_OF_SCOPE

### Topic 1: Authority over de-registration and supersession
A `Nullify_Binary` on a `pdef` tuple de-registers a definition, and anyone may emit `supersedes` into anyone's lineage — the note surfaces the politics (PR4, Open Question 1) but the substrate has no authorization layer anywhere, so "who may withdraw an endorsement or claim succession" is protocol-layer territory, consistent with how the shipped classes already behave. New territory, not an error here.

**Why out of scope**: the note correctly inherits the substrate's stance (record claims, let readers adjudicate); an authority model would be a new layer touching every class, not a repair to this one.

### Topic 2: Signature compatibility across supersession
PR4 resolves *addresses* through `tip()`, but a successor may carry a different `Γ_D` than its predecessor; a tip-following consumer's `args` environment can fail the new `sig`'s precondition (PR3 guards this per-call, so nothing is unsound). A lineage-level compatibility discipline — or a validated supersede surface checking the successor is itself a registered definition with a stated relation to the predecessor's signature — is future work.

**Why out of scope**: PR4 deliberately commits only to the shipped S2 semantics "with no new machinery"; per-call soundness is already guarded by `evaluate`'s precondition.

### Topic 3: Lifecycle of never-registered runs
Content allocated toward a registration that is then rejected (parse failure, interleaved allocation breaking chain-contiguity at condition (i), de-registered referents at (iv)) persists forever by S0, permanently unregistered. Space accounting and authoring-side recovery (re-append a fresh contiguous run) are implementation/application territory adjacent to the fenced "concrete encoding" parameter.

**Why out of scope**: immutability making failed attempts permanent is a substrate-wide property, not a defect of the registration design; the spec-level contract (reject, no tuple) is complete.

VERDICT: REVISE
