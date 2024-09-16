import sqlite3
from app import Concert, Band, Venue

# Connect to the SQLite database
def setup_database():
    conn = sqlite3.connect('music_festival.db')
    cursor = conn.cursor()

    # Ensure tables exist (assuming band, venue, and concert tables have been created)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bands (
        id INTEGER PRIMARY KEY,
        name TEXT,
        hometown TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS venues (
        id INTEGER PRIMARY KEY,
        name TEXT,
        city TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS concerts (
        id INTEGER PRIMARY KEY,
        band_id INTEGER,
        venue_id INTEGER,
        date TEXT,
        FOREIGN KEY(band_id) REFERENCES bands(id),
        FOREIGN KEY(venue_id) REFERENCES venues(id)
    );
    ''')

    conn.commit()
    conn.close()

# Insert test data into the database
def insert_test_data():
    conn = sqlite3.connect('music_festival.db')
    cursor = conn.cursor()

    # Insert bands
    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('The Rockers', 'New York')")
    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('The Jazzers', 'Chicago')")
    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('The Blues Band', 'New Orleans')")

    # Insert venues
    cursor.execute("INSERT INTO venues (name, city) VALUES ('Madison Square Garden', 'New York')")
    cursor.execute("INSERT INTO venues (name, city) VALUES ('Chicago Theatre', 'Chicago')")
    cursor.execute("INSERT INTO venues (name, city) VALUES ('House of Blues', 'New Orleans')")

    # Insert concerts
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (1, 1, '2023-01-01')")
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (2, 2, '2023-02-01')")
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (3, 3, '2023-03-01')")

    conn.commit()
    conn.close()

# Test the Concert class methods
def test_concert_methods():
    concert = Concert(1)

    print("Testing Concert Methods:")
    
    # Test hometown_show()
    print("Is it a hometown show?:", concert.hometown_show())  # Expected: True (New York band, New York venue)

    # Test introduction()
    print("Introduction:", concert.introduction())  # Expected: "Hello New York!!!!! We are The Rockers and we're from New York"

# Test the Band class methods
def test_band_methods():
    band = Band(1)

    print("Testing Band Methods:")

    # Test play_in_venue()
    print("Playing at a new venue...")
    band.play_in_venue(2, '2024-01-01')  # Band 1 plays at venue 2 on this date

    # Test all_introductions()
    introductions = band.all_introductions()
    print("All Introductions for the band:")
    for intro in introductions:
        print(intro)

    # Test most_performances()
    print("Band with the most performances:")
    most_perf_band = Band.most_performances()
    print(f"Band ID: {most_perf_band[0]}, Name: {most_perf_band[1]}, Concerts: {most_perf_band[2]}")

# Test the Venue class methods
def test_venue_methods():
    venue = Venue(1)

    print("Testing Venue Methods:")

    # Test concert_on()
    concert_on = venue.concert_on('2023-01-01')
    print(f"Concert on 2023-01-01: {concert_on}")

    # Test most_frequent_band()
    print("Most frequent band at this venue:")
    most_frequent = venue.most_frequent_band()
    print(f"Band ID: {most_frequent[0]}, Name: {most_frequent[1]}, Performances: {most_frequent[2]}")

if __name__ == '__main__':
    # Step 1: Set up the database
    setup_database()

    # Step 2: Insert test data into the database
    insert_test_data()

    # Step 3: Test each class
    test_concert_methods()  # Test Concert class methods
    test_band_methods()     # Test Band class methods
    test_venue_methods()    # Test Venue class methods
