# Integrate Extension Claims into Base ASN

You are integrating claims from a converged extension ASN into its base
ASN's reasoning document. The extension claims have already been reviewed
and verified — your job is to place them appropriately in the base document.

## Extension ASN (claims to integrate)

{{ext_content}}

## Task

Read the base ASN at `{{base_path}}`.

Integrate the extension's claims into the base reasoning document:

1. **Place each claim in the right section.** Read the base ASN's structure
   and find where each claim belongs logically — after its dependencies,
   before anything that would use it, consistent with the document's flow.

2. **Preserve the claim's content.** Copy the formal statement, proof, and
   worked examples from the extension. Do not modify the mathematical content.
   Adapt formatting (section headings, transition prose) to fit the base
   document's style.

3. **Update the statement registry.** Add each integrated claim to the base
   ASN's registry table with status `introduced`.

4. **Update the date.** Add today's date ({{date}}) as a revision date in the
   header.

5. **Do NOT modify existing claims.** Only add the new ones. Do not
   rephrase, reorder, or "improve" existing content.

Write the updated base ASN back to `{{base_path}}` using the Edit tool.
Make targeted edits — do not rewrite the entire document.
