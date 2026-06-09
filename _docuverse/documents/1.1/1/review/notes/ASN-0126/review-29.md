# Review of ASN-0126

## REVISE

### Issue 1: Retraction re-expression leaves the attribution source undefined and overstates faithfulness

**ASN-0126, Single-source**: "The framework re-expresses retraction in the attributed form `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})` ... Here `r` is an unbound attribution parameter — some attribution-bearing source span ... ASN-0086's `nullified`/`L_R`/active-subset machinery ... carry over unchanged."

**Problem**: The note correctly observes that ASN-0086's literal `F = ∅` Nullify is unexpressible under `→_sh`, but then presents `[r]` as a universal stand-in with `r` left "unbound." ASN-0086's RetractionDirectionality explicitly reserves `F = ∅` for *unattributed* retractions. Under `|F| = 1` there is no `r` to supply for an unattributed retraction, so the operation has no `→_sh` image at all. Calling this a "re-expression" that carries over "unchanged" understates a genuine loss of expressiveness, and "unbound `r`" makes the canonical retraction read as a defined operation when it is actually a schema with a hole.

**Required**: State plainly that unattributed retraction is not framework-expressible (a real restriction inherited from `|F| = 1`), or pin a canonical attribution address for the unattributed case. Do not characterize the re-expression as faithful when one ASN-0086 branch has no image.

### Issue 2: Triple forward-pointer to the same born-nullified witness

**ASN-0126, Single-source / The shape-gated emit (wp) / gate-vs-landing paragraph**: "(the Worked illustration, Step 1, exhibits exactly this)" … "witnessed concretely in the Worked illustration" … "the born-nullified case, witnessed concretely in the Worked illustration."

**Problem**: Three paragraphs in different sections defer to the same downstream location for the same gate-vs-landing example. This is exactly the accreted forward-reference pattern: the reader is told three times that a witness exists below before reaching it.

**Required**: Keep one forward-pointer (at the wp gate-vs-landing distinction, where the separation is first claimed) and delete the other two.

### Issue 3: Duplicated registry-immutability statement

**ASN-0126, Registration entries (final paragraph)**: "Distinct registries yield distinct substrates. There is no notion of altering the registry within a single substrate's evolution. Every registration is therefore an entry present in `Σ_init.registry` ... no entry is added at runtime."

**Problem**: This restates what Registry permanence and P1 already establish ("The registry is fixed when `Σ_init` is defined"; `Σ.registry = Σ_init.registry`). The only new content is the "distinct registries ⇒ distinct substrates" framing; the no-runtime-addition material is verbatim duplication.

**Required**: Reduce to the one new sentence (distinct registries are distinct substrates) and drop the re-derivation of immutability.

### Issue 4: `idem` field and P3 carry no in-note role, contradicting the "and only that" scope claim

**ASN-0126, intro / Registration entries / P3**: "This note supplies that — and only that." … P3 (IdemStability) establishes that `idem(K)` is constant across states.

**Problem**: `idem` participates in no shape check — only `shape(K)` gates `Sh-conf`. Its semantics are wholly deferred (Open question 1). Yet the note stores it, sets it in the Worked illustration, and elevates a stability claim to a numbered property. Pre-provisioning a field in an immutable registry may be defensible, but the note never gives that justification, so a semantics-free field with an established property reads as scope creep against "and only that."

**Required**: Either justify `idem`'s presence explicitly (e.g., the registry is immutable so fields must be provisioned at `Σ_init`) or move the field and P3 to the successor note that supplies idem semantics.

## OUT_OF_SCOPE

### Topic 1: Idempotence semantics at emit
**Why out of scope**: What `idem=⊤` *does* on a duplicate emit is genuinely operational and is already named in Open question 1. The structural decision flagged in Issue 4 is the field's bare presence, not its semantics.

### Topic 2: Multi-source relations and arity beyond 3
**Why out of scope**: The `|F| = 1`, `N = 3` narrowing is the deliberate commitment of this note; loosening it (Open question 6) is new territory, not an error here.

VERDICT: REVISE
