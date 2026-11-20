# Figure and sample-size code: "Should Clinical Foundation Models Reason Through Disease Labels?"

Code accompanying the Viewpoint *Should Clinical Foundation Models Reason Through Disease Labels? A Falsifiable Case for Diagnosis as an Interface* (Huang J-R, Lu W-H; JMIR Medical Informatics, manuscript 106804, under review).

All figures are schematic. They illustrate the form of the argument and contain no measured data.

| Script | Output |
|---|---|
| `figures/fig1_representational_stack.py` | Figure 1, the representational stack |
| `figures/fig2_ib_staircase.py` | Figure 2, the information curve with the human-usable frontier |
| `figures/fig1_historical_arc.py` | Supplementary Figure S1 (Multimedia Appendix 1), the historical arc |
| `tools/sample_size_tost_auc.py` | Sample-size table in Multimedia Appendix 3, section 6 (analytic Hanley–McNeil calculation with a simulation check) |

## Running

Python 3.10 or later.

```
pip install -r requirements.txt
python figures/fig1_representational_stack.py
python figures/fig2_ib_staircase.py
python figures/fig1_historical_arc.py
python tools/sample_size_tost_auc.py
```

Run from the repository root. Figures are written to `figures/` as PDF and 300-dpi PNG.

## Citation

If you use this code, please cite the article and the archived release (Zenodo, https://doi.org/10.5281/zenodo.24390049, which resolves to the latest version).

## License

MIT; see `LICENSE`.
