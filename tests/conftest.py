import os
import pytest
import tempfile
from app import create_app, db

@pytest.fixture
def app():
    db_fp, db_path = tempfile.mkstemp()
    app = create_app(test_config={
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}'
    })

    with app.app_context():
        db.create_all()

    yield app

    os.close(db_fp)
    os.unlink(db_path)
