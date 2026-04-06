# Apply Patch to ASN

You are applying a targeted fix to a formalized ASN reasoning document.
The patch addresses a known issue identified during verification
(assembly validation, Dafny, Alloy, or proof review). Apply the fix
precisely and propagate any necessary downstream changes.

## Patch Instruction

{{patch_content}}

## Task

Read the ASN at `{{asn_path}}`.

Apply the changes described in the patch instruction:

1. **Apply the specific fix.** Make the exact changes described in the
   instruction. Do not interpret broadly — apply what is asked.

2. **Propagate downstream effects.** After applying the fix, check for
   references to the changed material elsewhere in the document:
   - Proofs that cite the changed property — update citations if needed
   - The property table — update status, dependencies, or statement
   - Formal contracts — update if the fix changes what the property
     establishes
   - Worked examples — update if they reference changed material

3. **Do NOT modify anything unrelated.** Only touch material directly
   affected by the patch instruction and its downstream references.
   Do not rephrase, reorder, or "improve" existing content.

4. **Do NOT remove content that appears after the formal contract.**
   Post-contract material (commentary, derived results, case analyses)
   is intentional and may be referenced by other ASNs.

5. **Do NOT rewrite the ASN from scratch.** Make targeted edits using
   the Edit tool. Preserve existing structure, notation, and reasoning.

Write the updated ASN back to `{{asn_path}}`.
