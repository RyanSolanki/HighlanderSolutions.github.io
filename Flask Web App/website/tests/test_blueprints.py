# test_blueprints.py

from ...website import create_app

def test_views(client):
    app = create_app()

    with app.test_client() as client:
        response = client.get('/views/')  # Adjust the route based on your blueprint
        assert response.status_code == 200
        assert b'Your expected content' in response.data
