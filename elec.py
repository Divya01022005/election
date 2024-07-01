import mysql.connector
from mysql.connector import Error

class ElectionResults:
    def _init_(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = self.create_connection()

    def create_connection(self):
        """ Create a database connection """
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                print("Connection to MySQL DB successful")
            return connection
        except Error as e:
            print(f"The error '{e}' occurred")
            return None

    def close_connection(self):
        """ Close the database connection """
        if self.connection.is_connected():
            self.connection.close()
            print("The connection is closed")

    def get_candidates(self):
        """ Retrieve the list of candidates """
        cursor = self.connection.cursor()
        query = "SELECT id, name FROM candidates"
        cursor.execute(query)
        candidates = cursor.fetchall()
        cursor.close()
        return candidates

    def count_votes(self):
        """ Count the votes for each candidate """
        cursor = self.connection.cursor()
        query = "SELECT candidate_id, COUNT(*) FROM votes GROUP BY candidate_id"
        cursor.execute(query)
        vote_counts = cursor.fetchall()
        cursor.close()
        return vote_counts

    def get_winner(self):
        """ Determine the winner of the election """
        vote_counts = self.count_votes()
        if not vote_counts:
            return None, 0

        max_votes = max(vote_counts, key=lambda item: item[1])
        winner_id = max_votes[0]
        winner_votes = max_votes[1]

        cursor = self.connection.cursor()
        query = "SELECT name FROM candidates WHERE id = %s"
        cursor.execute(query, (winner_id,))
        winner_name = cursor.fetchone()[0]
        cursor.close()

        return winner_name, winner_votes

    def print_results(self):
        """ Print the election results """
        candidates = self.get_candidates()
        vote_counts = self.count_votes()

        results = {candidate_id: 0 for candidate_id, _ in candidates}
        for candidate_id, count in vote_counts:
            results[candidate_id] = count

        print("Election Results:")
        for candidate_id, name in candidates:
            print(f"{name}: {results[candidate_id]} votes")

        winner_name, winner_votes = self.get_winner()
        if winner_name:
            print(f"\nThe winner is {winner_name} with {winner_votes} votes")
        else:
            print("\nNo votes have been cast.")

if _name_ == "_main_":
    host = "your_host"
    database = "your_database"
    user = "your_username"
    password = "your_password"

    election = ElectionResults(host, database, user, password)
    election.print_results()
    election.close_connection()
