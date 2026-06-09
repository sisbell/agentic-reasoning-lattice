# Review of ASN-0117

## REVISE

### Issue 1: Cross-document isolation (P5) is never exercised concretely
**ASN-0117, "A worked deletion"**: every scenario — the `q_3`/`c=2` deletion, the multi-position suffix shift, the two boundary cases, and the within-document sharing case — is single-document.

**Problem**: The worked examples verify P0, P1, P2, P3, P4, and the wp, but **P5 (DocumentIsolation)** — the operation's signature guarantee and the formal content of Nelson's "may remain included in other versions" — is never checked against a concrete scenario. The entire transclusion motivation rests on P5, yet no worked case introduces a second document `d'` that arranges an address in `A_del`. A key postcondition asserted but not concretely verified is a depth gap under the review standards.

**Required**: Add a worked scenario with a transcluding `d'` whose arrangement maps some `a_k ∈ A_del`, showing `M'(d') = M(d')` (DEL-FDOC) and that `d'` still resolves the deleted content via `C' = C` (P0) — i.e., the deletion in `d` is invisible to `d'`.

### Issue 2: DELETE is not pinned to a foundation transition kind, and the entity/provenance frame is unstated
**ASN-0117, "What is removed…" and "The document remains one coherent sequence"**: the state is taken as "a content store `Σ.C`… and a per-document arrangement `Σ.M(d)`" (plus link store), and referential integrity is read "at the two-subspace level as S3★ (GeneralizedReferentialIntegrity, ASN-0047)"; the discoverability argument invokes LP12/LP16/LP17/LP18 (ASN-0098).

**Problem**: S3★ and the LP-discoverability family are properties of the extended-state model `Σ = (C, L, E, M, R)`, and the LP lemmas are quantified over *reachable states / valid transitions* of that model. The ASN never identifies DELETE as that model's K.μ⁻ (ArrangementContraction) transition, never states the entity/provenance frames (`E' = E`, `R' = R`) that K.μ⁻ requires, and never confirms the provenance invariants that coexist with S3★ — P4★ (`Contains_C ⊆ R`) and P7a (every content address has a provenance record) — survive DELETE. Without that identification, the appeal to results proven over the fuller model rests on an unstated bridge. (The invariants are in fact preserved — `Contains_C` shrinks and `dom(C')=dom(C)`, so both hold with `R'=R` — which is exactly why it should be a one-line statement rather than a silent omission.)

**Required**: Either (a) identify DELETE as the K.μ⁻ transition of the foundation model and add the `E' = E`, `R' = R` frame clauses plus a one-line note that P4★/P7a are preserved; or (b) stay strictly in `(C, M, L)` and derive the referential-integrity property from S3 (ASN-0036) and the ASN's own link reasoning rather than borrowing the extended-state name S3★.

## OUT_OF_SCOPE

### Topic 1: General-depth (`m > 2`) text deletion
The operation restricts to `m = #p = 2`, inherited from the depth-2 foundation contraction (ASN-0082). Lifting DELETE to arbitrary text-subspace depth requires extending that foundation first; it is future territory, not an error here.

VERDICT: REVISE
