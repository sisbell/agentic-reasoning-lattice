# Review of ASN-0047

## REVISE

### Issue 1: S8★ content-subspace route applies ASN-0036's S8 to a *projection* without establishing subspace-closure
**ASN-0047, S8★ definition (Amendments to existing transitions)**: "*Content subspace.* `M(d)|_{V_{s_C}(d)} : V_{s_C}(d) → dom(C)` is a direct application of ASN-0036's S8: S3★ restricted to V_{s_C}(d) is exactly S3 (with target `dom(C)`), and S2, S7b, C1b ... are elementary-preserved per the verification below."

**Problem**: ASN-0036's S8 is stated over a full single-subspace arrangement, and its lockstep clause (a) quantifies `shift(v_j, k) ∈ dom(M(d))`. Applied to the *projection* `M(d)|_{V_{s_C}(d)}`, the lockstep image must land back in `V_{s_C}(d)` (not in `V_{s_L}(d)` or outside the projection) for S8 to "apply unchanged." This rests on `subspace(shift(v,k)) = subspace(v) = s_C` — OrdShiftHom(a). The link-subspace route below explicitly works through its lockstep clause and the `shift(t,0):=t` convention; the content route's "direct application" silently assumes the missing closure step. The asymmetry leaves the load-bearing fact (the content projection is shift-closed) unstated.

**Required**: Name OrdShiftHom(a) (subspace preservation under shift) in the content route, establishing that lockstep images of content V-positions remain content V-positions, so ASN-0036's S8 quantifier over `dom(M(d))` restricts soundly to `V_{s_C}(d)`.

### Issue 2: S8★ / K.δ verification-matrix cell labelled "frame" is imprecise
**ASN-0047, Class (a) verification matrix, S8★ row**: the K.δ cell reads `frame`.

**Problem**: K.δ for `Document(e)` does not frame M — it grows the arrangement family with a new empty arrangement (`dom(M') = dom(M) ∪ {e}`, `M'(e) = ∅`). The adjacent rows acknowledge this: the S8a/S8-depth/S8-fin K.δ cell reads "new doc has M(d)=∅ (vacuous)" and the S2 K.δ cell reads "frame (M(e)=∅ on new entity disjoint)". The S8★ cell's bare "frame" is inconsistent with these and misstates the discharge.

**Required**: Change the S8★/K.δ cell to "new doc M(d)=∅ (vacuous)" (the empty new arrangement satisfies S8★ vacuously; existing documents are framed), matching the S8a and S2 cells.

### Issue 3: NodeBaptism Open Question restates the axiom's own content
**ASN-0047, Open Questions**: "What must the node-provisioning boundary guarantee about freshness and lineage for NodeBaptism to hold, given that node baptism sits outside the docuverse transition model..."

**Problem**: NodeBaptism *is* the freshness-and-lineage guarantee — its body commits "(a) *Freshness:* `e ∉ Σ.E`" and "(b) *Bootstrap lineage:* `n₀ ≼ e`" at every node-allocation event. Asking "what must the boundary guarantee about freshness and lineage for NodeBaptism to hold" asks for exactly what the axiom already states; the answer is the axiom's two clauses. This is reviser drift — meta-prose circling an axiom rather than posing genuinely open territory (matching the flagged pattern "new prose around an axiom explains why the axiom is needed rather than what it says").

**Required**: Remove the question, or reframe it toward what is actually open (e.g., what *protocol-level* mechanism realizes boundary baptism, which is a different ASN's concern) rather than restating the axiom's premises.

## OUT_OF_SCOPE

### Topic 1: M2 (EmptyArrangement) supersession relative to foundation ASN-0093
**ASN-0047, Bridging lemma note**: "The sole exception is ASN-0093 M2 (EmptyArrangement) ... which is *not* inherited."

**Why out of scope**: ASN-0047 correctly documents that it populates arrangements and so does not carry ASN-0093's substrate-only M2. Whether M2 should have been scoped within ASN-0093 (as a substrate-layer property rather than a global invariant) is a question about the foundation's framing, not a defect in this ASN — its handling here is explicit and honest. No action required in ASN-0047.

### Topic 2: Link discoverability under cross-document contraction; link-capacity bounds; concurrency
**ASN-0047, Open Questions**: contraction-vs-discoverability, address-space exhaustion, concurrent allocation.

**Why out of scope**: These depend on the link-search/bidirectional-following mechanism and the concurrency/session model, both explicitly out of scope per the Scope section. They are correctly parked as Open Questions rather than under-specified here.

VERDICT: REVISE
