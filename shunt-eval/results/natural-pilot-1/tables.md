## Summary across all tasks

### Mean per run, all tasks and variants

Runs per arm: A · stock = 2, B · shunt = 2, C · hook + Explore = 2

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=2) | yes (k=2) | yes (k=2) |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 896 | 352 | 88 |
| Lines read by subagent or worker | 0 | 0 | 440 |
| Tool calls | 4.0 | 8.0 | 9.0 |
| Reads, whole file | 1.0 | 1.0 | 2.0 |
| Reads, targeted | 0.0 | 2.5 | 1.5 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 0.5 |
| Subagent or worker calls | 0.0 | 0.0 | 0.5 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 54.7 | 73.8 | 80.0 |
| API requests | 4.5 | 9.0 | 11.0 |
| Longest API call (s) | 27.6 | 33.2 | 32.6 |
| Time in tools (s) | 0.4 | 3.1 | 0.9 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.148 | 0.168 | 0.180 |
| Main model ($) | 0.148 | 0.168 | 0.156 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.025 |
| Finding phase ($) | 0.045 | 0.047 | 0.053 |
| Answering phase ($) | 0.103 | 0.121 | 0.114 |
| Input tokens, uncached | 9 | 18 | 12 |
| Cache write tokens | 24,516 | 16,757 | 12,824 |
| Cache read tokens | 140,204 | 293,944 | 206,963 |
| Output tokens | 5,048 | 5,904 | 3,586 |
| Spotify-style tokens avoided | 0 | 0 | 4,026 |

## Per example

### D1 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 1,020 | 50 | 175 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 6.0 | 6.0 | 10.0 |
| Reads, whole file | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 1.0 | 3.0 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 1.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 70.3 | 69.8 | 59.8 |
| API requests | 6.0 | 7.0 | 11.0 |
| Longest API call (s) | 27.6 | 37.9 | 15.8 |
| Time in tools (s) | 0.7 | 3.5 | 0.8 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.184 | 0.133 | 0.192 |
| Main model ($) | 0.184 | 0.133 | 0.192 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.052 | 0.032 | 0.055 |
| Answering phase ($) | 0.132 | 0.101 | 0.136 |
| Input tokens, uncached | 12 | 14 | 22 |
| Cache write tokens | 29,579 | 11,547 | 20,273 |
| Cache read tokens | 197,290 | 215,242 | 380,342 |
| Output tokens | 6,205 | 5,259 | 5,687 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### R1 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 771 | 655 | 0 |
| Lines read by subagent or worker | 0 | 0 | 879 |
| Tool calls | 2.0 | 10.0 | 8.0 |
| Reads, whole file | 1.0 | 1.0 | 3.0 |
| Reads, targeted | 0.0 | 4.0 | 0.0 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 1.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 39.1 | 77.8 | 100.2 |
| API requests | 3.0 | 11.0 | 11.0 |
| Longest API call (s) | 27.6 | 28.5 | 49.5 |
| Time in tools (s) | 0.2 | 2.7 | 0.9 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.113 | 0.204 | 0.169 |
| Main model ($) | 0.113 | 0.204 | 0.120 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.049 |
| Finding phase ($) | 0.039 | 0.062 | 0.050 |
| Answering phase ($) | 0.073 | 0.142 | 0.091 |
| Input tokens, uncached | 6 | 22 | 2 |
| Cache write tokens | 19,453 | 21,967 | 5,375 |
| Cache read tokens | 83,119 | 372,647 | 33,584 |
| Output tokens | 3,890 | 6,548 | 1,486 |
| Spotify-style tokens avoided | 0 | 0 | 8,052 |

