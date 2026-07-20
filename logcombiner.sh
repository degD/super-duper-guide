
#!/bin/bash

rm "logs/logscombined.log"
for f in $(ls "logs"); do
    echo $(cat "logs/$f")
    echo $(cat "logs/$f") >> "logs/logscombined.log"
done
