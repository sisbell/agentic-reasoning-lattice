# Review of ASN-0123

I verified the load-bearing proofs before turning to the anti-bloat pass. The mathematics is sound: VN-B1's induction (only frontier arrivals enter a version namespace), SA's antichain argument from LP-Sub, the V9 severance theorem and its O5(ii)-as-theorem discharge, V-WF's composite-validity discharge, V8's coverer-set equality, V9w's boundary use of P4★, V10's LP12 instantiation, and both worked instances all check out. No correctness or completeness gap surfaced — empty source (n=0), repeated I-addresses (|A|<n), links-only source, iterated forks, and cross-owner forks are each handled. The findings below are residual duplication, which is what this note's classifier targets.

## REVISE

### Issue 1: Redundant O5 recapitulation immediately after the V9 maximality proof

**ASN-0123, V9 preamble**: The three bullets establish `Document(v)`, `O5(i)`, and `O5(ii)` for `v` — and the `O5(ii)` maximality bullet (Z-mono on the prefix `[pfx(π), 0]`) is load-bearing and must stay. The sentence that follows them reads:

> "Every member of `S(pfx(π), 2)` has the form `[pfx(π), 0, k]`, which yields `pfx(π) ≼ v` (O5(i)) and, via Z-mono on the length-`(#pfx(π) + 1)` prefix `[pfx(π), 0]`, the maximality O5(ii); the within-stream index `k` plays no role."

**Problem**: This sentence restates four things already proved in the lines directly above it: the `[pfx(π), 0, k]` form (given verbatim in the preamble — "every member of the stream — `v` among them — has the form `v = [pfx(π)₁, …, 0, k]`"), `O5(i)` (the second bullet), the `O5(ii)`-via-Z-mono mechanism (the third bullet's actual proof), and "`k` plays no role" (already stated as "the within-stream index is immaterial"). The generalization to "every member of `S(pfx(π), 2)`" is not consumed downstream — severance (a) and ownership (b) use O5(i)/O5(ii) for `v` alone. A precise reader skips this sentence entirely to reach the "(a) Severance" proof.

**Required**: Delete the recapitulation sentence. Keep the three bullets — including the protected O5(ii) maximality proof — untouched.

### Issue 2: Foreign-link-exclusion argument carried in full in both G2 and V2b

**ASN-0123, G2 closing paragraph and V2b**: The same argument appears twice. G2:

> "CL-OWN requires `origin(M(d)(x)) = d` at every link-subspace position of every document, and every link arranged by `d_src` has `origin = d_src ≠ v`; correspondingly K.μ⁺_L's precondition `origin(ℓ) = d` admits only a document's own links into its link subspace. No reachable transition can seat a foreign link in `v`'s link subspace. … content anchoring is the only channel by which connectivity can cross a fork"

V2b:

> "`(A d, x : … subspace(x) = s_L : origin(M(d)(x)) = d)` (CL-OWN), and the sole link-subspace extension transition carries precondition `origin(ℓ) = d` (K.μ⁺_L); every link the source arranges has `origin = d_src ≠ v`, so the fork cannot carry the source's link arrangement … Cross-fork connectivity therefore has exactly one channel, content anchoring"

**Problem**: The CL-OWN + K.μ⁺_L-precondition + `origin = d_src ≠ v` chain and the identical "content anchoring is the only channel" conclusion are developed in full in both places. One is a redundant restatement of the other in different words; the proof in V2b reproduces the derivation rather than resting on it (the note already forward-references freely, e.g. "n = 0 below").

**Required**: Carry the argument once. The natural home is V2b (the formal claim, ForeignLinkExclusion); have G2 assert the conclusion and defer the proof to V2b, or vice versa — but not both in full.

## OUT_OF_SCOPE

None. The scope-delimited topics (document-from-scratch, comparison, content/link operations, delivery, replication) are respected; the cross-owner branch reuses the document-K.δ mechanism as a sub-step without specifying CREATENEWDOCUMENT, and the open questions defer future territory appropriately.

VERDICT: REVISE
