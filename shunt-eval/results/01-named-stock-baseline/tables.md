## Summary across all tasks

### Mean per run, all tasks and variants

Runs per arm: A · stock = 2, B · shunt = 0, C · hook + Explore = 0

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 |  |  |
| Pass rate | 100% |  |  |
| Pass^k (all reps passed) | yes (k=2) |  |  |
| Found target file | 100% |  |  |
| Lines read into main context | 896 |  |  |
| Lines read by subagent or worker | 0 |  |  |
| Tool calls | 1.5 |  |  |
| Reads, whole file | 1.0 |  |  |
| Reads, targeted | 0.0 |  |  |
| Reads blocked by hook | 0.0 |  |  |
| Hook bypassed via offset/limit | 0.0 |  |  |
| Subagent or worker calls | 0.0 |  |  |
| Re-read after delegation | 0.0 |  |  |
| **Latency** | | | |
| Wall clock (s) | 45.1 |  |  |
| API requests | 2.5 |  |  |
| Longest API call (s) | 37.8 |  |  |
| Time in tools (s) | 0.4 |  |  |
| Time in worker or subagent (s) | 0.0 |  |  |
| **Cost** | | | |
| Total, list price ($) | 0.163 |  |  |
| Main model ($) | 0.163 |  |  |
| Worker or subagent ($) | 0.000 |  |  |
| Finding phase ($) | 0.074 |  |  |
| Answering phase ($) | 0.090 |  |  |
| Input tokens, uncached | 5 |  |  |
| Cache write tokens | 33,394 |  |  |
| Cache read tokens | 56,294 |  |  |
| Output tokens | 4,242 |  |  |
| Spotify-style tokens avoided | 0 |  |  |

## Per example

### D1 · named prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 |  |  |
| Pass rate | 100% |  |  |
| Found target file | 100% |  |  |
| Lines read into main context | 1,020 |  |  |
| Lines read by subagent or worker | 0 |  |  |
| Tool calls | 1.0 |  |  |
| Reads, whole file | 1.0 |  |  |
| Reads, targeted | 0.0 |  |  |
| Reads blocked by hook | 0.0 |  |  |
| Hook bypassed via offset/limit | 0.0 |  |  |
| Subagent or worker calls | 0.0 |  |  |
| Re-read after delegation | 0.0 |  |  |
| **Latency** | | | |
| Wall clock (s) | 52.8 |  |  |
| API requests | 2.0 |  |  |
| Longest API call (s) | 47.1 |  |  |
| Time in tools (s) | 0.1 |  |  |
| Time in worker or subagent (s) | 0.0 |  |  |
| **Cost** | | | |
| Total, list price ($) | 0.125 |  |  |
| Main model ($) | 0.125 |  |  |
| Worker or subagent ($) | 0.000 |  |  |
| Finding phase ($) | 0.029 |  |  |
| Answering phase ($) | 0.097 |  |  |
| Input tokens, uncached | 4 |  |  |
| Cache write tokens | 23,531 |  |  |
| Cache read tokens | 53,225 |  |  |
| Output tokens | 4,741 |  |  |
| Spotify-style tokens avoided | 0 |  |  |

### R1 · named prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 |  |  |
| Pass rate | 100% |  |  |
| Found target file | 100% |  |  |
| Lines read into main context | 771 |  |  |
| Lines read by subagent or worker | 0 |  |  |
| Tool calls | 2.0 |  |  |
| Reads, whole file | 1.0 |  |  |
| Reads, targeted | 0.0 |  |  |
| Reads blocked by hook | 0.0 |  |  |
| Hook bypassed via offset/limit | 0.0 |  |  |
| Subagent or worker calls | 0.0 |  |  |
| Re-read after delegation | 0.0 |  |  |
| **Latency** | | | |
| Wall clock (s) | 37.4 |  |  |
| API requests | 3.0 |  |  |
| Longest API call (s) | 28.4 |  |  |
| Time in tools (s) | 0.7 |  |  |
| Time in worker or subagent (s) | 0.0 |  |  |
| **Cost** | | | |
| Total, list price ($) | 0.202 |  |  |
| Main model ($) | 0.202 |  |  |
| Worker or subagent ($) | 0.000 |  |  |
| Finding phase ($) | 0.119 |  |  |
| Answering phase ($) | 0.083 |  |  |
| Input tokens, uncached | 6 |  |  |
| Cache write tokens | 43,258 |  |  |
| Cache read tokens | 59,364 |  |  |
| Output tokens | 3,744 |  |  |
| Spotify-style tokens avoided | 0 |  |  |

