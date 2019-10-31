#! /bin/bash -v
mkdir -p safe
mkdir -p data
mv *.nc data/.
mv *inp* safe/.
mv *pbs safe/.
mv cleanup.sh safe/.
mv namoptions safe/.
rm *
mv safe/* .
rm -rf safe
