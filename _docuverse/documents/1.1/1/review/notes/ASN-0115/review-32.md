# Review of ASN-0115

## REVISE

### Issue 1: R8's "TransclusionRevelation" claims an output-level disclosure the operation does not provide

**ASN-0115, §"What co-delivery reveals: transclusion" (R8) and §"Synthesis"**:
- "this is what single-span delivery conceals. Delivered alone, each position arrives as a self-contained fragment; the *relation between* the two — their shared home `a` — is established only when both are resolved within one request, where their common resolution is exhibited."
- "co-delivery is the locus where that commonality is made manifest, because only co-resolution puts the two shared addresses side by side."
- Worked instance: "The two appearances are ascertainably one content because both resolved through the single address `a`."
- Synthesis: "Co-resolution reveals transclusion..."

**Problem**: The delivered output cannot reveal transclusion, and co-delivery discloses nothing a pair of single-span deliveries does not.

1. By **R0**, `deliver(R, Σ)` is the concatenation of per-spec deliveries; the co-delivery of two transcluded positions is *exactly* the concatenation of their two single-span deliveries. Co-delivery carries no information that two separate single-span requests would not.
2. By **R1**, a content item carries the *value* `Σ.C(a)`, never the address `a`. Two transcluded content positions deliver two identical values.
3. By **S4 (OriginBasedIdentity)**, value-equality does not entail address-identity. Two *coincidentally-equal* contents at distinct addresses deliver byte-identical output, indistinguishable from genuine transclusion — so no recipient can ascertain "one content" from the delivery.
4. **R9 — in this same ASN — states the matter correctly**: for content, `origin(a)` "is *not* recoverable from the output... an internal artifact of computing `deliver`." R8's "made manifest" / "ascertainably one content" / "puts the two shared addresses side by side" directly contradicts R9.

The sentence "the relation between the two... is established only when both are resolved within one request" is false on two counts: each single-span resolution already maps its position through `a` (the shared home is established per-position, not jointly), and `deliver` performs no comparison of the two resolutions — it concatenates `item(v)` and `item(v')`, each computed independently — so it "establishes" nothing about their relation in one request any more than in two.

The contrast with **R10** is telling, and the ASN gets R10 right: subspace crossing *is* output-observable because the item kinds differ (`⟨content,…⟩` vs `⟨ref,…⟩`). R8 has no analogous output manifestation — its claimed "revelation" lives only in the internal `v ↦ a` resolution, precisely the artifact R9 says does not reach the output.

**Required**: Align R8's prose with its own (correct) claims-table summary and with R9. State only what holds: transcluded content positions resolve through one shared address (a resolution-internal fact) and are delivered as identical values with no deduplication; the delivered output does not disclose the sharing and cannot distinguish transclusion from coincidental value-equality (S4, R9). Drop "reveals / made manifest / ascertainably one content / established only when both are resolved within one request / puts the two shared addresses side by side" — or, if output-level revelation is genuinely intended, redefine `item`/R0 to carry addresses for content, which contradicts R1 and R9 as written. The R8 title and the Synthesis sentence "Co-resolution reveals transclusion" inherit the same overclaim and must be reconciled.

### Issue 2: The inline Confinement lemma re-proves a foundation result (ASN-0058 C0a) without relating to it

**ASN-0115, §"What a spec-set is, and what delivery is" (Confinement lemma)**: "For an ordinal-level, level-uniform span `σ = (s, ℓ)` with `#s = #ℓ = m ≥ 2`, every `t ∈ ⟦σ⟧` agrees with `s` on its first `m − 1` components..."

**Problem**: This is the tumbler fact ASN-0058's **C0a (PrefixConfinement)** already states — "every `t ∈ ⟦σ⟧` satisfies `tⱼ = uⱼ` for all `1 ≤ j < m`... In particular `t₁ = u₁` (subspace confinement)." ASN-0058 is a foundation; the ASN should use it rather than re-derive it de novo. The one genuine gap is that C0a is stated for a *content reference*, whose well-formedness requires `V_{u₁}(d_s) ≠ ∅`, whereas ASN-0115 needs confinement also when `V_S(d) = ∅` (it invokes Confinement in the V-spec definition precisely to argue `act = ∅` there). The body already cites ASN-0058 for the depth discipline but not for confinement.

**Required**: Cite ASN-0058 C0a as the populated-subspace (`V_S(d) ≠ ∅`) instance and present the inline lemma as its extension to the `V_S(d) = ∅` case (where C0a's precondition fails), instead of proving confinement from scratch. One sentence relating the two suffices; keeping the fresh proof of the extension is fine.

## OUT_OF_SCOPE

The ASN's deferrals (Open Questions 1–5: inline content provenance, failure-vs-partial-delivery, dangling references, channel faithfulness, straddling spans) are appropriately scoped to future ASNs and need no coverage here.

VERDICT: REVISE
