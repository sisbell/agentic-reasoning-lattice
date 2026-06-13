# ASN-0123 Claim Statements

*Source: ASN-0123-createnewversion-operation.md (revised 2026-06-12) — Extracted: 2026-06-13*

## Definition — VersionNamespace

The version namespace of a document `d` is the sibling stream at depth 1:

`S(d, 1) = c₁, c₂, c₃, …` where `c₁ = inc(d, 1)` and `cₙ₊₁ = inc(cₙ, 0)`,

whose n-th member is, by the SiblingStream postcondition at depth 1 (which contributes `1 − 1 = 0` separator zeros), the tumbler `cₙ = [d₁, …, d_{#d}, n]` — the source's components with the single component `n` appended. We write `d·k` for the length-`(#d + 1)` extension of `d` by final component `k`, so `cₖ = d·k`.

## Definition — DerivesAddr

`derives_addr(v, d) := derives(v, d) ∧ d ≼ v`

---

## PS — PrincipalStructure (ASSUMPTION, assumption)

Every reachable docuverse state carries an ASN-0042-conforming principal structure:

> (i) *Dynamics* — `Π` and `pfx` satisfy O1a (account-tier prefixes) and O1b (prefix injectivity), and evolve per O12, O13, O15 across every atomic transition: principals persist, no prefix ever changes, and at most one principal enters per transition, by delegation.
> (ii) *Authority* — `allocated_by` attaches to K.δ: every entity-creating step is performed by some existing principal (O16) inside its own domain (O5).
> (iii) *Bootstrap coverage* — some `π₀ ∈ Π₀` covers the bootstrap node: `pfx(π₀) ≼ n₀`.
> (iv) *Incumbency* — every principal occupies a baptized entity: `pfx(π) ∈ E` for every `π ∈ Π`. An ASN-0042-conforming structure satisfies PrefixBaptismCoupling (`pfx(π) ∈ Σ.B`); since `pfx(π)` is account-tier (`zeros(pfx(π)) ≤ 1`, O1a) it is entity-level, and the entity-level `B`=`E` identification places it in `E`.

Consequence: **`ω : E → Π` is total and single-valued at every reachable state**.

---

## trunc — SingleComponentTruncation (DEF, function)

For `t ∈ T` with `#t ≥ 2`, `trunc(t)` is the tumbler of length `#t − 1` agreeing with `t` everywhere it is defined:

> `#trunc(t) = #t − 1  ∧  (A i : 1 ≤ i ≤ #t − 1 : trunc(t)ᵢ = tᵢ)`

Membership `trunc(t) ∈ T` is immediate from T0 — a finite sequence over ℕ of length ≥ 1, since `#t ≥ 2`. For every member of a version stream: `v ∈ S(d, 1) ⟹ trunc(v) = d`, because `v = d·k` agrees with `d` on positions `1 … #d` and has length `#d + 1`.

---

## Z-mono — ZeroCountMonotonicity (LEMMA, lemma)

Prefixing cannot lose zeros:

> `(A p, q ∈ T : p ≼ q : zeros(p) ≤ zeros(q))`

since `q` agrees with `p` on positions `1 … #p` — so every zero of `p` is a zero of `q` — and `q`'s further positions can only contribute more.

---

## SA — StoredAddressAntichain (INV, predicate)

No stored address extends another: at every reachable state `dom(C) ∪ dom(L)` is an antichain under `≼`, so for every stored `a`

> `{t ∈ T : a ≼ t} ∩ (dom(C) ∪ dom(L)) = {a}`.

---

## nextv — VersionFrontier (DEF, function)

The next unallocated member of `d`'s version namespace, given the registry:

> `nextv(E, d) = next(E, d, 1)`

with `next` as in ASN-0040: `inc(d, 1)` when `E ∩ S(d, 1) = ∅`, else `inc(max(E ∩ S(d, 1)), 0)`.

Equivalently:

> `nextv(E, d) = c_{hwm(E, d, 1) + 1}` — the gap-free successor.

Well-definedness: `E` is finite at every reachable state; and `(d, 1)` is a B6-valid namespace — `d` is T4-valid with `zeros(d) = 2` (M0), depth `1 ∈ {1, 2}`, and `zeros(d) + (1 − 1) = 2 ≤ 3`.

---

## VN-B1 — VersionNamespaceContiguity (INV, predicate)

At every reachable state, for every T4-valid `d` with `zeros(d) = 2`:

> `E ∩ S(d, 1) = {c₁, …, c_m}` for some `m ≥ 0` — the realized children are a contiguous prefix of the stream.

K.δ's freshness and operand constraints admit only frontier arrivals into a version namespace.

---

## VERSION — ForkVersion (SPEC, operation)

```
VERSION(π, d_src)

Preconditions
  P-src    d_src ∈ E_doc                (the source is an allocated document)
  P-prin   π ∈ Π                        (the forking principal)
  P-bdy    Σ is a composite boundary
  P-tier   ω(d_src) = π  ∨  zeros(pfx(π)) = 1

Abbreviations (evaluated at the initial state Σ)
  n  :=  |V_{s_C}(d_src)|
  A  :=  {M(d_src)(u) : u ∈ V_{s_C}(d_src)}          (the carried I-addresses)

Identity clause
  if  ω(d_src) = π  →  v := nextv(E, d_src)                  (fork in place)
  []  ω(d_src) ≠ π  →  v := the fresh document identity π allocates in its own
                         document-creation namespace as a single K.δ: allocated_by(π, v);
                         yields Document(v), v ∉ E, pfx(π) ≼ v (O5(i)), and
                         (A π'' ∈ Π : pfx(π'') ≼ v ⟹ #pfx(π'') ≤ #pfx(π)) (O5(ii))
  fi

Effect (net, from Σ to Σ')
  E'      =  E ∪ {v}
  M'(v)   =  M(d_src)|_{V_{s_C}(d_src)}              (the snapshot; ∅ when n = 0)
  M'(d)   =  M(d)         for every d ∈ E_doc        (in particular d = d_src)
  C'      =  C
  L'      =  L
  R'      =  R ∪ {(a, v) : a ∈ A}
  Π'      =  Π

Result
  v — the operation's value is the fresh identity; in the owned case: trunc(v) = d_src
```

---

## V-WF — WellFormedness (LEMMA, lemma)

VERSION is realizable as a valid composite at every reachable `Σ` with `d_src ∈ E_doc` — the owned branch at any forker tier, the cross-owner branch presupposing an account-tier forker (`zeros(pfx(π)) = 1`, so exactly one identity is minted); invoked at a composite boundary (P-bdy), its post-state is the terminal boundary of that composite, satisfying both the per-state invariants (ExtendedReachableStateInvariants) and the composite-boundary properties P4★ ∧ P4a ∧ P7a.

---

## derives — Derives (DEF, predicate)

`derives(v, d)` holds iff some `VERSION(·, d)` invocation produced `v`.

---

## VD — VersionNamespaceDiscipline (AXIOM, predicate)

Every allocation into a version namespace is a fork of its parent:

> `(A d ∈ E_doc, w ∈ E ∩ S(d, 1) :: w entered E as the output of a VERSION(·, d) invocation)`

Under VD, the registry decides address-encoded derivation:

> For `v ∈ S(d, 1)`: `derives(v, d) ⟺ v ∈ E`

Equivalently:

> `derives_addr(v, d) ⟺ v ∈ E ∩ S(d, 1)`

The unrestricted forward direction `derives(v, d) ⟹ v ∈ S(d, 1)` fails for cross-owner forks (severance, V9).

---

## V0 — FreshUniquePermanentIdentity (LEMMA, lemma)

Exactly one identity is allocated, it collides with nothing, and it never goes away:

> `E' = E ∪ {v}` with `v ∉ E`; `v` is distinct from the output of every other allocation event; and `(A Σ'' : Σ' →* Σ'' : v ∈ Σ''.E)`.

---

## V1 — ZeroContentFootprint (LEMMA, lemma)

> `C' = C  ∧  L' = L`

and consequently no allocated substance scales with the source: `ΔE = {v}` mints exactly one identity, and `C' = C ∧ L' = L` allocates zero content and link addresses, whatever the source's extent. `ΔR = A × {v}` with `|A| ≤ n`.

---

## V2 — ArrangementTranscription (LEMMA, lemma)

> `M'(v) = M(d_src)|_{V_{s_C}(d_src)}`, so `dom(M'(v)) = V_{s_C}(d_src)` and `ran(M'(v)) = A ⊆ dom(C)`.

---

## V2b — ForeignLinkExclusion (INV, predicate)

No reachable transition seats a link of foreign origin in any document's link subspace:

> `(A d, x : x ∈ dom(M(d)) ∧ subspace(x) = s_L : origin(M(d)(x)) = d)` (CL-OWN), and the sole link-subspace extension transition carries precondition `origin(ℓ) = d` (K.μ⁺_L);

every link the source arranges has `origin = d_src ≠ v`, so the fork cannot carry the source's link arrangement — not as a choice it declines but as a transition that does not exist.

---

## V3 — SourceFrame (LEMMA, lemma)

Every `d_src`-indexed observable is unchanged from `Σ` to `Σ'`:

> `d_src ∈ E'`;  `M'(d_src) = M(d_src)`;  `C' = C` and `L' = L` (stores and their values untouched);  `{(a, d) ∈ R' : d = d_src} = {(a, d) ∈ R : d = d_src}` — the fork is strictly additive and writes no forward pointer.

---

## V4 — AncestryPrefix (LEMMA, lemma)

For the owned fork, the version's identity bears to the source's identity the relation daughter by single-component extension, and the relation is total:

> `v ∈ S(d_src, 1)`, i.e. `v = d_src·k` for some `k ≥ 1`; hence
> (a) `d_src ≺ v` and `trunc(v) = d_src`;
> (b) `#v = #d_src + 1` and `zeros(v) = zeros(d_src) = 2`, so `Document(v)` with T4-validity;
> (c) `N(v) = N(d_src)`, `U(v) = U(d_src)`, and `D(v) = D(d_src)` extended by the final component `k`;
> (d) `acct(v) = acct(d_src)`.

---

## V5 — ChronologicalRank (LEMMA, lemma)

> (a) the k-th allocation into `S(d_src, 1)` (in commit order) receives the k-th stream member `d_src·k`; reading rank as fork order is exact precisely under VD — when forks of `d_src` are the namespace's only allocations;
> (b) the allocator is registry-pure: `(A Σ₁, Σ₂ : Σ₁.E ∩ S(d, 1) = Σ₂.E ∩ S(d, 1) : nextv(Σ₁.E, d) = nextv(Σ₂.E, d))` — `C`, `M`, `L`, `R` are not arguments;
> (c) ranks are never reused: identities never leave `E` (P1), so a rank once taken is taken forever.

---

## V6 — IterativeClosure (LEMMA, lemma)

`Document(v)` holds and `ω'(v)` is the forker (V8, V9), so `VERSION(·, v)` is enabled at `Σ'` with no further setup. For a chain `w₀ = d`, `wⱼ₊₁ ∈ S(wⱼ, 1)`:

> `#wⱼ = #d + j`, `zeros(wⱼ) = 2` at every depth, and `(A i : 0 ≤ i ≤ j : trunc^i(wⱼ) = w_{j−i})` — the full derivation path is read by iterated truncation.

---

## V7 — NavigationAsymmetry (LEMMA, lemma)

> *Upward* — from any version, every ancestor is computed by iterated truncation: a pure function of the identity, consulting no state (the same intrinsic-computation discipline as T2).
> *Downward* — the owned (address-discoverable) versions of `d` are the registry query `E ∩ S(d, 1) = {c₁, …, c_{hwm}}`, gap-free (VN-B1), so enumeration terminates at the first absentee; the full owned-descendant set `{e ∈ E : d ≺ e}` is T1-contiguous (T5), a single range scan of the ordered registry — and every address-encoded descendant of `d` is owned by `ω(d)`, since no account-tier prefix (`zeros ≤ 1`, O1a) can cover past `d` (`zeros = 2`, Z-mono). Cross-owner versions are not recovered here: `derives(v, d)` can hold with `¬(d ≼ v)` (severance, V9), placing `v` outside both `S(d, 1)` and `{e : d ≺ e}`.
> *Never* — a read of the source's own components: by V3 no `d_src`-indexed state mentions `v`.

---

## V8 — OwnershipInheritance (LEMMA, lemma)

When the forker owns the source, the version's owner is the source's owner — inherited structurally, with nothing allocated to record it:

> `ω(d_src) = π  ⟹  ω'(v) = π`, with `Π' = Π` and `acct(v) = acct(d_src)`.

Via `coverers(x) = {π'' ∈ Π : pfx(π'') ≼ x}`: `coverers(v) = coverers(d_src)`, because
- (⊇) `pfx(π'') ≼ d_src ≺ v` chains to `pfx(π'') ≼ v`
- (⊆) Suppose `pfx(π'') ≼ v`; both `pfx(π'')` and `d_src` are prefixes of `v`, hence comparable; the case `d_src ≼ pfx(π'')` gives `zeros(pfx(π'')) ≥ zeros(d_src) = 2` by Z-mono, contradicting O1a's account-tier bound; so `pfx(π'') ≼ d_src`

The coverer sets coincide; `ω` selects the unique maximal-length coverer (O2), `Π` is unchanged, so `ω'(v) = ω(d_src)`.

---

## V9 — CrossOwnerFork (LEMMA, lemma)

Let `π_o := ω(d_src) ≠ π`. Given the account-tier restriction `zeros(pfx(π)) = 1`, `allocated_by(π, v)`, `pfx(π) ≼ v` (O5(i)), and `(A π'' ∈ Π : pfx(π'') ≼ v ⟹ #pfx(π'') ≤ #pfx(π))` (O5(ii)):

> (a) **Severance** — `¬(d_src ≼ v)`: the new identity cannot lie in the source's subtree;
> (b) **Ownership** — `ω'(v) = π`: the forker owns the fork outright;
> (c) **Editability** — the forker's right to edit `v` follows from (b) and from nothing about the source's permissions, which the operation never consulted (P-src is the entire source-side precondition).

*Proof of (a).* Suppose `d_src ≼ v`. Then `pfx(π_o) ≼ d_src ≼ v`, so O5(ii) forces `#pfx(π_o) ≤ #pfx(π)`. Both `pfx(π_o)` and `pfx(π)` are prefixes of `v`, hence comparable; with the length bound, `pfx(π_o) ≼ pfx(π)`. Equality gives `π_o = π` by O1b — excluded — so `pfx(π_o) ≺ pfx(π)`. Now compare `pfx(π)` with `d_src`: both are prefixes of `v`, hence comparable. `d_src ≼ pfx(π)` gives `zeros(pfx(π)) ≥ 2` by Z-mono, contradicting O1a. So `pfx(π) ≼ d_src` — but then `π` covers `d_src` with a strictly longer prefix than `π_o`'s, contradicting `ω(d_src) = π_o`. Both branches close; `¬(d_src ≼ v)`.

*Proof of (b).* `pfx(π) ≼ v` by O5(i); any coverer of `v` longer than `pfx(π)` would violate O5(ii); `Π' = Π`, so `π` is the maximal coverer and `ω'(v) = π`.

---

## V9w — SharedContentWitness (LEMMA, lemma)

> `(A a ∈ A :: (a, d_src) ∈ R'  ∧  (a, v) ∈ R')`, and both rows persist in every successor state (P2).

The first conjunct holds via P4★ at the composite boundary (P-bdy): each `a ∈ A` is `M(d_src)(u)` for some `u ∈ V_{s_C}(d_src)`, so `(a, d_src) ∈ Contains_C(Σ) ⊆ R ⊆ R'`. The second is V13. The witness is identity-based — it survives arbitrary later editing of either arrangement, since `R` never shrinks — and symmetric: it does not orient derivation.

---

## V10 — LinkCarryThrough (LEMMA, lemma)

> `(A a ∈ dom(Σ'.L), i : 1 ≤ i ≤ |Σ'.L(a)| : project(a, i, v, Σ') ≠ ∅  ⟺  coverage(Σ.L(a).eᵢ) ∩ A ≠ ∅)`

`L' = L` and each link's slot coverage is transition-invariant (LP2, LP3), so the right-hand side may be read at `Σ`. `ran(Σ'.M(v)) = A` (V2). LP12's per-slot biconditional — `project(a, i, d, Σ') ≠ ∅ ⟺ coverage ∩ ran(Σ'.M(d)) ≠ ∅` — instantiated at `d = v` gives the claim.

---

## V11 — EditIndependence (LEMMA, lemma)

> (a) *Immediacy* — `v ∈ E'_doc` with `ω'(v)` the forker: the version stands under the same enabling conditions as any allocated document, with nothing `v`-specific outstanding. K.μ⁺ is enabled at `v` whenever `dom(C) ≠ ∅`; K.μ⁻ whenever its arrangement is non-empty (`n ≥ 1`); K.μ~ whenever its content image takes two distinct values.
> (b) *Isolation, both directions* — every arrangement transition names one document `d` and frames all others: `(A d' : d' ≠ d : M''(d') = M'(d'))` (the K.μ family). By induction over any subsequent transition sequence, edits scoped to `v` leave `M(d_src)` pointwise fixed, and edits scoped to `d_src` leave `M(v)` pointwise fixed.
> (c) *The shared substance is beyond reach from either side* — `(A a ∈ dom(C) :: C''(a) = C'(a))` (P0).

---

## V12 — IdentityContentBoundary (LEMMA, lemma)

At `Σ'`:

> `d_src ≠ v` (V0), yet `M'(v) = M'(d_src)|_{V_{s_C}(d_src)}` (V2 with V3) — two identities, one body of content.

The map from identity to content-subspace arrangement is therefore non-injective by construction: identity is not recoverable from content, however total the content.

---

## V13 — ProvenanceCoupling (LEMMA, lemma)

> `R' = R ∪ {(a, v) : a ∈ A}` — J1★ forces every pair in (each carried address is range-new in `v`'s content subspace), and J1'★ forbids any pair beyond.

Each row is permanent (P2).
