# Review of ASN-0112

## REVISE

### Issue 1: Referential-integrity fact stated over all of `O(d)` is the content-only S3, not the per-subspace S3★

**ASN-0112, "The substrate we measure"**: "**S3** (referential integrity): `(A v : v ∈ O(d) : M(d)(v) ∈ dom(C))`."

**Problem**: This ASN explicitly admits both subspaces into the arrangement — `O(d) = dom(M(d))` includes link V-positions (V6, the link-only case in V5, and the worked example with `[2,1] ↦ ℓ`). In the extended state with links in arrangements, a link V-position (`subspace = s_L`) maps to a link address in `dom(L)`, **not** `dom(C)`. The fact as quoted asserts every occupied position maps into `dom(C)`, which is false for every link position. The content-only S3 (ASN-0036) belongs to the pre-link arrangement model; the correct foundation here is ASN-0047's **S3★** (GeneralizedReferentialIntegrity): content positions → `dom(C)`, link positions → `dom(L)`. The ASN otherwise uses the starred per-subspace foundations (D-CTG★/D-MIN★/D-SEQ★) but slips back to the unstarred S3 here.

**Required**: Replace the S3 citation with S3★ (ASN-0047) and state it per subspace: `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)` and `subspace(v) = s_L ⟹ M(d)(v) ∈ dom(L)`.

### Issue 2: V14 permanence claim is false for link-subspace positions

**ASN-0112, V14**: "every *occupied* position in `O(d)` — every position the span covers that actually carries content — maps, through `M(d)`, to a permanent I-address in `dom(C)` (S3), and that content is immutable and never destroyed (S0, P0)."

**Problem**: Link V-positions are occupied positions in `O(d)` whose images lie in `dom(L)`, governed by **L12 (LinkImmutability)**, not by S0/P0 (which constrain the content store only). As written, V14 claims link-subspace images are in `dom(C)` and immutable by content permanence — both wrong. This is a direct consequence of Issue 1 propagating into the permanence claim.

**Required**: Split V14 by subspace: content positions map to permanent immutable `dom(C)` (S0/P0); link positions map to permanent immutable `dom(L)` (L12). Cite S3★ for the integrity step and L12 for link permanence.

### Issue 3: V8 origin permanence presumes the content depth `m_C` is constant across states without stating it

**ASN-0112, V8**: "for every document state in which the content subspace is non-empty, `origin_d = [s_C,1,…,1]`, invariant under all editing that leaves content present."

**Problem**: `origin_d = [s_C,1,…,1]` is a tumbler of depth `m_C`. D-MIN★ pins the *value* per state, but the depth `m_C` is re-pinnable "at any value ≥ 2" after full subspace clearance (the ASN itself notes this in V11/`m_S` re-pinning). The invariance claim therefore silently depends on the premise that `m_C` cannot change while content remains continuously present. That premise is true (re-pinning fires only after `V_{s_C}(d) = ∅`, which "editing that leaves content present" excludes), but it is load-bearing and unstated.

**Required**: Add the one-line justification that depth re-pinning occurs only on full subspace clearance, so while content stays present `m_C` — and hence the depth of `[s_C,1,…,1]` — is fixed.

## OUT_OF_SCOPE

None. The per-subspace structural reasoning (V5–V7) is used only to characterize the single returned span, not to report per-subspace extents, so it stays within scope.

VERDICT: REVISE
