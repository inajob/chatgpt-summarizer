export PYTHONUTF8=1
for f in `ls out/*/*.json`; do
  echo $f
  python summary.py $f
done
