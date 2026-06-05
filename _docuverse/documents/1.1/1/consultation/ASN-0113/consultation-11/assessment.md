# Channel Assignment — ASN-0113 review-11

**Date:** 2026-06-05 01:10

## Issue 1: Worked-instance reach annotations are dimensionally inconsistent at depth `m_S = 2`
Reason: This is a purely notational error derivable from the ASN's own W3 schema — at `m_S = 2` the interior `1,…,1` segment has length `m_S − 2 = 0`, so the canonical reach is `[S, 1+n_S]`; the note already states this general form and the depth-3 instance confirms the correct instantiation. No design intent or implementation evidence is needed.
