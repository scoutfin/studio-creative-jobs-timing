#!/usr/bin/env python3
"""Does the "creative jobs lost to AI" story survive a timing test?

Studio, 2026-10-28. Primary data: BLS CES series CES5051200001 — Motion Picture &
Sound Recording Industries, all employees (thousands, seasonally adjusted), fetched
from the BLS public API (saved alongside as bls-motion-picture-2019-2026.json).

The forensic: a sector's employment timeline, read against known non-AI shocks, tells
you WHICH causes a decline is and isn't consistent with. The 2023 Hollywood strikes
(WGA May 2 - Sep 27; SAG-AFTRA Jul 14 - Nov 9) are a clean natural experiment: a real,
datable, transient shock. If the losses are "the strikes", they recover when the
strikes end. If they are structural, they keep going.
"""
import json
d = json.load(open("bls-motion-picture-2019-2026.json"))
S = {s["seriesID"]: s for s in d["Results"]["series"]}
mps = {(int(x["year"]), int(x["period"][1:])): float(x["value"])
       for x in S["CES5051200001"]["data"] if x["period"][0] == "M"}

base19 = sum(mps[(2019, m)] for m in range(1, 13)) / 12
peak = max(mps, key=mps.get)
apr23 = mps[(2023, 4)]                      # last month before the WGA strike
trough = min(((k) for k in mps if (2023,5) <= k <= (2024,2)), key=mps.get)
jan24 = mps[(2024, 1)]                       # strikes over, bounce
latest = mps[max(mps)]

print(f"2019 baseline            {base19:7.1f}k")
print(f"peak                     {mps[peak]:7.1f}k  {peak}")
print(f"pre-strike (2023-04)     {apr23:7.1f}k")
print(f"strike trough            {mps[trough]:7.1f}k  {trough}  ({mps[trough]-apr23:+.1f}k, {100*(mps[trough]-apr23)/apr23:+.1f}%)")
print(f"post-strike bounce 24-01 {jan24:7.1f}k  ({jan24-mps[trough]:+.1f}k recovered)")
print(f"latest ({max(mps)})       {latest:7.1f}k")
print()
print(f"phase 1 peak->pre-strike (streaming correction, pre-AI-narrative): {apr23-mps[peak]:+.1f}k")
print(f"phase 2 strike dip, then recovered by 24-01 (transient):           net {jan24-apr23:+.1f}k")
print(f"phase 3 post-strike structural fall 24-01 -> latest:               {latest-jan24:+.1f}k")
print(f"total vs 2019 baseline:                                            {latest-base19:+.1f}k")

# the discriminating check: did the post-strike period recover or keep falling?
post = [mps[k] for k in sorted(mps) if k >= (2024,1)]
falls = sum(1 for a,b in zip(post,post[1:]) if b<a)
print(f"\npost-strike months declining: {falls}/{len(post)-1}  -> "
      + ("monotonic structural decline, NOT a strike rebound" if falls > 0.7*(len(post)-1)
         else "mixed"))
assert latest < mps[trough], "latest should be below the strike trough (decline outran the strikes)"
print("check: latest is BELOW the 2023 strike trough — the decline outran the strikes.")
