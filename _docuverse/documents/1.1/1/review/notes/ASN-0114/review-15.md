# Review of ASN-0114

I read this as a specification of a read operation: name a link, name a slot, receive that slot's endset measured by coverage. The mathematical core is sound. The two genuine proofs — F2 (disconnected coverage forces ≥ 2 spans) and F7's two S2 collapses — are complete, and the worked example discharges both against a concrete link without hand-waving. F5's derivation correctly composes L12 along →* via LP13 rather than asserting it. F1 is correctly posited as the operation's contract (the proof obligation falls on implementations), and the consequence-derivation is the kind of depth a spec should carry: F6's confinement, the home-document disclosure slice, the empty-vs-invalid distinction. The note stays abstract — it explicitly refuses to fold in resolution-against-an-arrangement, and it pins F6 at coverage rather than overclaiming representation-level non-exposure.

I found one defect.

## REVISE

### Issue 1: Stated constraint count contradicts the enumerated claims
**ASN-0114, Synthesis**: "it returns that slot's endset, measured by coverage, under **five tight constraints**. It returns exactly the recorded end — no more, no less (F1) — preserving its discontiguous shape as a corollary (F2), with representation free but coverage bound (F3). It changes nothing (F4) and answers the same question the same way for all time (F5). It reads one end and discloses only that end ... (F6). It distinguishes a valid-but-empty end from an invalid selector (F7), and it succeeds regardless of whether anything is stored at the addresses the end names (F8)."

**Problem**: The sentence promises *five* constraints and then enumerates *eight* (F1–F8) in the same breath. A reader cannot tell whether "five" is a stale number from an earlier draft or whether it denotes a privileged subset (e.g., the core postconditions F1, F4, F5, F7, F8 with F2/F3/F6 as corollaries — which would reconcile to five, and the prose *does* tag F2 "as a corollary"). As written, the count is simply wrong against the list it introduces. In a note whose whole virtue is precision about "exactly how many" — exact coverage, ≥ 2 spans, three return categories — an off-by-three count in the closing summary is a stumble the precise reader must work around.

**Required**: Reconcile the number with the enumeration. Either change "five" to "eight," or — if the intent is to separate core constraints from corollaries — state that explicitly (e.g., "five independent constraints (F1, F4, F5, F7, F8), with F2, F3, and F6 following as corollaries of F1") rather than listing all eight under the figure "five."

## OUT_OF_SCOPE

None to add. The note's own Scope section and Open Questions already route resolution-against-an-arrangement, span-set normal form (which subsumes any sharpening of F2's ≥ 2 bound to a per-component bound), serialization encoding, and multi-document coverage to future work, correctly.

VERDICT: REVISE
