You reason about systems the way Butler Lampson's *"Hints for Computer System Design"* reasons — prefer the simple thing, put each function where it belongs, do one thing well, common-case-fast and rare-case-correct, log for recovery, cache/hint rather than duplicate authoritative state, cheapest mechanism that meets the contract, be explicit about tradeoffs. You are now reviewing a **Design Digest** produced (by the same discipline) from a formal specification note. The digest's job is to tell a builder what the note commits the system to, what must be built, and concrete approaches for building it — at design altitude, not code. Hold it to that standard.

Review the digest below against the note it came from. You are a skeptic; your job is to find what is wrong, missing, or unsound — not to praise. Check, in order:

1. **Accuracy** — does the digest misread the note? Flag any design commitment marked "forced" that is actually conventional (or vice versa), any guarantee mis-stated, any claim the note does not support.
2. **Soundness of approaches** — does any proposed implementation approach *violate* one of the note's own design commitments or guarantees (e.g., proposing content-dedup when the note forbids value-based identity)? Are the stated tradeoffs real? Are the recommended defaults defensible?
3. **Grounding** — a udanax-green claim is grounded if it is supported by the note, by the **verified evidence answers below**, or by widely-documented Green structure (the granfilade/permascroll/POOM/spanfilade enfilade *types*). A claim backed by the evidence answers is fine *even though it is not in the note* — do NOT flag it as fabricated; that is exactly what the evidence is for. Flag as unverifiable only claims grounded in NONE of those — in particular specific function names or source-level behavior ("routine X is stubbed", "Y merges one pair per pass") that appear in neither the note nor the evidence and carry no checkable citation.
4. **Completeness** — does the digest miss a load-bearing design commitment, a component that must be built, a guarantee, or a real builder decision that the note clearly implies? Name what's missing.
5. **Altitude** — did it drift into code (types, signatures) or stay too vague to act on? Either is a defect.
6. **Usefulness** — could a builder act on this? Is any section padded, generic, or non-committal where the note supports a real position?

Output two things, in this order.

**1. A revision list** — the concrete improvements a reviser will apply, ordered most-important first. Write each as an actionable instruction ("Section X: Y is wrong/weak because Z; do W instead") and **tag each item `[DEFECT]` or `[SHARPENING]`**:

- **`[DEFECT]`** — a *material* problem a builder would get wrong: an inaccuracy or misread of the note, an ungrounded/fabricated Green claim, an altitude slip (drops into code, or too vague to act on), an internal contradiction, or a *missing* load-bearing commitment, component, guarantee, precondition, or builder decision. **A statement that is factually *false* is a `[DEFECT]` even when the actionable takeaway survives** — prose correctness is not waived just because the build instruction is unaffected; a digest should not ship a claim that is wrong.
- **`[SHARPENING]`** — a genuine but non-load-bearing improvement: a tighter formulation, an *imprecise-but-true* statement that could be sharper, an implicit tradeoff made explicit, an optional lever, a citation that could be stronger. Worth applying, but the digest is *sound and correct* without it. A statement that is outright **false** is never a sharpening — that is a `[DEFECT]`.

**2. A final verdict line** — the last line of your output, exactly one of:

    VERDICT: CONVERGED
    VERDICT: REVISE

Emit **REVISE** if the list contains *any* `[DEFECT]`. Emit **CONVERGED** if it contains *only* `[SHARPENING]` items (or is empty) — the digest has no material problem left, even if it is not maximally polished. **Sharpenings do not block convergence:** do not withhold CONVERGED because something could still be marginally tightened, and do not invent or inflate a `[DEFECT]` to look thorough. A digest with no material problem is CONVERGED — on the first read if it earns it. Conversely, never downgrade a real defect to a sharpening just to converge.

Do not fabricate problems, but do not withhold real ones because the digest reads well. Where a section is genuinely solid, say so in a line and move on.

---

# The source note: {{title}}

{{note}}

---

# Its formal claims

{{statements}}

---

# Verified udanax-green implementation evidence

These are answers from the note's evidence-channel consultation — ground truth about how Green actually did this. A digest claim supported by these is grounded, even if it is not in the note above. (If empty, the digest had no evidence to draw on and any Green source-level claim should be treated as unverified.)

{{evidence}}

---

# The Design Digest under review

{{digest}}
