# run from project directory  

DATA_DIR=pathtofiles
DB_PATH=pathtodb
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

  echo "doing: mongoimport --dbpath $DATA_DIR --db $DATABASE --collection $COLLECTION --file $f --jsonArray"

  mongoimport --dbpath $DB_PATH --db $DATABASE --collection $COLLECTION  --file $f --jsonArray
  
  echo "Done $f from $COLLECTION"
done

