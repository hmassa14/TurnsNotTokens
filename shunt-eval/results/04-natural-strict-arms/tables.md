## Summary across all tasks

### Mean per run, all tasks and variants

Runs per arm: A · stock = 12, B · shunt = 12, C · hook + Explore = 12, B' · shunt strict = 12, C' · Explore strict = 12

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 0.98 | 0.99 | 0.98 | 0.99 | 1.00 |
| Pass rate | 92% | 92% | 92% | 100% | 100% |
| Pass^k (all reps passed) | no (k=12) | no (k=12) | no (k=12) | yes (k=12) | yes (k=12) |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 593 | 364 | 325 | 74 | 125 |
| Lines read by subagent or worker | 0 | 0 | 191 | 0 | 173 |
| Tool calls | 5.9 | 8.2 | 9.9 | 11.2 | 8.8 |
| Reads, whole file | 0.8 | 0.8 | 1.0 | 0.9 | 1.7 |
| Reads, targeted | 0.7 | 2.0 | 1.6 | 0.6 | 0.5 |
| Reads blocked by hook | 0.0 | 0.5 | 0.3 | 1.2 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.2 | 0.2 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.2 | 0.0 | 0.2 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 60.6 | 56.8 | 56.2 | 67.5 | 59.3 |
| API requests | 6.8 | 9.1 | 10.8 | 11.0 | 9.6 |
| Longest API call (s) | 19.7 | 18.1 | 16.0 | 16.9 | 17.4 |
| Time in tools (s) | 11.0 | 2.5 | 2.3 | 2.3 | 2.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.161 | 0.177 | 0.177 | 0.217 | 0.192 |
| Main model ($) | 0.161 | 0.177 | 0.161 | 0.217 | 0.185 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.017 | 0.000 | 0.008 |
| Finding phase ($) | 0.033 | 0.034 | 0.037 | 0.035 | 0.030 |
| Answering phase ($) | 0.129 | 0.143 | 0.134 | 0.182 | 0.159 |
| Input tokens, uncached | 14 | 18 | 15 | 22 | 16 |
| Cache write tokens | 22,165 | 20,053 | 17,973 | 20,078 | 16,329 |
| Cache read tokens | 238,859 | 316,989 | 266,351 | 395,272 | 278,248 |
| Output tokens | 4,370 | 4,843 | 3,732 | 5,782 | 4,082 |
| Spotify-style tokens avoided | 0 | 0 | 671 | 0 | 0 |

## Per example

### D1 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 1,020 | 50 | 175 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 6.0 | 6.0 | 10.0 | 10.0 | 6.0 |
| Reads, whole file | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 1.0 | 3.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 70.3 | 69.8 | 59.8 | 71.3 | 54.9 |
| API requests | 6.0 | 7.0 | 11.0 | 11.0 | 7.0 |
| Longest API call (s) | 27.6 | 37.9 | 15.8 | 26.8 | 13.9 |
| Time in tools (s) | 0.7 | 3.5 | 0.8 | 0.6 | 1.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.184 | 0.133 | 0.192 | 0.191 | 0.156 |
| Main model ($) | 0.184 | 0.133 | 0.192 | 0.191 | 0.156 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.052 | 0.032 | 0.055 | 0.051 | 0.029 |
| Answering phase ($) | 0.132 | 0.101 | 0.136 | 0.140 | 0.128 |
| Input tokens, uncached | 12 | 14 | 22 | 22 | 14 |
| Cache write tokens | 29,579 | 11,547 | 20,273 | 13,989 | 17,851 |
| Cache read tokens | 197,290 | 215,242 | 380,342 | 351,292 | 231,556 |
| Output tokens | 6,205 | 5,259 | 5,687 | 6,428 | 3,830 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### D2 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 280 | 360 | 200 | 0 | 711 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 6.0 | 7.0 | 9.0 | 13.0 | 22.0 |
| Reads, whole file | 0.0 | 0.0 | 1.0 | 0.0 | 7.0 |
| Reads, targeted | 2.0 | 2.0 | 2.0 | 2.0 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 | 2.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 89.1 | 90.5 | 56.6 | 103.6 | 139.4 |
| API requests | 7.0 | 8.0 | 9.0 | 14.0 | 19.0 |
| Longest API call (s) | 47.4 | 24.0 | 16.7 | 22.2 | 41.9 |
| Time in tools (s) | 1.0 | 1.1 | 1.2 | 1.1 | 2.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.200 | 0.205 | 0.184 | 0.258 | 0.411 |
| Main model ($) | 0.200 | 0.205 | 0.184 | 0.258 | 0.411 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.030 | 0.029 | 0.029 | 0.029 |
| Answering phase ($) | 0.171 | 0.175 | 0.155 | 0.229 | 0.382 |
| Input tokens, uncached | 14 | 16 | 18 | 28 | 38 |
| Cache write tokens | 19,368 | 21,581 | 17,199 | 19,534 | 33,823 |
| Cache read tokens | 229,106 | 269,614 | 294,012 | 494,215 | 753,974 |
| Output tokens | 7,703 | 6,517 | 5,598 | 8,128 | 12,445 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### E1 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 230 | 220 | 230 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 3.0 | 3.0 | 3.0 | 5.0 | 2.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 12.9 | 16.2 | 9.6 | 18.8 | 8.7 |
| API requests | 4.0 | 4.0 | 4.0 | 6.0 | 3.0 |
| Longest API call (s) | 4.3 | 5.1 | 2.8 | 4.1 | 3.5 |
| Time in tools (s) | 0.1 | 0.1 | 0.2 | 0.2 | 0.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.076 | 0.078 | 0.078 | 0.087 | 0.060 |
| Main model ($) | 0.076 | 0.078 | 0.078 | 0.087 | 0.060 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.028 | 0.029 | 0.028 | 0.029 | 0.028 |
| Answering phase ($) | 0.047 | 0.049 | 0.050 | 0.058 | 0.032 |
| Input tokens, uncached | 8 | 8 | 8 | 12 | 6 |
| Cache write tokens | 11,580 | 11,681 | 11,583 | 9,942 | 9,382 |
| Cache read tokens | 118,086 | 118,271 | 117,528 | 177,355 | 85,814 |
| Output tokens | 573 | 734 | 769 | 1,154 | 492 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### E2 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 0 | 20 | 15 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 4.0 | 3.0 | 5.0 | 4.0 | 6.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 22.7 | 14.6 | 22.4 | 21.9 | 19.3 |
| API requests | 5.0 | 4.0 | 6.0 | 5.0 | 7.0 |
| Longest API call (s) | 7.4 | 4.7 | 4.7 | 5.4 | 3.9 |
| Time in tools (s) | 0.1 | 0.1 | 0.1 | 0.2 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.084 | 0.066 | 0.080 | 0.106 | 0.114 |
| Main model ($) | 0.084 | 0.066 | 0.080 | 0.106 | 0.114 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.030 | 0.028 | 0.030 | 0.029 |
| Answering phase ($) | 0.055 | 0.036 | 0.052 | 0.076 | 0.086 |
| Input tokens, uncached | 10 | 8 | 12 | 10 | 14 |
| Cache write tokens | 10,438 | 8,367 | 8,265 | 15,236 | 12,789 |
| Cache read tokens | 146,518 | 115,922 | 174,786 | 160,679 | 223,362 |
| Output tokens | 1,282 | 919 | 1,211 | 1,324 | 1,846 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### E3 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 110 | 90 | 100 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 3.0 | 3.0 | 3.0 | 4.0 | 5.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 1.0 | 1.0 | 0.0 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 16.2 | 15.0 | 15.8 | 16.5 | 17.6 |
| API requests | 4.0 | 4.0 | 4.0 | 5.0 | 6.0 |
| Longest API call (s) | 5.4 | 5.5 | 5.3 | 5.2 | 4.8 |
| Time in tools (s) | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.068 | 0.066 | 0.066 | 0.074 | 0.082 |
| Main model ($) | 0.068 | 0.066 | 0.066 | 0.074 | 0.082 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.029 | 0.028 | 0.029 | 0.028 |
| Answering phase ($) | 0.039 | 0.037 | 0.038 | 0.045 | 0.054 |
| Input tokens, uncached | 8 | 8 | 8 | 10 | 12 |
| Cache write tokens | 9,162 | 8,908 | 8,805 | 8,988 | 8,496 |
| Cache read tokens | 115,433 | 115,490 | 114,695 | 145,475 | 174,578 |
| Output tokens | 817 | 774 | 767 | 937 | 1,322 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### R1 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 771 | 655 | 0 | 108 | 0 |
| Lines read by subagent or worker | 0 | 0 | 879 | 0 | 771 |
| Tool calls | 2.0 | 10.0 | 8.0 | 15.0 | 7.0 |
| Reads, whole file | 1.0 | 1.0 | 3.0 | 2.0 | 2.0 |
| Reads, targeted | 0.0 | 4.0 | 0.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 1.0 | 0.0 | 1.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 39.1 | 77.8 | 100.2 | 70.3 | 69.9 |
| API requests | 3.0 | 11.0 | 11.0 | 16.0 | 10.0 |
| Longest API call (s) | 27.6 | 28.5 | 49.5 | 17.0 | 24.7 |
| Time in tools (s) | 0.2 | 2.7 | 0.9 | 1.2 | 0.9 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.113 | 0.204 | 0.169 | 0.285 | 0.159 |
| Main model ($) | 0.113 | 0.204 | 0.120 | 0.285 | 0.122 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.049 | 0.000 | 0.037 |
| Finding phase ($) | 0.031 | 0.050 | 0.050 | 0.056 | 0.039 |
| Answering phase ($) | 0.082 | 0.154 | 0.091 | 0.229 | 0.106 |
| Input tokens, uncached | 6 | 22 | 2 | 32 | 4 |
| Cache write tokens | 19,453 | 21,967 | 5,375 | 25,459 | 3,323 |
| Cache read tokens | 83,119 | 372,647 | 33,584 | 601,342 | 66,095 |
| Output tokens | 3,890 | 6,548 | 1,486 | 6,269 | 1,374 |
| Spotify-style tokens avoided | 0 | 0 | 8,052 | 0 | 0 |

### R2 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 0.96 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 617 | 434 | 616 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 3.0 | 12.0 | 7.0 | 10.0 | 7.0 |
| Reads, whole file | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 3.0 | 1.0 | 1.0 | 0.0 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 | 2.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 48.8 | 99.6 | 45.9 | 98.7 | 56.5 |
| API requests | 3.0 | 13.0 | 8.0 | 11.0 | 8.0 |
| Longest API call (s) | 37.4 | 27.4 | 16.0 | 18.9 | 14.8 |
| Time in tools (s) | 1.1 | 0.8 | 1.0 | 3.2 | 0.6 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.151 | 0.309 | 0.192 | 0.304 | 0.205 |
| Main model ($) | 0.151 | 0.309 | 0.192 | 0.304 | 0.205 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.031 | 0.056 | 0.050 | 0.030 | 0.038 |
| Answering phase ($) | 0.120 | 0.253 | 0.142 | 0.274 | 0.167 |
| Input tokens, uncached | 6 | 26 | 16 | 22 | 16 |
| Cache write tokens | 25,656 | 38,758 | 30,547 | 30,318 | 27,069 |
| Cache read tokens | 84,444 | 486,049 | 282,595 | 425,995 | 270,635 |
| Output tokens | 6,187 | 10,666 | 5,105 | 9,759 | 4,286 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### R3 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 0.87 | 1.00 | 0.85 | 0.90 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 1,412 | 1,361 | 1,533 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 1,302 |
| Tool calls | 19.0 | 16.0 | 21.0 | 20.0 | 12.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| Reads, targeted | 3.0 | 6.0 | 5.0 | 1.0 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 115.9 | 67.5 | 92.6 | 142.0 | 101.4 |
| API requests | 20.0 | 17.0 | 17.0 | 21.0 | 14.0 |
| Longest API call (s) | 16.9 | 13.5 | 18.2 | 26.9 | 23.7 |
| Time in tools (s) | 1.1 | 0.9 | 0.8 | 0.9 | 1.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.382 | 0.311 | 0.359 | 0.421 | 0.291 |
| Main model ($) | 0.382 | 0.311 | 0.359 | 0.421 | 0.235 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.056 |
| Finding phase ($) | 0.050 | 0.032 | 0.040 | 0.055 | 0.029 |
| Answering phase ($) | 0.332 | 0.279 | 0.320 | 0.367 | 0.238 |
| Input tokens, uncached | 40 | 34 | 34 | 42 | 2 |
| Cache write tokens | 42,200 | 39,135 | 48,054 | 33,617 | 2,827 |
| Cache read tokens | 880,438 | 682,871 | 691,155 | 850,389 | 41,499 |
| Output tokens | 9,159 | 6,787 | 9,297 | 11,671 | 2,256 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### R4 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 1,412 | 0 | 0 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 1,412 | 0 | 0 |
| Tool calls | 4.0 | 9.0 | 26.0 | 24.0 | 6.0 |
| Reads, whole file | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 |
| Reads, targeted | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| Reads blocked by hook | 0.0 | 2.0 | 0.0 | 3.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 25.4 | 30.7 | 100.6 | 61.3 | 22.0 |
| API requests | 5.0 | 9.0 | 29.0 | 11.0 | 6.0 |
| Longest API call (s) | 6.5 | 5.4 | 13.6 | 16.1 | 5.0 |
| Time in tools (s) | 0.2 | 0.5 | 0.7 | 1.1 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.135 | 0.122 | 0.209 | 0.203 | 0.099 |
| Main model ($) | 0.135 | 0.122 | 0.060 | 0.203 | 0.099 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.149 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.029 | 0.032 | 0.029 | 0.028 |
| Answering phase ($) | 0.107 | 0.092 | 0.138 | 0.173 | 0.071 |
| Input tokens, uncached | 10 | 18 | 2 | 22 | 12 |
| Cache write tokens | 28,862 | 10,927 | 2,455 | 16,527 | 10,752 |
| Cache read tokens | 174,118 | 278,877 | 30,173 | 365,132 | 177,131 |
| Output tokens | 1,989 | 3,001 | 691 | 6,350 | 2,041 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### W1 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 268 | 268 | 226 | 226 | 226 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 6.0 | 8.0 | 5.0 | 6.0 | 5.0 |
| Reads, whole file | 2.0 | 2.0 | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 147.3 | 65.3 | 30.4 | 41.9 | 31.2 |
| API requests | 7.0 | 9.0 | 6.0 | 7.0 | 6.0 |
| Longest API call (s) | 16.3 | 29.0 | 15.4 | 25.2 | 15.7 |
| Time in tools (s) | 104.2 | 0.3 | 0.6 | 0.2 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.134 | 0.172 | 0.117 | 0.159 | 0.125 |
| Main model ($) | 0.134 | 0.172 | 0.117 | 0.159 | 0.125 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.028 | 0.029 | 0.028 | 0.029 | 0.028 |
| Answering phase ($) | 0.106 | 0.143 | 0.089 | 0.130 | 0.097 |
| Input tokens, uncached | 14 | 18 | 12 | 14 | 12 |
| Cache write tokens | 16,705 | 17,447 | 14,301 | 15,832 | 13,615 |
| Cache read tokens | 227,911 | 293,988 | 185,905 | 222,195 | 185,295 |
| Output tokens | 3,850 | 6,041 | 3,583 | 5,147 | 3,329 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### W2 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 0.93 | 0.93 | 0.93 | 1.00 | 1.00 |
| Pass rate | 0% | 0% | 0% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 374 | 379 | 532 | 307 | 307 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 12.0 | 14.0 | 15.0 | 10.0 | 19.0 |
| Reads, whole file | 1.0 | 1.0 | 2.0 | 2.0 | 2.0 |
| Reads, targeted | 1.0 | 2.0 | 2.0 | 0.0 | 2.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 110.7 | 95.2 | 98.5 | 88.0 | 145.4 |
| API requests | 13.0 | 15.0 | 16.0 | 11.0 | 20.0 |
| Longest API call (s) | 21.5 | 17.7 | 17.3 | 18.8 | 41.7 |
| Time in tools (s) | 23.4 | 19.8 | 21.0 | 18.5 | 17.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.252 | 0.252 | 0.314 | 0.241 | 0.407 |
| Main model ($) | 0.252 | 0.252 | 0.314 | 0.241 | 0.407 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.028 | 0.029 | 0.051 | 0.029 | 0.028 |
| Answering phase ($) | 0.224 | 0.222 | 0.263 | 0.212 | 0.379 |
| Input tokens, uncached | 26 | 30 | 32 | 22 | 40 |
| Cache write tokens | 26,372 | 24,128 | 29,506 | 23,953 | 31,126 |
| Cache read tokens | 478,609 | 573,458 | 627,613 | 397,390 | 804,398 |
| Output tokens | 8,180 | 6,784 | 7,033 | 6,589 | 12,173 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

### W3 · natural prompt

| | A · stock | B · shunt | C · hook + Explore | B' · shunt strict | C' · Explore strict |
|---|---|---|---|---|---|
| **Performance** | | | | | |
| Score | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% | 100% | 100% |
| Lines read into main context | 617 | 526 | 270 | 252 | 252 |
| Lines read by subagent or worker | 0 | 0 | 0 | 0 | 0 |
| Tool calls | 3.0 | 7.0 | 7.0 | 13.0 | 8.0 |
| Reads, whole file | 1.0 | 1.0 | 1.0 | 2.0 | 2.0 |
| Reads, targeted | 0.0 | 3.0 | 3.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 | 2.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 1.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Latency** | | | | | |
| Wall clock (s) | 28.3 | 39.2 | 41.6 | 75.8 | 44.7 |
| API requests | 4.0 | 8.0 | 8.0 | 14.0 | 9.0 |
| Longest API call (s) | 18.4 | 18.6 | 16.5 | 15.7 | 14.9 |
| Time in tools (s) | 0.2 | 0.3 | 0.2 | 0.3 | 0.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Cost** | | | | | |
| Total, list price ($) | 0.159 | 0.202 | 0.166 | 0.277 | 0.200 |
| Main model ($) | 0.159 | 0.202 | 0.166 | 0.277 | 0.200 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.029 | 0.028 | 0.029 | 0.028 |
| Answering phase ($) | 0.130 | 0.173 | 0.138 | 0.247 | 0.172 |
| Input tokens, uncached | 8 | 16 | 16 | 28 | 18 |
| Cache write tokens | 26,603 | 26,185 | 19,315 | 27,542 | 24,897 |
| Cache read tokens | 131,239 | 281,442 | 263,829 | 551,804 | 324,633 |
| Output tokens | 2,599 | 4,089 | 3,551 | 5,626 | 3,593 |
| Spotify-style tokens avoided | 0 | 0 | 0 | 0 | 0 |

