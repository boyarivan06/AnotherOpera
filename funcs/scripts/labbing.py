from just_patterns import (NotificatedAdmin,
                           UserManager, UserDataBase, AdminStrategy,
                           DevStrategy, Subject, UserFactory)

def main():
    user1 = UserFactory.create_user('developer', 'Jim')
    user2 = UserFactory.create_user('admin', 'Michael')
    sender = Subject()
    sender.add_observer(user1)
    sender.add_observer(user2)
    admin_manager = UserManager(AdminStrategy)
    dev_manager = UserManager(DevStrategy)

    DB = UserDataBase()

    DB.append(user1)
    DB.append(user2)
    for user in DB:
        if type(user) == NotificatedAdmin:
            admin_manager.execute()
            sender.notify('Админ в работе')
        else:
            dev_manager.execute()
            sender.notify('Прогер в работе')
    print(DB)

if __name__ == '__main__':
    main()