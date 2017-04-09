import DbConnection

db = DbConnection.DbManager()


def test_creation():
    test_user = 'testname1'
    test_email = 'test@email.com'
    db.create_user(test_user, test_email)
    if db.fetch_user(test_user, test_email) != [(test_user, test_email)]:
        raise NameError("User creation test failed")
    else:
        return True


def test_update():
    test_user1 = 'testname1'
    test_email1 = 'test1@email.com'
    test_user2 = 'testname2'
    test_email2 = 'test2@email.com'
    db.create_user(test_user1, test_email1)
    db.create_user(test_user1, test_email2)
    try:
        db.update_user(test_user1, 'error')
    except NameError:
        return True

    return NameError('Ambiguous user update test failed.')


test_creation()
test_update()
