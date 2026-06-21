I read the foundation contracts and then the ASN as a system, tracing the precondition chains across WF/WR → S1/S3/S4/S5 → S8/S9/S10 and the SC → S11* difference cone. The mathematical core is sound: the WF/WR endpoint-recovery lemmas correctly discharge D1/D2 (including the equal-length exclusion of the prefix case), the carrier-membership of reach tumblers is consistently re-derived through TumblerAdd before every WF application, the SC five-case split is genuinely exhaustive and mutually exclusive, and the normalization existence/uniqueness pair (S8/S9) and order-independence (S10) chain correctly. The difference cone (S11, S11a–d) covers all SC cases with the bound 2 tight only at containment. I found no broken precondition chain or unsound proof step. The findings below are framing/attribution and reviser-drift noise.

### S5/S4 attribute T12's preconditions to T12 as if they were postconditions
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness) — postconditions are (a) s⊕ℓ ∈ T, (b) s ∈ span, (c) order-convexity; Pos(ℓ) and actionPoint(ℓ) ≤ #s are *preconditions*.
**ASN**: S5: "*Pos(d)*: T12 on λ gives d > 0." and "*k_d ≤ #s*: T12 on λ bounds the action point of d by #s." (also S4's discharge of T12 preconditions).
**Issue**: Pos(d) and actionPoint(d) ≤ #s are T12's *preconditions*, not exports. They are genuinely established — by WF, whose postcondition is "γ is a well-formed level-uniform span," i.e. Pos(width) and actionPoint(width) ≤ #start hold. The cited source ("T12 on λ") is the consumer of these facts, not their producer. The logic is sound, but a downstream reader could wrongly infer T12 exports Pos.
**What needs resolving**: n/a (OBSERVE) — attribution could read "by WF, λ is well-formed, so Pos(d) and actionPoint(d) ≤ #s."

### S6 Formal Contract carries meta-prose justifying its precondition, inconsistent with the inline S6
**Class**: OBSERVE
**Foundation**: TumblerAdd result-length identity #(a⊕w) = #w, earned under Pos(w) and actionPoint(w) ≤ #a.
**ASN**: S6 Formal Contract: "Level-uniformity alone does not yet entitle us to a length for reach(σ)… Drop a precondition — say Pos(ℓ) — and s ⊕ ℓ need not be defined, so the length identity has nothing to stand on." vs inline S6: "For a level-uniform span, #reach(σ) = #s by the result-length identity."
**Issue**: The inline S6 states the reach-length identity for "a level-uniform span" unconditionally; the Formal Contract adds a paragraph arguing *why* Pos(ℓ)/actionPoint are needed and constructing a hypothetical level-uniform-but-not-well-formed pair. Under the Span definition (which already presupposes Pos(ℓ), actionPoint(ℓ) ≤ #s), every "span" is well-formed, so the inline reading is correct and the contract's caveat is explaining why an axiom is needed rather than what it says — the reviser-drift pattern. The two presentations also disagree on whether "level-uniform span" can fail well-formedness.
**What needs resolving**: n/a (OBSERVE).

### WR Formal Contract lists a proof-internal derivation in the Precondition slot
**Class**: OBSERVE
**Foundation**: Divergence, T1.
**ASN**: WR Formal Contract: "*Preconditions:* … divergence(s, reach(σ)) = k ≤ #s of type (i) (T1, Divergence)."
**Issue**: divergence(s, reach(σ)) ≤ #s is derived in WR's body from s < reach(σ) and equal length (exactly as WF does), not assumed of the caller. Placing it among preconditions misrepresents the interface — a caller would think it must supply this, when the genuine preconditions are just s level-uniform and well-formed.
**What needs resolving**: n/a (OBSERVE).

### Defensive meta-prose in S2 and S7
**Class**: OBSERVE
**Foundation**: T12 (S2); T0/T0(b) (S7).
**ASN**: S2: "This second condition is a comparison of natural numbers … not of the end offset s ⊕ ℓ, which is a tumbler." S7: "(The membership of each extension is what is load-bearing here; the existential UnboundedLength claim T0(b) … is not what we invoke.)"
**Issue**: Both are defensive disambiguations against a confusion the proof does not actually risk — a type-coherence aside in S2 and a use-site inventory in S7 distinguishing which T0 clause is invoked. They restate correct facts but do not advance the reasoning; the precise reader must skip past them.
**What needs resolving**: n/a (OBSERVE).

VERDICT: OBSERVE