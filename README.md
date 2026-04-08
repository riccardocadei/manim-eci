# Presentation: *Exploratory Causal Inference in SAEnce* 

[Interactive slides](https://www.riccardocadei.com/manim-eci/presentation.html) for the oral presentation of [*Exploratory Causal Inference in SAEnce*](https://arxiv.org/abs/2510.14073) at [ICLR 2026](https://iclr.cc/) by Riccardo Cadei. Built with [Manim Community](https://www.manim.community/) and [manim-slides](https://github.com/jeertmans/manim-slides), the presentation renders animated scenes into a self-contained HTML slide deck.

## Reproduce the Presentation Locally

### 1. Set up the environment

Install [Conda](https://docs.conda.io/), then create an environment with the required packages:

```bash
conda create -n visualize python=3.11
conda activate visualize
pip install manim manim-slides[pyqt6]
```

> If your environment has a different name, tell the build script with `export CONDA_ENV=myenv`.

### 2. Render and open the slides

```bash
./build.sh                # render all scenes and open the presentation
```

The output is saved to `output/presentation.html`.

### 3. Optional commands

```bash
./build.sh s01            # render a single scene (e.g. s01) and open it
./build.sh s03 low        # choose quality: low | medium | high (default) | production | 4k
./build.sh html           # convert already-rendered scenes to HTML (skip rendering)
./build.sh clean          # remove all build artifacts (media/, slides/, output/)
```


## Reference

```bibtex
@inproceedings{mencattini2026exploratory,
  title     = {Exploratory Causal Inference in SAEnce},
  author    = {Tommaso Mencattini and Riccardo Cadei and Francesco Locatello},
  booktitle = {The Fourteenth International Conference on Learning Representations},
  year      = {2026},
  url       = {https://openreview.net/forum?id=Ml8t8kQMUP}
}
```
