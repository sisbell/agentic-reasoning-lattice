# Claim File Compression

You are cleaning up a formalization claim file that has accumulated
defensive prose from repeated review cycles. Strip the meta-commentary;
keep the substance. The math is sound; the presentation is not.

## REMOVE

Delete these without asking:

1. **Defensive scope language.** "This list is exhaustive," "each clause
   is in its stated scope," "explicitly endorses," "does not appear
   because..." — all instances.

2. **Inline citation tracking.** Prose listing use sites:
   - "as TumblerAdd's proof does at `0 + wₖ = wₖ`"
   - "T1, TA5, TA5a... at their successor-chain sites"
   - "invoked at twenty-two distinct sites"

   This belongs in the `Depends:` field. One line per dependency.

3. **Bundling justification.** "Bundled with closure because both
   statements concern..." — one sentence in the axiom body max;
   delete the rest.

4. **Naming-choice meta-explanation.** "`NatArithmeticClosureAndIdentity`
   signals that..." — the name speaks for itself.

5. **Nested parentheticals 3+ levels deep.** Flatten or split.

6. **Inline design-decision asides.** Mid-proof commentary about
   avoided operators or conventions in other files belongs in those
   files, not here.

## KEEP

- The claim statement
- The Derivation/Proof, every step
- The Formal Contract (Preconditions, Postconditions, Depends)
- Notation, labels, canonical names
- Genuine substance about why something is true (distinct from why
  it's structured this way)

## STRUCTURE

- **Preamble ≤ 2 sentences.** State what the claim IS. Do not justify
  structure.
- **Depends is the citation home.** One line per dependency: label,
  canonical name, brief phrase of what's used. No use-site enumeration.
- **Derivation is operational.** Each step: "from X, conclude Y by Z."
  No asides.

## OUTPUT

Produce the cleaned file content only. No summary, no code fences,
no commentary. If uncertain whether to remove something, remove it.
Bloat is the problem; brevity is the goal.

---

## The file to clean
