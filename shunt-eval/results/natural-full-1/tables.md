## Summary across all tasks

### Mean per run, all tasks and variants

Runs per arm: A · stock = 12, B · shunt = 12, C · hook + Explore = 12

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 0.98 | 0.99 | 0.98 |
| Pass rate | 92% | 92% | 92% |
| Pass^k (all reps passed) | no (k=12) | no (k=12) | no (k=12) |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 593 | 364 | 325 |
| Lines read by subagent or worker | 0 | 0 | 191 |
| Tool calls | 5.9 | 8.2 | 9.9 |
| Reads, whole file | 0.8 | 0.8 | 1.0 |
| Reads, targeted | 0.7 | 2.0 | 1.6 |
| Reads blocked by hook | 0.0 | 0.5 | 0.3 |
| Hook bypassed via offset/limit | 0.0 | 0.2 | 0.2 |
| Subagent or worker calls | 0.0 | 0.0 | 0.2 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 60.6 | 56.8 | 56.2 |
| API requests | 6.8 | 9.1 | 10.8 |
| Longest API call (s) | 19.7 | 18.1 | 16.0 |
| Time in tools (s) | 11.0 | 2.5 | 2.3 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.161 | 0.177 | 0.177 |
| Main model ($) | 0.161 | 0.177 | 0.161 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.017 |
| Finding phase ($) | 0.034 | 0.036 | 0.038 |
| Answering phase ($) | 0.127 | 0.140 | 0.134 |
| Input tokens, uncached | 14 | 18 | 15 |
| Cache write tokens | 22,165 | 20,053 | 17,973 |
| Cache read tokens | 238,859 | 316,989 | 266,351 |
| Output tokens | 4,370 | 4,843 | 3,732 |
| Spotify-style tokens avoided | 0 | 0 | 671 |

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

### D2 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 280 | 360 | 200 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 6.0 | 7.0 | 9.0 |
| Reads, whole file | 0.0 | 0.0 | 1.0 |
| Reads, targeted | 2.0 | 2.0 | 2.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 89.1 | 90.5 | 56.6 |
| API requests | 7.0 | 8.0 | 9.0 |
| Longest API call (s) | 47.4 | 24.0 | 16.7 |
| Time in tools (s) | 1.0 | 1.1 | 1.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.200 | 0.205 | 0.184 |
| Main model ($) | 0.200 | 0.205 | 0.184 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.030 | 0.029 |
| Answering phase ($) | 0.171 | 0.175 | 0.155 |
| Input tokens, uncached | 14 | 16 | 18 |
| Cache write tokens | 19,368 | 21,581 | 17,199 |
| Cache read tokens | 229,106 | 269,614 | 294,012 |
| Output tokens | 7,703 | 6,517 | 5,598 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### E1 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 230 | 220 | 230 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.0 | 3.0 | 3.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 1.0 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 12.9 | 16.2 | 9.6 |
| API requests | 4.0 | 4.0 | 4.0 |
| Longest API call (s) | 4.3 | 5.1 | 2.8 |
| Time in tools (s) | 0.1 | 0.1 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.076 | 0.078 | 0.078 |
| Main model ($) | 0.076 | 0.078 | 0.078 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.037 | 0.038 | 0.037 |
| Answering phase ($) | 0.038 | 0.040 | 0.041 |
| Input tokens, uncached | 8 | 8 | 8 |
| Cache write tokens | 11,580 | 11,681 | 11,583 |
| Cache read tokens | 118,086 | 118,271 | 117,528 |
| Output tokens | 573 | 734 | 769 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### E2 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 0 | 20 | 15 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 4.0 | 3.0 | 5.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 0.0 | 1.0 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 22.7 | 14.6 | 22.4 |
| API requests | 5.0 | 4.0 | 6.0 |
| Longest API call (s) | 7.4 | 4.7 | 4.7 |
| Time in tools (s) | 0.1 | 0.1 | 0.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.084 | 0.066 | 0.080 |
| Main model ($) | 0.084 | 0.066 | 0.080 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.030 | 0.028 |
| Answering phase ($) | 0.055 | 0.036 | 0.052 |
| Input tokens, uncached | 10 | 8 | 12 |
| Cache write tokens | 10,438 | 8,367 | 8,265 |
| Cache read tokens | 146,518 | 115,922 | 174,786 |
| Output tokens | 1,282 | 919 | 1,211 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### E3 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 110 | 90 | 100 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.0 | 3.0 | 3.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 1.0 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 16.2 | 15.0 | 15.8 |
| API requests | 4.0 | 4.0 | 4.0 |
| Longest API call (s) | 5.4 | 5.5 | 5.3 |
| Time in tools (s) | 0.1 | 0.1 | 0.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.068 | 0.066 | 0.066 |
| Main model ($) | 0.068 | 0.066 | 0.066 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.029 | 0.028 |
| Answering phase ($) | 0.039 | 0.037 | 0.038 |
| Input tokens, uncached | 8 | 8 | 8 |
| Cache write tokens | 9,162 | 8,908 | 8,805 |
| Cache read tokens | 115,433 | 115,490 | 114,695 |
| Output tokens | 817 | 774 | 767 |
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

### R2 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 617 | 434 | 616 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.0 | 12.0 | 7.0 |
| Reads, whole file | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 3.0 | 1.0 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 1.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 48.8 | 99.6 | 45.9 |
| API requests | 3.0 | 13.0 | 8.0 |
| Longest API call (s) | 37.4 | 27.4 | 16.0 |
| Time in tools (s) | 1.1 | 0.8 | 1.0 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.151 | 0.309 | 0.192 |
| Main model ($) | 0.151 | 0.309 | 0.192 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.031 | 0.056 | 0.050 |
| Answering phase ($) | 0.120 | 0.253 | 0.142 |
| Input tokens, uncached | 6 | 26 | 16 |
| Cache write tokens | 25,656 | 38,758 | 30,547 |
| Cache read tokens | 84,444 | 486,049 | 282,595 |
| Output tokens | 6,187 | 10,666 | 5,105 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### R3 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 0.87 | 1.00 | 0.85 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 1,412 | 1,361 | 1,533 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 19.0 | 16.0 | 21.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 3.0 | 6.0 | 5.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 115.9 | 67.5 | 92.6 |
| API requests | 20.0 | 17.0 | 17.0 |
| Longest API call (s) | 16.9 | 13.5 | 18.2 |
| Time in tools (s) | 1.1 | 0.9 | 0.8 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.382 | 0.311 | 0.359 |
| Main model ($) | 0.382 | 0.311 | 0.359 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.050 | 0.032 | 0.040 |
| Answering phase ($) | 0.332 | 0.279 | 0.320 |
| Input tokens, uncached | 40 | 34 | 34 |
| Cache write tokens | 42,200 | 39,135 | 48,054 |
| Cache read tokens | 880,438 | 682,871 | 691,155 |
| Output tokens | 9,159 | 6,787 | 9,297 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### R4 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 1,412 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 1,412 |
| Tool calls | 4.0 | 9.0 | 26.0 |
| Reads, whole file | 2.0 | 2.0 | 2.0 |
| Reads, targeted | 0.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 2.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 1.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 25.4 | 30.7 | 100.6 |
| API requests | 5.0 | 9.0 | 29.0 |
| Longest API call (s) | 6.5 | 5.4 | 13.6 |
| Time in tools (s) | 0.2 | 0.5 | 0.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.135 | 0.122 | 0.209 |
| Main model ($) | 0.135 | 0.122 | 0.060 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.149 |
| Finding phase ($) | 0.029 | 0.038 | 0.032 |
| Answering phase ($) | 0.107 | 0.084 | 0.138 |
| Input tokens, uncached | 10 | 18 | 2 |
| Cache write tokens | 28,862 | 10,927 | 2,455 |
| Cache read tokens | 174,118 | 278,877 | 30,173 |
| Output tokens | 1,989 | 3,001 | 691 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### W1 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 268 | 268 | 226 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 6.0 | 8.0 | 5.0 |
| Reads, whole file | 2.0 | 2.0 | 1.0 |
| Reads, targeted | 0.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 147.3 | 65.3 | 30.4 |
| API requests | 7.0 | 9.0 | 6.0 |
| Longest API call (s) | 16.3 | 29.0 | 15.4 |
| Time in tools (s) | 104.2 | 0.3 | 0.6 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.134 | 0.172 | 0.117 |
| Main model ($) | 0.134 | 0.172 | 0.117 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.028 | 0.029 | 0.028 |
| Answering phase ($) | 0.106 | 0.143 | 0.089 |
| Input tokens, uncached | 14 | 18 | 12 |
| Cache write tokens | 16,705 | 17,447 | 14,301 |
| Cache read tokens | 227,911 | 293,988 | 185,905 |
| Output tokens | 3,850 | 6,041 | 3,583 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### W2 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 0.93 | 0.93 | 0.93 |
| Pass rate | 0% | 0% | 0% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 374 | 379 | 532 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 12.0 | 14.0 | 15.0 |
| Reads, whole file | 1.0 | 1.0 | 2.0 |
| Reads, targeted | 1.0 | 2.0 | 2.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 110.7 | 95.2 | 98.5 |
| API requests | 13.0 | 15.0 | 16.0 |
| Longest API call (s) | 21.5 | 17.7 | 17.3 |
| Time in tools (s) | 23.4 | 19.8 | 21.0 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.252 | 0.252 | 0.314 |
| Main model ($) | 0.252 | 0.252 | 0.314 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.028 | 0.029 | 0.051 |
| Answering phase ($) | 0.224 | 0.222 | 0.263 |
| Input tokens, uncached | 26 | 30 | 32 |
| Cache write tokens | 26,372 | 24,128 | 29,506 |
| Cache read tokens | 478,609 | 573,458 | 627,613 |
| Output tokens | 8,180 | 6,784 | 7,033 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### W3 · natural prompt

| | A · stock | B · shunt | C · hook + Explore |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Found target file | 100% | 100% | 100% |
| Lines read into main context | 617 | 526 | 270 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.0 | 7.0 | 7.0 |
| Reads, whole file | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 3.0 | 3.0 |
| Reads blocked by hook | 0.0 | 1.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 1.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 28.3 | 39.2 | 41.6 |
| API requests | 4.0 | 8.0 | 8.0 |
| Longest API call (s) | 18.4 | 18.6 | 16.5 |
| Time in tools (s) | 0.2 | 0.3 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.159 | 0.202 | 0.166 |
| Main model ($) | 0.159 | 0.202 | 0.166 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.029 | 0.029 | 0.028 |
| Answering phase ($) | 0.130 | 0.173 | 0.138 |
| Input tokens, uncached | 8 | 16 | 16 |
| Cache write tokens | 26,603 | 26,185 | 19,315 |
| Cache read tokens | 131,239 | 281,442 | 263,829 |
| Output tokens | 2,599 | 4,089 | 3,551 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

