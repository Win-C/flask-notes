from app import db
from models import User, Note

db.drop_all()
db.create_all()

u1 = User.register(
    username="test1",
    password="password1",
    email="test1@gmail.com",
    first_name="test1",
    last_name="test1",
    )

u2 = User.register(
    username="test2",
    password="test2",
    email="test2@gmail.com",
    first_name="test2",
    last_name="test2",
)

db.session.add(u1)
db.session.add(u2)
db.session.commit()

n1 = Note(
    title="testNote",
    content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quaerat ad placeat enim ipsum temporibus ullam distinctio laboriosam labore cum aperiam, iure ipsa tempore harum. Repellendus quam iste tempora sunt soluta?st1",
    owner="test1",
)

n2 = Note(
    title="testNote",
    content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quaerat ad placeat enim ipsum temporibus ullam distinctio laboriosam labore cum aperiam, iure ipsa tempore harum. Repellendus quam iste tempora sunt soluta?st1",
    owner="test1",
)

db.session.add(n1)
db.session.add(n2)
db.session.commit()
