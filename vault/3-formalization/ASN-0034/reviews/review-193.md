# Cone Review — ASN-0034/TA5a (cycle 8)

*2026-04-17 19:33*

### TA5a attributes "differs only at position" / "extends t by k positions" to TA5(c) or TA5(d) alone, omitting TA5(b)'s agreement clause
**Foundation**: TA5 (HierarchicalIncrement) — distinct postconditions (b), (c), (d). (b) carries the *agreement* clause on unchanged positions (for k=0: `(A i : 1 ≤ i ≤ #t ∧ i ≠ sig(t) : t'ᵢ = tᵢ)`; for k>0: `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)`). (c) gives only `#t' = #t` and `t'_{sig(t)} = t_{sig(t)} + 1`. (d) gives only `#t' = #t + k` and the values at positions `#t+1, …, #t+k`.
**ASN**: TA5a, Case k=0:
> "By TA5(c), `t'` has the same length as `t` and differs only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`."

TA5a, Case k=1:
> "By TA5(d), `t'` extends `t` by one position: `#t' = #t + 1`, with `t'_{#t+1} = 1`."

TA5a, Case k=2:
> "By TA5(d), `t'` extends `t` by two positions: `t'_{#t+1} = 0` (one field separator) and `t'_{#t+2} = 1` (the first child)."

TA5a's Depends entry for TA5 lists only "TA5(c) at case `k = 0`" and "TA5(d)" at cases `k = 1`, `k = 2`, `k ≥ 3`; no TA5(b) citation appears.
**Issue**: The phrases "differs only at position `sig(t)`" (case k=0) and "extends `t` by one/two positions" (cases k=1, k=2) assert that `t'` agrees with `t` at every original position not explicitly modified — exactly the content of TA5(b). TA5(c)/(d) alone fix only the length and the values at the modified positions; without (b) they permit arbitrary values at the unchanged positions, under which (i) "no zero components are added or removed at position `sig(t)`" in case k=0 could not conclude `zeros(t') = zeros(t)` (an arbitrary change at some other position could add or remove a zero), (ii) cases k=1 and k=2 could not conclude that `t'_{#t} = t_{#t}` and therefore could not invoke T4's boundary clause on `t` to discharge the left-flank non-zeroness of the appended component or separator. Both load-bearing steps presume the agreement clause TA5(b), which the Depends list and the inline citations silently absorb into the (c)/(d) labels.
**What needs resolving**: TA5a's case prose and Depends list must surface TA5(b) at the sites where agreement on unchanged positions is consumed — case k=0 for "no zero components are added or removed at positions other than `sig(t)`" and `t'_{#t} = t_{#t}` (in combination with TA5-SigValid's `sig(t) = #t`), and cases k=1 and k=2 for `t'_{#t} = t_{#t}` used to import T4's boundary clause onto `t'`'s left-flank position — so that the "differs only at …" and "extends … by … positions" readings source their agreement component to TA5(b) rather than to TA5(c)/(d) alone. Alternatively, the TA5 postconditions must be restated so that (c)/(d) internally carry the agreement content that TA5a's summary already attributes to them, with TA5(b) elided as redundant.
