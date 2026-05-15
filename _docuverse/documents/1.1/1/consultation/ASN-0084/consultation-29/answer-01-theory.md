## Question 1 [theory]

> Did Nelson's design fix the text subspace at depth 2, or leave the depth operator-chosen subject only to m ≥ 2?

Looking at this carefully — the curated sources give partial information but don't definitively answer the fixed-vs-operator-chosen question. Let me check the raw pages on tumbler structure.

[Based on curated sources only:]

The curated sources establish the **basic structure** but not the formal degree of freedom:

**What is clear:**
- Within the Element/Contents field, Nelson distinguishes subspaces by leading digit: `1` for bytes (text), `2` for links
- Byte addresses take the form `N.0.U.0.D.V.0.1.position` 
- Link addresses take the form `N.0.U.0.D.V.0.2.N`

From the v-space-addresses curated source (4/30):
> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address."

The phrasing "**the** digit" (singular) suggests Nelson's primary description is two-digit: `subspace_selector.position` — so m=2 for text.

**What is suggestive of openness, but only for links:**

The curated links source quotes 4/31:
> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed."

Note: this "distinct possibility" language is applied to **links**, not to **text/bytes**. The curated sources show no parallel statement about subdividing text addresses below the position digit.

**Tentative answer:**
For text, Nelson appears to **fix** the structure at depth 2 (`0.1.position`) — the bytes are sequential and rearrangeable within Vstream, and "the digit after the one" implies a single position digit. For links he explicitly contemplated deeper structure. This is asymmetric.

NEED_RAW: 4/26-4/31 (raw pages 193-198) — to verify whether Nelson explicitly states the text subspace is fixed at depth 2 or whether he addresses the operator-chosen-depth question for bytes specifically. The curated extracts don't show a definitive statement either way for the text case; the link "distinct possibility" passage may or may not be intended to generalize.
