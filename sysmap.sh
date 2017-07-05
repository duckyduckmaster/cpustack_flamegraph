#
# sysmap v 0.1
# usage : ./sysmap (wildcard word for svg file prefixes) (comma delimited list with functionnames)
#  
# example usage: 
#   files: heat_file1.svg, heat_file2.svg  functions of interest : func1,func2 
# 	
#   command: ./sysmap heat func1,func2
#

>pnames

echo ""
IFS=',' read -r -a array <<< "$2"

echo "[" >> pnames
for a in ./$1*; do 
    echo $a >> pnames
    echo "," >> pnames
done
echo "]" >> pnames
cat pnames | tr -d '\n' 
echo ""


for el in "${array[@]}"; do
	echo " ";
	> numbers
	> allnumbers
	for a in ./$1*; do 
		( cat $a |grep $el |awk -F"samples" '{ print $2 }' |cut -d ')' -f1 |cut -d '%' -f1 |awk '{print $2}' ) |awk 'NF' > numbers;
		if [ -z $( head -1 numbers) ]; then
			echo "0.0" >> allnumbers
		else
			paste -s -d+ numbers |bc >> allnumbers 
		fi 	
		echo "," >> allnumbers
		>numbers
	done
	echo "[" >> allnumbers2
	sed '$d' allnumbers >> allnumbers2
	echo "]," >> allnumbers2
	cat allnumbers2 | tr -d '\n'
	>allnumbers
	>allnumbers2
done	
echo ""
echo ""