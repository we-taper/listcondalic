listcondalic conda ../../environment.yml > tmp.json
python check_conda.py tmp.json
rm tmp.json