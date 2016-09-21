#!/bin/bash
out="Project1_data_shuf.csv"
sed -n -e 2,8712p Project1_data.csv > temp
shuf temp > $out 
percent=`echo "scale=0; 8712-(8712*0.2)"| bc -l`
rounded=`printf "%.0f" $percent`
echo $rounded
split -l $rounded $out
mv xaa Project1_data_training.csv
mv xab Project1_data_TEST.csv
rm $out
rm temp
