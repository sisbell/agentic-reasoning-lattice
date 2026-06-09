# Review of ASN-0121

## REVISE

### Issue 1: FL-REACH(d) overstates the relation to ASN-0098's discoverable union

**ASN-0121, §"Cross-document reach", consequence (d) and the FL-REACH table row**: heading "*Superset of the per-document discoverable union*"; table: "is a superset of the per-document discoverable union (including orphans)"; prose: "The reach subsumes ASN-0098's per-document discoverable_from".

**Problem**: `discoverable_from(a, d, Σ)` is **request-independent** — by LP12 it holds iff some slot's coverage meets `ran(Σ.M(d))`, with no reference to `q`. Hence `⋃_d {a : discoverable_from(a, d, Σ)}` is the set of *all non-orphan links*, irrespective of the request. `findlinks(q, Σ)` is request-dependent and, for a restrictive `q`, is far smaller. Concretely, for `q = (∗, ∅, ∗, ∗)` (a constrained empty from-slot), FL-EMP gives `findlinks(q, Σ) = ∅`, while the discoverable union may contain many links. So `findlinks(q, Σ) ⊉ ⋃_d discoverable_from(·, d, Σ)` in general — the headed superset claim is false. The careful sentence at the end of the paragraph ("at least as complete as any document-by-document enumeration of the *satisfying* links") states the true claim, which contradicts the heading and table phrasing.

**Required**: Restrict the claim throughout to *satisfying* links: `findlinks(q, Σ) ⊇ ⋃_d { a : sat(a, q, Σ) ∧ discoverable_from(a, d, Σ) }`, with strict superset in the presence of satisfying orphans. Correct the heading and the FL-REACH table row to drop the bare "discoverable union" wording.

### Issue 2: "I-address request" is used as a load-bearing qualifier but never defined

**ASN-0121, FL-STB and FL-REACH**: "for an I-address request `q` …"; FL-STB hypothesis "an I-address request `q`".

**Problem**: The request grammar in FL-DEF defines exactly one kind of request: `q = (H, F, G, Θ)` with each component an `Endset` or `∗`. There is no formal "V-spec request." The "I-address vs V-spec" distinction appears only informally in the editing-stability section, where V-spec phrasing is called "a separable front-end convenience" and left out of scope. As a result, the qualifier "I-address request" in two load-bearing claims has no formal referent, leaving a reader unable to determine whether FL-STB/FL-REACH apply to *all* requests admitted by FL-DEF or to some unstated subset.

**Required**: Either drop the qualifier (since every request in the grammar is over addresses, the claims hold for all `q`), or formalize the I-address/V-spec request distinction so the qualifier carries definite content.

## OUT_OF_SCOPE

### Topic 1: Version-/time-qualified inquiry over retracted links
The first Open Question (a link retracted in the current state but still present in prior versions) is correctly deferred as an open question rather than asserted as a claim; FL-RET appropriately scopes its guarantee to current addressability. No action needed.

### Topic 2: Federated multi-store reach
The federation completeness question (last Open Question) is properly left to a future ASN; the present operation specifies reach over a single `Σ.L`.

VERDICT: REVISE
