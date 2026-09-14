# Arm B'' · `shunt-fixed`

`shunt-strict` (Spotify's hook with the offset/limit exception removed) plus one change to the worker path:
`scripts/bulk-read` sends each file with line numbers (`cat -n`) instead of bare text. Spotify's script sends
the bare file, so the worker's "Line N" claims are guesses (off by 14 to 23 lines in the second grid), and the
bulk-reader skill's last line tells the main model to verify line numbers before using them, which sends it back
into the file it was meant to avoid. This arm tests whether delegation pays once the summary can be trusted.
Everything else is identical to `shunt-strict`.
