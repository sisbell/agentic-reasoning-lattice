# Review of ASN-0087

## REVISE

### Issue 1: D-CTG★ proof asserts an unestablished reachable pre-state, contradicting M-DepthConv

**ASN-0087, Invariant Preservation (D-CTG★ discharge)**: "At the canonical commit depth `m_L^{Σ'}(d) = 2` the slice is exactly `{[s_L, k]}` and last-component contiguity is the whole claim, but `m_L(d) ≥ 3` is reachable as a pre-state — K.μ⁺_L's `ValidFirstLinkPosition` admits any `m ≥ 2` from a non-MAKELINK placer — so we supply the interior-component step explicitly."

**Problem**: Two coupled defects.

(a) *Overclaim.* The reachability of an `m_L(d) ≥ 3` pre-state is asserted as fact ("is reachable as a pre-state") but never established. M-DepthConv states MAKELINK commits the minimal depth `m = 2` for every first link it places, after which S8-depth pins `m_L(d) = 2` for all later link V-positions of that document. The K.μ⁺_L non-empty precondition then forces `#v_ℓ = m_L(d) = 2` on every subsequent placement. The *only* route to `m_L(d) ≥ 3` is a non-MAKELINK placement of the *first* link at a document — and no such operation is named or shown to exist in this note. The justification invokes a hypothetical "non-MAKELINK placer" the ASN does not exhibit. As written, the note both claims `m_L(d) = 2` is forced (M-DepthConv) and claims `m_L(d) ≥ 3` is reachable (D-CTG★), without reconciling them.

(b) *Meta-prose.* The sentence does not advance the proof — it justifies *why* the interior-component step is supplied ("so we supply the interior-component step explicitly"). A reader must skip it to reach the actual argument ("The post-state set is `V_{s_L}^{Σ'}(d) = ...`").

**Required**: Resolve the tension explicitly. Either (i) establish that a non-MAKELINK operation can place a first link V-position at depth ≥ 3 (a scope statement that the general proof defends against future operations would suffice), keeping the interior-component step but dropping the false "is reachable" assertion in favor of "to keep the proof independent of how `m_L(d)` was established"; or (ii) if MAKELINK is the canonical link-creation operation and `m_L(d) = 2` is therefore guaranteed, strengthen M-DepthConv to that effect and reduce the D-CTG★ branch accordingly. Either way, strip the "so we supply..." justification — keep the argument, drop the rationale for including it.

### Issue 2: Motivational essay prose in claim-bearing slots

**ASN-0087, What Is Indexed?**: "...discoverability is therefore symmetric (M-DiscSymmetry): `ℓ` is discoverable from every document whose arrangement range meets some endset coverage, realizing Nelson's intent that all parties reaching a link's endpoints discover it by querying their own content."

**Problem**: The clause "realizing Nelson's intent that all parties reaching a link's endpoints discover it by querying their own content" is design-motivation essay content appended to the formal statement of M-DiscSymmetry. It does not advance the symmetry claim, which is fully established by the LP12 uniformity argument preceding it. This is the anti-bloat pattern of essay content occupying a structural slot.

**Required**: Drop the motivational clause; the formal symmetry statement stands on its own.

## OUT_OF_SCOPE

### Topic 1: Existence and depth discipline of non-MAKELINK link-V-position placers
**Why out of scope**: Whether any operation other than MAKELINK places link V-positions (and at what depth) depends on the broader operation vocabulary — REARRANGE/COPY mechanics and future composites — which is not this note's subject. Issue 1 asks only that the note stop asserting reachability it has not established; the actual enumeration of placers belongs elsewhere.

VERDICT: REVISE
