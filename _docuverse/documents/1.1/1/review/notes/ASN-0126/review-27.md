# Review of ASN-0126

The structural core is sound: `→_sh` refines ASN-0086's `K.λ` cleanly, the projection `π` legitimately imports the `→*`-domain lemmas, P1–P6 are correctly derived, and the worked illustration's addresses check out (I verified `a_R = ...2.3`, `g = ...2.4 ∈ coverage(G_rng) = [...2.4, ...2.7)`, so the born-nullified landing failure is real and correctly traced to the inherited third wp conjunct). The wp analysis is non-trivial and the gate-vs-landing separation is genuinely illuminating.

The note carries `review-mode.anti-bloat`, and that is where it fails. The same handful of points are restated across sections.

## REVISE

### Issue 1: Multi's triviality stated four times
**ASN-0126, Three shapes / Shape-conformance**: "Multi structurally admits `|G| = 0`..."; "For Multi the conjunct `|G| < ∞` holds for *every* endset... so Multi places no real bound on G's span count — it is the unrestricted shape, constraining only F"; "Multi is the permissive endpoint, not a third disjoint bucket"; "(the permissive endpoint, per Three shapes)".
**Problem**: The fact that `|G| < ∞` is vacuous and Multi bounds only F is asserted at least four separate times across two sections. Once is enough.
**Required**: State it once (in Shape-conformance, where the `Endset = 𝒫_fin(Span)` justification lives) and delete the restatements.

### Issue 2: "commitment, not the link store underneath" duplicated
**ASN-0126, Single-source**: para 1 — "a tuple filed directly into the link store (ASN-0043) may carry `|F| > 1`"; final para — "The link store underneath the substrate (ASN-0043) permits arbitrary higher arity... An app needing multi-source relations drops to a *different* substrate".
**Problem**: The framework-vs-raw-link-store distinction and the "drop to ungated `→` for multi-source" escape are made twice. The second paragraph adds the base-case/induction content, which is substantive; the restated distinction around it is not.
**Required**: Keep the inductive-closure argument in the final paragraph; drop the redundant restatement of the |F|>1 permission already given in para 1.

### Issue 3: Exhaustiveness enumeration of absent variants
**ASN-0126, Single-source**: "Within the gated fragment there is no two-source variant, no zero-source variant, no variadic-F."
**Problem**: `|F| = 1` already says precisely this. Enumerating the three things it excludes is meta-prose padding a commitment that is complete on its own.
**Required**: Delete the sentence.

### Issue 4: Properties-established re-derives instead of indexing
**ASN-0126, The shape-gated emit vs Properties established**: P6's full proof (statement through ∎) appears in "Gate realizability"; the *Derived (The shape-gated emit)* entry under "Properties established" then re-walks the same derivation ("ASN-0086's `Emit_K` operation at the projected `→*`-reachable state `π(Σ)` realizes an ungated `K.λ` step that pins its fresh address..."). The same double-home pattern recurs for P2 (two-halves argument in Registry permanence and again in P2).
**Problem**: A summary index should point to the proof, not reproduce its derivation. The reproduced reasoning will drift out of sync with the source across cycles.
**Required**: Reduce the *Derived* clauses to one-line pointers ("Derived in The shape-gated emit") and let the proof live in one place.

### Issue 5: Triple deferral to the same downstream spot
**ASN-0126, The shape-gated emit (×2) and Gate realizability**: "the born-nullified case, witnessed concretely in the Worked illustration"; "may still fail to land active when an inherited landing conjunct is false — the born-nullified case, witnessed concretely in the Worked illustration"; "the born-nullified gap, witnessed concretely in the Worked illustration."
**Problem**: Three forward pointers to the identical Worked-illustration witness. Forward-reference accretion — exactly the pattern the classifier flags.
**Required**: Make the forward reference once, at the point the born-nullified separation is first introduced.

### Issue 6: Justificatory use-site inventory and minimalism self-description
**ASN-0126, intro / Single-source / conclusion**: "The lattice's actual usage — classifiers, citations, supersession chains, holdings, retractions — is uniformly single-source"; "This note supplies that — and only that"; "The framework here is intentionally minimal: shape vocabulary, conformance check, registry permanence. Everything else layers."
**Problem**: The use-site inventory justifies the `|F|=1` choice by appeal to current lattice usage rather than advancing the commitment; the minimalism framing is stated in both intro and conclusion. Neither carries reasoning the proofs need.
**Required**: Cut the minimalism restatement (keep at most one); the usage inventory can be a single clause, not a roster.

## OUT_OF_SCOPE

### Topic 1: Binary R no longer gate-guarantees single-tuple-scope
The note honestly discloses that registering R as Binary admits a non-unit (but contiguous) range G, so R-Scope's `{t : a ≼ t} ∩ A_rel = {a}` is "preserved by that construction, not by the registration." Whether the substrate should provide a gate-enforced unit-depth retraction shape (rather than leaving it operational) is a real design question — but it belongs to the successor note that layers operational semantics, which Open Question 4 already names. Not an error here.

VERDICT: REVISE
