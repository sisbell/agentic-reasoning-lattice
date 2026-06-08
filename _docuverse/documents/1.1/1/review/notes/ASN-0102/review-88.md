# Review of ASN-0102

I checked the COPY definition, the X1–X16 derivations, the wp(S3★) reduction, the invariant-discharge in X14, and all five worked examples. The arithmetic of the displacement, the tiling in X16, the cross-origin/merge reasoning in X8/X11/X12, and the self-transclusion pre-state pinning all hold up. Two issues remain — one a genuine notational defect, one accreted prose flagged under the anti-bloat classifier.

## REVISE

### Issue 1: Overloaded symbol `c` in the X16 tiling list
**ASN-0102, X16 (PostStateDensity), the three-class tiling bullets**: "*copied* (`v + c`, `0 ≤ c < W`): last component `c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`"
**Problem**: In this bullet `c` is bound as the shift *offset* (`0 ≤ c < W`), but the same `c` is then asserted to be the *last-component value* (`c ∈ [p, p + W)`). The last component is `p + c`, not `c` — the bullet's own trailing clause (`v + c = [s_C,1,…,1,p+c]`) contradicts the label. Compounding this, the neighbouring *unmoved* (`c ∈ [1, p)`) and *displaced* (`c ∈ [p, n_S]`) bullets use `c` to mean the last-component value, so the symbol carries two different meanings inside one list and the copied bullet is internally inconsistent. A reader tracking the tiling `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W]` has to silently rewrite `c` to `p+c` to make the copied range come out right.
**Required**: Use the actual last-component value in the copied bullet — "last component `p + c ∈ [p, p + W)`" — or introduce a distinct symbol for the offset versus the last-component value and apply it uniformly across all three bullets.

### Issue 2: Self-transclusion well-definedness stated twice
**ASN-0102, "The source designation and its resolution"**: "This single pre-state pinning is what makes self-transclusion (`d_s = d`) well-defined: the copied span is read from the frozen pre-state image even as `d` is simultaneously displaced."
**ASN-0102, X10(b)**: "The guarantee here is not non-alteration but the pre-state pinning fixed by the source-resolution convention: the target-as-source is read at the pre-state `Σ` and is itself displaced by `· + W`."
**Problem**: These two passages assert the same fact in different words — pre-state resolution makes self-transclusion well-defined because the target-as-source is read frozen while being displaced. The opening section's role is to *fix the convention* (resolution pinned to `Σ`); the *significance* for self-transclusion is the content of X10(b) and is independently demonstrated in the second worked example ("Pre-state resolution (X10(b)) is what makes this self-transclusion well-defined"). The significance sentence in the opening section is therefore redundant relocation of X10(b)'s content.
**Required**: In the opening section, keep only the convention statement (resolution pinned to the pre-state `Σ`) and drop the "what makes self-transclusion well-defined" sentence; let X10(b) and the worked example carry the self-transclusion rationale.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
