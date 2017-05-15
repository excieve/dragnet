#!/bin/bash

python3 utils/merge.py ~/workspace/meta_1M_upd.csv ~/workspace/red_flags_1M.csv ~/workspace/step_11_incomes_agg.csv ~/workspace/step_12_assets_agg.csv ~/workspace/step_3_estate_agg.csv ~/workspace/step_6_vehicles_agg.csv -o ~/workspace/dragnet_humble_with_flags_corrected.csv

