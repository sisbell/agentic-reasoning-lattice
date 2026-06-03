# Review of ASN-0075

## REVISE

### Issue 1: K.δ account-precursor shorthand misapplied to the second document
**ASN-0075, D-DISCR "second bundling" paragraph**: "We therefore write `K.δ(d) ≡ K.δ(A); K.δ(d)` as shorthand, where `A = inc(n_0, 2)` is the account and `d = inc(A, 2)` is the document. The same convention applies to `K.δ(d_A)` and `K.δ(d_B)` in the worked example below."
**Problem**: The convention is correct only for the *first* document allocated from `Σ_0`. The second document is not created via a fresh account precursor:
- In the worked example, line 5 is explicitly `d_B = inc(d_A, 1)` — a K.δ case (ii) `k = 1` version fork requiring only `d_A ∈ E_doc`, no precursor account. So the account-precursor convention does **not** apply to `K.δ(d_B)`, contrary to the quoted sentence.
- In D-DISCR's own histories, the prefix `K.δ(d); K.δ(d')` cannot create `d'` by re-running `K.δ(A); K.δ(d')` with the same `A = inc(n_0, 2)`: that step re-mints an account already in `E`, violating K.δ freshness (`e ∉ E`). `d'` must be a sibling `inc(d, 0)` or version `inc(d, 1)`.

The construction is reachable (siblings/versions need no second account), but the stated shorthand is wrong for the second document and would, taken literally, produce an invalid composite.
**Required**: State the shorthand for the first document only, and create the second document (`d'` / `d_B`) explicitly as a sibling or version fork that needs no account precursor; drop the claim that the account-precursor convention "applies to `K.δ(d_B)`."

### Issue 2: Coupling-discharge explanation restated four-plus times (anti-bloat)
**ASN-0075, D-DISCR Histories 1 and 2, and the Worked Example**: e.g. "(discharging J1★, since K.μ⁺'s frame leaves R unchanged on its own)" and, in the worked example, "(K.μ⁺'s frame leaves R unchanged on its own, so K.ρ is what supplies the provenance update the coupling demands)."
**Problem**: The identical mechanical fact — *K.μ⁺ does not touch R, so the bundled K.ρ is what discharges J1★* — is re-explained at each composite in both histories and again in the worked example. This is accreted verification prose: the reader re-parses the same J0/K.μ⁺/K.ρ discharge pattern repeatedly. The per-composite "K.α produces…, K.μ⁺ places…, K.ρ records…" gloss compounds the repetition.
**Required**: State the bundle-validity pattern (K.α→J0, K.μ⁺ frames R, K.ρ→J1★/J1'★) once, before the histories, then let each history cite it without re-derivation.

### Issue 3: Witness interpretation duplicated (anti-bloat)
**ASN-0075, SHOWDELETIONS definition section vs. end of Worked Example**: The definition section already explains "The presence of the 'witness' document … is what makes the deletion observable as recoverable." The worked example closes with a second pass on the same idea ("`b` is reported as deleted from `d_A` only because `d_B` still holds it … Cross-document SHOWDELETIONS exposes exactly the asymmetric losses").
**Problem**: Two paragraphs in different sections make the same interpretive point about the witness. The example-grounded version is the more useful one.
**Required**: Keep the concrete witness illustration in the worked example; trim the abstract restatement in the definition section to a single sentence (or vice versa), not both at length.

## OUT_OF_SCOPE

### Topic 1: Multi-document (>2) deletion families and third-document witnesses
The Open Questions about families of more than two documents and content "deleted from both compared documents but current in a third" are correctly deferred. The binary asymmetric-pair structure is sufficient for this ASN; the generalization is new territory, not a defect here.

### Topic 2: Restoration / recovery operation
D-ACT establishes the output is consumable by an I-address-based operation, but the actual restoration operation (reintroducing deleted content while preserving origin and link-resolvability) belongs to a future ASN, as the Open Questions note.

VERDICT: REVISE
