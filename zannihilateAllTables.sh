echo "Drop all database tables"

# Drop in this order:
psql -U djuser djdb -f ./zannihilateAllTables.txt
# then regenerate the data tables
echo "All tables dropped."
# python manage.py validate
# python manage.py shell