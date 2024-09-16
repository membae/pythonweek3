import sqlite3

class Concert:
    
    def __init__(self, concert_id):
        self.concert_id = concert_id

    def hometown_show(self):
        conn = sqlite3.connect('music_festival.db')
        cursor = conn.cursor()
        query = '''
        SELECT venues.city, bands.hometown
        FROM concerts
        JOIN venues ON concerts.venue_id = venues.id
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.id = ?;
        '''
        cursor.execute(query, (self.concert_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == result[1]:  # Compare venue city and band's hometown
            return True
        return False

    def introduction(self):
        conn = sqlite3.connect('music_festival.db')
        cursor = conn.cursor()
        query = '''
        SELECT venues.city, bands.name, bands.hometown
        FROM concerts
        JOIN venues ON concerts.venue_id = venues.id
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.id = ?;
        '''
        cursor.execute(query, (self.concert_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            venue_city, band_name, band_hometown = result
            return f"Hello {venue_city}!!!!! We are {band_name} and we're from {band_hometown}"
        


class Band:
    
    def __init__(self, band_id):
        self.band_id = band_id

    def play_in_venue(self, venue_id, date):
        conn = sqlite3.connect('music_festival.db')
        cursor = conn.cursor()
        query = '''
        INSERT INTO concerts (band_id, venue_id, date)
        VALUES (?, ?, ?);
        '''
        cursor.execute(query, (self.band_id, venue_id, date))
        conn.commit()
        conn.close()

    def all_introductions(self):
        conn = sqlite3.connect('music_festival.db')
        cursor = conn.cursor()
        query = '''
        SELECT venues.city, bands.name, bands.hometown
        FROM concerts
        JOIN venues ON concerts.venue_id = venues.id
        JOIN bands ON concerts.band_id = bands.id
        WHERE bands.id = ?;
        '''
        cursor.execute(query, (self.band_id,))
        concerts = cursor.fetchall()
        conn.close()
        
        introductions = []
        for concert in concerts:
            venue_city, band_name, band_hometown = concert
            introductions.append(f"Hello {venue_city}!!!!! We are {band_name} and we're from {band_hometown}")
        return introductions

    @staticmethod
    def most_performances():
        conn = sqlite3.connect('music_festival.db')
        cursor = conn.cursor()
        query = '''
        SELECT bands.id, bands.name, COUNT(concerts.id) as concert_count
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        GROUP BY bands.id
        ORDER BY concert_count DESC
        LIMIT 1;
        '''
        cursor.execute(query)
        band = cursor.fetchone()
        conn.close()
        return band  # Returns the band with the most performances


class Venue:
    
    def __init__(self, venue_id):
        self.venue_id = venue_id

    def concert_on(self, date):
        conn = sqlite3.connect('music_festival.db')
        cursor = conn.cursor()
        query = '''
        SELECT concerts.id, concerts.date 
        FROM concerts
        WHERE concerts.venue_id = ? AND concerts.date = ?
        LIMIT 1;
        '''
        cursor.execute(query, (self.venue_id, date))
        concert = cursor.fetchone()
        conn.close()
        return concert  # Returns the first concert on that date at the venue

    def most_frequent_band(self):
        conn = sqlite3.connect('music_festival.db')
        cursor = conn.cursor()
        query = '''
        SELECT bands.id, bands.name, COUNT(concerts.id) as performance_count
        FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.venue_id = ?
        GROUP BY bands.id
        ORDER BY performance_count DESC
        LIMIT 1;
        '''
        cursor.execute(query, (self.venue_id,))
        band = cursor.fetchone()
        conn.close()
        return band  # Returns the band that has performed the most at the venue

