#!/bin/bash

if [ -n "$(echo 'First Condition')" ]; then
    # First step goes here
    echo "Hello, World!" &
fi

if [ -n "$(echo 'Second Condition')" ]; then
      # Second step goes here 
     ls &
fi

# Third thing goes here
wait
echo "Third thing!"
