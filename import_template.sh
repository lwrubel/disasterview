# imports each file in mongodb database
# run from project directory  

DATA_DIR=pathtofiles
DATABASE=yourdbname
FILES=$DATA_DIR/*.json

for f in $FILES

do
  echo "Importing file $f..."

  COLLECTION=$f

# strip out directories
  COLLECTION=${COLLECTION#$DATA_DIR/}
 
# strip out longest substring starting with "-" from the back of the string, i.e. all but subject name
  COLLECTION=${COLLECTION%%-*}

  echo "doing: mongoimport --db $DATABASE --collection $COLLECTION --file $f --jsonArray"

  mongoimport --db $DATABASE --collection $COLLECTION  --file $f --jsonArray
  
  echo "Done $f from $COLLECTION"
done

