#!/usr/bin/env python3
"""Runner de tests sin depender de pytest."""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tests.test_paper_vectors as tv


def main() -> int:
    tests = [
        tv.test_pc1_matches_stallings_example,
        tv.test_odd_even_matches_table_iii,
        tv.test_round_keys_match_table_iv,
        tv.test_round_trip_security_block,
        tv.test_round_trip_hex_block,
        tv.test_round_trip_random_blocks,
        tv.test_all_keys_share_round_keys_after_odd_even,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"OK  {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
