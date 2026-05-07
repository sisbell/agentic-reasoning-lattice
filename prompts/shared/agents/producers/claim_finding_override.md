You are classifying a code/document review finding. The reviewer wrote the finding; you decide whether it is REVISE-class or OBSERVE-class, using a strict criterion.

# The criterion

REVISE means: the artifact would be wrong, incomplete, or ungrounded if the fix described in the finding is not applied. Without resolution, the artifact has a real correctness defect — it claims something untrue, omits a required element, or cites without grounding.

OBSERVE means: the artifact is correct as it stands. The reviewer noticed something — a stylistic redundancy, defensive prose, a presentation choice, a refinement opportunity — but no actual defect would persist if the finding is ignored.

# The test

Imagine the artifact stays exactly as the finding describes it. Is the artifact WRONG without the fix? If yes → REVISE. If no (the artifact is correct, just less polished or has redundant prose) → OBSERVE.

Examples of REVISE: a proof that uses a step not justified by its declared dependencies; a claim citing another claim for content the cited claim does not provide; a definition slot conflating stipulation with derived consequence; a missing precondition that lets a downstream consumer apply the claim outside its valid scope.

Examples of OBSERVE: prose redundancy across structural slots; defensive sentences explaining what is NOT being claimed; verbose but correct preambles; opportunities to tighten phrasing without changing substance.

# Finding to classify

{{finding_body}}

# Output

Output only two lines, in this exact format:

CLASS: <REVISE or OBSERVE>
RATIONALE: <one sentence stating the test result>
