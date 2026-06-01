# Review of ASN-0086

## REVISE

### Issue 1: The wp Case 2 self-nullification boundary — the analysis's load-bearing case — is never concretely verified

**ASN-0086, Weakest-Precondition Analysis, Case 2 / Worked Sketch**: "The fresh emission therefore self-nullifies iff `K ~ R ∧ a_emit(Σ, d) ∈ coverage(G)`, and the disjunction is precisely the negation of that conjunction."

**Problem**: The wp's entire substance is the second conjunct, and its load-bearingness rests on the self-nullifying call: an `Emit_K` at `K ~ R` whose to-set covers its own deterministic emission address `a_emit(Σ, d)`. The Worked Sketch is the ASN's only concrete scenario, and it carefully exercises R0, R0a, R1–R3, R5, R6a–c, L‑ContiguousPrefix(-Cor1) — but every retraction it stages (`b₁` targets `a₁`; `b₂` targets `b₁`) targets a *different* address. The one analytically subtle case the wp exists to characterize — an emission landing in `L_R^{Σ'}` with `a ∈ coverage(G)`, collapsing the disjunction to false — is asserted abstractly and never instantiated. Per Standard 6, a key postcondition (here the wp's defining boundary) must be checked against a specific scenario.

**Required**: Add one concrete step (or sub-case) exhibiting `Emit_R(Σ, d, ∅, {(a_emit(Σ, d), δ(1, #a_emit(Σ, d)))})` — computing `a_emit`, showing `a_emit ∈ coverage(G)`, and confirming `(a, F, G) ∉ A_R^{Σ'}` — so the disjunction's false branch is verified, not just described.

### Issue 2: Anti-bloat — repeated "P1 gates only the postcondition, not emission" and a defensive justification of the type-index omission

**ASN-0086, Definition — Nullify / Definition — Unit-depth retraction discipline / WP Case 1**: the fact that P1 gates the postcondition `a ∈ nullified(Σ')` rather than emission is stated in full three times.
- Definition — Nullify: "Thus P1 gates only the postcondition `a ∈ nullified(Σ')`, not emission."
- Unit-depth retraction discipline: "since P1 gates only the postcondition, not emission, an unqualified Nullify call may deposit a unit-depth to-span rooted at a `b ∉ A_rel^Σ`…"
- WP Case 1: re-derives P2's absence from the same fact.

**Problem**: This is the "two paragraphs say the same thing in different words" pattern compounded across three sites. The fact is established once in Definition — Nullify; the later two restate rather than reference it. Additionally, the WP Case 2 Result carries a defensive paragraph — "The index membership `K ∈ T_admissible` is not a wp conjunct: by the Definition of `Emit_K`, K is a type-index that selects *which* operation is named — there is no operation `Emit_∅`…" — which explains *why the omission is justified* rather than advancing the wp; this is the "new prose explaining why rather than what" reviser-drift pattern.

**Required**: State the P1-gating fact once (at Definition — Nullify) and have the discipline definition and WP Case 1 cite it. Drop or compress the `Emit_∅` justification to at most a parenthetical.

## OUT_OF_SCOPE

### Topic 1: R7a's general decomposition beyond the relational layer
**Why out of scope**: R7a proves any substrate-conforming layer's `Σ.L`-effects replay as K-steps, but the only consumer here — the relational layer — reduces to a single `Emit_K` *by its own definition* (`m = 1`), so R7a's general machinery is unused by this note's operation set. Whether other layers need the general lemma is future territory; it is not an error in this ASN.

VERDICT: REVISE
