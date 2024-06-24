from database.DB_connect import DBConnect
from model.album import Album
from model.connessione import Connessione

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodi(prezzo):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.*
from album a ,track t 
where a.AlbumId=t.AlbumId 
group by t.AlbumId 
having sum(t.UnitPrice)>%s"""

        cursor.execute(query,(prezzo,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(n):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.a1 as v1, t2.a2 as v2, round(t1.p1-t2.p2) as peso
from(select t.AlbumId as a1, sum(t.UnitPrice) as p1
from track t 
group by t.AlbumId 
having sum(t.UnitPrice)>%s) as t1,
(select t.AlbumId as a2, sum(t.UnitPrice) as p2
from track t 
group by t.AlbumId 
having sum(t.UnitPrice)>%s) as t2
where t1.a1<t2.a2  """

        cursor.execute(query,(n,n,))

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result