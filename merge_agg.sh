#!/bin/bash

python3.5 utils/merge.py data/export/meta_1M_upd.csv data/export/red_flags_1M.csv data/export/step_11_incomes_agg.csv data/export/step_12_assets_agg.csv data/export/step_3_estate_agg.csv data/export/step_6_vehicles_agg.csv -o data/export/dragnet_humble_with_flags.csv

