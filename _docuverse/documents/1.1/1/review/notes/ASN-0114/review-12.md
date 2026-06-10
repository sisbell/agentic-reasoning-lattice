# Review of ASN-0114

I checked each of F0–F8, the wp derivations, the two S2 "collapse" arguments, and the worked instance. The mathematics is sound: F2 follows correctly from F1 + S0 (convexity) + S2 (non-empty spans); the wp for `R = ⟨⟩` is genuinely non-trivial and correctly derived; F5 properly composes L12 along `Σ →*` via LP13 rather than hand-waving the closure; the worked example's interval arithmetic (`a₃ ⊕ δ(2,#a₃) = a₅`, disconnectedness witness `a₃ < a₅ < a₇`, `F`-restriction to `{a₃,a₄,a₇,a₈}`) checks out. All cross-references are to foundation ASNs (0034, 0043, 0053, 0093, 0098); no reinvented notation. The substantive content is correct and the operation is stated at the right level of abstraction (coverage-bound, representation-free), so no META.

The one finding is anti-bloat: meta-prose accreted around the two `S2` collapses in the F7 section.

## REVISE

### Issue 1: Bookkeeping scaffolding around the two collapses in F7
**ASN-0114, "The empty end versus the invalid selector"**: three phrases comment on where facts get used rather than advancing the argument:
- "Slot 3 is the lone exception: L3 ... mandates `Σ.L(a).e₃ ≠ ∅` ... — **a consequence discharged precisely once the two collapses below are in hand**."
- "Two collapses follow, **and we reuse both below**."
- "**The first collapse is what licenses writing `followlink(Σ, a, i) = ⟨⟩` as a literal value-equality in F7, whereas for a non-empty end we could assert only an equality of coverage.**"

**Problem**: These are exactly the forward-reference / use-site-inventory patterns the anti-bloat classifier targets. The first phrase is a promissory note the reader must carry three sentences until the slot-3 fact is actually discharged. "and we reuse both below" announces downstream consumption instead of just consuming. The third sentence explains the *notational role* of the first collapse rather than stating any new fact — the notation `followlink(Σ, a, i) = ⟨⟩` is self-evidently licensed the moment the collapse `R = ⟨⟩ ⟺ coverage(R) = ∅` is in hand; the meta-commentary about what it "licenses" is prose a precise reader skips. The two collapses themselves are one-line consequences of S2; the scaffolding is several times their length.

Note that the adjacent observation — "The type selector thus never yields the empty-success `⟨⟩`; the empty-versus-invalid collision this section forbids is reachable only at the non-type slots" — is a legitimate *statement of what the operation does/does not do* and should be **kept**; the finding is only the bookkeeping scaffolding, not the slot-3 result.

**Required**: Drop "and we reuse both below"; replace the promissory "a consequence discharged precisely once the two collapses below are in hand" with the discharge stated where the collapses appear (or simply assert the slot-3 fact there directly); delete the "is what licenses writing … in F7" sentence — the value-equality needs no separate justification once the first collapse is stated. (One analogous closer, "These are the only ingredients. Everything below is derived from them," at the end of "The substrate we build on," is the same mild pattern and can go with it. The rest of the note is clean.)

## OUT_OF_SCOPE

None. The deferrals the note makes itself — resolution of the recorded endset against a particular document's arrangement (the "boundary we must respect" section), normal-form selection (Open Question 1), and the serialization re-encoding of `⟨⟩`/`⊥` (Open Question 3) — are correctly placed outside this operation rather than left as gaps.

VERDICT: REVISE
