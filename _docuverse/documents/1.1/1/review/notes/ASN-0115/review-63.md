# Review of ASN-0115

I checked the core proofs (Confinement, R6's no-interior-hole/terminal-overrun analysis, R7's active-set agreement, R8's link-vacuity via CL-OWN + CL-UNIQ) and the five worked instances (R6, R8, R9, R10, R11) against the substrate. The mathematics is sound: the `act(ρ,Σ)` override is consistently applied, the depth-compatibility case splits hold, the deep-case emptiness claim discharges via Confinement + S8-depth + the prefix-ordering of T1, and the worked arithmetic (`[1,2] ⊕ [0,5] = [1,7]`, the `s=[1,5], ℓ=[2,0]` straddle counterexample, the K.μ⁻ orphaning instance) all check out. No correctness defect found. One prose finding remains, against the note's `review-mode.anti-bloat` mandate.

## REVISE

### Issue 1: R7's closing sentence imports R11's guarantee into the repeatability proof
**ASN-0115, "Repeatability" (R7), final sentence**: "The foundation of permanent citation is thus not an impossibility of in-place arrangement editing but the immutable content store (S0): the bytes at an I-address never change, so a reference whose binding survives resolves to the same value for all time."

**Problem**: This is essay content appended after R7's proof is already complete ("…and the two deliveries are identical"), and it restates R11 (PermanentSourcing) — "a reference whose binding survives resolves to the same value for all time" is precisely R11's reference-level guarantee. R7's actual hypothesis is restriction-level (the *entire* consulted restriction `Σ.M(dⱼ)|⟦σⱼ⟧` is unchanged), not the per-reference survival condition R11 names. So the sentence both (a) duplicates a dedicated downstream claim and (b) mildly blurs R7's hypothesis with R11's weaker per-binding condition by labelling R11's mechanism "the foundation of permanent citation" inside R7. The preceding sentence ("The arrangement is the sole mutable input … which a caller secures by citing a version whose arrangement it does not subsequently edit") already discharges the practical framing R7 needs.

**Required**: Trim the final sentence; let the permanent-citation point live in R11, where it is the dedicated claim and the wp decomposition makes the reference-level scope precise. (The S0-vs-arrangement-immutability distinction, if wanted in R7, can be stated in R7's own terms — equal restrictions yield equal values — without borrowing R11's "binding survives" framing.)

## OUT_OF_SCOPE

No scope violations. The note correctly uses FINDDOCSCONTAINING / RETRIEVEDOCVSPAN only as Nelson-quote foils in motivation (defines no claims for them), confines link-structure reading (READLINK) out via R10's reference-only delivery, and routes boundary-straddling spans, channel faithfulness, and inline provenance to the Open Questions rather than claiming them. All ASN dependencies are to foundation ASNs.

VERDICT: REVISE
