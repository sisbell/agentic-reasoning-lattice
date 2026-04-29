# Validate-Revise — Acyclic Depends (Propose Only)

## Context

You are addressing a structural violation of invariant #8 from the Claim Document Contract:

> **Acyclic dependency graph.** The `depends` relation across all file pairs in the lattice is a DAG.

The validator found one or more cycles in the yaml `depends` graph. Breaking a cycle requires a semantic decision — which edge is wrong, and why — not a mechanical fix. You do NOT edit any file. You produce a proposal document for human review.

## Claim directory

{claim_dir}

## Cycles found

{findings_list}

## What to produce

For each cycle, produce a numbered section with:

1. **Cycle**: list the edges (e.g., `AllocatedSet → T9 → T8 → AllocatedSet`).
2. **Per-edge analysis**: for each edge `A → B` in the cycle, describe what claim A's yaml summary / markdown content says about its dependence on B. What is A using from B? Is that dependence genuinely structural (A's proof uses a fact from B) or is it an over-citation (A references B but doesn't actually depend on B's content)?
3. **Proposed resolutions**: enumerate the candidate edges to remove. For each, describe the consequence — what does A lose if it no longer cites B? What lemma or postcondition is now without support?
4. **Recommendation**: which edge do you recommend removing and why.

Do not edit any file. Output the proposal as the final text of your response.

## How to investigate

Use Read to examine each claim's yaml (for summary, depends list) and markdown (for how the dependence is actually used in the proof or axiom body). For each edge `A → B`, open A's markdown and search for where B is cited. The cite's context tells you what A really needs from B.

## On apparent false positives

Cycles are graph-level findings — hard to be false positives. But if the yaml `depends` lists you see don't actually form the cycle the validator reported (e.g., because yaml was edited since the validator ran), say so and stop.

## Tools

Read only. No edits. No file system changes. Your output is a document for human review.
