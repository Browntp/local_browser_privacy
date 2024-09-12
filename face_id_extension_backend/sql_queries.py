import mysql.connector
import os
import matplotlib.pyplot as plt
conn = mysql.connector.connect(host='localhost', password='Wesome01', user='root', database = 'image_processing_db')
if conn.is_connected():
    print("MySql connection established...")

# Create a cursor object
cursor = conn.cursor()

# Function to insert image processing data
def insert_image_data(name):

    print(name)
    year = name[:4]
    month = name[4:6]
    day = name[6:8]
    hour = name[9:11]
    minute = name[11:13]
    user = name[16:-3]
    if user == '':
        user = "no face"
    # SQL query to insert data
    query = """
    INSERT INTO processed_images (year, month, day, hour, minute, name)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    # Execute the query with the values
    cursor.execute(query, (year, month, day, hour, minute, user))

    # Commit the transaction
    conn.commit()

folder_path = 'uploads'
def upload_to_sql():
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file
        if os.path.isfile(file_path):
            # Here, "view" or process the file (e.g., read the content)
            insert_image_data(filename)
            
            # Delete the file after viewing/processing
            os.remove(file_path)
            print(f"File deleted: {filename}")

upload_to_sql()

def fetch_all_rows(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    if rows:
        print(f"Rows in table '{table_name}':")
        for row in rows:
            print(row)
    else:
        print(f"No rows found in table '{table_name}'.")


def pie_chart() -> list[tuple]:
    query = """
    SELECT name, COUNT(*) as count
    FROM processed_images
    GROUP BY name
    """
    cursor.execute(query)
    data = cursor.fetchall()
    names = [row[0] for row in data]
    counts = [row[1] for row in data]

    # Step 4: Create the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=names, autopct='%1.1f%%', startangle=140)
    plt.title('Processed Images by User Name')
    plt.savefig('plots/piechart.png')
    

pie_chart()

fetch_all_rows(cursor, 'processed_images')
# Close the connection
cursor.close()
conn.close()