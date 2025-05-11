from data.user import User
from data import db_session

db_session.global_init('db/users.db')
session = db_session.create_session()

user = User()
user.name = 'Алексей'
user.gender = 'Мужской'
user.additionally = 'Развожу лошадей'
user.hashed_password = 'ogurec666'
user.age = 20
user.image = 'static/images/img.png'
user.link = '@alekseyAlekseyevich'

user1 = User()
user1.name = 'Жанна'
user1.gender = 'Женский'
user1.additionally = 'Голливудская звезда'
user1.hashed_password = 'йцу123'
user1.age = 45
user1.image = 'static/images/img_1.png'
user1.link = '@star'

user2 = User()
user2.name = 'Оксана'
user2.gender = 'Женский'
user2.additionally = 'Заботливая мама двух львят'
user2.hashed_password = '16.05.1986'
user2.age = 36
user2.image = 'static/images/img_2.png'
user2.link = '@Oksanochka'

user3 = User()
user3.name = 'Дарина'
user3.gender = 'Женский'
user3.additionally = 'Задумалась'
user3.hashed_password = 'qwerty'
user3.age = 21
user3.image = 'static/images/img_3.png'
user3.link = '@Darinka777'

user4 = User()
user4.name = 'Екатерина'
user4.gender = 'Женский'
user4.additionally = 'Ищу достойного мужчину'
user4.hashed_password = 'фффффффф'
user4.age = 28
user4.image = 'static/images/img_4.png'
user4.link = '@Ekaterina1999'

user5 = User()
user5.name = 'Ольга'
user5.gender = 'Женский'
user5.additionally = 'Жду мальчика'
user5.hashed_password = 'tir555'
user5.age = 19
user5.image = 'static/images/img_5.png'
user5.link = '@Olga'

user6 = User()
user6.name = 'Сергей'
user6.gender = 'Мужской'
user6.additionally = 'Успешен, умен, богат'
user6.hashed_password = 'ghjkl33'
user6.age = 21
user6.image = 'static/images/img_6.png'
user6.link = '@Sergey'

user7 = User()
user7.name = 'Тимур'
user7.gender = 'Мужской'
user7.additionally = 'Снимался в сериале'
user7.hashed_password = 'ghjkl344'
user7.age = 25
user7.image = 'static/images/img_8.png'
user7.link = '@Timur'

user8 = User()
user8.name = 'Марина'
user8.gender = 'Женский'
user8.additionally = 'Ищу красивого молодого мальчика, готова переписать наследство'
user8.hashed_password = '123456789'
user8.age = 52
user8.image = 'static/images/imgg.jpg'
user8.link = '@Marina'

user9 = User()
user9.name = 'Алина'
user9.gender = 'Женский'
user9.additionally = 'Идеальная женщина'
user9.hashed_password = '12345678910'
user9.age = 25
user9.image = 'static/images/img_7.png'
user9.link = '@Alina'


session.add(user)
session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.add(user6)
session.add(user7)
session.add(user8)
session.add(user9)
session.commit()