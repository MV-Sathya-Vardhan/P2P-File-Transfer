import mysql.connector


def connection(publicIP):
    db = mysql.connector.connect(
        host = publicIP,
        user = "OpenLab",
        passwd = "peer2peer",
        database = "openlabdatabase")

    mycursor = db.cursor(buffered=True)
    return mycursor,db