from database import Database

database = Database()

async def get_session():
    return database.get_session()

# Starting new database
# database.init()

# Drop database when application is closed
# @app.on_event('shutdown')
# def shutdown_event():
#     database.drop()
#     print("Database dropped")