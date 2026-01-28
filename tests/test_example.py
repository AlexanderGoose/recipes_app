from app import app

def test_home_route():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'<h1 id="hero-text">Recipes made easier.</h1>' in response.data
