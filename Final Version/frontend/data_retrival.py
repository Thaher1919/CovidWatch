import os
import requests
import sqlite3

# Step 1: Print paths for debugging
print("Current working directory:", os.getcwd())
print("Script directory:", os.path.dirname(__file__))

# Step 2: Connect to the primary local SQLite database
primary_db_path = os.path.join(os.getcwd(), os.path.dirname(__file__), "userdata.db")
print("Primary DB Path:", primary_db_path)
primary_connection = sqlite3.connect(primary_db_path)
primary_cursor = primary_connection.cursor()
# Step 2: Connect to the secondary local SQLite database
secondary_db_path = os.path.join(os.getcwd(), os.path.dirname(__file__), "..", "mail_data.db")
secondary_connection = sqlite3.connect(secondary_db_path)
secondary_cursor = secondary_connection.cursor()

# Step 3: Retrieve "email," "username," and "state" columns from the primary database
# Only retrieve data if the "subscription" field is set to "subscribed"
primary_cursor.execute("SELECT email, username, state FROM user_details WHERE subscription = 'subscribed'")
user_data_list = primary_cursor.fetchall()

# Step 4: Update existing records and insert new records into the secondary database
for user_data in user_data_list:
    email, username, state = user_data

    # Check if the record exists in the secondary database
    secondary_cursor.execute("SELECT * FROM mailList WHERE lower(userName) = lower(?)", (username,))
    existing_record = secondary_cursor.fetchone()

    if existing_record:
        # If the record exists, update the fields
        secondary_cursor.execute(
            "UPDATE mailList SET email = ?, stateName = ? WHERE lower(userName) = lower(?)",
            (email, state, username)
        )
    else:
        # If the record doesn't exist, insert a new record
        secondary_cursor.execute(
            "INSERT INTO mailList (email, userName, stateName) VALUES (?, ?, ?)",
            (email, username, state)
        )

# Step 5: Move currentCases to pastCases in the secondary database
secondary_cursor.execute("UPDATE mailList SET pastCases = currentCases")
secondary_connection.commit()

# Step 6: Connect to the API
api_url = "https://disease.sh/v3/covid-19/states"
response = requests.get(api_url, headers={"accept": "application/json"})
api_data = response.json()

# Step 7: Update the current cases with "cases" field in API if and only if secondarydb.state matches with API.state
for api_entry in api_data:
    state = api_entry["state"]
    cases = api_entry["cases"]

    # Check if the "state" field from the API matches "state" column in the secondary database (case-insensitive)
    secondary_cursor.execute("SELECT currentCases FROM mailList WHERE lower(stateName) = lower(?)", (state,))
    current_cases = secondary_cursor.fetchone()

    if current_cases:
        # If there is a match, update the "currentCases" field in the secondary database
        secondary_cursor.execute("UPDATE mailList SET currentCases = ? WHERE stateName = ?", (cases, state))

# Step 8: Commit changes to the secondary database
secondary_connection.commit()

# Step 9: Print the updated data in the secondary database
print("After updating secondary database based on API data")
secondary_cursor.execute("SELECT * FROM mailList")
print(secondary_cursor.fetchall())
print("Changes committed to secondary database")

# Close the database connections
primary_connection.close()
secondary_connection.close()
