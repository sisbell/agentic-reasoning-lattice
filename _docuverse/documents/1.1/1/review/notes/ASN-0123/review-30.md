# Review of ASN-0123

The mathematics is sound. I checked the load-bearing proofs — SA's antichain argument, VN-B1's K.δ case split (Node/k=2/k=1/k=0 is exhaustive and each closes), V-WF's two-clause composite discharge, V9's structural O5(ii) and the severance derivation, V8's coverer-set equality, the PS ω-totality induction (position-1 preservation under inc), and the two worked instances — and found no correctness gaps. Boundary cases (empty source n=0, repeated addresses |A|<n, owned vs. cross-owner, first vs. later fork) are all handled, and the concrete examples verify V2/V13/V9w/V10 against specific addresses as required.

This note carries `review-mode.anti-bloat`, and the findings are accretion: the same argument restated across sections. Each is a place where the precise reader must skip past prose already read elsewhere.

## REVISE

### Issue 1: The cross-owner "single mint / no intermediate account" rationale is stated three-plus times
**ASN-0123, P-tier comment / V0 / V1 / V9 worked instance**: The argument *"the cross-owner branch is restricted to an account-tier forker so it allocates one document K.δ and mints no intermediate account; a node-tier forker would have to baptize an account first (a second permanent entity), which is why it is excluded"* is developed in full at least three times:
- P-tier comment: "reaching a document from a node prefix would first baptize an intermediate account — a second permanent entity (P1), breaking the single-mint guarantee — so it must establish an account first…"
- V0: "a node-tier forker, lacking a document namespace, would have to baptize an intermediate account first, a second permanent entity, which is precisely why VERSION excludes that path (P-tier)."
- V1: "(V0 — the cross-owner branch's account-tier restriction is what holds the count to one, rather than minting an account alongside the version)."
- V9 worked instance: "the fork is one document K.δ: no intermediate account is baptized, and the registry grows by the single identity v."

**Problem**: The reasoning advances nothing on its second and third appearances. The "Π' = Π, no principal minted" conjunct is similarly stated in the Effect clause, the identity clause, and V9.
**Required**: Prove count-one once (V0 is the natural home, being the FreshUniquePermanentIdentity claim); state the node-tier exclusion rationale once with P-tier (the precondition that excludes it); everywhere else cite, don't re-explain.

### Issue 2: V-WF previews and duplicates V9's structural derivation
**ASN-0123, V-WF and V9 preamble**: V-WF restates the stream form, Document(v), O5(i), and the "which k" gloss that V9's preamble then re-establishes. The "which k is out of scope" point in particular appears twice in near-identical substance:
- V-WF: "Which document number k the frontier carries stays out of scope — the form [pfx(π), 0, k] holds for any k ≥ 1, and the guarantees turn on it, not the value."
- V9: "the placement detail the identity clause left out of scope (which k) is genuinely not needed, since the form [pfx(π), 0, k] holds across the whole stream and the argument turns only on the separator at #pfx(π) + 1."

**Problem**: V-WF's composite-validity argument genuinely consumes only the stream form (to get `Document(v)` for the K.μ⁺ precondition) and freshness. It does not consume O5(i) or O5(ii). The sentence "the maximality (O5(ii)); this is what the remaining steps, the couplings, and V9's severance and ownership claims consume" is therefore imprecise: the remaining steps (K.μ⁺, K.ρ) and the couplings (J0/J1★/J1'★) consume `Document(v)`, freshness, and S3★ — not coverer-maximality, which only V9's claims consume.
**Required**: V-WF should establish what its own argument needs (Document(v), freshness via ChildSpawnFreshness/FrontierEquivalence) and defer the ownership-facing facts to V9 without restating the stream form, O5(i), and "which k." Keep V9's O5(ii) maximality derivation intact — this finding is about removing the *preview/duplication*, not the discharge.

### Issue 3: The "cross-owner derivation is recoverable only via V9w, never the registry" argument is made twice
**ASN-0123, V7 and VD**: Both sections develop the same point — a cross-owner fork yields `v` with `derives(v,d)` yet `¬(d ≼ v)`, so it escapes every address-based descendant scan and is witnessed only by shared content:
- V7: "…a cross-owner fork's derivation is recoverable only through the shared-content witness (V9w), never the registry."
- VD: "Such a derivation is recoverable only through the shared-content witness (V9w), never the registry — the downward limit V7 records."

VD even cross-references V7 ("the downward limit V7 records"), acknowledging the overlap rather than removing it.
**Problem**: Two sections in near-verbatim phrasing carrying the identical conclusion. VD's role is derivation-decidability; V7's is navigation. One should own the argument; the other should cite the conclusion.
**Required**: State the severance-escapes-the-registry/only-content-witnesses argument once (it is most at home in VD, which defines `derives`/`derives_addr` and the registry-decidability fragment) and have V7 cite it.

## OUT_OF_SCOPE

None. The note keeps editing, comparison, creation, link, delivery, and replication operations out, touching them only as frame conditions or consequences (V10/V11 discuss links and edits as *consequences* of the fork, which is appropriate, not as defining those operations).

VERDICT: REVISE
