# Channel Assignment — ASN-0058 review-17

**Date:** 2026-05-13 19:14

## Issue 1: M16's length formula has an off-by-one error
Reason: The fix is purely internal bookkeeping — reconciling M16's length equation with S7's definition of origin in ASN-0036, which is already cited in the proof. The reviewer has identified both valid fix paths (correct the equation or extend the notation to include the trailing separator); no design intent or implementation evidence is required.
