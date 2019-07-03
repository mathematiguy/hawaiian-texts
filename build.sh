set -ex

export RUN=''
export LOG_LEVEL=INFO

make crawl

cp ulukau/nupepa.json ulukau/nupepa.log /output
cp D3/* /publish
