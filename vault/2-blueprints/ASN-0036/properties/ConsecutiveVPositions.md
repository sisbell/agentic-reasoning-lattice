**Definition (ConsecutiveVPositions).** Consecutive V-positions within a subspace differ only at the ordinal (last) component: under S8-depth, all positions in subspace `s` share components `v₁, ..., v_{m-1}`, so "next position" means incrementing `vₘ` alone. Formally, positions `s.x` and `s.(x+1)` are consecutive in the usual ordinal sense, and the notion is well-defined precisely because S8-depth guarantees uniform depth within each subspace.

*Contract:*

- *Label:* S8-depth(a)
- *Name:* ConsecutiveVPositions
- *Definition:* Consecutive V-positions within a subspace differ only at the ordinal (last) component; well-defined under uniform depth
- *Status:* introduced
- *Dependencies:* S8-depth (FixedDepthVPositions)
- *Notes:* —
