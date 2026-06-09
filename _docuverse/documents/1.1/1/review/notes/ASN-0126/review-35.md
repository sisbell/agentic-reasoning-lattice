# Review of ASN-0126

This note carries the `review-mode.anti-bloat` classifier. The structural proofs (P1–P7, the wp derivation, the projection bridge, the born-nullified illustration) are sound and internally consistent — I checked the worked addresses and they hold. The findings below are all accumulated meta-prose around the forward references and axioms, which the classifier asks me to surface.

## REVISE

### Issue 1: Defensive framing prose in Single-source
**ASN-0126, Single-source**: "This is a genuine, narrow loss of expressiveness, **and we state it as such rather than as a faithful carry-over**."
**Problem**: The first clause states an object-level fact (the `F = ∅` Nullify has no `→_sh` image — a real loss). The trailing clause describes the authors' framing choice, not the system. It advances no reasoning.
**Required**: Delete the trailing clause. The loss is established by the sentence before it.

### Issue 2: C0 introduction explains why the axiom is needed, not what it says
**ASN-0126, Registration entries**: "P1 freezes whatever `Σ_init.registry` contains — an ill-formed registry (two `~`-equal keys with differing shapes) exactly as faithfully as a well-formed one — so single-valuedness of `shape(·)` is not a transition property but a separate obligation on `Σ_init` itself, which we raise to an explicit *framework commitment*:"
**Problem**: This is the flagged pattern — prose around an axiom justifying its necessity rather than stating its content. C0's content (the registry is a finite partial function on coverage classes) stands on its own.
**Required**: Cut to a single clause: "C0 constrains `Σ_init.registry` directly, since P1 freezes ill-formed registries as faithfully as well-formed ones." Then state C0.

### Issue 3: Use-site inventory of the projection bridge
**ASN-0126, The shape-gated emit**: "**Two consequences of the bridge are used below.** First, `a_emit` reads only the M and L components... Second, ASN-0086's structural lemmas... are quantified over `→*`-reachable three-component states..."
**Problem**: "are used below" frames the two consequences as a downstream-consumer inventory. State the two consequences as facts; the reader does not need to be told in advance that they will be used.
**Required**: Drop "are used below"; present the two facts directly.

### Issue 4: Disciplined-domain digression justifies a choice it didn't make
**ASN-0126, The shape-gated emit (Disciplined-domain simplification)**: "We condition the simplification on ASN-0086's `UnitDepthRetractionDiscipline`... **not on layer-reachability, which is too strong: layer-reachability requires every `L_R`-growing step to be an `F = ∅` Nullify, which the framework's *attributed* (`|F| = 1`) retraction leaves at its first emit.**"
**Problem**: This is reviser-drift: a paragraph explaining why a *stronger* condition was not used. The conditional simplification's value is the result, not the road not taken. The whole conditional simplification is also tangential — it characterizes a sub-domain the note never reasons over again.
**Required**: Either drop the "not on layer-reachability" justification entirely, or cut the conditional simplification — at a general `→_sh`-reachable state the full inherited wp already stands, which is what the note uses.

### Issue 5: No-residence-check rationale stated three times
**ASN-0126**: The "Sh-conf consults no state-indexed set, so ghost references are admissible" argument appears in full in **Shape-conformance** (with the Nelson/Gregory citations), again in **P5** ("the verdict coincides because `Sh-conf` reads only the intrinsic span counts"), and a third time in the **Worked illustration** ("This is the concrete content of both P5 and the no-residence-check decision").
**Problem**: Two paragraphs saying the same thing in different words is the flagged pattern; here it is three. The worked-illustration restatement is the concrete witness (keep), but the rationale paragraph and P5's restatement overlap heavily.
**Required**: State the rationale once in Shape-conformance; let P5 cite it rather than re-derive it.

### Issue 6: P6 stated in full twice
**ASN-0126, The shape-gated emit** and **Properties established**: P6's full formula plus the closer "P6 lands the tuple in the audit slice `L_K^{Σ'}`, not necessarily the active subset" appears verbatim in both sections.
**Problem**: The Properties-established summary should point to the home derivation, not re-state the entire formula and caveat.
**Required**: In Properties established, give the one-line P6 claim and a pointer; drop the duplicated formula and audit-slice caveat.

## OUT_OF_SCOPE

### Topic 1: idem semantics
The `idem` field is registered and frozen (P3) but does nothing operational in this note. Its emit-time behavior is correctly deferred (Open questions #1). Establishing the immutable field now is appropriate; no error here.

VERDICT: REVISE
