# Review of ASN-0043

## REVISE

### Issue 1: FSE under-justifies `home(a') = home(a)` — the exact inference L1c declares insufficient

**ASN-0043, FSE (FreshSiblingExistence), proof**: "*Apply CPP with `t₀ = a`, `p = #home(a)`: ... CPP yields that `a'` agrees with `a` on positions `1..#home(a)`, so `home(a') = home(a)`, whence `#E(a') = #E(a)`.*"

**Problem**: This concludes home preservation from agreement on positions `1..#home(a)` alone. But this ASN's own L1c "`s = home(a)`" argument explicitly establishes that agreement on `1..#s` does **not** pin the home document: "*This first invocation says nothing about position `#s + 1` ... agreement on `1..#s` alone would permit `a`'s third zero to fall at `#s + 2` or later.*" To fix `home(a')`, one must additionally pin the element-separator (third) zero at position `#home(a) + 1`. CPP with `p = #home(a)` covers positions `1..#home(a)` only and is silent on `#home(a) + 1` — precisely the position that determines where `a'`'s third zero sits and hence what `home(a')` is. The conclusion is true (because each `inc(·, 0)` modifies only the terminal position `#a`, and `#home(a) + 1 < #a` since `#E(a) ≥ 2` by L1b, so the separator zero is non-terminal and untouched), but that terminal-only fact is never invoked for this step. As written, FSE makes exactly the inference L1c spent a paragraph refuting.

**Required**: Either add the one-line observation that `inc(·, 0)` leaves position `#home(a) + 1 < #a` fixed (so `a'` inherits `a`'s separator zero there), or run the second CPP invocation on the post-`a` sub-chain as L1c does. Since `inc(·, 0)` agrees with `a` on every non-terminal position, the terminal-only fact alone settles `home(a') = home(a)` without CPP.

### Issue 2 (anti-bloat): L9 Case A re-derives L1c's two-CPP home-pinning argument instead of citing the L1c postcondition

**ASN-0043, L9 proof, Case A**: "*Freshness: every step from `t₁ = d.0.1` onward operates at length `> #d`, so CPP (with `t₀ = d`, `p = #d`) gives ... This first invocation is silent on position `#d + 1` ... We pin the third zero with a second CPP invocation: the opening child-spawn `k₁ = 2` seats a zero at position `#d + 1` ... CPP then yields `a_{#d+1} = (t₁)_{#d+1} = 0`. Combining the two invocations ... `home(a) = d`.*"

**Problem**: This is a verbatim-structure reproduction of L1c's "*Postcondition: `s = home(a)`*" argument (same two-CPP "first invocation is silent on `#s+1` / second invocation pins the third zero / combine to get `home = seed`" sequence), with `d` substituted for `s`. Case A constructs an explicit L1c-form chain seeded at `d` (`k₁ = 2`, `#tᵢ > #d` for all `i`), so `home(a) = d` is exactly L1c's `s = home(a)` postcondition instantiated at `s = d`. Re-running the two-CPP derivation duplicates a result the chain already carries. Two paragraphs in the same document execute the same argument in different words.

**Required**: Replace Case A's two-CPP block with a citation: the constructed chain is an L1c-form chain seeded at `d`, so L1c's `s = home(a)` postcondition gives `home(a) = d` directly; freshness then follows from the empty-set case hypothesis.

## OUT_OF_SCOPE

### Topic 1: Extending content-side disjointness beyond the `s_C`-resident slice
**Why out of scope**: L14/L14a are scoped to `dom(Σ.C)|_{s_C}` and the ASN itself flags the global-content-subspace-constant question as an Open Question. Closing it requires a content-side invariant that is new territory, not an error here.

VERDICT: REVISE
