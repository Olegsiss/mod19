from api import PetFriends
from setting import valid_email, valid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_api_key_for_failed_user(email='valid_email', password='valid_password'):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    if email == valid_email:
        print('Invalid password')
    elif password == valid_password:
        print('Invalid email')
    else:
        print('Invalid password and email')


def test_get_my_pets_with_valid_key(filter="my_pets"):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_my_pets(auth_key, filter)
    print('Количество питомцев:', len(result['pets']))

    assert status == 200
    assert len(result['pets']) == 2


def test_delete_my_pets(filter="my_pets"):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_my_pets(auth_key, filter)
    print('Количество питомцев:', len(result['pets']))

    if len(result['pets']) > 0:
        pet_id = result['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
    else:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "cat1.jpg")
        _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Котик', animal_type='домашний',
                                             age='1', pet_photo='cat1.jpg'):
            pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
            _, auth_key = pf.get_api_key(valid_email, valid_password)
            status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

            assert status == 200
            assert result['name'] == name


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_photo_replacement_my_pets(pet_photo='cat2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
    try:
        pet_id = '5abc4f7a-54e8-400b-bf00-1c5bdab27303'
        status = pf.update_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 200
    except AssertionError:
        pet_id = my_pets['pets'][0]['id']
        status = pf.update_pet_photo(auth_key, pet_id, pet_photo)
        assert status == 200


def test_add_new_pet_with_invalid_data(name='крот', animal_type='домашний',
                                     age='1', pet_photo='cat3.gif'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 500


def test_delete_data_my_pets(name="5"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")

    status, result = pf.delete_pet_info(auth_key, my_pets['pets'][0]['id'], name)
    assert status == 200
    assert result['name'] == name


def test_delete_all_my_pets(filter="my_pets"):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_my_pets(auth_key, filter)
    d = len(result['pets'])
    if d == 0:
        assert status == 200
        assert d == 0
    else:
        pet_id = result['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
        assert status == 200
        assert d == 0





