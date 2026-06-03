# Review of ASN-0098

## REVISE

### Issue 1: "Third role" distinction raised only to be dismissed
**ASN-0098, "State Components"**: "Links inhabit a third role — stored at link-subspace I-addresses but referencing content-subspace I-addresses through their endsets — but for the projection question this role-distinction is immaterial. What matters is that endsets reference I-addresses, and arrangements map V-positions to I-addresses, and the bridge between them is computed live."
**Problem**: The sentence imagines a distinction (links as a "third role") and then states the projection question excludes it. This is the "imagines a case the claim already excludes" pattern: the projection definition consumes only `coverage(e)` and `Σ.M(d)`, so the link/content storage distinction never enters. The second sentence restates the two facts the section already established (endsets→I-addresses, arrangements→I-addresses).
**Required**: Delete the passage. The `project` definition makes the irrelevance self-evident; nothing downstream needs the role-distinction to have been named and waved off.

### Issue 2: Use-site inventory in LP18
**ASN-0098, "LP18 — Resurrection"**: "The transition sequence may include document registration (K.δ in the `Document(e)` case of ASN-0047, governed by LP8), K.μ⁺ or K.μ⁺_L (extending an existing arrangement, possibly via fork), or any other combination of operations that preserves the link store."
**Problem**: This enumerates the operations the sequence "may include," but the proof uses none of this taxonomy — it needs only (i) link-store preservation (for Store Monotonicity★ and LP3★) and (ii) the introduced arrangement entry `Σ'.M(d)(v) = a*`. The catalogue of possible operations is a use-site inventory that the actual derivation ignores.
**Required**: Drop the inventory sentence. The proof already names the two hypotheses it consumes; the list of admissible operation mixes adds nothing.

### Issue 3: Roadmap + unproven exhaustiveness assertion before LP12a
**ASN-0098, between LP12 and LP12a**: "LP12 characterises discoverability at a fixed state. The matching question for *displacement* is: given a particular editing operation, what must already hold at the pre-state for discoverability to survive into the post-state? K.μ⁻ is the only K.μ family member that can *destroy* discoverability."
**Problem**: Two patterns. First, "The matching question for displacement is…" is roadmap prose the section heading and LP12a's statement already convey. Second, "K.μ⁻ is the only K.μ family member that can *destroy* discoverability" is an exhaustiveness claim asserted, not derived, here — it would have to be read off LP9 (grows), LP10 (shrinks), LP11 (rebinds, preserving the reached I-address set), but no such derivation is given at this point.
**Required**: Cut the roadmap sentence. Either derive the exhaustiveness claim from LP9–LP11 explicitly, or drop it; an asserted "only X can do Y" with no chain is exactly the kind of meta-claim this note is being scrubbed of.

### Issue 4: Persistence-vs-discoverability contrast restated three times
**ASN-0098, LP13 / LP12a boundary / LP17**:
- LP13: "Persistence requires only `a ∈ dom(Σ.L)` and is independent of arrangement state, whereas discoverability is arrangement-conditional… A holder can therefore rely on the stored object permanently, but not on discoverability from any particular document…"
- LP12a boundary: "This boundary case isolates the precise sense in which storage and discoverability are independently regulated: storage cannot be undone by any contraction, but discoverability from a specific document can be…"
- LP17: "The link is not destroyed; it is invisible to forward navigation, but its stored endsets continue to identify the I-addresses it once reached…"
**Problem**: The same "storage is permanent, discoverability is conditional" contrast is delivered three times in different words across three lemmas. LP13's statement is the canonical home for it; the LP12a-boundary and LP17 restatements carry no new technical fact beyond their own local result (`R=∅ ⟹ wp=false`; orphan persistence).
**Required**: Keep the contrast at LP13. Trim the LP12a-boundary and LP17 prose to their local technical content (the false-wp specialisation; the empty-projection-everywhere fact), dropping the re-explanation of the storage/discoverability split.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive invariants
**Why out of scope**: The note correctly defers "given a V-position, return links whose projections contain it" to the Open Questions; it is a new operation, not a gap in this ASN's projection account.

### Topic 2: V-order/I-order correspondence within a projection
**Why out of scope**: Whether projected V-positions reflect the I-order of their I-addresses under K.μ~ is genuinely new territory (the note proves only set-level rebinding via π); belongs in a future ASN, as the Open Questions already flag.

VERDICT: REVISE
