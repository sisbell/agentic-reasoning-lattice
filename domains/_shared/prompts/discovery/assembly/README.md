# Discovery Assembly Prompts

These prompts operate on **discovery-stage ASNs** — narrative reasoning documents with claim tables but without formal contracts or structured proof sections.

## Prompts

### produce-statements.md

LLM-based extraction of formal statements from narrative prose. The ASN has a claim table (Label, Statement, Status) that serves as a roster — the LLM reads the surrounding prose for each claim and extracts just the formal math, stripping narrative, examples, and rationale.

Output: `formal-statements.md` in the ASN's manifests directory.

**Not for formalized ASNs.** Formalized ASNs have structured sections with formal contracts — use the mechanical assembly path (`formalization/assembly/produce-interface.md`) instead.
