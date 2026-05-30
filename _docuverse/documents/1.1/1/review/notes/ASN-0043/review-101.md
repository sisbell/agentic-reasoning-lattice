# Review of ASN-0043

## REVISE

### Issue 1: L12 carries an out-of-scope operations deferral
**ASN-0043, L12 (LinkImmutability), closing prose**: "Immutability is not removal: how an old link ceases to be discoverable or resolvable is a question about operations, deferred to Open Questions."
**Problem**: Operations (and the deletion/discoverability model) are explicitly out of scope for this ASN. This sentence neither advances the L12 invariant (address persists, value fixed) nor states what L12 *does* — it raises an out-of-scope question and defers it downstream. It is exactly the "prose defers to a downstream location" pattern the anti-bloat classifier targets. The preceding sentence ("To effectively change a connection, the owner creates a new link via MAKELINK…") is also operation narrative riding on the immutability claim.
**Required**: Delete the deferral sentence; trim the MAKELINK-procedure narrative to the structural fact (a new link gets a fresh address, the old persists by L12).

### Issue 2: L4(c) appends an editorial forward-pointer to a substantive permission
**ASN-0043, L4(c) (Cross-subspace endsets)**: "Endset spans may reference addresses in the link subspace — that is, addresses of other links. This is L4's most consequential implication; we develop it fully under Reflexive Addressing below."
**Problem**: The first sentence is a legitimate "what the model permits" statement and should stay. The trailing "This is L4's most consequential implication; we develop it fully under Reflexive Addressing below" is pure editorial cross-reference — it advances no reasoning, and the content is in fact developed in L13. This is the forward-reference accretion the note's classifier flags.
**Required**: Drop the trailing clause; the permission statement stands on its own, and L13 already carries the development.

### Issue 3: L9's "Application to L9" block re-states hypotheses already established by the construction
**ASN-0043, L9 (TypeGhostPermission), "*Application to L9.*"**: the (h3) *Shape* and (h1)/(h2) *Freshness and producibility* bullets.
**Problem**: The construction paragraphs (*Construction of g*, *Choice of a*, Case A, Case B) already establish, in both cases, that `a` has `subspace_I(a) = s_L`, `zeros(a) = 3`, `#E(a) ≥ 2`, is T4-valid, is fresh, and is producible from `home(a) = d' ∈ dom(Σ.M)`. The "*Application to L9*" (h3) bullet restates the shape verbatim and the (h1)/(h2) bullet is a bare back-pointer ("established by the Case A / Case B construction above"). Only the *Payload* bullet's T12 check on `{(g, δ(1, #g))}` is new work. This is the "two paragraphs say the same thing in different words" pattern — the reader re-reads established facts before the FSP invocation.
**Required**: Collapse the discharge to one line — "h1–h3 are established in the construction above; the payload's single span is T12-well-formed since `#g = #d' + 3 ≥ 1` gives `δ(1, #g) > 0` with action point `#g`; apply FSP" — keeping only the genuinely new T12 verification.

## OUT_OF_SCOPE

None. The note correctly fences operations, resolution, and the deletion model into Open Questions and the Scope list.

VERDICT: REVISE
