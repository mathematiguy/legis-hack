#!/bin/bash

# print out the file name
file_name=$1
echo "Current file name is: ${file_name}"

# check whether the file name exists in the current folder
# exit with an error if that file doesn't exist
if [ -f "$file_name" ]
then
	echo "$file_name found."
else
	echo "$file_name not found."
  exit 1
fi

# rename the file so as to remove the numeric prefix
new_file_name=`echo "${file_name}" | sed -e 's[0-9][0-9][0-9][0-9]_//g'`
echo "New file name is: ${new_file_name}"
mv ${file_name} legislation/${new_file_name}


# upload the file to Github
git status
git add --all
git commit -m "amendments specified in ${file_name}"
git push origin master
