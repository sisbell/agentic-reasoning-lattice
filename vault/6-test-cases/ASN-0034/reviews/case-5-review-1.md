```
VERDICT: REVISE
```

### TC-010: assert is a bare inequality of two given literals — no function called

`d₁` and `d₂` are handed in as Given. Asserting `d₁ ≠ d₂` compares two different constants by inspection; nothing is executed and nothing can fail. Myers: "A test case that cannot be executed mechanically detects nothing."

**Fix:**
```
Assert: eq(d₁, d₂) = false
```

### TC-013: assert compares two calls instead of pinning the concrete value

The example states both documents share node field `[1]`. Asserting `node_field(d₁) = node_field(d₂)` would pass even if `node_field` returns the wrong value for both — it only checks agreement, not correctness.

**Fix:**
```
Assert: node_field(d₁) = [1]
```
(Add a companion `node_field(d₂) = [1]` or fold into one TC with two asserts.)

### TC-014: assert is inequality between two function calls — concrete expected values available

The example gives explicit values: `d₁ user=[1]`, `d₂ user=[2]`. Asserting `user_field(d₁) ≠ user_field(d₂)` would pass if the extractor returned any two distinct wrong values. Pin the values.

**Fix:**
```
Assert: user_field(d₁) = [1]
```
```
Assert: user_field(d₂) = [2]
```
(Split into two test cases, or expand TC-014 to two asserts.)