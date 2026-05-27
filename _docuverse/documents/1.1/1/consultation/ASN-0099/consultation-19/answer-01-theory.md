## Question 1 [theory]

> Is reservation of link allocation to MAKELINK an architectural axiom of the design — such that K.μ⁺, K.μ⁻, and K.ρ are constitutionally forbidden from allocating links — or is it a convention that happens to hold but isn't axiomatic, leaving the substrate spec free to allow incidental link allocation by non-allocating operations?

**Position: design intent treats it as axiomatic, but I did not formalize it as such in the text.**

The convention is unambiguous in Literary Machines: MAKELINK is the only operation described as allocating a link, and it is explicit about returning the receipt — "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. **It returns the id of the link made.**" [LM 4/68]

The editing operations are described purely in content/arrangement terms with no link-allocation side effects. COPY is explicit transclusion: "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>" [LM 4/67] — it shares I-addresses with the source; no new links allocated. INSERT, DELETEVSPAN, REARRANGE, APPEND likewise make no mention of link IDs.

The framing of FEBE supports axiomatic treatment: "What the Xanadu storage and hypertext system does — and thus is — is defined by the commands to which it responds." [LM 4/61] Each command has a stated purpose; the clean separation IS the design.

**However**, I do not find in the curated sources an explicit prohibition clause ("only MAKELINK may allocate links"). The text describes what each operation does, not what each is forbidden from doing. "The links designated by a tumbler address are in their permanent order of arrival" [LM 4/31] implies sequential allocation but does not specify which operations may invoke it.

**My recommendation: axiomatize it.** Allowing K.μ⁺, K.μ⁻, K.ρ to incidentally allocate links violates the spirit of clean operational separation. Ownership becomes ambiguous (whose link, attached how?), the user can no longer reason about when allocation occurs, and "MAKELINK returns the id of the link made" stops being a complete account. The substrate spec should harden the convention into an axiom — that is the design intent even though I did not write it as a forbidden-from clause.

NEED_RAW: none — 4/61–4/79 (operations) and 4/31 (link addressing) in the curated sources are sufficient.
