# Sum up 23 November's world news in one image

A one-page newspaper front page for Monday 23 November 2026, drawn with
Python/PIL (`draw.py`) from stories verified against BBC World and Al Jazeera
reporting dated 23 November 2026.

## Layout

- **Date first, biggest type on the page:** MONDAY 23 NOVEMBER 2026.
- **Hero:** Ukrainian drones strike a Russian warship off Libya — Zelensky
  says the strikes sank the corvette Merkury and hit the cargo vessel
  Angara, spreading the war to the Mediterranean.
- **Three medium stories:** COP31 ends with no climate deal; Russian
  strikes kill 15 near Kyiv; Gaza now a "toxic wasteland", Oxfam says.
- **Four small stories:** Nvidia reinstates Jensen Huang; tankers ablaze
  in the Strait of Hormuz; Belgium cost-of-living strike; India pledges
  $1.6bn to Nepal.
- **Briefs:** eight more verified stories from the day, plus a sources
  line (BBC World · Al Jazeera).

No map, no invented stories, no garbled text: every line is drawn from
fixed strings, and the render is deterministic.

## Files

- `draw.py` — renders `entry.png` (1024×1024, deterministic).
- `entry.png` — the image itself.
- `main.ts` — Node 22, standard library only; copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` (default `/output`).

## Verify

```sh
python3 draw.py            # re-render entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
sha256sum entry.png out/entry.png   # the two hashes must match
```

## License

MIT — see `LICENSE`.
