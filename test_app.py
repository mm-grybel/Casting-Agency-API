import json
import unittest
import HtmlTestRunner
from flask_sqlalchemy import SQLAlchemy

import config
from app import APP
from models import db


casting_assistant_token = config.bearer_tokens['casting_assistant']
casting_director_token = config.bearer_tokens['casting_director']
executive_producer_token = config.bearer_tokens['executive_producer']


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        APP.config['SQLALCHEMY_DATABASE_URI'] = config.TEST_DATABASE_URL
        self.app = APP
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def test_home_page(self):
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Casting Agency' in response.get_data(as_text=True))

    def test_get_actors(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().get(
            '/actors',
            headers=self.headers
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['actors'], list)

    def test_get_actors_no_auth(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_new_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['actor'], dict)
        self.assertIsInstance(data['actor']['id'], int)
        self.assertEqual(data['actor']['name'], 'Jason Bourne')
        self.assertEqual(data['actor']['age'], 35)
        self.assertEqual(data['actor']['gender'], 'male')
        self.assertIsInstance(data['actor']['movies'], list)

    def test_add_new_actor_missing_data(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'age': 35,
                'gender': 'male'
            })
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_add_new_actor_no_auth(self):
        response = self.client().post(
            '/actors',
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_new_actor_no_permission(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        original_data = json.loads(response.data)

        response = self.client().patch(
            f"/actors/{original_data['actor']['id']}",
            headers=self.headers,
            data=json.dumps({
                'name': 'Ann Smith',
                'age': 30,
                'gender': 'female'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['actor'], dict)
        self.assertIsInstance(data['actor']['id'], int)
        self.assertEqual(data['actor']['name'], 'Ann Smith')
        self.assertEqual(data['actor']['age'], 30)
        self.assertEqual(data['actor']['gender'], 'female')
        self.assertIsInstance(data['actor']['movies'], list)

    def test_update_actor_no_actor_id(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().patch(
            '/actors/12345',
            headers=self.headers,
            data=json.dumps({
                'name': 'Ann Smith',
                'age': 30,
                'gender': 'female'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_actor_no_auth(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        original_data = json.loads(response.data)

        response = self.client().patch(
            f"/actors/{original_data['actor']['id']}",
            data=json.dumps({
                'name': 'Ann Smith',
                'age': 30,
                'gender': 'female'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_actor_no_permission(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        original_data = json.loads(response.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().patch(
            f"/actors/{original_data['actor']['id']}",
            headers=self.headers,
            data=json.dumps({
                'name': 'Ann Smith',
                'age': 30,
                'gender': 'female'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_actor(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        original_data = json.loads(response.data)

        response = self.client().delete(
            f"/actors/{original_data['actor']['id']}",
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], original_data['actor']['id'])

    def test_delete_actor_no_actor_id(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().delete(
            '/actors/12345',
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor_no_auth(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        original_data = json.loads(response.data)

        response = self.client().delete(
            f"/actors/{original_data['actor']['id']}"
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_actor_no_permission(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_director_token}'}
        )
        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        original_data = json.loads(response.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().delete(
            f"/actors/{original_data['actor']['id']}",
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])

    def test_get_movies(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().get(
            '/movies',
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movies'], list)

    def test_get_movies_no_auth(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_new_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movie'], dict)
        self.assertIsInstance(data['movie']['id'], int)
        self.assertEqual(data['movie']['title'], 'The Devil All the Time')
        self.assertEqual(data['movie']['release_year'], '2020')
        self.assertEqual(data['movie']['genre'], 'Drama')
        self.assertIsInstance(data['movie']['actors'], list)

    def test_add_new_movie_missing_data(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_add_new_movie_no_auth(self):
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_new_movie_no_permission(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])

    def test_update_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        original_data = json.loads(response.data)

        response = self.client().patch(
            f"/movies/{original_data['movie']['id']}",
            headers=self.headers,
            data=json.dumps({
                'title': 'It',
                'release_year': '2017',
                'genre': 'Horror'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movie'], dict)
        self.assertIsInstance(data['movie']['id'], int)
        self.assertEqual(data['movie']['title'], 'It')
        self.assertEqual(data['movie']['release_year'], '2017')
        self.assertEqual(data['movie']['genre'], 'Horror')
        self.assertIsInstance(data['movie']['actors'], list)

    def test_update_movie_no_movie_id(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().patch(
            '/movies/12345',
            headers=self.headers,
            data=json.dumps({
                'title': 'It',
                'release_year': '2017',
                'genre': 'Horror'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_movie_no_auth(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        original_data = json.loads(response.data)

        response = self.client().patch(
            f"/movies/{original_data['movie']['id']}",
            data=json.dumps({
                'title': 'It',
                'release_year': '2017',
                'genre': 'Horror'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_movie_no_permission(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        original_data = json.loads(response.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().patch(
            f"/movies/{original_data['movie']['id']}",
            headers=self.headers,
            data=json.dumps({
                'title': 'It',
                'release_year': '2017',
                'genre': 'Horror'
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        original_data = json.loads(response.data)

        response = self.client().delete(
            f"/movies/{original_data['movie']['id']}",
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie_id'], original_data['movie']['id'])

    def test_delete_movie_no_movie_id(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().delete(
            '/movies/12345',
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_movie_no_auth(self):
        response = self.client().delete(
            '/movies/1',
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_movie_no_permission(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        original_data = json.loads(response.data)

        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().delete(
            f"/movies/{original_data['movie']['id']}",
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])

    def test_add_actor_to_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        movie_data = json.loads(response.data)

        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        actor_data = json.loads(response.data)

        response = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movie'], dict)
        self.assertIsInstance(data['movie']['id'], int)
        self.assertEqual(data['movie']['title'], 'The Devil All the Time')
        self.assertEqual(data['movie']['release_year'], '2020')
        self.assertEqual(data['movie']['genre'], 'Drama')
        self.assertIsInstance(data['movie']['actors'], list)
        self.assertIsInstance(data['movie']['actors'][0], dict)
        self.assertEqual(data['movie']['actors'][0]['name'], 'Jason Bourne')
        self.assertEqual(data['movie']['actors'][0]['age'], 35)
        self.assertEqual(data['movie']['actors'][0]['gender'], 'male')

    def test_add_actor_to_movie_already_exists(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        movie_data = json.loads(response.data)

        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        actor_data = json.loads(response.data)

        response = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(response.data)

        response = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 409)
        self.assertFalse(data['success'])

    def test_add_actor_to_movie_no_auth(self):
        response = self.client().post(
            '/movies/1/actors',
            headers=self.headers,
            data=json.dumps({
                'actor_id': 1
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_actor_to_movie_no_permission(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().post(
            '/movies/1/actors',
            headers=self.headers,
            data=json.dumps({
                'actor_id': 1
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])

    def test_delete_actor_from_movie(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        movie_data = json.loads(response.data)

        response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        actor_data = json.loads(response.data)

        response = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(response.data)

        movie_id = movie_data['movie']['id']
        actor_id = actor_data['actor']['id']

        response = self.client().delete(
            f"/movies/{movie_id}/actors/{actor_id}",
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], movie_data['movie']['id'])
        self.assertEqual(data['movie_id'], actor_data['actor']['id'])

    def test_delete_actor_from_movie_no_role(self):
        self.headers.update(
            {'Authorization': f'Bearer {executive_producer_token}'}
        )
        movie_response = self.client().post(
            '/movies',
            headers=self.headers,
            data=json.dumps({
                'title': 'The Devil All the Time',
                'release_year': '2020',
                'genre': 'Drama'
            })
        )
        movie_data = json.loads(movie_response.data)

        actor_response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        actor_data = json.loads(actor_response.data)

        actor2_response = self.client().post(
            '/actors',
            headers=self.headers,
            data=json.dumps({
                'name': 'Jason Bourne',
                'age': 35,
                'gender': 'male'
            })
        )
        actor2_data = json.loads(actor2_response.data)

        add_role_response = self.client().post(
            f"/movies/{movie_data['movie']['id']}/actors",
            headers=self.headers,
            data=json.dumps({
                'actor_id': actor_data['actor']['id']
            })
        )
        data = json.loads(add_role_response.data)

        movie_id = movie_data['movie']['id']
        actor2_id = actor2_data['actor']['id']
        response = self.client().delete(
            f"/movies/{movie_id}/actors/{actor2_id}",
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor_from_movie_no_auth(self):
        response = self.client().delete(
            '/movies/1/actors/1',
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_actor_from_movie_no_permission(self):
        self.headers.update(
            {'Authorization': f'Bearer {casting_assistant_token}'}
        )
        response = self.client().delete(
            '/movies/1/actors/1',
            headers=self.headers
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="./test_results/"))
