# Review of ASN-0126

## REVISE

### Issue 1: "R is registered Binary" contradicts Open Question 4 and C0
**ASN-0126, Single-source**: "This shape — `|F| = 1`, `|G| = 1` — is exactly **Binary**, so R is registered Binary."
**Problem**: The note treats R as definitively registered, and the retraction wrapper depends on it (an `Emit_R` that fails gate precondition (i) when R is unregistered is dead). But Open Question 4 lists "the retraction type `R` (Binary)" as merely a *candidate* for pre-registration and explicitly leaves open whether `Σ_init.registry` is "composed entirely of app-declared entries." C0 (RegistryWellFormedness) requires only well-formedness and finiteness — it does **not** commit R to `Σ_init.registry`. So whether retraction is even expressible in a given framework-governed substrate is simultaneously asserted (Single-source) and left open (OQ4). Under P7, an unregistered R means *no* retraction has a `→_sh` image at all.
**Required**: Resolve the tension. Either (a) commit R ∈ `Σ_init.registry` as a C-level requirement (a clause in C0), and drop R from OQ4's candidate list; or (b) restate Single-source as conditional — "R's shape, *when registered*, is Binary" — and make clear retraction availability is app-registry-dependent.

### Issue 2: The `idem` field is dead state threaded through four sites (anti-bloat)
**ASN-0126, Registration entries**: "a reserved **idem** field — value in `{⊤, ⊥}`, fixed at `Σ_init` and frozen by P1; no predicate, gate, or operation in this note reads it."
**Problem**: An immutable registry field that nothing in the note consults is forward-reference accretion to a successor note. It appears in C0, in the Registration-entries list, in P2, and in OQ1 — and P2 carries a sentence whose only content is that the field does nothing: "The same argument applies to the reserved `idem` field — being a registry component, it too is frozen by P1 — though no claim in this note depends on that." That sentence is pure noise (a property load-bearing on nothing), and the apparatus is spread across four locations to support a future note.
**Required**: Confine `idem` to a single forward pointer (the one OQ1 line), or drop it from the registry definition until the successor note that gives it a reader. Remove the P2 idem sentence.

### Issue 3: The gate-enables / landing-may-fail distinction is re-explained redundantly (anti-bloat)
**ASN-0126, The shape-gated emit / P6 / Worked illustration**: The point "a gate-enabled emit may still fail the active-subset postcondition" is stated in the wp paragraph ("a legal `→_sh` emit may still fail to land active when an inherited landing conjunct is false — the born-nullified case"), again immediately after ("Those two are not enablement conditions but *landing* conditions"), again in P6 ("P6 lands the tuple in the *audit slice*… not necessarily the active subset"), and again in P6's Properties-established entry, before finally being *demonstrated* in Worked illustration.
**Problem**: The same idea is paraphrased four times in prose before the one place it earns its keep (the concrete born-nullified witness). This is the "multiple paragraphs say the same thing in different words" pattern.
**Required**: State the gate-vs-landing separation once at its definition, then let the worked example carry the demonstration; cut the repeated prose restatements in P6 and its property entry.

### Issue 4: Infinite-coverage derivation argues against an unproposed design
**ASN-0126, Shape-conformance**: "No non-empty endset therefore has singleton coverage, so a `|coverage(F)| = 1` discipline would admit nothing; span-count, not coverage, is the measure."
**Problem**: A multi-step T0(b)/T1 derivation is spent establishing why an alternative measure (`|coverage|`) that the note never adopts would fail. The legitimate content — that span-count and coverage diverge, witnessed by a unit-depth span — is already made by the preceding sentence's concrete example. The "a `|coverage(F)|=1` discipline would admit nothing" elaboration justifies a rejected non-design.
**Required**: Keep the one-line divergence statement with its unit-depth witness; cut the infinitude derivation and the rejected-alternative justification.

## OUT_OF_SCOPE

### Topic 1: Idem semantics, behavior catalog, default/composed predicates
**Why out of scope**: OQ1–5 correctly defer operational semantics (idem-at-emit, predicate composition, standard registrations) to a successor note. These are new territory, not defects here — modulo Issue 2, which is about *carrying dead apparatus for them in this note*, not about the deferral itself.

### Topic 2: Discontiguous multi-target retraction and multi-source relations
**Why out of scope**: The note explicitly routes multi-source needs to ASN-0086's ungated `→` and defers discontiguous multi-target retraction to the front end (Single-source, OQ6). Leaving these to a different substrate / future note is a scoping decision, not an error.

VERDICT: REVISE
