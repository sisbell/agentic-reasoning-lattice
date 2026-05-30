# Review of ASN-0042

## REVISE

### Issue 1: O7(c) omits the freshness gate (vii) from recursive-delegation obligations
**ASN-0042, O7 postcondition (c) and its proof**: "the delegation relation is satisfiable with `π'` as delegator for any sub-prefix `p''` (with `pfx(π') ≺ p''`) at every state at which (ii) `π'` remains the most-specific covering principal for `p''` ... and (vi) no existing principal has a prefix strictly extending `p''`."
**Problem**: The `delegated` predicate now carries **seven** conditions; condition (vii) (`pfx(π') ∉ Σ.B`, freshness) was added but O7(c) was not updated. The proof body addresses (i), (ii), (iv), (v), (vi) and never discharges (vii); the formal contract names only (ii) and (vi) as re-checking obligations. Yet (vii) is a genuine re-check: if `π'` has already baptized `p''` as an organizational namespace (entering it into `Σ.B`), it can never delegate `p''`. The worked example states exactly this ("Namespace baptism and principal baptism are mutually exclusive futures for the same prefix"), so O7(c)'s claim of a delegation right "for any sub-prefix `p''`" contradicts the ASN's own mechanism. The account-level chain witness (`π_k → π_{k+1}` with `pfx = [1,0,1,…,1]`) likewise never verifies `pfx(π_{k+1}) ∉ Σ.B` at each link.
**Required**: Add condition (vii) as a re-checking obligation in both the O7(c) prose and the formal contract, and discharge it for the chain witness (each `pfx(π_{k+1})` is fresh because it is the unique newly-baptized prefix at its step).

### Issue 2: O2 design justification misattributes exclusivity to `tumbleraccounteq`
**ASN-0042, O2, "Nelson uses the definite article…"**: "Gregory's predicate returns a boolean — true or false, with no provision for multiple true results from distinct principals. The system requires exactly one effective owner per address."
**Problem**: For a nested address `a` with `pfx(π_N) = [1] ≼ a` and `pfx(π_A) = [1,0,2] ≼ a`, the prefix/account predicate returns **true for both** distinct principals. Exclusivity is not a property of the predicate — it is supplied by the *longest-match selection rule* of O2 (Step 4). The cited implementation performs an account-level equality check against the single session account; it enumerates no registry and computes no longest match, so it cannot "confirm" O2's resolution rule. The sentence conflates "one effective owner" (a model theorem) with "predicate returns one true result" (false). This same overreach recurs at O8 ("`validaccount` is a stub… confirms") — the implementation confirms *absence of revocation*, not the longest-match exclusivity O8 actually rests on.
**Required**: Rephrase the O2 evidence to state that the predicate decides *containment* (which may hold for several nested principals), and that exclusivity comes from O2's longest-match rule — not from the boolean's arity. Audit the "Gregory confirms" claims at O2/O8 to match what the account-level predicate actually establishes.

### Issue 3 (anti-bloat): Preservation proofs of O1a, O1b, T4 are deferred far downstream
**ASN-0042, "The Account-Level Boundary" (O1a), the O1b statement, and the Delegation section**: O1a, O1b, and per-principal T4 are *stated* early (some flagged "derived invariant; ... preserved by Delegation cond. (iv)") but their inductive preservation proofs all live in the Delegation section, and NestingByDelegation defers O1b with "excluded by O1b (preserved across transitions — see below)."
**Problem**: Three invariants in three different sections all defer to one downstream location, and a reader following O1b at NestingByDelegation must skip to the Delegation section to confirm a load-bearing step. This is the forward-reference accretion the anti-bloat classifier targets.
**Required**: Either co-locate each invariant's statement with its preservation proof, or add a single explicit pointer block rather than scattered "see below" deferrals.

### Issue 4 (anti-bloat): Meta-prose explaining why (vii)/O18 exist rather than what they assert
**ASN-0042, Definition (delegated) and O18**: "Condition (vii) makes the predicate the complete admission gate: it carries the freshness requirement that O18 records on the post-state side, so that an admissible delegation is determined by the predicate alone."
**Problem**: This paragraph justifies *why* (vii) is needed and how it relates to O18, rather than stating what (vii) asserts. It is the "why the axiom is needed" pattern; combined with O18's own prose ("This is the address-side counterpart of O15") it produces two slots restating the (vii)/O18 coupling.
**Required**: Reduce to the assertion (`pfx(π') ∉ Σ.B` pre-state; `pfx(π') ∈ Σ'.B ∖ Σ.B` post-state) and state the coupling once.

### Issue 5 (anti-bloat): Repeated `acct(a)` definition and repeated `tumbleraccounteq` description
**ASN-0042, AccountField / AccountPrefix / O6 / Properties table; O1a section / Structural Provenance**: The `acct(a)` case definition is restated four times (AccountField prose, its Formal Contract, AccountPrefix's Formal Contract, the Properties table), and the `tumbleraccounteq` mantissa-walk description appears in both the O1a section and the Structural Provenance section in near-identical words.
**Problem**: "Two paragraphs in the same document say the same thing in different words" — verbatim restatement of a definition and of an implementation walkthrough is noise the precise reader routes around.
**Required**: Define `acct(a)` once (the Formal Contract slot), reference it elsewhere; keep the `tumbleraccounteq` description at one site.

## OUT_OF_SCOPE

### Topic 1: Whether account-level `tumbleraccounteq` enforcement matches model longest-match
The structural risk that an account-level predicate keyed on the second zero cannot distinguish a node-level principal (`zeros = 0`) from an account holder when resolving a delegated sub-account is an *enforcement* gap. The ASN correctly quarantines this in "Principal Identity and the Trust Boundary." It is real but belongs to enforcement/authentication, explicitly out of scope — except insofar as it makes the "Gregory confirms" claims overreach (Issue 2).

VERDICT: REVISE
