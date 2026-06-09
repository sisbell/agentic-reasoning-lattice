# Review of ASN-0118

This is a carefully constructed ASN. The composite decomposition (K.μ⁻ + K.μ⁺ + K.ρ), the append/empty vs. displacing case split, the tiling argument for no-holes, the initial-to-final coupling discharge for provenance, the self-transclusion handling, and the partial-binding decision are all handled with genuine rigor. The worked example exercises the key postconditions numerically, and the link-discoverability wp is a real non-trivial analysis. I found one load-bearing derivation gap.

## REVISE

### Issue 1: CP0(a) rests on an asserted "coincidence" whose one-line proof is omitted

**ASN-0118, "What a spec-set names, and what resolution recovers" (CP0(a))**: The ASN defines `resolve(R, Σ) = expand(resolve(R))` over ASN-0058's run-pairs, then states it "coincides with the per-position reading `⟨ Σ.M(d_s)(v) : v ∈ act(ρ, Σ) ascending ⟩`," and derives CP0(a) by reading it "off the per-position form of resolution directly: each `cᵢ` is `Σ.M(d_s)(vⱼ)` for some active position `vⱼ ∈ act(ρ, Σ)`."

**Problem**: The coincidence is load-bearing, not cosmetic. CP0(a) must hold for the *interior* addresses of a run — `aⱼ+1, …, aⱼ+(nⱼ−1)` produced by `expand` — and the only thing that guarantees each of these equals `M(d_s)(vⱼ+k)` for a *bound* position `vⱼ+k ∈ act(ρ, Σ)` (and hence lands in `dom(Σ.C)` via S3★) is precisely that `expand`'s run-pairs reproduce the per-position ascending reading. The ASN asserts this equality ("coincides") but never shows it. This is exactly the "X follows from Y is a claim, not a proof" pattern the standards flag: the maximal-run lockstep clause (`M(d_s)(vⱼ+k) = aⱼ+k` for bound `vⱼ+k`) plus C1b's V-start ordering of the runs is what makes the two objects equal, and that step should be exhibited — it is the sole bridge from ASN-0058's compressed run-pairs to the per-position form the CP0(a) derivation actually consults.

**Required**: A one- to two-step argument that `expand(resolve(R))` equals the per-position ascending reading over `act(ρ, Σ)` — naming the maximal-run lockstep property and C1b run-ordering as premises — so that CP0(a)'s `cᵢ ∈ dom(Σ.C)` is grounded for every expanded address (including run interiors), not just for the run-leading addresses `aⱼ` that the per-position phrasing makes obvious.

## OUT_OF_SCOPE

### Topic 1: Width preservation under partial binding (C2 loss)
**Why out of scope**: The Open Questions section correctly defers the relationship between a partially-bound span's nominal extent and its smaller placed width `W`. ASN-0058's C2 is honestly recorded as unused, and the question of what COPY must guarantee about the shortfall is new territory, not an error here.

### Topic 2: Ordering invariant for overlapping/repeated source spans, depth-mixing, link-subspace transclusion, conditional undiscoverability, and correspondence
**Why out of scope**: These are listed as Open Questions, deferred to future ASNs. They are not defined claims in this ASN and are appropriately left open.

VERDICT: REVISE
