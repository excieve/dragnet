#!/bin/bash

python3.5 utils/export.py meta normal_form -u admin -p admin -o data/export/meta_1M_upd.csv &&\
python3.5 utils/export.py red_flags normal_form -u admin -p admin -o data/export/red_flags_1M.csv &&\
python3.5 utils/export.py step_3_estate_agg normal_form -u admin -p admin -o data/export/step_3_estate_agg.csv &&\
python3.5 utils/export.py step_6_vehicles_agg normal_form -u admin -p admin -o data/export/step_6_vehicles_agg.csv &&\
python3.5 utils/export.py step_11_incomes_agg normal_form -u admin -p admin -o data/export/step_11_incomes_agg.csv &&\
python3.5 utils/export.py step_12_assets_agg normal_form -u admin -p admin -o data/export/step_12_assets_agg.csv

