# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s2** — 26 questions (23 single-answer, 3 multi-select). Random-guess baseline: **25.0%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_A | 39.0% | 78% | 35.9% |
| similar_twin_member | 43.0% | 56% | 35.1% |
| position_C | 33.3% | 78% | 31.5% |
| position_B | 32.8% | 80% | 31.2% |
| avoid_longest | 25.4% | 99% | 25.4% |
| stem_keyword_overlap | 24.8% | 78% | 24.8% |
| position_D | 23.1% | 75% | 23.5% |
| shortest_option | 19.8% | 100% | 19.8% |
| longest_option | 19.2% | 100% | 19.2% |
| odd_one_out | 7.5% | 100% | 7.5% |
| most_hedged | 10.4% | 17% | – |
| avoid_hedged | 31.2% | 17% | – |
| least_absolute | 23.1% | 14% | – |
| most_absolute | 30.8% | 14% | – |
| code_formatted_only | 26.7% | 11% | – |
| numeric_middle | 34.6% | 6% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (6)

- `s2-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 27 chars vs longest distractor 25, ratio 1.08) (in >=1 displayed pool variant)
- `s2-q018` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 101 chars vs longest distractor 78, ratio 1.29) (in >=1 displayed pool variant)
- `s2-q022` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 50 chars vs longest distractor 46, ratio 1.09) (in >=1 displayed pool variant)
- `s2-q023` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 61 chars vs longest distractor 60, ratio 1.02) (in >=1 displayed pool variant)
- `s2-q024` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 61 chars vs longest distractor 49, ratio 1.24) (in >=1 displayed pool variant)
- `s2-q030` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 94 chars vs longest distractor 82, ratio 1.15) (in >=1 displayed pool variant)
