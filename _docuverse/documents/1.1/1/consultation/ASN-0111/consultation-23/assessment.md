# Channel Assignment — ASN-0111 review-23

**Date:** 2026-06-08 12:11

## Issue 1: Motivational section duplicates RL1/RL2/RL5 (anti-bloat)
Reason: Pure editorial reduction — the section restates RL1/RL2/RL5 already formalized in this ASN, and the surviving point (RL4 ownership) is likewise internal. No design intent or implementation evidence is needed to trim restatement.

## Issue 2: Open Question 2 is already answered by RL1 + RL8
Reason: The resolution is fully derivable from this ASN's own claims — RL1 returns distinct values (`∅` vs. recorded spans) and RL8 separates "unwitnessed" from "gone"; the only genuinely open part is resolution-level indistinguishability, which the ASN already scopes to FOLLOWLINK. Internal fix.
