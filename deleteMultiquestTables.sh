echo "Drop and regenerate database tables"

# Drop in this order:
psql -U djuser djdb -f ./dropTableQuery.txt
# then regenerate the data tables
echo "Verify that there are no errors, then execute python manage.py syncdb"
python manage.py validate
# python manage.py shell