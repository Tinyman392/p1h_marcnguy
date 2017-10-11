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
# the (useless) downloaded content to temp.html.
#
# The error output is redirected to grep to find the word 
# "Location" which contains the final URL, this is then cut to
# parse out the URL and the PubChem ID
#
# Note that temp.html is only used if the URL brings us to a 
# search results page (multiple compounds) in which case, we try
# to extract the first search hit.  If none exist, we don't do
# anything
#
pcid=$(wget $url --content-disposition -O temp.html 2> >(grep Location) | cut -f2 -d' ' | rev | cut -f1 -d'/' | rev)

#
# If a PubChem ID couldn't be found, grab first item in search 
# results
# If no results exist, exit script
#
if [ "$pcid" == "" ]; then
	if [[ $(grep "Select item" temp.html) =~ (Select item )([0-9]*) ]]; then
		pcid=$(echo ${BASH_REMATCH[0]} | rev | cut -f1 -d' ' | rev)
	else
		rm temp.html
		exit
	fi
fi

# echo $1 $pcid

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

rm temp.html

# https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2733526/record/SDF/?record_type=3d&response_type=save&response_basename=Structure3D_CID_2733526
