# Review of ASN-0063

I have verified every definition, lemma, theorem, and proof chain in this ASN. The formal content is correct. The link-subspace fixity argument under K.μ~ is particularly impressive — the counting argument (injection from size-N into size-(N−r) forces r = 0) is elegant and airtight. The dependency chain S3★ → S3★-aux → fixity → P4★ is non-circular and correctly ordered in the proof text.

What follows are the issues I found.

## REVISE

### Issue 1: CL0 element-level equality claim compressed beyond safety

**ASN-0063, CL0 proof**: "the only depth-#v_β tumbler between v_β + k and v_β + (k + 1) is v_β + k itself"

**Problem**: This one-sentence justification carries the entire CL0 proof. The claim requires a T1-based argument: any depth-#a_β tumbler t satisfying a_β + k ≤ t < a_β + (k+1) must agree with a_β + k on components 1 through #a_β − 1 (if it differed at some earlier position j, then t_j > (a_β + k)_j = (a_β + (k+1))_j, giving t > a_β + (k+1) by T1(i), contradiction). Then t_{#a_β} is forced to equal (a_β + k)_{#a_β} by the integer gap. This two-step argument (prefix agreement by contradiction, then last-component uniqueness by integer constraint) is not shown.

**Required**: Expand the element-level equality justification to show both steps: (1) any same-depth tumbler in the interval must share the prefix (by T1 contradiction), and (2) the last component is then forced by the integer gap. Three sentences would suffice.

### Issue 2: Orphan link withdrawal — K.μ⁻ capabilities understated

**ASN-0063, orphan link discussion**: "When |V_{s_L}(d)| ≥ 2, only the maximum V-position can be removed without violating D-CTG or D-MIN"

**Problem**: This describes single-position removal. But K.μ⁻ operates on sets: dom(M'(d)) ⊂ dom(M(d)). Removing any suffix {[s_L, 1, …, 1, k] : n' < k ≤ n} for 0 ≤ n' < n also satisfies D-CTG and D-MIN (contiguous remainder starting at the minimum, or empty). In particular, removing *all* link-subspace positions at once (n' = 0) is valid — D-CTG and D-MIN hold vacuously for the empty set. This enables a link reordering composite (K.μ⁻ removing all link-subspace positions + K.μ⁺_L re-adding in new order) that the current text implies is impossible.

**Required**: State that valid link-subspace contractions are suffix truncations: the result is {[s_L, 1, …, 1, k] : 1 ≤ k ≤ n'} for any 0 ≤ n' < n, not only single-position removal from the maximum. Note the K.μ⁻ amendment text ("removal from the maximum end of V_S(d) or removal of all positions") already captures this correctly — the orphan link paragraph should match.

### Issue 3: Resolve's dependence on canonical decomposition is normative but unmarked

**ASN-0063, Definition — Resolve**: "resolve(d, Ψ) is the finite endset constructed by collecting all CL0 I-spans from the canonical block decomposition of M(d)"

**Problem**: Different block decompositions of M(d) produce different endset *span-sets* with the same coverage. Since L8 (TypeByAddress) compares type endsets by set equality of spans — not coverage equality — the choice of decomposition is normative for type identity. Two links created with the same V-span selection but resolved against different decompositions would have different type endsets and fail L8 comparison. The canonical decomposition (unique by M12) prevents this within a single state. But the fact that canonical decomposition is a *design choice with semantic consequences* — not merely an implementation detail — is not noted.

**Required**: Add a brief note that resolve's use of the canonical decomposition is normative: it determines which spans appear in the endset, and therefore affects type identity under L8. Note that M12 (CanonicalUniqueness) ensures resolve is deterministic within a given state.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism
**Why out of scope**: The ASN correctly identifies withdrawal as an open question. The D-CTG constraint on K.μ⁻ and link-subspace fixity under K.μ~ create a design space (suffix truncation, rebuild-in-new-order, or inactive-status flags) that belongs in a dedicated ASN.

### Topic 2: Discovery mechanism — range queries and ordering
**Why out of scope**: disc is defined as a point-level function on I-addresses. Whether it should support range queries, role-attributed results, or ordered output are interface design questions for the discovery ASN.

### Topic 3: Resolution timing guarantees
**Why out of scope**: The ASN correctly notes that arrangement changes between selection and resolution are unaddressed. This is a concurrency/consistency question that belongs with the concurrent CREATELINK open question.

VERDICT: REVISE
