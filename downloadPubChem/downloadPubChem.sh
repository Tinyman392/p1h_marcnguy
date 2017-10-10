# downloadPubChem.sh [NSC number] [output]
#
# for i in $(cat drugs.in.combo.txt); do bash downloadPubChem.sh $i sdf_files/$i.sdf; done
#

#
# Convert NSC number to a search term that matches "NSC ######"
# %22 is used to replace a single double quote in a search term
# %20 is used to replace asingle space in a search term
#
sTerm=$(echo \"NSC $1\" | sed 's/"/%22/g' | sed 's/ /%20/g')

#
# Create the URL to search the compound
#
url="https://www.ncbi.nlm.nih.gov/pccompound?term="$sTerm

#
# We want to get the final URL that pops out of the, I use wget
# to do this with the --content-disposition option, I also send
# the (useless) downloaded content to /dev/null
#
# The error output is redirected to grep to find the word 
# "Location" which contains the final URL, this is then cut to
# parse out the URL and the PubChem ID
#
pcid=$(wget $url --content-disposition -O /dev/null 2> >(grep Location) | cut -f2 -d' ' | rev | cut -f1 -d'/' | rev)

#
# If a PubChem ID couldn't be found, exit the script
#
if [ "$pcid" == "" ]; then
	exit
fi

#
# If we did find a PubChem ID, try to find the 3D version of the
# chemical
#
wget https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/$pcid/record/SDF/\?record_type\=3d\&response_type\=save\&response_basename\=Structure3D_CID_$pcid -O $2

#
# If the 3D version doesn't exist, delete the output from the 
# wget command
#
if [ $? -ne 0 ]; then
	rm $2
fi

# https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2733526/record/SDF/?record_type=3d&response_type=save&response_basename=Structure3D_CID_2733526