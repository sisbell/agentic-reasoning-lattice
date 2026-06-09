# Review of ASN-0126

## REVISE

### Issue 1: Canonical from-fill contradicts the note's own F/home separation
**ASN-0126, Single-source**: "the from-set records only what the link derives *from*, never who performs it … for the case ASN-0086 wrote as `F = ∅` — no derivation source — the canonical fill is the home document's own unit-depth span, `r = (d_retr, δ(1, #d_retr))`, which names exactly the owning party ASN-0086's home channel already carries."
**Problem**: The note builds a sharp Nelson-grounded distinction — F is the *derivation* slot, `home` is the *owner/attribution* slot, and the two must not be conflated — then resolves the `|F|=1` retraction problem by filling the derivation slot F with the owner span `[d_retr]`. By its own framing, a retraction does not "derive from" the entire owning-document subtree; the fill injects owner data into a slot the note just argued is *not* for owners, and it duplicates information already carried by the address-derived `home`. The note presents this as natural ("names exactly the owning party") when its own argument condemns it. Either the F/home separation is the wrong lens here, or the canonical fill is semantically wrong; the note cannot have both.
**Required**: Either (a) drop the derivation-vs-owner argument and justify `[d_retr]` purely as a shape-satisfying neutral placeholder whose F-content is conventionally ignored, or (b) keep the separation and acknowledge explicitly that the framework forces non-derivation data into F as a known semantic cost of losing `F = ∅`.

### Issue 2: Defensive justification and repeated deferral around the idem slot
**ASN-0126, Registration entries**: "The **idem** flag carries no in-note role … We provision it here nonetheless, rather than in the successor note that will read it, because the registry is immutable (P1) … This does not breach the note's 'and only that' scope: idem is a reserved slot with a stability guarantee, not an operational commitment; what the slot *means* is exactly what this note leaves open."
**Problem**: This is meta-prose defending a design decision rather than advancing the registry's definition, and idem defers to Open question 1 from at least three sites (Registration entries, the "carries no in-note role" paragraph, and P3). The structural fact needed is one sentence: idem is a registry field with shape, fixed at `Σ_init` and frozen by P1; semantics deferred. The "does not breach scope" self-defense and the repeated forward pointers are accretion.
**Required**: Collapse to a single statement that idem is a frozen, semantically-deferred field; delete the scope-defense and the duplicate deferrals.

### Issue 3: Exhaustiveness claim stated as fact
**ASN-0126, Three shapes by G span count**: "Three shapes capture every usage observed in the lattice."
**Problem**: This is an unverifiable use-site/exhaustiveness assertion of the kind the anti-bloat pass exists to remove. The structural content — three registrable shapes parameterized by `|G|` — stands on its own; the empirical "captures every usage" claim adds nothing checkable and invites the reader to take a survey on faith.
**Required**: State the shapes and their conformance conditions; drop the exhaustiveness claim (or relegate it to a non-normative motivating remark, not a load-bearing sentence).

### Issue 4: Trailing restatement of P3 in the worked illustration
**ASN-0126, Worked illustration**: "By P3, `idem(approved) = ⊤` and `idem(touched) = ⊥` are structural facts equal at every Σ."
**Problem**: The worked illustration exists to check P4, P5, and the gate-vs-landing separation. idem plays no role in any of those scenarios. This sentence re-asserts P3 with no scenario behind it — a checkmark, not a check.
**Required**: Remove it, or replace with an actual P3 exercise (e.g. evaluating `idem(touched)` at two distinct reachable states) if a concrete P3 witness is wanted.

## OUT_OF_SCOPE

### Topic 1: Idem operational semantics, behavior catalog, default predicates, standard registrations, composition, F>1/N>3 extension
**Why out of scope**: These are the note's own Open questions and are correctly deferred. The framework defines state (the registry component), an operation gate (`K.λ_sh`/`→_sh`), and invariants (P1–P6) abstractly; layering operational meaning onto the reserved fields is genuinely successor-note territory, not a defect here.

### Topic 2: Whether `[d_retr]` is the *right* attribution semantics for retraction
**Why out of scope**: The framework's only formal commitment is `|F| = 1`; Sh-conf counts spans and never reads F's content. What F *should mean* for retraction is an operational-semantics question for the successor note. (Issue 1 above is in scope only as an internal-coherence defect in this note's justification, not as a demand that the semantics be settled here.)

VERDICT: REVISE
