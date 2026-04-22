# Apply Patch to ASN

You are applying a targeted fix to an ASN's reasoning document based on specific
instructions. The patch addresses a known issue identified during review. Your job
is to apply the fix precisely and propagate any necessary downstream changes.

## Patch Instruction

{{patch_content}}

## Task

Read the ASN at `{{asn_path}}`.

Apply the changes described in the patch instruction:

1. **Apply the specific fix.** Make the exact changes described in the instruction.
   Do not interpret broadly — apply what is asked.

2. **Propagate downstream effects.** After applying the fix, check for references
   to the changed material elsewhere in the document:
   - Proofs that cite the changed claim — update citations if labels changed
   - The statement registry — update labels, wording, or status if affected
   - Worked examples that reference the changed material — update if needed
   - Transition prose that introduces the changed claim — adjust if needed

3. **Do NOT modify anything unrelated.** Only touch material directly affected
   by the patch instruction and its downstream references. Do not rephrase,
   reorder, or "improve" existing content that is not affected.

4. **Do NOT rewrite the ASN from scratch.** Make targeted edits using the Edit
   tool. Preserve the existing structure, notation, and reasoning where it is
   not affected by the patch.

Write the updated ASN back to `{{asn_path}}`.
