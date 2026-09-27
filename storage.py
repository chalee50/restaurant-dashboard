# storage.py
# โมดูลจัดการไฟล์ (บันทึก/โหลดข้อมูล) สำหรับระบบจัดการร้านอาหาร
# ใช้ไฟล์ JSON ในการเก็บข้อมูล เพื่อให้ปิดโปรแกรมแล้วเปิดใหม่ ข้อมูลยังอยู่

import json
import os

MENU_FILE = "menu.json"
TABLE_FILE = "tables.json"
ORDER_FILE = "orders.json"
SALES_FILE = "sales.json"

TABLE_STATUSES = ("ว่าง", "มีลูกค้า", "รอเช็คบิล")   # tuple: ค่าคงที่ ไม่ต้องเปลี่ยนแปลง
ORDER_STATUSES = {"รอทำ", "กำลังทำ", "เสร็จแล้ว"}     # set: ใช้ตรวจสอบสถานะที่ถูกต้อง


def load_json(filename, default_value):
    """
    โหลดข้อมูลจากไฟล์ JSON
    parameter: filename (str) ชื่อไฟล์, default_value ค่าที่จะคืนถ้าไม่มีไฟล์/ไฟล์เสีย
    return: ข้อมูลที่โหลดได้ (list หรือ dict)
    """
    data = default_value
    if os.path.exists(filename):
        try:
            file = open(filename, "r", encoding="utf-8")
            data = json.load(file)
            file.close()
        except (json.JSONDecodeError, OSError):
            print(f"⚠ ไม่สามารถอ่านไฟล์ {filename} ได้ จะใช้ข้อมูลเริ่มต้นแทน")
            data = default_value
    return data


def save_json(filename, data):
    """
    บันทึกข้อมูลลงไฟล์ JSON
    parameter: filename (str), data (list/dict)
    return: True ถ้าบันทึกสำเร็จ, False ถ้าไม่สำเร็จ
    """
    success = False
    try:
        file = open(filename, "w", encoding="utf-8")
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.close()
        success = True
    except OSError:
        print(f"⚠ ไม่สามารถบันทึกไฟล์ {filename} ได้")
        success = False
    return success


def create_default_menu():
    """สร้างเมนูตั้งต้น (ใช้ตอนยังไม่มีไฟล์ menu.json)"""
    default_menu = [
        {"id": 1, "name": "ผัดกะเพราหมู", "category": "อาหารจานเดียว", "price": 50.0,
         "image": "kaprao.jpg", "out_of_stock": False},
        {"id": 2, "name": "ข้าวผัดปู", "category": "อาหารจานเดียว", "price": 60.0,
         "image": "khaopad.jpg", "out_of_stock": False},
        {"id": 3, "name": "ต้มยำกุ้ง", "category": "ต้ม/แกง", "price": 120.0,
         "image": "tomyum.jpg", "out_of_stock": False},
        {"id": 4, "name": "ชาเย็น", "category": "เครื่องดื่ม", "price": 25.0,
         "image": "chayen.jpg", "out_of_stock": False},
    ]
    return default_menu


def create_default_tables(number_of_tables=10):
    """สร้างโต๊ะตั้งต้นตามจำนวนที่กำหนด (ใช้ตอนยังไม่มีไฟล์ tables.json)"""
    tables = []
    index = 1
    while index <= number_of_tables:      # while loop แบบมีตัวแปรนับ (index-based)
        tables.append({"id": index, "status": "ว่าง"})
        index += 1
    return tables
