#!/bin/bash

python3.5 utils/addview.py views/meta.es6 -u admin -p admin -D meta -v normal_form -l chakra -b &&\
python3.5 utils/addview.py views/step_3_estate_agg.es6 -u admin -p admin -D step_3_estate_agg -v normal_form -l chakra -b &&\
python3.5 utils/addview.py views/step_6_vehicles_agg.es6 -u admin -p admin -D step_6_vehicles_agg -v normal_form -l chakra -b &&\
python3.5 utils/addview.py views/step_11_incomes_agg.es6 -u admin -p admin -D step_11_incomes_agg -v normal_form -l chakra -b &&\
python3.5 utils/addview.py views/step_12_assets_agg.es6 -u admin -p admin -D step_12_assets_agg -v normal_form -l chakra -b &&\
python3.5 utils/addview.py views/red_flags.es6 -u admin -p admin -D red_flags -v normal_form -l chakra -b

