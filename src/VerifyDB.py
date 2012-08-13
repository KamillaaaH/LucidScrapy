# -*- coding: utf-8 *-*
__author__ = "kamilla"
__date__ = "$Aug 11, 2012 12:06:02 PM$"


class VerifyDB():

    def verifyDB(self, con):
        db = self.verifyDBExistence(con)
        print "Verify DB existence"
        if db:
            print "Database already created: " + str(db)
        else:
            db = self.createDB(con)

            
    def verifyDBExistence(self, con):
        for s in con.database_names():
            if s == "test_database":
                return con.test_database
            else:
                return None
                

    def verifyCollection(self, db, nameCollection):
        for s in db.collection_names():
            if s == nameCollection:
                print "Collection " + s + " already created."
                return True
            else:
                return None
        

    def createDB(self, con):
        try:
            db = con.test_database
            print "Database created!"
            return db
        except:
            print "Can't create database!"

            