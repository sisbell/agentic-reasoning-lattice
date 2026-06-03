# Channel Assignment — ASN-0071 review-75

**Date:** 2026-06-03 16:22

## Issue 1: Query section pre-states and defers the empty-source result
Reason: This is a pure editorial/structural fix — relocating a defensive justification, forward pointer, and pre-stated result out of *The query*. The content (admissibility of empty-source vspecs) is already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: The empty-source resolution is stated in three places
Reason: Deduplication of a fact already derived in *Resolution*. Deciding which instance is load-bearing is internal to the ASN's own structure; no external channel is required.

## Issue 3: Repetitive sibling-creation narration in the worked scenario
Reason: Editorial compression of repeated boilerplate discharge recitations. The discharge pattern and references are self-contained in the ASN's worked scenario; no channel needed.
