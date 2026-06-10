# Review of ASN-0126

I worked through the six property proofs, the weakest-precondition derivation, the projection bridge, and the worked illustration line by line. The formal core is sound: the wp guard semantics (`g ∧ wp(S, R)` is correct here, since the active-subset postcondition is unattainable unless the emit fires), the absorption of L3 / `K ∈ T_admissible` / arity-(0) into the gate, Lemma (RegisteredAdmissible), the `π`-bridge induction, and the born-nullified address arithmetic (`a_R = inc(ℓ₂,0) = …2.3 ∉ coverage(G_rng)`, citation born at `g = …2.4 ∈ coverage(G_rng)`) all check out. The C2-vs-C3 distinction — C2 inherited and already live in ASN-0086, C3 newly live because Binary admits non-unit retraction to-spans — is exactly right. I found no correctness gap.

The remaining issues are an accumulated inventory and one misattributed citation.

## REVISE

### Issue 1: "Properties established" is a bare use-site inventory
**ASN-0126, Properties established**: "For a consuming app, the framework's six guarantees and the section where each is stated and proved: — **P1 (RegistryInvariance)** — Registry permanence. — **P2 (ShapeStability)** — Registration entries. …"

**Problem**: This section advances no reasoning. It is a name→section pointer table; every property is already stated and proved, under its own name, in the cited section. It is precisely the use-site-inventory / downstream-consumer-enumeration pattern this note is flagged for — meta-prose that restates nothing. A precise reader skips it to reach the worked illustration.

**Required**: Either make it a genuine one-line-per-guarantee summary that states *what* each property buys the consuming app (e.g., "P1: `Σ.registry` is byte-identical at every `→_sh*`-reachable state"; "P6: every stored link is a registered, shape-conforming standard triple") — which would earn its place for the note's stated audience — or remove it as redundant navigation.

### Issue 2: PrefixSpanCoverage misattributed and mischaracterized in the projection bridge
**ASN-0126, The shape-gated emit (projection bridge)**: "ASN-0086's structural lemmas — R0 (fresh-address emission), `a_emit` totality, L-ContiguousPrefix, PrefixSpanCoverage — are quantified over `→*`-reachable three-component states, so they hold at `π(Σ)` for every state Σ this note reasons about"

**Problem**: PrefixSpanCoverage is an ASN-0043 lemma — the note itself cites it correctly as "PrefixSpanCoverage, ASN-0043" in Single-source, Shape-conformance, and the worked illustration — not an ASN-0086 lemma. More than a citation slip: it is *not* "quantified over `→*`-reachable three-component states." It is an unconditional tumbler fact ("For any tumbler `x` with `#x ≥ 1`, …"). The bridge offers one uniform justification — *quantified over reachable states ⟹ holds at `π(Σ)`* — and that justification does not fit this member of the list. PrefixSpanCoverage holds at `π(Σ)` for a stronger, state-independent reason. The conclusion (the lemma is available) is correct; the stated rationale is wrong for one of the four lemmas it covers.

**Required**: Drop PrefixSpanCoverage from this list (it is used directly as an unconditional ASN-0043 fact and needs no bridge), or split it out with the correct attribution and note that it holds at every tumbler, reachable state or not.

## OUT_OF_SCOPE

### Topic 1: Region-scope Binary retraction forfeits R-Scope's single-tuple guarantee
The note correctly observes (Single-source) that registering R as **Binary** admits non-unit G-spans — `(t, δ(2, #t))` is Binary-conformant — so `→_sh`-reachable states need not be unit-depth-disciplined and ASN-0086's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` no longer holds in general.

**Why out of scope**: This is flagged as a caveat, not asserted away; none of P1–P6 depend on single-tuple scope. A stricter "unit-depth Binary" registration that re-establishes single-tuple scope as a framework guarantee is new territory for a successor note, not an error here.

### Topic 2: The F=1 / N=3 narrowing
The gate fires only on standard triples (arity 3) with `|F| = 1`; higher-arity ASN-0086 links and every empty-from emit have no `→_sh` image by construction.

**Why out of scope**: The narrowing is deliberate and self-consistently handled (precondition (0); the empty-from exclusion in Single-source), and the note's own Open question 6 routes richer arity to a successor. Not a defect in this note.

VERDICT: REVISE
