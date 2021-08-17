#! /usr/bin/env bash

# Invoke python script via its virtual env

DIR=/apps/n2t/sv/cur/build/eggnog/t/n2t/e/admin

[[ ! "$1" ]] && {
	echo "Expects an address argument, prints longitude and latitude (x, y)"
	exit
}

$DIR/venv/bin/python - << EOT

# Derived 2021 from https://github.com/chloepochon/ARKA_map.

import sys
from geopy.geocoders import Nominatim

geocoder = Nominatim(user_agent="ARK NAAN Registrar") 
location = geocoder.geocode("$1")
if location == None:
    sys.exit("Error: $1: address yielded no longitute/latitude")

print([location.longitude, location.latitude])

EOT

#echo PERL version
#
#perl << 'EOT'
#use Geo::Coder::OSM;
#
#my $geocoder = Geo::Coder::OSM->new;
#my $location = $geocoder->geocode(
#    location => 'Hollywood and Highland, Los Angeles, CA'
#);
#
#EOT
