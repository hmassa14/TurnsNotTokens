## Summary across all tasks

### Mean per run, all tasks and variants

Runs per arm: A · stock = 57, B' · shunt strict = 57

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 0.98 | 0.98 |
| Pass rate | 96% | 98% |
| Pass^k (all reps passed) | no (k=57) | no (k=57) |
| Found target file | 95% | 95% |
| Lucky passes (right answer, target never found) | 5% | 5% |
| Target content into main context, any tool (tokens, chars/4) | 6,068 | 3,291 |
| Lines read into main context (Read only) | 475 | 59 |
| Lines read by subagent or worker | 2 | 6 |
| Tool calls | 6.5 | 8.8 |
| Reads, whole file | 1.0 | 0.9 |
| Reads, targeted | 0.7 | 1.1 |
| Reads blocked by hook | 0.0 | 1.5 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.2 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 46.6 | 68.2 |
| API requests | 7.1 | 9.1 |
| Longest API call (s) | 14.8 | 14.3 |
| Time in tools (s) | 5.9 | 18.3 |
| Time in worker or subagent (s) | 0.0 | 10.0 |
| **Cost** | | |
| Total, list price ($) | 0.140 | 0.162 |
| Main model ($) | 0.140 | 0.153 |
| Worker or subagent ($) | 0.000 | 0.008 |
| Finding phase ($) | 0.028 | 0.027 |
| Answering phase ($) | 0.112 | 0.126 |
| Input tokens, uncached | 14 | 18 |
| Cache write tokens | 20,245 | 17,313 |
| Cache read tokens | 243,872 | 311,979 |
| Output tokens | 3,585 | 4,493 |
| Spotify-style tokens avoided | 730 | 2,006 |

## Per example

### CT1 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 2,581 | 2,767 |
| Lines read into main context (Read only) | 268 | 226 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 5.0 | 12.0 |
| Reads, whole file | 2.0 | 1.0 |
| Reads, targeted | 0.0 | 1.0 |
| Reads blocked by hook | 0.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 39.8 | 87.8 |
| API requests | 6.0 | 13.0 |
| Longest API call (s) | 18.3 | 31.2 |
| Time in tools (s) | 0.3 | 25.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.109 | 0.221 |
| Main model ($) | 0.109 | 0.221 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.020 |
| Answering phase ($) | 0.089 | 0.201 |
| Input tokens, uncached | 12 | 26 |
| Cache write tokens | 14,564 | 22,107 |
| Cache read tokens | 187,846 | 463,099 |
| Output tokens | 3,508 | 7,356 |
| Spotify-style tokens avoided | 0 | 0 |

### CT2 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 0.93 | 1.00 |
| Pass rate | 0% | 100% |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 3,067 | 3,067 |
| Lines read into main context (Read only) | 542 | 307 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 12.0 | 11.0 |
| Reads, whole file | 2.0 | 2.0 |
| Reads, targeted | 2.0 | 2.0 |
| Reads blocked by hook | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 103.4 | 85.2 |
| API requests | 13.0 | 12.0 |
| Longest API call (s) | 18.9 | 35.3 |
| Time in tools (s) | 26.2 | 0.8 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.235 | 0.239 |
| Main model ($) | 0.235 | 0.239 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.021 |
| Answering phase ($) | 0.215 | 0.218 |
| Input tokens, uncached | 26 | 24 |
| Cache write tokens | 28,512 | 24,751 |
| Cache read tokens | 498,293 | 429,255 |
| Output tokens | 6,376 | 9,101 |
| Spotify-style tokens avoided | 0 | 0 |

### CT3 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 819 | 763 |
| Lines read into main context (Read only) | 108 | 108 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 4.0 | 2.0 |
| Reads, whole file | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 23.5 | 7.7 |
| API requests | 5.0 | 3.0 |
| Longest API call (s) | 11.0 | 2.4 |
| Time in tools (s) | 0.1 | 0.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.069 | 0.041 |
| Main model ($) | 0.069 | 0.041 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.050 | 0.030 |
| Answering phase ($) | 0.019 | 0.011 |
| Input tokens, uncached | 10 | 6 |
| Cache write tokens | 9,366 | 7,990 |
| Cache read tokens | 148,256 | 84,036 |
| Output tokens | 1,579 | 425 |
| Spotify-style tokens avoided | 0 | 0 |

### HM1 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 3,826 | 3,605 |
| Lines read into main context (Read only) | 243 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 3.0 | 5.7 |
| Reads, whole file | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 2.7 |
| Reads blocked by hook | 0.0 | 2.7 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 11.7 | 17.3 |
| API requests | 4.0 | 6.7 |
| Longest API call (s) | 3.4 | 3.3 |
| Time in tools (s) | 0.2 | 0.3 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.061 | 0.085 |
| Main model ($) | 0.061 | 0.085 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.020 |
| Answering phase ($) | 0.041 | 0.065 |
| Input tokens, uncached | 8 | 13 |
| Cache write tokens | 11,984 | 12,915 |
| Cache read tokens | 118,910 | 201,627 |
| Output tokens | 699 | 1,221 |
| Spotify-style tokens avoided | 0 | 0 |

### HM2 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 2,957 | 1,765 |
| Lines read into main context (Read only) | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 4.0 | 7.3 |
| Reads, whole file | 0.0 | 0.0 |
| Reads, targeted | 0.0 | 1.7 |
| Reads blocked by hook | 0.0 | 1.7 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 17.0 | 26.1 |
| API requests | 5.0 | 8.3 |
| Longest API call (s) | 5.0 | 4.8 |
| Time in tools (s) | 0.2 | 0.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.075 | 0.100 |
| Main model ($) | 0.075 | 0.100 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.021 | 0.021 |
| Answering phase ($) | 0.054 | 0.079 |
| Input tokens, uncached | 10 | 17 |
| Cache write tokens | 12,367 | 11,542 |
| Cache read tokens | 152,294 | 257,933 |
| Output tokens | 1,366 | 1,969 |
| Spotify-style tokens avoided | 0 | 0 |

### HM3 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 1,833 | 3,065 |
| Lines read into main context (Read only) | 70 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 3.7 | 5.0 |
| Reads, whole file | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 2.0 |
| Reads blocked by hook | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 15.7 | 19.8 |
| API requests | 4.7 | 6.0 |
| Longest API call (s) | 4.8 | 4.6 |
| Time in tools (s) | 0.2 | 0.3 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.059 | 0.078 |
| Main model ($) | 0.059 | 0.078 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.021 |
| Answering phase ($) | 0.039 | 0.058 |
| Input tokens, uncached | 9 | 12 |
| Cache write tokens | 9,270 | 12,200 |
| Cache read tokens | 136,625 | 180,224 |
| Output tokens | 891 | 1,191 |
| Spotify-style tokens avoided | 0 | 0 |

### HM4 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 12,969 | 3,784 |
| Lines read into main context (Read only) | 1,058 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 8.7 | 15.3 |
| Reads, whole file | 1.0 | 1.0 |
| Reads, targeted | 0.7 | 1.3 |
| Reads blocked by hook | 0.0 | 2.3 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 97.8 | 171.1 |
| API requests | 9.7 | 16.3 |
| Longest API call (s) | 40.8 | 25.8 |
| Time in tools (s) | 2.7 | 46.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.256 | 0.283 |
| Main model ($) | 0.256 | 0.283 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.025 | 0.032 |
| Answering phase ($) | 0.232 | 0.251 |
| Input tokens, uncached | 19 | 33 |
| Cache write tokens | 33,870 | 23,303 |
| Cache read tokens | 405,700 | 614,112 |
| Output tokens | 9,035 | 10,214 |
| Spotify-style tokens avoided | 0 | 0 |

### HM5 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 9,487 | 7,583 |
| Lines read into main context (Read only) | 795 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 7.0 | 12.0 |
| Reads, whole file | 0.7 | 0.3 |
| Reads, targeted | 1.3 | 1.7 |
| Reads blocked by hook | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.3 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 93.1 | 111.6 |
| API requests | 8.0 | 13.0 |
| Longest API call (s) | 33.9 | 33.0 |
| Time in tools (s) | 1.4 | 1.9 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.221 | 0.264 |
| Main model ($) | 0.221 | 0.264 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.022 | 0.022 |
| Answering phase ($) | 0.200 | 0.243 |
| Input tokens, uncached | 16 | 26 |
| Cache write tokens | 29,741 | 26,439 |
| Cache read tokens | 301,819 | 461,617 |
| Output tokens | 8,657 | 10,575 |
| Spotify-style tokens avoided | 0 | 6,209 |

### ND1 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 1,251 | 597 |
| Lines read into main context (Read only) | 22 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 3.3 | 5.0 |
| Reads, whole file | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 1.7 |
| Reads blocked by hook | 0.0 | 1.7 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 19.6 | 22.0 |
| API requests | 4.3 | 6.0 |
| Longest API call (s) | 4.1 | 4.2 |
| Time in tools (s) | 1.4 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.057 | 0.069 |
| Main model ($) | 0.057 | 0.069 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.030 |
| Answering phase ($) | 0.037 | 0.039 |
| Input tokens, uncached | 9 | 12 |
| Cache write tokens | 8,787 | 8,281 |
| Cache read tokens | 126,659 | 177,162 |
| Output tokens | 1,004 | 1,290 |
| Spotify-style tokens avoided | 0 | 0 |

### ND2 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 1,209 | 2,328 |
| Lines read into main context (Read only) | 0 | 0 |
| Lines read by subagent or worker | 43 | 0 |
| Tool calls | 6.0 | 4.0 |
| Reads, whole file | 0.3 | 0.0 |
| Reads, targeted | 0.7 | 0.3 |
| Reads blocked by hook | 0.0 | 0.3 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.7 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 38.2 | 23.2 |
| API requests | 7.7 | 5.0 |
| Longest API call (s) | 10.0 | 8.2 |
| Time in tools (s) | 1.2 | 1.3 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.118 | 0.076 |
| Main model ($) | 0.118 | 0.076 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.031 | 0.041 |
| Answering phase ($) | 0.087 | 0.035 |
| Input tokens, uncached | 4 | 10 |
| Cache write tokens | 5,447 | 11,898 |
| Cache read tokens | 59,011 | 153,573 |
| Output tokens | 634 | 1,593 |
| Spotify-style tokens avoided | 13,874 | 0 |

### ND3 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 33% | 67% |
| Lucky passes (right answer, target never found) | 67% | 33% |
| Target content into main context, any tool (tokens, chars/4) | 467 | 705 |
| Lines read into main context (Read only) | 42 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 5.0 | 2.7 |
| Reads, whole file | 0.0 | 0.0 |
| Reads, targeted | 0.7 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 22.0 | 22.7 |
| API requests | 6.0 | 3.7 |
| Longest API call (s) | 5.6 | 10.2 |
| Time in tools (s) | 2.1 | 1.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.074 | 0.061 |
| Main model ($) | 0.074 | 0.061 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.008 | 0.031 |
| Answering phase ($) | 0.066 | 0.030 |
| Input tokens, uncached | 12 | 7 |
| Cache write tokens | 9,508 | 9,348 |
| Cache read tokens | 182,184 | 105,386 |
| Output tokens | 1,351 | 1,661 |
| Spotify-style tokens avoided | 0 | 0 |

### ND4 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 67% | 33% |
| Lucky passes (right answer, target never found) | 33% | 67% |
| Target content into main context, any tool (tokens, chars/4) | 1,464 | 1,577 |
| Lines read into main context (Read only) | 50 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 6.0 | 6.0 |
| Reads, whole file | 0.0 | 0.3 |
| Reads, targeted | 1.0 | 0.3 |
| Reads blocked by hook | 0.0 | 0.3 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 33.4 | 29.3 |
| API requests | 7.0 | 7.0 |
| Longest API call (s) | 11.4 | 6.9 |
| Time in tools (s) | 1.3 | 2.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.100 | 0.099 |
| Main model ($) | 0.100 | 0.099 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.038 | 0.019 |
| Answering phase ($) | 0.062 | 0.079 |
| Input tokens, uncached | 14 | 14 |
| Cache write tokens | 11,610 | 11,324 |
| Cache read tokens | 224,541 | 246,016 |
| Output tokens | 2,598 | 2,117 |
| Spotify-style tokens avoided | 0 | 0 |

### SB1 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 10,689 | 3,900 |
| Lines read into main context (Read only) | 617 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 4.3 | 9.3 |
| Reads, whole file | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 1.0 |
| Reads blocked by hook | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 1.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 41.4 | 128.8 |
| API requests | 5.0 | 10.0 |
| Longest API call (s) | 20.4 | 22.8 |
| Time in tools (s) | 1.9 | 57.6 |
| Time in worker or subagent (s) | 0.0 | 54.7 |
| **Cost** | | |
| Total, list price ($) | 0.154 | 0.246 |
| Main model ($) | 0.154 | 0.199 |
| Worker or subagent ($) | 0.000 | 0.047 |
| Finding phase ($) | 0.029 | 0.034 |
| Answering phase ($) | 0.125 | 0.166 |
| Input tokens, uncached | 10 | 20 |
| Cache write tokens | 29,265 | 22,394 |
| Cache read tokens | 174,960 | 345,249 |
| Output tokens | 4,597 | 7,408 |
| Spotify-style tokens avoided | 0 | 8,349 |

### SB2 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 0.90 | 0.90 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 5,770 | 3,352 |
| Lines read into main context (Read only) | 461 | 240 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 10.0 | 6.7 |
| Reads, whole file | 2.0 | 2.3 |
| Reads, targeted | 0.0 | 0.3 |
| Reads blocked by hook | 0.0 | 0.7 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 48.3 | 28.8 |
| API requests | 8.3 | 6.0 |
| Longest API call (s) | 14.4 | 10.9 |
| Time in tools (s) | 2.8 | 1.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.141 | 0.099 |
| Main model ($) | 0.141 | 0.099 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.050 | 0.030 |
| Answering phase ($) | 0.092 | 0.068 |
| Input tokens, uncached | 17 | 12 |
| Cache write tokens | 18,240 | 13,937 |
| Cache read tokens | 272,750 | 195,280 |
| Output tokens | 4,105 | 2,496 |
| Spotify-style tokens avoided | 0 | 0 |

### SB3 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 0.82 | 0.82 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 2,958 | 1,624 |
| Lines read into main context (Read only) | 242 | 126 |
| Lines read by subagent or worker | 0 | 116 |
| Tool calls | 7.0 | 6.7 |
| Reads, whole file | 2.7 | 2.7 |
| Reads, targeted | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.3 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 31.4 | 42.1 |
| API requests | 6.0 | 5.3 |
| Longest API call (s) | 10.3 | 16.9 |
| Time in tools (s) | 1.9 | 1.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.099 | 0.109 |
| Main model ($) | 0.099 | 0.109 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.024 | 0.023 |
| Answering phase ($) | 0.075 | 0.086 |
| Input tokens, uncached | 12 | 6 |
| Cache write tokens | 13,929 | 9,355 |
| Cache read tokens | 187,477 | 89,757 |
| Output tokens | 2,659 | 1,976 |
| Spotify-style tokens avoided | 0 | 413 |

### SB4 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 0.96 | 1.00 |
| Pass rate | 67% | 100% |
| Pass^k (all reps passed) | no (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 2,563 | 2,720 |
| Lines read into main context (Read only) | 189 | 189 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 8.3 | 6.0 |
| Reads, whole file | 2.0 | 2.0 |
| Reads, targeted | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 70.6 | 71.0 |
| API requests | 8.0 | 5.7 |
| Longest API call (s) | 11.4 | 15.2 |
| Time in tools (s) | 38.2 | 39.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.129 | 0.104 |
| Main model ($) | 0.129 | 0.104 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.027 | 0.021 |
| Answering phase ($) | 0.103 | 0.083 |
| Input tokens, uncached | 16 | 11 |
| Cache write tokens | 17,388 | 16,223 |
| Cache read tokens | 273,100 | 181,823 |
| Output tokens | 3,100 | 2,670 |
| Spotify-style tokens avoided | 0 | 0 |

### SC1 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 9,106 | 8,339 |
| Lines read into main context (Read only) | 771 | 36 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 5.7 | 14.3 |
| Reads, whole file | 1.0 | 1.3 |
| Reads, targeted | 0.0 | 2.0 |
| Reads blocked by hook | 0.0 | 3.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 1.3 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 55.6 | 148.9 |
| API requests | 6.7 | 15.0 |
| Longest API call (s) | 20.2 | 18.1 |
| Time in tools (s) | 7.0 | 71.1 |
| Time in worker or subagent (s) | 0.0 | 67.4 |
| **Cost** | | |
| Total, list price ($) | 0.146 | 0.293 |
| Main model ($) | 0.146 | 0.243 |
| Worker or subagent ($) | 0.000 | 0.050 |
| Finding phase ($) | 0.035 | 0.030 |
| Answering phase ($) | 0.111 | 0.213 |
| Input tokens, uncached | 13 | 30 |
| Cache write tokens | 23,096 | 25,979 |
| Cache read tokens | 232,421 | 552,532 |
| Output tokens | 4,213 | 6,754 |
| Spotify-style tokens avoided | 0 | 9,217 |

### SC2 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 0.96 | 0.84 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 11,801 | 5,948 |
| Lines read into main context (Read only) | 1,267 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 18.3 | 16.3 |
| Reads, whole file | 0.3 | 0.0 |
| Reads, targeted | 5.0 | 1.7 |
| Reads blocked by hook | 0.0 | 1.7 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 88.4 | 101.0 |
| API requests | 19.3 | 17.3 |
| Longest API call (s) | 21.6 | 17.0 |
| Time in tools (s) | 1.8 | 3.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.356 | 0.305 |
| Main model ($) | 0.356 | 0.305 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.055 | 0.051 |
| Answering phase ($) | 0.301 | 0.255 |
| Input tokens, uncached | 39 | 35 |
| Cache write tokens | 39,926 | 28,655 |
| Cache read tokens | 820,699 | 662,721 |
| Output tokens | 9,170 | 10,098 |
| Spotify-style tokens avoided | 0 | 0 |

### SC3 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 14,066 | 2,451 |
| Lines read into main context (Read only) | 1,412 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 4.0 | 13.0 |
| Reads, whole file | 2.0 | 1.3 |
| Reads, targeted | 0.0 | 0.7 |
| Reads blocked by hook | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 27.3 | 42.7 |
| API requests | 4.0 | 9.7 |
| Longest API call (s) | 10.5 | 8.6 |
| Time in tools (s) | 0.7 | 1.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 |
| **Cost** | | |
| Total, list price ($) | 0.128 | 0.139 |
| Main model ($) | 0.128 | 0.139 |
| Worker or subagent ($) | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.021 |
| Answering phase ($) | 0.108 | 0.117 |
| Input tokens, uncached | 8 | 19 |
| Cache write tokens | 29,601 | 14,197 |
| Cache read tokens | 136,316 | 316,361 |
| Output tokens | 2,707 | 3,984 |
| Spotify-style tokens avoided | 0 | 0 |

### SC4 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 0.99 |
| Pass rate | 100% | 67% |
| Pass^k (all reps passed) | yes (k=3) | no (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 9,868 | 4,581 |
| Lines read into main context (Read only) | 617 | 0 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 3.0 | 8.3 |
| Reads, whole file | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 1.3 |
| Reads blocked by hook | 0.0 | 2.3 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 1.0 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 23.9 | 71.5 |
| API requests | 4.0 | 9.3 |
| Longest API call (s) | 14.9 | 21.1 |
| Time in tools (s) | 0.3 | 21.2 |
| Time in worker or subagent (s) | 0.0 | 18.8 |
| **Cost** | | |
| Total, list price ($) | 0.119 | 0.185 |
| Main model ($) | 0.119 | 0.165 |
| Worker or subagent ($) | 0.000 | 0.020 |
| Finding phase ($) | 0.020 | 0.021 |
| Answering phase ($) | 0.099 | 0.144 |
| Input tokens, uncached | 8 | 19 |
| Cache write tokens | 26,609 | 20,388 |
| Cache read tokens | 131,766 | 302,161 |
| Output tokens | 2,599 | 5,352 |
| Spotify-style tokens avoided | 0 | 8,513 |

### SC5 · natural prompt

| | A · stock | B' · shunt strict |
|---|---|---|
| **Performance** | | |
| Score | 1.00 | 1.00 |
| Pass rate | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 10,854 | 2,401 |
| Lines read into main context (Read only) | 870 | 310 |
| Lines read by subagent or worker | 0 | 0 |
| Tool calls | 9.7 | 15.3 |
| Reads, whole file | 2.7 | 3.0 |
| Reads, targeted | 0.0 | 1.7 |
| Reads blocked by hook | 0.0 | 2.7 |
| Hook bypassed via offset/limit | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.7 |
| Re-read after delegation | 0.0 | 0.0 |
| **Latency** | | |
| Wall clock (s) | 93.6 | 157.5 |
| API requests | 9.3 | 14.0 |
| Longest API call (s) | 22.0 | 17.9 |
| Time in tools (s) | 37.3 | 88.4 |
| Time in worker or subagent (s) | 0.0 | 50.1 |
| **Cost** | | |
| Total, list price ($) | 0.224 | 0.306 |
| Main model ($) | 0.224 | 0.264 |
| Worker or subagent ($) | 0.000 | 0.042 |
| Finding phase ($) | 0.033 | 0.027 |
| Answering phase ($) | 0.191 | 0.237 |
| Input tokens, uncached | 19 | 28 |
| Cache write tokens | 36,529 | 32,286 |
| Cache read tokens | 418,208 | 558,609 |
| Output tokens | 4,902 | 7,169 |
| Spotify-style tokens avoided | 0 | 5,423 |

