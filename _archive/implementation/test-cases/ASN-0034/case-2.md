# Test Cases — Example 2: T4 — Valid address and boundary violations

Source: vault/5-examples/{ASN label}/examples-1.md, Example 2

## TC-001: valid element address accepted
**Property:** T4 (valid case)
**Given:** addr = [1, 0, 3, 0, 2, 0, 1, 5]
**Assert:** t4(addr) == Valid

## TC-002: four zero-separators rejected
**Property:** T4 (at-most-three-zeros)
**Given:** addr = [1, 0, 3, 0, 2, 0, 1, 0]
**Assert:** t4(addr) == Invalid

## TC-003: adjacent zeros rejected
**Property:** T4 (structural conditions ↔ non-empty fields)
**Given:** addr = [1, 0, 0, 3]
**Assert:** t4(addr) == Invalid

## TC-004: leading zero rejected
**Property:** T4 (structural conditions ↔ non-empty fields)
**Given:** addr = [0, 1, 0, 3]
**Assert:** t4(addr) == Invalid

## TC-005: trailing zero rejected
**Property:** T4 (structural conditions ↔ non-empty fields)
**Given:** addr = [1, 0, 3, 0]
**Assert:** t4(addr) == Invalid

## TC-006: T3 holds for x₁
**Property:** T3 (canonical representation)
**Given:** addr = [1, 0, 0, 3]
**Assert:** t3(addr) == Valid

## TC-007: T3 holds for x₂
**Property:** T3 (canonical representation)
**Given:** addr = [0, 1, 0, 3]
**Assert:** t3(addr) == Valid

## TC-008: T3 holds for x₃
**Property:** T3 (canonical representation)
**Given:** addr = [1, 0, 3, 0]
**Assert:** t3(addr) == Valid

## TC-009: T3 holds for x₄
**Property:** T3 (canonical representation)
**Given:** addr = [1, 0, 3, 0, 2, 0, 1, 0]
**Assert:** t3(addr) == Valid

## TC-010: T3 holds for v
**Property:** T3 (canonical representation)
**Given:** addr = [1, 0, 3, 0, 2, 0, 1, 5]
**Assert:** t3(addr) == Valid