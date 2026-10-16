# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s2** — 39 questions (36 single-answer, 3 multi-select). Random-guess baseline: **24.4%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_C | 31.4% | 80% | 30.0% |
| position_D | 31.4% | 80% | 30.0% |
| similar_twin_member | 30.9% | 65% | 28.6% |
| position_A | 28.2% | 79% | 27.4% |
| position_B | 27.6% | 81% | 27.0% |
| stem_keyword_overlap | 25.2% | 58% | 24.9% |
| longest_option | 23.6% | 100% | 23.6% |
| avoid_longest | 23.1% | 78% | 23.4% |
| shortest_option | 20.8% | 100% | 20.8% |
| odd_one_out | 11.8% | 100% | 11.8% |
| most_hedged | 10.4% | 11% | – |
| avoid_hedged | 31.2% | 11% | – |
| least_absolute | 17.6% | 12% | – |
| most_absolute | 47.1% | 12% | – |
| code_formatted_only | 26.3% | 9% | – |
| numeric_middle | 34.6% | 4% | – |
| largest_image_option | 6.8% | 22% | – |
| smallest_image_option | 25.0% | 22% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (7)

- `s2-q010` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 27 chars vs longest distractor 25, ratio 1.08) (in >=1 displayed pool variant)
- `s2-q018` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 101 chars vs longest distractor 78, ratio 1.29) (in >=1 displayed pool variant)
- `s2-q022` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 50 chars vs longest distractor 46, ratio 1.09) (in >=1 displayed pool variant)
- `s2-q023` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 61 chars vs longest distractor 60, ratio 1.02) (in >=1 displayed pool variant)
- `s2-q030` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 94 chars vs longest distractor 82, ratio 1.15) (in >=1 displayed pool variant)
- `s2-q036` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 109 chars vs longest distractor 99, ratio 1.10) (in >=1 displayed pool variant)
- `s2-q037` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 87 chars vs longest distractor 80, ratio 1.09) (in >=1 displayed pool variant)
