**Definition (CorrespondenceRun).** A *correspondence run* is a triple `(v, a, n)` with `n ≥ 1` such that

`M(d)(v + k) = a + k` for all `0 ≤ k < n`

where `v` is a V-position, `a` is an I-address, and `+` denotes ordinal displacement (with the `k = 0` identity from **Definition (OrdinalDisplacementExtension)**). The triple captures a contiguous block of the arrangement in which ordinal displacement in V-space maps exactly to ordinal displacement in I-space. Correspondence runs are the atoms of the span decomposition (S8).

*Contract:*

- *Label:* S8-depth(c)
- *Name:* CorrespondenceRun
- *Definition:* Triple `(v, a, n)` with `n ≥ 1` such that `M(d)(v + k) = a + k` for all `0 ≤ k < n`
- *Status:* introduced
- *Dependencies:* S8-depth(b) (OrdinalDisplacementExtension)
- *Notes:* Atoms of span decomposition. See S8-depth-C1 for depth/prefix uniformity within a run.
</content>
</parameters>
</tool_call>

<tool_result>
File written to vault/2-blueprints/ASN-0036/properties/S8-depth.md
</tool_result>
