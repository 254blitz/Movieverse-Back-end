from app import app, db
from sqlalchemy import inspect, text

def nuclear_reset():
    with app.app_context():
        print("💥 Performing nuclear database reset...")
        
        if 'sqlite' in str(db.engine.url):
            db.session.execute(text('PRAGMA foreign_keys=OFF'))
        
        inspector = inspect(db.engine)
        for table in inspector.get_table_names():
            db.session.execute(text(f'DROP TABLE IF EXISTS {table}'))
            print(f"🔥 Dropped table: {table}")
        
        try:
            db.session.execute(text('DROP TABLE IF EXISTS alembic_version'))
            print("🔥 Dropped alembic_version table")
        except:
            pass
        
        if 'sqlite' in str(db.engine.url):
            db.session.execute(text('PRAGMA foreign_keys=ON'))
        
        db.session.commit()
        print("✅ Nuclear reset complete")

if __name__ == "__main__":
    nuclear_reset()