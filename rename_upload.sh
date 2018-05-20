#!/bin/bash

# Check whether input params are provided
if [ $# -eq 0 ]
  then
    echo "The file name needs to be supplied as an argument"
		exit 1
fi

# print out the file name
input_params=$1
echo "Input parameter is: ${input_params}"

file_name=`basename "${input_params}"`
echo "File name is: ${file_name}"

# check whether the file name exists in the current folder
# exit with an error if that file doesn't exist
if [ -f "${input_params}" ]
then
	echo "File ${input_params} exists."
else
	echo "File ${input_params} does not exist!"
  exit 1
fi

# rename the file so as to remove the numeric prefix
new_file_name=`echo "${file_name}" | sed -e 's/[0-9][0-9][0-9][0-9]_//g'`
echo "New file name is: ${new_file_name}"
cp -rf ${input_params} legislation/${new_file_name}


# upload the file to Github
git status
git add legislation/${new_file_name}
git commit -m "amendments specified in ${file_name}"
