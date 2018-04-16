# Config variables local to the script
version=${SOLR_VERSION:-6.6.0}
file="solr-${version}.tgz"
url="http://archive.apache.org/dist/lucene/solr/${version}/${file}"

# Make a downloads dir to cache and change working dir to it
mkdir -p downloads
cd downloads

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
echo "Starting solr and creating core ${SOLR_CORE}..."
bin="solr-${version}/bin/solr"
$bin start
if [ $? -eq 0 ];
then
        echo "Solr appears to have started..."
else
        exit 1
fi

# Try to make a core
echo "Creating solr core with managed schema"
$bin create -c $SOLR_CORE -n basic_configs

if [ $? -ne 0 ];
then
        echo "There was an error while creating the Solr core"
        exit 1
fi

echo "Core created and Solr running on default port of 8983..."
