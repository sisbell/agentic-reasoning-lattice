# Review of ASN-0047

## REVISE

### Issue 1: The "link-subspace mappings don't participate in provenance" fact is restated in five places

**ASN-0047, P4★ / P4a / J1'★ / J1★-derivation / J4**: The same reasoning — *link-subspace V-positions target `dom(L)`, which is disjoint from `dom(C)` (L14), so they neither trigger nor witness provenance* — appears, reworded, at least five times:

- P4★ def: "the link-subspace pairs that an unscoped `Contains(Σ) ⊆ R` would demand are exactly the ones P7 forbids, since S3★/L14 make `dom(L) ∩ dom(C) = ∅` structural."
- P4a def: "the content-subspace qualification is essential: J1'★ scopes provenance recording to content-subspace range changes (link-subspace mappings target `dom(L)`, which is disjoint from `dom(C)` by L14...)."
- J1'★ (trailing paragraph): "Link-subspace extensions (K.μ⁺_L) do not trigger provenance recording... so ℓ is not in the content-subspace range of M'(d), and J1★ is vacuous."
- J1★ derivation: "K.μ⁺_L extends only the link subspace... contributing nothing to the difference — the wp computation is vacuous for K.μ⁺_L on P4★."
- J4: "Link-subspace mappings from the source document are not copied..."

**Problem**: This is the "two paragraphs say the same thing in different words" accretion pattern, multiplied across sections. Each restatement re-derives the `s_L ≠ s_C ⟹ dom(L)∩dom(C)=∅ ⟹ no provenance` chain from scratch, forcing the reader to re-confirm it is the same fact each time. It is the kind of meta-prose the precise reader must skip past.

**Required**: State the fact once (the natural home is the J1★/J1'★ definition block, since the scoping is the substantive content there) as a named consequence, and replace the other four occurrences with a bare citation to it.

### Issue 2: The non-trivial `m ≥ 3` branch of D-SEQ★ is never exercised by a concrete example

**ASN-0047, D-SEQ★ derivation (Case m ≥ 3) and the worked examples**: The `m ≥ 3` case is the hard half of the D-SEQ★ derivation — Step 1 forces inner positions to 1 via an infinite-family contradiction against S8-fin (the `u_M` construction). Every worked example, however, fixes `m_{s_C} = m_{s_L} = 2` and explicitly invokes "the practical case driving every text-subspace worked example," so the `m ≥ 3` argument is verified only abstractly.

**Problem**: Standard 6 makes a concrete check of key proved claims mandatory, and the `u_M` infinite-construction is precisely the kind of multi-step argument that benefits from one grounding instance. As written, the only proved-but-unexemplified branch is the structurally harder one.

**Required**: Add one short concrete trace at `m = 3` (e.g. element field `[s_C, 1, k]`), showing that an attempted interior value `[s_C, 2, 1]` is excluded and that `V_{s_C}(d)` collapses to `{[s_C,1,k] : 1 ≤ k ≤ n}` — verifying Step 1 against a specific arrangement.

## OUT_OF_SCOPE

### Topic 1: Link-subspace capacity / address-space exhaustion
The Open Questions already raise "must the system guarantee that a fresh link address is always available... or can link allocation fail due to address space exhaustion?" This is genuinely new territory (it touches the unbounded-component guarantee T0(a)/T0(b) and a liveness/progress axiom this ASN deliberately does not furnish), correctly deferred rather than treated as a gap here.

### Topic 2: Interior link withdrawal with renumbering (DELETEVSPAN semantics)
The Open Question on a "renumbering-aware link-arrangement contraction" correctly identifies that K.μ⁻'s suffix-only model does not cover the implementation's interior compaction. This belongs to the operation layer (explicitly out of scope) and to a future contraction-refinement ASN, not to a revision of this transition taxonomy.

VERDICT: REVISE
