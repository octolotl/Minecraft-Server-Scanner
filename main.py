import os
import socket
import sqlite3
from threading import Thread
from random import randint


class Finder:
    def __init__(self):
        if not os.path.isfile('./serverlite.db'):
            with open('serverlite.db', 'w'):
                db = sqlite3.connect('serverlite.db')
                cur = db.cursor()
                cur.execute('''CREATE TABLE servers
                                   (ip)''')
                db.commit()
                db.close()
        self.ip = str(input('[?] Ip- '))
        self.threadnum = input("[?] Threads- ")
        processes = []
        if self.isopen(self.ip, 25565):
            db = sqlite3.connect('serverlite.db')
            cur = db.cursor()
            cur.execute(f"""SELECT "ip"
                                                                       FROM "main"."servers"
                                                                       WHERE "ip"=?""", (self.ip,))
            result = cur.fetchone()
            if not result:
                cur.execute(f"""INSERT INTO "main"."servers"(ip) VALUES ("{self.ip}")""")
                db.commit()
        for i in range(int(self.threadnum)):
            p = Thread(target=self.getip)
            p.daemon = True
            processes.append(p)
        for i in range(int(self.threadnum)):
            processes[i].start()
        for i in range(int(self.threadnum)):
            processes[i].join()

    @staticmethod
    def convert(obj):
        if isinstance(obj, bool):
            return str(obj).lower()

    @staticmethod
    def isopen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False
        finally:
            s.close()

    def getip(self):
        ipparts = self.ip.split(".")
        for _ in iter(int, 1):
            ip2 = str(ipparts[0]) + "." + str(randint(0, 255)) + "." + str(randint(0, 255)) + "." + str(randint(0, 256))
            if self.isopen(ip2, 25565):
                print(ip2 + " | OPEN")
                db = sqlite3.connect('serverlite.db')
                cur = db.cursor()
                cur.execute(f"""SELECT "ip"
                                                                                       FROM "main"."servers"
                                                                                       WHERE "ip"=?""", (ip2,))
                result = cur.fetchone()
                if not result:
                    cur.execute(f"""INSERT INTO "main"."servers"(ip) VALUES ("{ip2}")""")
                    db.commit()
                    db.close()


Finder()
