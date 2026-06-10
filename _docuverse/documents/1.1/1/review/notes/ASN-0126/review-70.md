# Review of ASN-0126

## REVISE

### Issue 1: The projection-bridge introduction is a use-site inventory plus structural justification
**ASN-0126, The projection bridge**: "The bridge is load-bearing — Retraction as an attributed Binary, the weakest precondition of the gated emit, P5, and P6 all rest on it — so we establish it once, as a lemma, and cite its two consequences thereafter rather than re-deriving them at each site." And in (B2): "This carries, in particular, R0 (fresh-address emission), `a_emit` totality, L-ContiguousPrefix, R-Scope (single-tuple scope), wp Case 2, and L12 (LinkImmutability) from `π(Σ)` to Σ."

**Problem**: Both sentences enumerate downstream consumers and justify the decision to factor out a lemma — the "this is consumed by X, Y, Z … so we establish it once rather than re-derive at each site" pattern. The lemma's meaning is already fully carried by the two preceding sentences ("`π` … carries this framework's gated dynamics onto ASN-0086's ungated dynamics, so that every ASN-0086 result holds, suitably projected, here"). The consumer list and the "establish it once … rather than re-deriving" rationale advance no reasoning, and each named result is re-cited at its own use-site regardless (R-Scope in Retraction, wp Case 2 in the wp section, L12 in P6, L-ContiguousPrefix in the worked illustration). B2's "in particular, R0 … L12" list is the same inventory in consequence form.

**Required**: Drop the load-bearing/consumer inventory and the structural justification. State the bridge and its two consequences (B1, B2) generically; let each use-site name the specific lemma it needs.

### Issue 2: "Single-source" reasons about `→_sh` before `→_sh` exists
**ASN-0126, Single-source**: "it falls outside the shape-gated transition `→_sh` we define below (The shape-gated emit): it has **no** `→_sh` image" and "we supply that re-expression once `→_sh` and the projection bridge are in hand (Retraction as an attributed Binary)."

**Problem**: This section's job is to state `|F| = 1`. Its second and third paragraphs instead reason about `→_sh`'s image (empty-from emits, Nullify) — machinery defined only in the following section — forcing two forward-reference signposts the reader must skip ahead to resolve. The substantive claim ("the `|F| = 1` rule excludes every empty-from emit") is legitimate; its placement before `→_sh` is defined is what generates the scaffolding.

**Required**: State `|F| = 1` here; relocate the empty-from / Nullify-has-no-`→_sh`-image consequence to "The shape-gated emit," where it motivates the retraction re-expression without a forward reference.

### Issue 3: The gate is stated before the registry it gates on is defined
**ASN-0126, The shape-gated emit**: "(i) *K is registered* — the registry records a shape for K … (ii) `Sh-conf(K, F, G)`."

**Problem**: Precondition (i) and the `shape(K)` read by (ii) presuppose (a) `Σ.registry` as a state component — introduced only in the *next* section, "Registry permanence" — and (b) that `shape(K)` is a well-defined function of the coverage class `[K]`, which rests on C0's uniqueness-of-coverage-class-keys condition, established far later in "Registration entries." Without C0, two `~`-equal entries could record different shapes and `shape(K)` would be ambiguous, so (ii) is not yet a well-defined predicate. This is a logical dependency, not just presentation order: the note itself signals the inversion when RegisteredAdmissible cites "C0 (RegistryWellFormedness, **Registration entries below**)."

**Required**: Establish the registry's structure (the `Σ.registry` component, coverage-class keying, C0 well-formedness, and the consequent well-definedness of `shape(·)` on `[K]`) before "The shape-gated emit" gates on "K registered" / `shape(K)`.

### Issue 4: The gated-wp guard uses the partial predicate `Sh-conf` in a flat conjunction
**ASN-0126, Weakest precondition of the shape-gated emit**: "With added guard `g_sh ≡ K registered ∧ Sh-conf(K, F, G)` …"

**Problem**: The note deliberately makes `Sh-conf` partial — "For an unregistered K, `shape(K)` does not exist and `Sh-conf(K, F, G)` carries no truth value." In the gate this is handled by *ordering* precondition (i) before (ii), so `Sh-conf` is reached only where defined ("well-defined wherever (ii) is reached"). The wp guard, by contrast, is a flat conjunction; under classical (non-short-circuit) `∧` the second conjunct is evaluated for unregistered K, where it has no truth value, so `g_sh` — and hence the derived wp — is not a well-typed predicate there. The wp breaks the very discipline the gate establishes.

**Required**: State that the conjunction is conditional/short-circuit (K registered guards `Sh-conf`), or total-ize `Sh-conf` to `⊥` on unregistered K, so the wp formula is well-defined as written.

## OUT_OF_SCOPE

### Topic 1: The six open questions
**Why out of scope**: Idem semantics at emit, the behavior catalog, default predicates, standard registrations, predicate composition, and extension beyond `F=1`/`N=3` are each genuinely new territory for a successor note, correctly deferred. They are not gaps in this framework, which deliberately fixes only the shape catalog, the gate, and registry permanence. The proofs of P1–P6, the projection bridge, RegisteredAdmissible, P5, and the born-nullified worked illustration are sound and complete as given.

VERDICT: REVISE
