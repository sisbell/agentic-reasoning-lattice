# Review of ASN-0066

## REVISE

### Issue 1: D-CTG-depth lists incomplete dependencies
**ASN-0066, D-CTG-depth**: "(COROLLARY; from D-CTG, S8-fin)"
**Problem**: The statement refers to "depth m" — a single common depth for all positions in the subspace. That depth exists only because of S8-depth (ASN-0036), which guarantees all V-positions in a subspace share the same tumbler depth. Without S8-depth, the claim "all positions share components 2 through m − 1" has no well-defined m. S8-depth is invoked at the top of the ASN as context but is not listed in D-CTG-depth's formal dependencies or in the statement registry entry.
**Required**: Add S8-depth to D-CTG-depth's dependency list: "(COROLLARY; from D-CTG, S8-fin, S8-depth)". Update the registry row accordingly.

### Issue 2: D-SEQ derivation chain not shown
**ASN-0066, D-SEQ**: "Combining D-CTG-depth with D-MIN and S8-fin, we obtain the general form"
**Problem**: The premises are named but the chain is not shown. The critical missing step: D-CTG-depth establishes that components 2 through m−1 are *shared* across all positions, but does not determine their value. D-MIN establishes that the minimum position has those components equal to 1. The inference that therefore the shared value *is* 1 is nowhere stated — it is the step that bridges D-CTG-depth and D-MIN into D-SEQ's specific set characterization.
**Required**: Add the explicit derivation (3–4 sentences suffice):
1. By D-CTG-depth (m ≥ 3) or trivially (m = 2), all positions share components 2 through m−1.
2. By D-MIN, min(V_S(d)) = [S, 1, …, 1], so those shared components are 1.
3. All positions are therefore [S, 1, …, 1, k] for varying k. By D-CTG restricted to the last component, no gaps. By D-MIN, minimum k = 1. By S8-fin, maximum k = n for some finite n.

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG and D-MIN
**Why out of scope**: The ASN correctly identifies this as a verification obligation for each operation's ASN. DELETE, INSERT, COPY, and REARRANGE each require their own preservation argument — this is future work, not a gap in the current ASN.

VERDICT: REVISE
