# Review of ASN-0047

## REVISE

### Issue 1: Organizational meta-prose that advances no reasoning
**ASN-0047, multiple sites**: Several sentences exist only to narrate the document's own structure and citation conventions, not to advance any claim:

- *Definition (Provenance relation)*: "That every entry has an actual content-subspace containment witness at its recording boundary — not merely eligibility — is not assumed by the definition alone; it is established as P4a below, by induction over J1'★, P2, and P0." A definition body should fix the type of R; this is a forward inventory of what a downstream theorem proves.
- *Contains(Σ) discussion*: "This is the single site at which the unsatisfiability of the unscoped bound is argued; later sections cite P4★ by name."
- *Destruction confinement*: "This is its canonical statement; later sites refer to P3 by name."
- *K.δ case (ii) discharge*: "We state this guard-vs-conclusion distinction and the GlobalUniqueness-preserves-distinctness fact once, here; each sub-case below carries only its distinguishing content."

**Problem**: Each is meta-prose about where things are said and how they are cited, of the kind the anti-bloat classifier flags. A reader following the argument must skip past them. They will accrete further across cycles.
**Required**: Delete. A named property and its proof location are self-evident; "stated once here / cited by name later" carries no content.

### Issue 2: `m_L(d)` is asserted constant but constancy is not established across an emptied link subspace
**ASN-0047, *Link-subspace V-position depth (operational)***: "The depth is chosen at the first link-subspace insertion into `d` ... and held constant thereafter by S8-depth (uniform depth within a subspace, ASN-0036)."
**Problem**: S8-depth only constrains a *non-empty* subspace. K.μ⁻ admits full link-subspace clearance (`n'_{s_L} = 0`, exercised in the *link allocation* worked example, Step 5 reduces toward this and the operation permits 0). After clearance `V_{s_L}(d) = ∅`, S8-depth is vacuous, and a later K.μ⁺_L re-pins `m_L(d)` to "any value ≥ 2." Nothing forces the re-pinned depth to equal the prior one, so "held constant thereafter" overclaims — `m_L(d)` is not a per-document constant across an empty interval.
**Required**: Either state that `m_L(d)` denotes the depth of the *current* non-empty link subspace (constant only within a contiguous non-empty stretch), or add and prove an invariant that re-pinning must reuse the prior depth. The content subspace carries the identical imprecision via `ValidFirstInsertionPosition`; fix both or state the scope explicitly.

### Issue 3: "Valid composite" is defined twice, the first by forward reference to undefined couplings
**ASN-0047, *Coupling and isolation* vs *Scoped coupling constraints***: The *Definition (Valid composite transition)* in "Coupling and isolation" states clause (2) as "J0 and the content-subspace provenance couplings J1★, J1'★" — but J1★ and J1'★ are not defined until the later "Scoped coupling constraints" section. It then supplies inline "link-free readings" of those not-yet-defined couplings, and closes with "The explicit elementary-transition enumeration for the extended state is given by ValidComposite★." ValidComposite★ then restates the entire definition with the same two clauses.
**Problem**: This is two definitions of the same object, the first forward-referencing properties stated only later and then superseded. It is exactly the "multiple paragraphs deferring to the same downstream location" / "two paragraphs say the same thing" accretion pattern. A reader cannot evaluate clause (2) of the first definition without jumping forward, and gains nothing the second definition does not give.
**Required**: Collapse to one definition. State J0/J1★/J1'★ before the Valid-composite definition that consumes them, or state Valid-composite once (as ValidComposite★) at the point where all three couplings exist. Drop the inline link-free paraphrases, which duplicate the "reduces to the unscoped readings" remarks already attached to P4★ and J1★/J1'★.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
J4 leaves a forked document's link subspace empty and notes a link-inheritance mechanism "would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope."
**Why out of scope**: This is new operative territory (a distinct composite shape), correctly deferred; it is not an error in the present fork definition.

### Topic 2: Interior link withdrawal / tombstoning
D-CTG★/D-MIN★ confine K.μ⁻ to per-subspace suffix removal, so withdrawing an interior link is impossible without a separate mechanism; the ASN catalogues this in Open Questions.
**Why out of scope**: Reconciling Nelson's tombstoning (LM 4/9) with the strengthened contiguity invariants is a future-ASN mechanism, not a defect in this one.

VERDICT: REVISE
