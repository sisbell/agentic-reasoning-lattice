# Review of ASN-0123

## REVISE

### Issue 1: V7 and VD restate the cross-owner severance/downward-limit argument twice
**ASN-0123, V7 and VD**:
- V7: "a VERSION(π, d) with π ≠ ω(d) yields a first-class version v … yet ¬(d ≼ v) by severance (V9), so **v falls in neither S(d, 1) nor {e : d ≺ e}** and no address-based descendant scan reaches it … the cross-owner remainder is decided only by shared content, never the registry."
- VD: "a cross-owner fork VERSION(π, d) with π ≠ ω(d) makes derives(v, d) hold … yet ¬(d ≼ v) (severance, V9) … Such a derivation escapes every address-based descendant scan — **v lies in neither S(d, 1) nor {e : d ≺ e}**, so no registry enumeration over the source's subtree reaches it — and is recoverable only through the shared-content witness (V9w), never the registry."

**Problem**: These are the same argument — {cross-owner fork, derives holds, ¬(d≼v), v outside both `S(d,1)` and `{e:d≺e}`, no address scan reaches it, only shared content witnesses} — stated at length in two sections, down to the identical clause "neither/lies in neither S(d, 1) nor {e : d ≺ e}." A precise reader works through the same derivation twice. This is the forward-reference accretion the classifier names.
**Required**: Let one site carry the argument and the other cite it. VD is the natural home (it owns the `derives` biconditional and its failure direction); V7's cross-owner paragraph should reduce to the navigation consequence plus a pointer to VD.

### Issue 2: V-WF carries a downstream-consumer inventory of O5(i)/(ii)
**ASN-0123, V-WF**: "The ownership-facing consequences of the stream form — pfx(π) ≼ v (O5(i)) and the coverer-maximality (O5(ii)) — are derived at V9 and consumed only by its severance and ownership claims; neither these steps nor their couplings (which turn on Document(v), freshness, and S3★) consume them."
**Problem**: This is use-site bookkeeping ("derived at V9 … consumed only by … neither … consume them"), not part of V-WF's precondition discharge. V-WF needs from the stream form exactly `Document(v)` (for the K.μ⁺ precondition `v ∈ E_doc`), and that single dependency is already stated in the preceding sentence. The inventory of where O5(i)/(ii) are and are not consumed adds nothing to the discharge a reader is following here.
**Required**: Cut to a bare forward pointer (the ownership consequences are established at V9) or remove. To be unambiguous: this targets the consumer-inventory sentence only — the V9 maximality derivation itself (the protected O5(ii) discharge) is load-bearing and stays untouched.

### Issue 3: The boundary/interior P4★ subtlety is developed twice, and the atomicity remark's second paragraph is a use-site inventory
**ASN-0123, atomicity remark and V9w**:
- Remark: "Two boundary assumptions must be kept apart. P-bdy … is what **licenses P4★ at Σ in V9w and the boundary properties at Σ' in V-WF** … the implementation happens to realize it (whole-request serialization; **see the evidence section**)."
- V9w: "The boundary hypothesis is load-bearing and may not be waived: at an interior start it fails. Were Σ to lie inside a predecessor composite that had already extended d_src's content range with a … but not yet recorded the matching provenance … P4★ is exactly the property that may fail at such interiors …"
**Problem**: The "P4★ holds at boundaries, fails at interiors" point is built up at length in both places. The remark's second paragraph is largely a use-site inventory (it names V9w, V-WF, and the evidence section as where each half is consumed/realized), which is the "defer to downstream locations" pattern; V9w independently re-derives the same point via a counterfactual that imagines an interior start — a case P-bdy already excludes. The remark's *first* paragraph (foundations make atomic steps indivisible but not the composite a unit; the interior state after K.δ is genuinely reachable) is the part that advances reasoning and is not duplicated.
**Required**: State the boundary-vs-interior distinction and why P4★ needs a boundary once — V9w is the load-bearing site, since it consumes P4★ for the source-side row. Reduce the remark's second paragraph to the genuinely new content (the composite is not atomic; the interior state exists and is reachable absent the stronger serialization convention) and drop the use-site inventory and the counterfactual restatement.

## OUT_OF_SCOPE

None to add. The note's scope boundary is drawn correctly: the cross-owner branch *uses* the document-creation allocator `A_doc` (an ASN-0047 construct) without specifying document creation; V11 guarantees the version is edit-enabled without specifying the edit operations; V10 reasons about discoverability of existing links without specifying link operations. The eight Open Questions enumerate the genuine future territory (version-namespace discipline for non-fork allocators, derivation-direction recovery, concurrency serialization, windowing, withdrawal/supersession). No out-of-scope topic is smuggled in as a claim.

VERDICT: REVISE
