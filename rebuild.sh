#!/usr/bin/bash

uv run main.py collect xml ../preguntas/ -o ../blocks/full.xml

uv run main.py collect xml ../preguntas/top/p1/p1a/ -o ../blocks/teoria.xml
uv run main.py collect xml ../preguntas/top/p1/codigo -o ../blocks/codigo.xml

