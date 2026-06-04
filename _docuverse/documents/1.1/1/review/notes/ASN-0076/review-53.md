# Review of ASN-0076

## REVISE

### Issue 1: Introduction restates its thesis across separate paragraphs
**ASN-0076, Introduction**: Paragraph beginning "We will resolve the tension..." asserts "the existing primitives are sufficient to express it as a composite. No new primitive is required, no existing invariant is weakened, and every guarantee the original link enjoyed continues to hold unaffected." The later paragraph "We formalize this composite as EDITLINK..." again asserts the composite "realizes every property a user would expect of an 'edit' ... while leaving the original link entirely undisturbed."
**Problem**: The "original undisturbed / guarantees preserved" thesis is stated twice in different words (anti-bloat pattern: two paragraphs saying the same thing). The reader following the formal claims must skip past the repetition.
**Required**: Collapse to a single thesis statement; the proven content lives in E1/E8/E0's invariant-inheritance paragraph.

### Issue 2: E6 proof carries a forward deferral that does not advance the claim
**ASN-0076, E6 "Application-layer note"**: "selection and authorization of `d_new` — including whether a party other than `home(ℓ_old)`'s owner may publish a supersession against `ℓ_old` — is an application-layer concern deferred to a future ASN on authorization and capabilities."
**Problem**: The substantive half ("The link model has no executor field and so cannot distinguish who fires K.λ") is a legitimate statement of what the model does not do. The trailing deferral-to-future-ASN clause is meta-prose — it neither advances E6 nor belongs in a proof slot; this is the deferral-accretion pattern the note is classified against. The same scope point is already carried by the Open Questions section.
**Required**: Keep the "no executor field" observation; drop the "deferred to a future ASN on authorization and capabilities" deferral (or fold it into Open Questions, where authorization scope already lives).

## OUT_OF_SCOPE

### Topic 1: Authorization / who may publish a supersession
**Why out of scope**: This is correctly identified by E6 and the Open Questions as belonging to a future ASN on authorization and capabilities; the link model has no executor field, so it is genuinely new territory, not a defect here.

### Topic 2: Supersession-chain traversal, cycles, "current successor" computation
**Why out of scope**: The Open Questions list these as future work; EDITLINK's job is to establish the composite and its per-edit invariants, which it does. Chain-level guarantees are a separate ASN.

VERDICT: REVISE
