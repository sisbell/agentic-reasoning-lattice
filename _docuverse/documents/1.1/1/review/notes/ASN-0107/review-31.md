# Review of ASN-0107

## REVISE

### Issue 1: The canonical-prefix retention constraint is justified three times

**ASN-0107, R1 / R2 / R6**: The fact that `K.μ⁻` retains a per-subspace canonical prefix — so an interior consulted position cannot be dropped while a later one is kept, on pain of violating D-MIN★/D-CTG★ — is re-derived in three separate places:

- R1 (P-max): "dropping an interior position while keeping a later one would violate D-MIN★/D-CTG★."
- R2: "to remove the endpoint at a non-maximal position `[S, j]` the operation must set `n'_S < j`, which necessarily also removes every later endpoint … Surgical removal of a single interior endpoint is impossible — only when `a` is itself the arrangement-maximal consulted position (R1's (P-max)) does the contraction touch exactly one endpoint."
- R6: "the canonical prefix set `R := …` — not an arbitrary subset of `dom(Σ.M(d_q))`, since dropping an interior position while keeping a later one would violate D-MIN★/D-CTG★."

**Problem**: The same structural fact, with the same D-MIN★/D-CTG★ justification, appears in all three R-laws. R2 additionally re-explains R1's (P-max) inline. This is the compounding anti-bloat pattern (same content in different sections; reviser drift re-stating an established precondition).

**Required**: State the canonical-prefix/no-interior-drop fact once (it is a property of K.μ⁻ from PerSubspaceContractionScope, ASN-0047) and let R1/R2/R6 cite it without re-deriving. Remove R2's restatement of R1's (P-max) and R6's parenthetical re-justification.

### Issue 2: Q0 restates the preceding paragraph verbatim

**ASN-0107, "State and the Counting Request"**: The prose paragraph "**Request representation invariance.** `sat` reads each request part … So a request re-expressed with the same coverage but a different span decomposition is the same request to the count." is immediately followed by Q0, which states the identical content: "If `Q` and `Q'` have `Qᵢ = Q'ᵢ` as address sets … then `match(Q, Σ) = match(Q', Σ)` … Equal-coverage requests yield equal counts; this is immediate from `sat` …".

**Problem**: Unlike the `sat`/`match`/`num` lead-ins (where prose motivates and the block formalizes complementary content), here the prose paragraph already fully states the claim and its justification, and Q0 repeats both. Two paragraphs saying the same thing in different words.

**Required**: Drop the standalone prose paragraph and keep only Q0, or reduce the prose to a one-line motivation that does not pre-state the claim.

### Issue 3: A1b's name "no incoming links" is weaker than its formal premise

**ASN-0107, A1b (FreshContentNeutrality, discovery)**: "inserting freshly-allocated content carrying *no incoming links* … The neutrality is conditioned on that no-incoming-links premise: no stored link has `a_new ∈ coverage(Σ.L(a).eᵢ)`."

**Problem**: "Incoming links" denotes links whose *to*-endset points at `a_new`, but the formal premise quantifies over *all* slots `i` (from, to, and type). The two are not equivalent: a link referencing `a_new` only in its from-slot is not an "incoming link," yet arranging `a_new` into a queried from-region could newly satisfy that link's slot and raise the discovery count. The informal name undersells the actual (correct, stronger) premise, and a reader relying on the name would draw a false neutrality conclusion.

**Required**: Rename the premise to reflect all-slot referencing (e.g., "content not referenced by any stored link in any slot") so the informal label matches the formal condition.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored multi-document requests
The first open question (request parts anchored to different evolving documents) is correctly deferred — it is new territory, not a gap in this ASN.

VERDICT: REVISE
