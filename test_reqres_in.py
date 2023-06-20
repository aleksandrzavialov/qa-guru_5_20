from jsonschema import validate
from helpers.schema_helpers import load_json_schema, regres_session


def test_create_a_user_with_name_only():
    name = "John"

    response = regres_session.post(
        url='/api/users',
        json={
            "name": name
        }
    )

    assert response.status_code == 201
    assert response.json()['name'] == name
    assert 'job' not in response.json()

    schema1 = load_json_schema('post_create_user_name_only.json')

    validate(instance=response.json(), schema=schema1)


def test_create_a_user_with_name_only_schema_validation():
    name = "jane"
    job = "job"
    schema = load_json_schema('post_create_user_name_only.json')

    response = regres_session.post(
        url='/api/users',
        json={
            "name": name,
            "job": job}
    )

    validate(instance=response.json(), schema=schema)


def test_update_a_user_with_put_both_name_and_job():
    name = "John"
    job = 'Wrestler'

    response = regres_session.put(
        url='/api/users/2',
        json={
            "name": name,
            "job": job
        }
    )

    assert response.status_code == 200
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_update_a_user_with_put_both_name_and_job_schema_validation():
    name = "John"
    job = 'Wrestler'

    schema = load_json_schema('put_update_a_user_with_put_both_name_and_job.json')

    response = regres_session.put(
        url='/api/users/2',
        json={
            "name": name,
            "job": job
        }
    )

    validate(instance=response.json(), schema=schema)


def test_update_a_user_with_patch_only_job():
    job = 'Wrestler'

    response = regres_session.patch(
        url='/api/users/2',
        json={
            "job": job
        }
    )

    assert response.status_code == 200
    assert response.json()['job'] == job
    assert 'name' not in response.json()


def test_update_a_user_with_patch_only_job_schema_validation():
    job = 'Wrestler'

    schema = load_json_schema('put_update_a_user_with_put_both_job_only.json')
    response = regres_session.patch(
        url='/api/users/2',
        json={
            "job": job
        }
    )

    validate(instance=response.json(), schema=schema)


def test_register_an_existing_user():
    email = "lindsay.ferguson@reqres.in"
    password = "1234qwerty"

    response = regres_session.post(
        url='/api/register',
        json={
            "email": email,
            "password": password,
        }
    )

    assert response.status_code == 200
    assert len(str(response.json()['id'])) >= 1
    assert len(response.json()['token']) >= 17


def test_register_an_existing_user_schema_validation():
    email = "lindsay.ferguson@reqres.in"
    password = "1234qwerty"

    schema = load_json_schema('post_register_an_existing_user.json')
    response = regres_session.post(
        url='/api/register',
        json={
            "email": email,
            "password": password,
        }
    )

    validate(instance=response.json(), schema=schema)


def test_unable_to_register_a_not_existing_user():
    email = "test@test.com"
    password = "1234qwerty"

    response = regres_session.post(
        url='/api/register',
        json={
            "email": email,
            "password": password,
        }
    )

    assert response.status_code == 400
    assert (response.json()['error']) == 'Note: Only defined users succeed registration'


def test_unable_to_register_a_not_existing_user_schema_validation():
    email = "test@test.com"
    password = "1234qwerty"

    schema = load_json_schema('post_unable_to_register_a_not_existing_user.json')

    response = regres_session.post(
        url='/api/register',
        json={
            "email": email,
            "password": password,
        }
    )

    validate(instance=response.json(), schema=schema)


def test_unable_to_register_a_existing_user_sending_username_only():
    username = "byron.fields@reqres.in"

    response = regres_session.post(
        url='/api/register',
        json={
            "username": username
        }
    )

    assert response.status_code == 400
    assert (response.json()['error']) == 'Missing password'


def test_unable_to_register_a_existing_user_sending_username_only_schema_validation():
    username = "byron.fields@reqres.in"

    schema = load_json_schema('post_unable_to_register_a_existing_user_sending_username_only.json')

    response = regres_session.post(
        url='/api/register',
        json={
            "username": username
        }
    )

    validate(instance=response.json(), schema=schema)


def test_login_with_existing_user():
    email = "lindsay.ferguson@reqres.in"
    password = "1234qwerty"

    response = regres_session.post(
        url='/api/login',
        json={
            "email": email,
            "password": password,
        }
    )

    assert response.status_code == 200
    assert len(response.json()['token']) >= 17


def test_login_with_existing_user_schema_validation():
    email = "lindsay.ferguson@reqres.in"
    password = "1234qwerty"

    schema = load_json_schema('post_login_with_existing_user.json')

    response = regres_session.post(
        url='/api/login',
        json={
            "email": email,
            "password": password,
        }
    )

    validate(instance=response.json(), schema=schema)


def test_unable_login_with_non_existing_user():
    email = "test.superuser@yandex.ru"
    password = "1234qwerty"

    response = regres_session.post(
        url='/api/login',
        json={
            "email": email,
            "password": password,
        }
    )

    assert response.status_code == 400
    assert (response.json()['error']) == 'user not found'


def test_unable_login_with_non_existing_user_schema_validation():
    email = "test.superuser@yandex.ru"
    password = "1234qwerty"

    schema = load_json_schema('post_unable_login_with_non_existing_user.json')

    response = regres_session.post(
        url='/api/login',
        json={
            "email": email,
            "password": password,
        }
    )

    validate(instance=response.json(), schema=schema)


def test_requested_per_page_number_with_delay_default_page():
    per_page = 3
    delay = 5

    response = regres_session.get('/api/users', params={'delay': delay, 'per_page': per_page})

    assert response.status_code == 200
    assert response.json()['page'] == 1
    assert response.json()['per_page'] == per_page
    assert response.json()['total_pages'] == 4
    assert response.json()['total'] == 12


def test_requested_per_page_number_with_delay_default_page_schema_validation():
    per_page = 3
    delay = 5

    schema = load_json_schema('get_requested_per_page_number_with_delay_default_page.json')

    response = regres_session.get('/api/users', params={'delay': delay, 'per_page': per_page})

    validate(instance=response.json(), schema=schema)


def test_requested_per_page_number_with_delay_second_page():
    per_page = 2
    page = 2
    delay = 3

    response = regres_session.get('/api/users', params={'delay': delay, 'per_page': per_page, 'page': page})

    assert response.status_code == 200
    assert response.json()['page'] == page
    assert response.json()['per_page'] == per_page
    assert response.json()['total_pages'] == 6
    assert response.json()['total'] == 12


def test_requested_per_page_number_with_delay_second_page_schema_validation():
    per_page = 2
    page = 2
    delay = 3

    schema = load_json_schema('get_requested_per_page_number_with_delay_second_page.json')

    response = regres_session.get('/api/users', params={'delay': delay, 'per_page': per_page, 'page': page})

    validate(instance=response.json(), schema=schema)





