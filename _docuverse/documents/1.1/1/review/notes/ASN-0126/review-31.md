# Review of ASN-0126

## REVISE

### Issue 1: The Binary-vs-unit-depth distinction is restated in three separate sections

**ASN-0126, Single-source / The shape-gated emit / Worked illustration**: The same fact — that Binary registration enforces only `|G| = 1` and therefore does *not* entail ASN-0086's unit-depth retraction discipline — is developed three times:

- Single-source: "Binary registration does **not** by itself entail ASN-0086's UnitDepthRetractionDiscipline: a single G-span of non-unit length … is equally Binary-conformant … `→_sh` does **not** guarantee unit-depth …"
- wp section, *Disciplined-domain simplification (conditional)*: "`→_sh`'s gate enforces only Binary conformance on R … a general `→_sh`-reachable state may carry an `L_R` tuple with a non-unit (but Binary) range to-span …"
- Worked illustration, Step 1: "Binary admits a *non-unit-length* G span, so the gate enforces only Binary, not ASN-0086's unit-depth retraction discipline …"

**Problem**: Two prose paragraphs (Single-source and the wp simplification) say the same thing in different words. The Worked-illustration concrete witness is legitimate — it demonstrates the gap rather than restating it — but it should not also re-narrate the rule. This is the "two paragraphs in the same document say the same thing" pattern, compounded across the retraction discussion.

**Required**: State the Binary ⊋ unit-depth fact once (Single-source is the natural home), and have the wp section and Worked illustration *use* it by reference rather than re-deriving it in prose.

### Issue 2: Attribution rationale is essay content in a structural slot

**ASN-0126, Single-source**: "What is *not* lost is attribution. In Nelson's design the responsible party for a link rides on an always-present channel independent of the from-set — the link's home document, which 'indicates who owns it, and not what it points to.' … We do not introduce a distinct unattributed-retraction operator, because — Nelson is explicit — a link with no responsible party is not a coherent object."

**Problem**: The structural commitment here is narrow: R is registered Binary, and the from-slot is filled by the app's case span or the canonical home-document span `r = (d_retr, δ(1, #d_retr))`. The surrounding paragraph defends *why* this is acceptable (attribution survives, no unattributed operator) rather than advancing the definition. This is design rationale, not a claim that does work — a precise reader must skip past it to reach the actual wrapper definition.

**Required**: Reduce to the operative statement: R is Binary; the from-slot carries the app's source span, or canonically `(d_retr, δ(1, #d_retr))`. Drop the Nelson-design justification or relocate it to a non-structural note.

### Issue 3: Idem-field provisioning is justified by document ordering, with a forward deferral

**ASN-0126, Registration entries**: "The **idem** flag is a registry field fixed at `Σ_init` and frozen by P1, with its operational semantics deferred (Open question 1). It is provisioned here, rather than in the successor note that will read it, because the immutable registry admits no field added at runtime — every field the operational layer will eventually consult must already be present at `Σ_init`."

**Problem**: The second sentence justifies *where* the field is declared ("provisioned here rather than in the successor note … because …") — the "prose justifies document ordering" pattern — and the first sentence defers semantics downstream ("Open question 1"). The structural content is only: idem is a registry field in `{⊤, ⊥}`, fixed at `Σ_init`, frozen by P1. The provisioning-justification adds no guarantee.

**Required**: Keep the field declaration and its `{⊤, ⊥}` / P1-frozen status. Drop the document-ordering justification; the open-question pointer is redundant once semantics are out of scope.

### Issue 4: The Multi table row's prose contradicts its own formal admission of `G = ∅`

**ASN-0126, Three shapes by G span count**: the table gives Multi as "What it expresses: A single source connected to finitely many target spans," while the text immediately states "Multi subsumes both [Unary and Binary]" and Shape-conformance gives Multi as `|F| = 1 ∧ |G| < ∞`, which is satisfied by `G = ∅`.

**Problem**: "connected to … target spans" reads as ≥ 1 target, but a Multi registration admits `|G| = 0` (a bare marker, identical to Unary). The informal gloss misdescribes the boundary case the formal definition permits.

**Required**: Adjust the Multi gloss to admit the zero-target case (e.g., "a single source connected to finitely many — possibly zero — target spans"), or note in the row that Multi subsumes Unary/Binary.

## OUT_OF_SCOPE

### Topic 1: Idem semantics, behavior catalog, default predicates, standard registrations, predicate composition

**Why out of scope**: The ASN explicitly defers these (Open questions 1–5) to a successor operational-semantics note. They are new territory layered on top of this framework, not defects in the registry/gate/shape commitments this note actually makes.

### Topic 2: Extension beyond `|F| = 1` and arity 3

**Why out of scope**: Multi-source relations and richer arity (Open question 6) require loosening the framework's central commitment; that is a parallel or successor framework, not a correction to this one. This note correctly routes such needs to ASN-0086's ungated `→`.

VERDICT: REVISE
