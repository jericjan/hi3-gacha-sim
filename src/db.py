import json
import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS "pulls" (
                    "id" INTEGER,
                    "name" TEXT,
                    "rounds" INTEGER,
                    "valk_pity" INTEGER,
                    "gear_pity" INTEGER,
                    "data" TEXT,
                    PRIMARY KEY("id")
                )"""
            )
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.conn.commit()

    def count_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pulls")
        count = cursor.fetchone()[0]
        cursor.close()
        self.conn.commit()
        return count

    def add(self, name, rounds, valk_pity, gear_pity, data):
        cursor = self.conn.cursor()
        data_json = json.dumps(data)

        # Prepare the query with the parameters
        query = (
            "INSERT INTO pulls "
            "(name, rounds, valk_pity, gear_pity, data) "
            "VALUES (?, ?, ?, ?, ?)"
        )

        params = (name, rounds, valk_pity, gear_pity, data_json)

        # Execute the query with the parameters
        cursor.execute(query, params)
        cursor.close()
        self.conn.commit()

    def show_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, rounds, valk_pity, gear_pity " "FROM pulls")
        rows = cursor.fetchall()
        print(
            f"{'ID'.center(5)} | {'Name'.center(30)} | {'Rounds'.center(7)} | "
            f"{'Valk Pity'.center(9)} | {'Gear Pity'.center(9)}"
        )
        for row in rows:
            print(
                f"{str(row[0]).center(5)} | {str(row[1]).center(30)} | "
                f"{str(row[2]).center(7)} | {str(row[3]).center(9)} | "
                f"{str(row[4]).center(9)}"
            )
        cursor.close()
        self.conn.commit()

    def get_row(self, id):
        cursor = self.conn.cursor()

        cursor.execute("SELECT data, name FROM pulls WHERE id = ?", (id,))
        row = cursor.fetchone()
        cursor.close()
        self.conn.commit()

        return row

    def delete_row(self, id):
        cursor = self.conn.cursor()

        cursor.execute("DELETE FROM pulls WHERE id = ?", (id,))

        cursor.close()
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
