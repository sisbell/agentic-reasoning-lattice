# Review of ASN-0086

## REVISE

### Issue 1: L-ContiguousPrefix duplicates the foundation lemma ASN-0093 ChainMembershipForOrigin, and the two are cited interchangeably for the same fact

**ASN-0086, L-ContiguousPrefix** proves: `{a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ}`. ASN-0093's foundation lemma **ChainMembershipForOrigin** already states this verbatim for links: `dom(L) ∩ {ℓ' : origin(ℓ') = d} = {s_1, …, s_{n_d}}` (link contiguous prefix), "at every reachable state."

**Problem**: The note re-proves a foundation result by induction over conformance clauses (b)–(c), never citing ChainMembershipForOrigin — yet the worked example derives L-ContiguousPrefix's own conclusion *from* it: "a contiguous prefix of `A_L(d)`'s chain enumeration (by ASN-0093 ChainMembershipForOrigin) — so L-ContiguousPrefix holds at Σ_2." So on `→*`-reachable states the two coincide and the local lemma adds nothing; the note uses both names for one fact. The only genuine added content is the extension to substrate-conforming-but-not-reachable states (used in R0a Case 2 and R7a), but that relationship is never stated.

**Required**: Either cite ChainMembershipForOrigin directly for the reachable case and state L-ContiguousPrefix solely as its extension to substrate-conforming states (with the extension explicitly justified), or drop the local lemma. Do not cite both for the same derivation step.

### Issue 2: Meta-prose justifying proof ordering / non-circularity in R7a

**ASN-0086, R7a proof**: "We establish this before invoking any conformance-dependent fact at Σ', so that L-ContiguousPrefix — whose own induction `Σ_init = Σ_0, …, Σ_N = Σ` requires every prior step to preserve clauses (a)–(c) — applies at Σ' on the strength of Σ's conformance plus the single preserving step, not merely on the local constraints of the `Σ → Σ'` transition."

**Problem**: This is an essay about the order in which proof steps are performed and why the structure is non-circular — exactly the "prose justifies document ordering / non-circular by Y argument" accretion pattern. It advances no reasoning about the claim; the reader must skip it to follow the discharge.

**Required**: Delete. The substantive content — "Σ' is substrate-conforming (Σ conforming + layer preservation)" — is already stated in the preceding sentence.

### Issue 3: Orientation meta-prose and duplicated alias boilerplate

**ASN-0086, before R6a**: "The active/audit distinction announced above is made possible by R5 (self-referential retraction) and R3 (monotone audit); R6a, R6b, R6c carry its substantive properties."

**ASN-0086, R2 and R4**: both close with the identical sentence "It is a definitional alias, recorded in the Properties table; no separate obligation."

**Problem**: The pre-R6a sentence is pure structural orientation — it names which prior properties enable what follows, advancing no argument. The R2/R4 closing sentence is verbatim boilerplate repeated across two sections, and the Properties table already records the alias status of both (rows R2, R4), so the in-text repetition is triply redundant.

**Required**: Remove the orientation sentence; remove the repeated "recorded in the Properties table; no separate obligation" clause from R2 and R4 (the table already carries it).

### Issue 4: R6b label inconsistency

**ASN-0086, R6b** is headed "(LEMMA, postcondition)" but the Properties table lists it as "DEF-Consequence," and its proof is a one-line unfolding of the `nullified` definition.

**Problem**: A definitional restatement billed as a LEMMA overstates its status; the body and table disagree.

**Required**: Reconcile to "DEF-Consequence" (or equivalent) in both places.

## OUT_OF_SCOPE

### Topic 1: Persistence of nullification across categorical (`↝`) transitions
R6a and R6c are proved only over `→` (and `→*`). Higher-layer `↝` transitions are defined but their effect on `nullified` is not addressed. Since L12/L12a forbid removing or altering existing links, stability should extend to any L-preserving `↝` layer.

**Why out of scope**: The relational layer reduces to `→` (R7a corollary), so the `→`-only scope is internally sufficient for this note. Extending stability to arbitrary categorical transitions is new territory for a later ASN, not a defect here.

META: not applicable — the note specifies abstract state-derived sets (nullified, A_K), operations, and invariants of a relational layer, which is system-guarantee territory rather than implementation mechanics.

VERDICT: REVISE
