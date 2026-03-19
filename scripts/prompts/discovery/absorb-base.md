# Integrate Extension Properties into Base ASN

You are integrating properties from a converged extension ASN into its base
ASN's reasoning document. The extension properties have already been reviewed
and verified — your job is to place them appropriately in the base document.

## Extension ASN (properties to integrate)

{{ext_content}}

## Task

Read the base ASN at `{{base_path}}`.

Integrate the extension's properties into the base reasoning document:

1. **Place each property in the right section.** Read the base ASN's structure
   and find where each property belongs logically — after its dependencies,
   before anything that would use it, consistent with the document's flow.

2. **Preserve the property's content.** Copy the formal statement, proof, and
   worked examples from the extension. Do not modify the mathematical content.
   Adapt formatting (section headings, transition prose) to fit the base
   document's style.

3. **Update the statement registry.** Add each integrated property to the base
   ASN's registry table with status `introduced`.

4. **Update the date.** Add today's date ({{date}}) as a revision date in the
   header.

5. **Do NOT modify existing properties.** Only add the new ones. Do not
   rephrase, reorder, or "improve" existing content.

Write the updated base ASN back to `{{base_path}}` using the Edit tool.
Make targeted edits — do not rewrite the entire document.
