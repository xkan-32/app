import mysql.connector

# MySQLに接続する
cnx = mysql.connector.connect(
    user='ユーザー名',
    password='パスワード',
    host='ホスト名',
    database='データベース名'
)

# 接続できているか確認する
print(cnx)

# テーブル作成用のSQL文
create_table = """
CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255),
    address VARCHAR(255)
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    paid_at DATETIME NOT NULL,
    FOREIGN KEY(member_id) REFERENCES members(id)
);
"""

# テーブル作成
cursor = cnx.cursor()
for result in cursor.execute(create_table, multi=True):
    pass
cursor.close()

# コミットする
cnx.commit()

# MySQLから切断する
cnx.close()
