# Formalization Patch

Applies targeted fixes to formalized ASNs from downstream findings
(assembly validation, Dafny verification, Alloy checking, local review).

## Usage

1. Identify the issue from pipeline output (review files, error logs)
2. Write a patch file in `lattices/xanadu/discovery/patches/ASN-NNNN/`
3. Run the patch: `python scripts/formalize-patch.py NNNN --patch file.md`
4. Run the formalization pipeline to verify: `./run/formalize.sh --from dependency-review NNNN`

## Patch File Format

Free-form markdown describing what to fix. Be specific — name the
claim, quote the finding, state the required change. Example:

```markdown
# TA5 — add t' ∈ T postcondition

Assembly validation found: MISSING_POSTCONDITION — the proof establishes
t' ∈ T for both cases (k=0 and k>0) but the formal contract omits it.

Add `t' ∈ T` to the postconditions in TA5's formal contract.
```

## After Patching

Run the formalization pipeline to verify the fix didn't break anything:

```
./run/formalize.sh --from dependency-review NNNN
```

For multiple patches, batch them first, then run the pipeline once.
