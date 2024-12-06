#! /bin/bash

python src/db_init.py
streamlit run src/home.py --server.port 8080