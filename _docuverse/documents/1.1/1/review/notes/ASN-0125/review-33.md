# Review of ASN-0125

This is a mature, logically sound note. I checked the operational contracts (EL6, EL7), the discipline-maintenance induction (EL-DM), the boundary constructions (EL9(2) de-listing at `j=1`/`j=n`/interior; EL10 position reuse; EL14(c) standoff), the `wp` result (EL0), and the worked example address-by-address — they hold. Directionality is consistent throughout (`F` = superseding/`new`, `G` = superseded/`old`; `succ = {(old, new)}`). The dependency between EL6(iii)'s active-at-birth and EL7(vi)'s discipline preservation is non-circular. Cross-ASN references are all to foundation ASNs (0034/0036/0043/0047/0086/0093/0098), so the self-containment rule is satisfied.

The findings below are remaining-prose and one induction-completeness item. None is a correctness gap, but the note carries `review-mode.anti-bloat`, and the patterns it names are present.

## REVISE

### Issue 1: Aphoristic restatements occupy claim and remark bodies
**ASN-0125, EL13 / EL16 / EDITop remarks / worked example**: e.g. EL13 "the trace knows, the state does not."; EL16 "the record retains the bytes and loses the literature — retention without correspondence" and "the past stays exact, and the future is reachable — as data, not as identity transfer"; the third EDITop remark "Under immutability, undo is just another statement."; worked example "The current view forgets; the record cannot."
**Problem**: Each restates a result the surrounding sentence has already proved (EL13's commutation, EL16's reference-survival contrast, the revert remark, EL11's two-regime split). They are essay content in structural slots — they encapsulate, they do not advance the argument — exactly the accretion the anti-bloat classifier targets. A precise reader skips them to reach the next claim.
**Required**: Drop the aphoristic closers; the technical sentence that precedes each already carries the content.

### Issue 2: Forward-reference deferral in EL2(b)
**ASN-0125, EL2(b)**: "A slot-borne record is expressible only *at birth* — an option we assess (and reject) below."
**Problem**: EL2(b)'s job is to close off "appended *later*" (done, via L12). The trailing clause pivots to a different option (slot *at* birth) only to defer its disposition to EL3. That rejection — RQ1 post-hoc assertability eliminating a birth-only carrier — is self-standing in EL3 and needs no advance signpost here. This is the forward-reference meta-prose the classifier flags.
**Required**: End EL2(b) at the in-place closure (slots fixed at birth ⇒ no later annotation). Let EL3/RQ1 carry the at-birth rejection without the "we assess (and reject) below" pointer.

### Issue 3: EL-DM's Nullify step justifies only the P1 target branch
**ASN-0125, EL-DM, Nullify step**: "Emits exactly one `[R]`-class tuple, with to-set `{(t, δ(1, #t))}` and `t ∈ dom(Σ.L)` — its unit-depth retraction schema (ASN-0086) — preserving clause (i)."
**Problem**: Df-LAY issues "`Nullify` (from ASN-0086)" unrestricted, and ASN-0086's Nullify precondition P-tgt admits a *self-emit* branch, `a = a_emit(Σ, d_retr)`, where the target is **not** in `dom(Σ.L)` — it equals the emitter and enters `dom(Σ'.L)`. For that branch the stated witness "`t ∈ dom(Σ.L)`" is false. The conclusion (clause (i) preserved) still holds — ASN-0086's schema reads membership "at the state in question," i.e. the post-state — but the induction step as written shows only the P1 branch of an operation the layer admits in both. By the show-each-case standard, the self-emit branch is unaddressed.
**Required**: Either restrict the editing layer's Nullify to P1 targets in Df-LAY, or add the self-emit branch to the EL-DM step (target `= a_emit(Σ, d_retr) =` the fresh emitter `∈ dom(Σ'.L)`, so clause (i) holds at the post-state by ASN-0086's "at the state in question" reading).

## OUT_OF_SCOPE

### Topic 1: The eight Open Questions
**Why out of scope**: They are correctly future-facing — cross-asserter retraction *authority* (placed in the ASN-0042 ownership layer by EL8(b), not derivable from `Σ`), span-level endset correspondence under endset-reshaping edits, stratification of claims-targeting-claims, non-empty-currency assertion disciplines, temporal witnesses beyond per-home order, registry-listing coupling, and subtype-family observation closure. Each is new territory, not a gap in this note's stated scope (links treated as opaque endpoints). No action.

META: not applicable — the note specifies state-relation structure (supersession as a typed link-to-link claim), operations on it (`assert_sup`, `editlink`), and their invariants (edit-discipline, monotone `succ_h`, set-valued `current`) at a level any implementation must satisfy; it has not drifted into implementation mechanics.

VERDICT: REVISE
