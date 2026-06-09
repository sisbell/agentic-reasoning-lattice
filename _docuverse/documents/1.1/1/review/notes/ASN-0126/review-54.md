# Review of ASN-0126

I checked the four core derivations — the wp of the shape-gated emit, the projection bridge, P5 (liveness), and P6 (state-level closure) — against ASN-0043/0086. The mathematics holds: the wp's five conjuncts are correct (C2 ∧ C3 ⟺ `a ∉ nullified(Σ')` reproduces ASN-0086 exactly), RegisteredAdmissible is sound, the projection bridge legitimately transfers the `→*`-reachable lemmas, and P6's induction discharges all three conjuncts (L12 for value, P1 for registration, P4 for verdict). The "born nullified" worked illustration computes correctly down to the addresses. The findings below are structural and one rigor-accounting gap, not correctness errors.

## REVISE

### Issue 1: "Properties established" re-derives P1–P4 that already have a narrative home

**ASN-0126, Properties established**: "P1 (RegistryInvariance). Stated and derived in Registry permanence — by induction on `→_sh*`-derivation length, the registry sitting in the frame of every step kind." / "P2 ... — single-valuedness from C0 ..., state-independence from P1 ..." / "P3 ... — immediate from `K.λ_sh`'s ... preconditions on the only `dom(Σ.L)`-extending step kind."

**Problem**: P1, P2, P3 are each *fully* stated and derived in their narrative section — Registry permanence runs the complete induction for P1 and the registry-function + P1-invariance argument for P2; The shape-gated emit proves P3 outright. The summary then restates each *derivation* (not just its name) in compressed form: the same argument in fewer words. P4 is split rather than recapped: its definedness derivation appears once in Registry permanence ("registration status is itself state-independent by P1 ... defined at Σ exactly when it is defined at Σ' (P4)") and again in full here. So P1–P4 are dual-homed, while P5 here is a bare pointer and P6 lives only here. The section cannot decide whether it is an index or the home of record, and that indecision buys a re-derivation of every property that already had a home.

**Required**: One home per property. Make the P1–P3 and P5 entries pure pointers (drop the method recaps), and give P4 a single home — either fold its full statement into Registry permanence or delete the narrative pre-statement and keep it here.

### Issue 2: the wp equation drops the L3 conjunct it names in the gate, without discharging it

**ASN-0126, The shape-gated emit (weakest precondition)**: the gate is "`g_sh ≡ K registered ∧ Sh-conf(K, F, G)`, together with the inherited L3 and `d ∈ dom(Σ.M)`", yet the derived wp is "`K registered ∧ Sh-conf(K, F, G) ∧ d ∈ dom(Σ.M) ∧ (K ≁ R ∨ ...) ∧ ¬(∃ ...)`" — `d ∈ dom(Σ.M)` survives, L3 does not.

**Problem**: The derivation is scrupulous about every other precondition: (0) is omitted "because the postcondition's arity-3 slice `|Σ.L(a)| = 3` already forces it," and `K ∈ T_admissible` is absorbed into "K registered" via the RegisteredAdmissible lemma. L3 — explicitly named as a gate component — is the one guard that simply vanishes from the wp with no accounting. The omission is *correct* (L3 = arity ≥ 3 ∧ slots ∈ Endset ∧ slot 3 ≠ ∅ is covered by (0), the input typing `F, G ∈ Endset`, and RegisteredAdmissible's `K ≠ ∅`), but a reader tracking where each guard went is left to assemble that. In an argument this meticulous about (0) and `T_admissible`, the silent drop of L3 reads as an oversight.

**Required**: Add the parallel one-liner — L3's three clauses are discharged by (0), the input typing `F, G ∈ Endset`, and RegisteredAdmissible (slot-3 non-emptiness), hence absorbed and absent from the wp — completing the conjunct accounting.

### Issue 3: "load-bearing vs convenience" and cross-substrate name prose is meta-commentary

**ASN-0126, Registration entries**: "This is the load-bearing condition; name-uniqueness is by contrast a convenience for app-side lookup. The substrate makes no commitment about which name strings are admissible — that is the app's namespace. Distinct substrates may carry registries with overlapping names ..."

**Problem**: This ranks which well-formedness clause matters and editorializes on cross-substrate name overlap — commentary *about* the conditions rather than the conditions. The structural facts (coverage-class keys unique ⟹ the registry is a partial function `T_admissible/~ ⇀ (name, shape)`; names unique within one substrate) are stated immediately around it; the prioritization is the part a reader skips to reach C0.

**Required**: Keep the two structural facts. Drop the "load-bearing vs convenience" ranking and the cross-substrate-overlap aside.

## OUT_OF_SCOPE

### Topic 1: Multi-shaped retraction (multi-target Nullify)
The note registers R as Binary and routes retraction through a one-span wrapper. `nullified` already reads `coverage(G')` over a multi-span `G'`, so registering R as Multi would withdraw several targets in one tuple — but the semantics and discipline of that are a relational-layer convention.
**Why out of scope**: which shape an app picks for its retraction type, and the operational guarantees it then gets, is successor-note territory (Open questions 1–2), not a gap in the gate this note defines.

### Topic 2: Arity > 3 and `|F| > 1`
Precondition (0) hard-restricts `→_sh` to arity 3 and every shape fixes `|F| = 1`.
**Why out of scope**: the note flags this itself (Open question 6); the extension path is explicitly deferred.

VERDICT: REVISE
