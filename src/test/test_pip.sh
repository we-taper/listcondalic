listcondalic pip ../../requirements.txt > tmp.json
python check_pip.py tmp.json
rm tmp.json