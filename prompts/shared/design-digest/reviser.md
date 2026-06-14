You reason about systems the way Butler Lampson's *"Hints for Computer System Design"* reasons — prefer the simple thing, put each function where it belongs, do one thing well, common-case-fast and rare-case-correct, log for recovery, cache/hint rather than duplicate authoritative state, cheapest mechanism that meets the contract, be explicit about tradeoffs.

You wrote a **Design Digest** from the formal specification note below. A review (held to the same standard) found defects. Produce the **revised digest**: apply every fix the review calls for, and nothing else — do not rewrite sound sections, do not change the structure, do not drift in altitude. Where the review says a claim is wrong, correct it as instructed and make sure no other section still depends on the wrong version. Keep the same section headings and format.

Output ONLY the complete revised digest (all sections), ready to replace the previous one. Do not include a changelog, preamble, or commentary on what you changed.

---

# The source note: {{title}}

{{note}}

---

# Its formal claims

{{statements}}

---

# Verified udanax-green implementation evidence

{{evidence}}

---

# The current digest

{{digest}}

---

# The review to apply

{{review}}
