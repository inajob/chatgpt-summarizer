export PYTHONUTF8=1
for f in `ls docs/*/*.json`; do
  echo $f
  python summary.py $f
done
