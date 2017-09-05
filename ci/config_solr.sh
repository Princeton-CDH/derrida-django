# Config variables local to the script
version=${SOLR_VERSION:-6.6.0}
file="solr-${version}.tgz"
url="http://archive.apache.org/dist/lucene/solr/${version}/${file}"

# Check if the file exists for some reason, shouldn't but out of parsimony
if [ -f $file ];
then
        echo "File exists, skipping download..."
else
        wget $url
fi
# Untar
tar xzf $file

# Start the solr instance with all default settings
echo "Starting solr and making core..."
bin="solr-${version}/bin/solr"
$bin start
if [ $? -eq 0 ];
then
        echo "Solr appears to have started..."
else
        exit 1
fi

# Try to make a core
echo "Trying to make a core"
$bin create -c $SOLR_CORE

if [ $? -ne 0 ];
then
        echo "There was an error while creating the Solr core"
        exit 1
fi

echo "Core created and Solr running on default port of 8983..."
