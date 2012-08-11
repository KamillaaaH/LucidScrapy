# -*- coding: utf-8 *-*
__author__ = "kamilla"
__date__ = "$Aug 11, 2012 12:06:02 PM$"

from pymongo import Connection

class VerifyDB():

    def verifyDB(self):
        con = Connection('localhost', 27017)
        db = self.verifyDBExistence(con, "test_database")
        print "Verify DB existence"
        if db:
            print "Database already created: " + str(db)
        else:
            db = self.createDB(con, "test_database")

        print db.collection_names()

            
    def verifyDBExistence(self, con, dbName):
        for s in con.database_names():
            if s == dbName:
                return con.dbName
            else:
                return None
                

    def verifyCollections(self, db):
        for s in db.collection_names():
            if s == "receitas":
                print "Collection \'receitas\' already created"
            elif s == "despesas":
                print "Collection \'despesas\' already created"
            else:
                self.createCollections()
        

    def createDB(self, con, dbName):
        try:
            db = con.dbName
            print "Database created!"
            return db
        except:
            print "Can't create database!"
            
            
    def createCollection(self, db, collectionName):
        try:
            coll = db.collectionName
            print "Collection created!"
            return coll
        except:
            print "Can't create collection!"

            