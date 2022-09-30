from hashlib import new
import logging
import logging.config

import os

import json

class UserManager(object):
    def __init__(self):
        self.premium_user_file_path = '/usr/src/app/src/premium-users-list'
        self.non_premium_users_directory = '/usr/src/app/src/non_premium-users/'

        self.attempts_for_non_premium_users = 1

        try:
            os.makedirs("/usr/src/app/src/premium-users/")
            os.makedirs(self.non_premium_users_directory)
        except Exception as e:
            print(f"{e=}")
        # open(self.premium_user_file_path, 'w')
        # logging.config.fileConfig(fname='/home/dspitsyn/KNU/ascii-art/telebot/src/logger.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger(__class__.__name__)

    def add_premium_user(self, user_id):
        print(f"{os.path.exists(self.premium_user_file_path)=}")

        self.logger.info(f"{os.path.exists(self.premium_user_file_path)=}")
        if not os.path.exists(self.premium_user_file_path):
            with open(self.premium_user_file_path, 'x') as file:
                file.write(str(user_id) + '\n')
        with open(self.premium_user_file_path, 'a') as file:
            file.write(str(user_id) + '\n')

    def is_premium_user(self, user_id) -> bool:
        with open(self.premium_user_file_path, 'r') as file:
            for line in file:
                self.logger.info(f"{line=}")
                print(f"{line=}")
                print(f"{line.find(str(user_id))=}")
                if (line.find(str(user_id))>=0):
                    return True
            return False

    def is_non_premium_user_able_to_send_image(self, user_id)->bool:
        self.logger.info(__name__ + f" Started with parameters {user_id=}")
        non_premium_user_file = self.non_premium_users_directory + str(user_id)
        self.logger.info(f"{non_premium_user_file=}")
        # if user file is not exist it is his first attempt to create ascii art
        if not os.path.exists(non_premium_user_file):
            self.logger.info(f"Creating file for {user_id=}")
            with open(non_premium_user_file, 'w') as file :
                file.write('1')
            return True
        else:
            with open(non_premium_user_file, "r") as file:
                image_n = file.read()
                self.logger.info(f"{image_n=}")
                self.logger.info(f"{user_id=} did {image_n} ascii arts")
                # checking if non premium user did more than 3 attempts
                # if he is able to do ascii art
            try:
                if int(image_n) < self.attempts_for_non_premium_users:
                    with open(non_premium_user_file, "w") as file:
                        new_n = str(int(image_n) + 1)
                        self.logger.info(f"{new_n=}")
                        file.write(new_n)
                        return True
                else:
                    return False
            except Exception as e:
                self.logger.error(e)


# if __name__ == '__main__':
#     user_mgr = UserManager()

#     user_mgr.add_premium_user('007')
#     user_mgr.add_premium_user('1000')

#     user_mgr.add_premium_user('1001')
#     user_mgr.add_premium_user('1110')

#     user_mgr.logger.info(f"{user_mgr.is_premium_user('1')=}")
#     print(f"{user_mgr.is_premium_user('1')=}")


#     print(f"{user_mgr.is_premium_user('1001')=}")
