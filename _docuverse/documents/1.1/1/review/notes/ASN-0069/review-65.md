# Review of ASN-0069

## REVISE

### Issue 1: Use-site inventory enumerating downstream consumers of `d_op`
**ASN-0069, §"What Must Be Constructed"**: "We carry `d_op` through every content-inheritance and correspondence claim below (V4, V4a, V4b, V8, V8b, V10(b), V11, V12(d)); the identity, ancestry, and source-isolation claims (V1, V2, V5) remain phrased in terms of `d_src`..."

**Problem**: This is a definition-time enumeration of downstream consumers — the flagged anti-bloat pattern "a definition's introduction enumerates downstream consumers ('this is consumed by X, Y, Z') rather than advancing the definition's meaning." The reader does not need a manifest of which later labels mention `d_op`; each claim states its own operand. The inventory rots as labels move and forces the reader to skip past it.

**Required**: Reduce to the operative rule — "content-inheritance and correspondence claims are stated against `d_op`; identity, ancestry, and source-isolation claims against `d_src`" — and delete the parenthetical label list.

### Issue 2: Use-site inventory in V5a justification
**ASN-0069, §"Frame: Source Isolation"** (before V5a): "We formulate the claim at that level of generality so its use sites — source isolation against fork-side edits (here), sibling fork independence (V10(b)), and transitive identity along fork chains (V11) — all consume the same lemma."

**Problem**: Same pattern — the lemma's generality is justified by listing its consumers (V10(b), V11). The generality stands on its own (it is a frame property of the arrangement-modifying vocabulary); naming the three call sites is meta-prose the reader must skip to reach V5a itself.

**Required**: State that the lemma is per-document and per-sequence over the arrangement-modifying vocabulary; drop the consumer list.

### Issue 3: Forward-deferral paragraph after V1/V2
**ASN-0069, §"Identity by Sub-Allocation"**: "They do not establish that `d_new` carries any content; that is the work of K.μ⁺. They do not establish any relationship between the source's V-stream and the fork's V-stream; that is the work of the content-sharing argument below. They do not establish that the source is unaffected by the creation; that is a frame condition we will discharge separately."

**Problem**: Three forward deferrals stacked in one paragraph ("that is the work of … below," "we will discharge separately"). This matches the flagged pattern of multiple deferrals to downstream locations. The substantive content (V1/V2 are identity-only) is one sentence; the rest is scaffolding pointing forward.

**Required**: Collapse to a single sentence noting V1/V2 establish identity and ancestry only, with content inheritance, correspondence, and source isolation following. Remove the per-clause forward pointers.

### Issue 4: V4-strengthens-J4 stated twice
**ASN-0069, §"Identity by Sub-Allocation"**: "The one place where this ASN genuinely *deviates* from J4 is the arrangement discipline: J4's clause (ii) installs content via an order-preserving bijection `φ : V_{s_C}(d_op) → V_{s_C}(d_new)`, while this ASN commits to the stronger *literal* inheritance (`φ` is the identity on V-positions) — that deviation is developed and justified at V4 below."

**Problem**: This forward reference states the full substance (the φ-identity strengthening) and is then restated at the site in §"The Arrangement Layer" — both the V4 parenthetical ("J4's clause (ii) installs content via an order-preserving bijection … Literal inheritance fixes `φ` to be the identity") and the "V4 *strengthens* J4's clause (ii)" paragraph. Matches "two paragraphs in the same document say the same thing in different words." A forward reference should point, not pre-prove.

**Required**: Reduce the §"Identity by Sub-Allocation" mention to a bare pointer ("the literal-inheritance deviation is V4") and keep the full deviation account at V4 only.

## OUT_OF_SCOPE

None requiring action. The Open Questions section correctly defers concurrent-modification semantics, snapshot-vs-living forks, transcludent sources, and descendant enumeration to future ASNs rather than asserting claims about them.

VERDICT: REVISE
