# Presentation: Exploratory Causal Inference in SAEnce 

Interactive slides for the oral presentation of *Exploratory Causal Inference in SAEnce* at ICLR 2026.

[[ICLR]](https://openreview.net/forum?id=BFMCkJbJXx) [[arXiv]](https://arxiv.org/abs/2510.14073) [[Presentation]](https://www.riccardocadei.com/manim-eci/presentation.html)

Built with [Manim Community](https://www.manim.community/) and [manim-slides](https://github.com/jeertmans/manim-slides), the presentation renders animated scenes into a self-contained HTML slide deck.

## Citation

```bibtex
@inproceedings{mencattini2026exploratory,
  title     = {Exploratory Causal Inference in SAEnce},
  author    = {Tommaso Mencattini and Riccardo Cadei and Francesco Locatello},
  booktitle = {The Fourteenth International Conference on Learning Representations},
  year      = {2026},
  url       = {https://openreview.net/forum?id=BFMCkJbJXx}
}
```

## Build

**Prerequisites:** [Conda](https://docs.conda.io/) with an environment containing `manim` and `manim-slides`.

By default the build script uses a conda environment called `visualize`. Set the `CONDA_ENV` variable to use a different one:

```bash
export CONDA_ENV=myenv
```

```bash
# Render all scenes and open the full presentation
./build.sh

# Render a single scene (e.g. s01) and open it
./build.sh s01

# Choose quality: low, medium, high (default), production, 4k
./build.sh s03 low

# Convert already-rendered scenes to HTML (skip rendering)
./build.sh html

# Remove all build artifacts (media/, slides/, output/)
./build.sh clean
```

Output is written to `output/presentation.html`.
