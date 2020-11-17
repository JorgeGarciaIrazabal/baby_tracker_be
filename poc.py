from passlib.hash import sha256_crypt

from src.app import Session
from src.models import Parent
from src.services.auth import encrypt_password

password = sha256_crypt.hash("password")
password2 = sha256_crypt.hash("password")

hash = '$5$rounds=535000$fflD0vlqYhDw604y$BUnK2G5Wixtt0cPFpxqYQxghe5nxA2Tn/vRyvTsyvG4'
print(password)
print(password2)

if __name__ == '__main__':
    db = Session()
    for parent in db.query(Parent).all():
        parent.password = encrypt_password(parent.password)
        db.add(parent)
    db.commit()
    db.close()
