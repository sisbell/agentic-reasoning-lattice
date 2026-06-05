# Review of ASN-0103

This is an unusually thorough ASN — the frame analysis, the version/document length filter, and the deferral of the `ω`-valued ownership claim are all handled with care. The worked example correctly exhibits the collision the length filter averts. I found one load-bearing step that is asserted rather than proved.

## REVISE

### Issue 1: The version-dominance argument assumes `A ≼ t` without justification

**ASN-0103, Effect One ("Strict advance," subsequent case)**: "Let `t` be its operand; `Document(t)` since `t ∈ E_doc`. Being the first such fork, no `k=1` step precedes it, so **t's derivation from A** uses only the depth-2 descent and `k=0` sibling steps … That step is off `A` itself — a `k=0` step off `A` would yield a sibling account differing from `A` at position `#A`, **breaking `A ≼ t`**."

**Problem**: The entire sub-argument ("exactly one `k=2` step, off `A` itself") presupposes that `t` descends from `A` — i.e. that `A ≼ t`. But the only prefix hypothesis the text introduces is `A ≼ v` (from the definition "any entity with `A ≼ v` and `#v > #A + 2`"). The operand `t` is given only as `t ∈ E_doc` (a `Document`); nothing stated forces `A ≼ t`. Since `A ≼ t` is the premise that the "`k=0` step off `A` breaks `A ≼ t`" clause leans on, and the first-case argument inherits this same length argument by forward reference, the gap is load-bearing in both branches.

The fact is in fact derivable — `v` agrees with `t` on positions `1..#t` (after `e₁ = inc(t,1)`, lengths are non-decreasing and `sig ≥ #t`), and if `#t < #A` then `t ≼ A`, forcing `zeros(t) ≤ zeros(A) = 1`, contradicting `zeros(t) = 2`; hence `#t ≥ #A` and `A ≼ t`. But this multi-step bridge is exactly the kind of inference this ASN justifies explicitly everywhere else (it cites TA5(b)/(c), B5a, P1, etc. for steps of comparable weight), so the silent omission is inconsistent with its own standard.

**Required**: Insert the derivation that `A ≼ t` (via `v` agreeing with `t` on `1..#t` together with the `zeros`-mismatch ruling out `t ≼ A`) before invoking "`t`'s derivation from `A`."

## OUT_OF_SCOPE

None — the forking contrast, content/link allocation, and registry-coupling questions are all correctly deferred (the latter to a registry-carrying ASN, with the precise missing invariant named).

VERDICT: REVISE
