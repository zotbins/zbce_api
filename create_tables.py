"""
Description: This script provides a series of functions you can use to help create
the database schema for the ZotBins Community Edition Ecosystem. For more details
about the project https://zotbins.github.io/zbceblog
"""

from models import db

def recreate_tables():
    """
    """
    print("Dropping all tables in specified database...")
    db.drop_all()
    print("Dropped.")
    db.session.commit()
    print("Creating all tables in specified database...")
    db.create_all()
    print("Created.")

if __name__ == "__main__":
    recreate_tables()
