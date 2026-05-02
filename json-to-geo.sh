#!/bin/bash
# Extract latitude and longitude from JSON and output geo: URL

sed -n 's/.*"latitude":\([^,]*\).*"longitude":\([^,]*\).*/geo:\1,\2?z=9/p'

