# Update Source ASN After Absorb

You are updating a source ASN after its claims have been absorbed into a base
ASN's domain. Make targeted edits only. Do not rewrite the ASN from scratch.

## Context

Extension {{ext_label}} extracted claims from {{source_label}} and placed them
in {{base_label}}'s domain. The extension has been reviewed, converged, and exported.
Those claims now officially belong to {{base_label}}.

Your job: update {{source_label}} so it **cites** these claims instead of
deriving them locally.

## Extension ASN (what was extracted)

{{ext_content}}

## Claims to Convert to Citations

These claim labels were extracted: {{claim_labels}}

## Instructions

1. Read the source ASN at `{{source_path}}`

2. For each extracted claim, find its local derivation in the source ASN and replace
   the proof with a one-line citation. Keep the surrounding context that introduces or
   motivates the claim — just remove the proof block and worked examples.

   Before:
   ```
   **Lemma** (*Name*). [formal statement]

   *Proof.* [multi-paragraph proof]  ∎

   *Worked example.* [example]
   ```

   After:
   ```
   [Brief context sentence] ([new-label], {{base_label}}).
   ```

   The citation should preserve the formal statement inline where it helps readability.

3. Update the statement registry table. For each extracted claim:
   - Change the Label to match the extension's label if it was renamed
   - Add the base ASN reference in the Statement column
   - Change Status from `introduced` to `cited`

4. Do NOT modify any claim that is NOT in the extraction list.
   Do NOT change section headings, dates, or other content.
   Do NOT add or remove sections.

5. Write the updated ASN back to `{{source_path}}` using the Edit tool.
