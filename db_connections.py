from datetime import datetime

import pymysql

db = pymysql.connect(
    host="localhost",
    db="mysql",
    user="root",
    password="kiwMmya7xtS%DE"
)
cursor = db.cursor()


def init_table():
    """初始化Users, VehicleInfo, ChargeRecords, RFIDTags表"""
    create_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password BLOB NOT NULL
    )
    """
    create_vehicle_info = """
    CREATE TABLE IF NOT EXISTS vehicle_info (
        VehicleID INT AUTO_INCREMENT PRIMARY KEY,
        LicensePlate VARCHAR(20) NOT NULL,
        VehicleType VARCHAR(50),
        OwnerName VARCHAR(100),
        ContactInfo VARCHAR(100)
    )
    """
    create_rfid_tags = """
    CREATE TABLE IF NOT EXISTS rfid_tags (
        TagID INT AUTO_INCREMENT PRIMARY KEY,
        TagNumber VARCHAR(50) NOT NULL,
        VehicleID INT,
        IsActive TINYINT(1) DEFAULT 1,
        FOREIGN KEY (VehicleID) REFERENCES vehicle_info(VehicleID)
    );
    """
    create_charge_records = """
    CREATE TABLE IF NOT EXISTS charge_records (
        RecordID INT AUTO_INCREMENT PRIMARY KEY,
        VehicleID INT,
        RFIDTagID INT,
        EntryTime DATETIME,
        ExitTime DATETIME,
        Charge DECIMAL(10, 2),
        FOREIGN KEY (VehicleID) REFERENCES vehicle_info(VehicleID),
        FOREIGN KEY (RFIDTagID) REFERENCES rfid_tags(TagID)
    );
    """
    cursor.execute(create_users)
    cursor.execute(create_vehicle_info)
    cursor.execute(create_rfid_tags)
    cursor.execute(create_charge_records)


def add_user(username, password):
    """插入用户名密码，密码使用AES加密"""
    sql = "INSERT INTO users (username, password) VALUES (%s, AES_ENCRYPT(%s, 'usee111'))"
    cursor.execute(sql, (username, password))
    db.commit()


def authenticate_user(username, password):
    """验证用户账号密码，密码进行相同的AES加密之后与数据库中的密码比对"""
    sql = "SELECT * FROM users WHERE username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    if result:
        sql = "SELECT * FROM users WHERE username=%s and password=AES_ENCRYPT(%s, 'usee111')"
        if cursor.execute(sql, (username, password)):
            print("登录成功")
            return 1
        else:
            print("密码错误")
            return 0
    else:
        print("用户不存在")
        return -1


def change_password(username, old_password, new_password):
    """修改用户密码"""
    # 验证用户身份
    result = authenticate_user(username, old_password)
    if result == 1:
        # 更新密码
        update_sql = "UPDATE users SET password=AES_ENCRYPT(%s, 'usee111') WHERE username=%s"
        cursor.execute(update_sql, (new_password, username))
        db.commit()
        print("Password updated successfully")
        return 1
    elif result == 0:
        print("Invalid old password")
        return 0
    else:
        print("User not found")
        return -1


def add_new_car(car: str, card_id: str):
    """添加一条车辆数据以及关联的RFIDTag"""
    try:
        # 检查LicensePlate是否已经存在
        cursor.execute("SELECT VehicleID FROM vehicle_info WHERE LicensePlate = %s", (car,))
        existing_vehicle = cursor.fetchone()

        if existing_vehicle:
            print(f"车辆已存在，VehicleID: {existing_vehicle[0]}")
        else:
            # 插入车辆数据
            insert_data_query = "INSERT INTO vehicle_info (LicensePlate) VALUES (%s)"
            cursor.execute(insert_data_query, car)
            db.commit()  # 提交事务

            # 获取插入后的车辆ID0j
            cursor.execute("select LAST_INSERT_ID()")
            vehicle_id = cursor.fetchone()[0]

            # 插入RFID标签数据
            insert_rfid = "INSERT INTO rfid_tags (TagNumber, VehicleID) VALUES (%s, %s)"
            cursor.execute(insert_rfid, (card_id, vehicle_id))
            db.commit()
    except Exception as e:
        db.rollback()  # 发生异常时回滚事务
        print(f"An error occurred: {e}")


def car_entry(tag_number):
    """车辆进入"""
    try:
        # 查找与标签号相关的车辆和RFID标签ID
        cursor.execute("SELECT VehicleID, TagID AS RFIDTagID FROM rfid_tags WHERE TagNumber = %s", tag_number)
        (vehicle_id, rfid_tag_id) = cursor.fetchone()

        # 获取当前时间并截取到秒
        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 记录车辆进入时间
        insert_entry_time_query = "INSERT INTO charge_records (VehicleID, RFIDTagID, EntryTime) VALUES (%s, %s, %s)"
        cursor.execute(insert_entry_time_query, (vehicle_id, rfid_tag_id, entry_time))
        db.commit()  # 提交事务
    except Exception as e:
        db.rollback()  # 发生异常时回滚事务
        print(f"An error occurred: {e}")


def car_exit(tag_number):
    """车辆离开，并返回总费用"""
    try:
        # 查找与标签号相关的车辆和RFID标签ID
        cursor.execute("SELECT VehicleID, TagID AS RFIDTagID FROM rfid_tags WHERE TagNumber = %s", tag_number)
        (vehicle_id, rfid_tag_id) = cursor.fetchone()

        # 获取当前时间并截取到秒作为离开时间
        exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 查询入场时间
        cursor.execute("SELECT EntryTime FROM charge_records WHERE RFIDTagID = %s AND ExitTime IS NULL", rfid_tag_id)
        entry_time = cursor.fetchone()[0]

        # 计算费用（费率为每小时 X 元）
        hourly_rate = 10  # 费率为 10 元/小时
        exit_time = datetime.strptime(exit_time, '%Y-%m-%d %H:%M:%S')
        time_difference = exit_time - entry_time
        hours = time_difference.total_seconds()
        charge = hours * hourly_rate / 3600
        charge = round(charge, 2)

        # 更新离开时间和费用
        update_query = "UPDATE charge_records SET ExitTime = %s, Charge = %s WHERE RFIDTagID = %s AND ExitTime IS NULL"
        cursor.execute(update_query, (exit_time, charge, rfid_tag_id))
        db.commit()  # 提交事务
        return charge

    except Exception as e:
        db.rollback()  # 发生异常时回滚事务
        print(f"An error occurred: {e}")


def determine_entry_or_exit(tag_number):
    """检测到IC卡之后判断是车辆进入还是离开，执行对应的函数，返回-1 or -2 or 费用"""

    cursor.execute("SELECT COUNT(*) FROM rfid_tags WHERE TagNumber = %s", tag_number)
    exist = cursor.fetchone()[0]
    if exist == 0:
        return -2
    cursor.execute("SELECT VehicleID FROM rfid_tags WHERE TagNumber = %s", tag_number)
    vehicle_id = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM charge_records WHERE VehicleID = %s AND ExitTime IS NULL",
        vehicle_id)
    entry_count = cursor.fetchone()[0]

    if entry_count > 0:
        charge = car_exit(tag_number)
        return charge
    else:
        car_entry(tag_number)
        return -1


def delete_all():
    cursor.execute("DROP TABLE IF EXISTS users, charge_records, vehicle_info, rfid_tags")

