# restaurant.py
# โมดูลตรรกะหลักของระบบจัดการร้านอาหาร
# ประกอบด้วย: จัดการเมนู, จัดการโต๊ะ, รับออเดอร์, หน้าจอครัว, เช็คบิล, รายงานยอดขาย

import datetime
from storage import (
    load_json, save_json,
    MENU_FILE, TABLE_FILE, ORDER_FILE, SALES_FILE,
    TABLE_STATUSES, ORDER_STATUSES,
    create_default_menu, create_default_tables
)


# ---------- ฟังก์ชันช่วยรับข้อมูลจากผู้ใช้ (มี try/except ทุกจุด) ----------

def input_int(prompt, min_value=None):
    """รับค่า int จากผู้ใช้พร้อมตรวจสอบความถูกต้อง (return: int)"""
    valid = False
    result = 0
    while not valid:
        try:
            text = input(prompt).strip()
            value = int(text)
            if min_value is not None and value < min_value:
                print(f"กรุณากรอกตัวเลขที่มากกว่าหรือเท่ากับ {min_value}")
            else:
                result = value
                valid = True
        except ValueError:
            print("กรุณากรอกเป็นตัวเลขจำนวนเต็มเท่านั้น")
    return result


def input_float(prompt, min_value=None, max_value=None):
    """รับค่า float จากผู้ใช้พร้อมตรวจสอบความถูกต้อง (return: float)"""
    valid = False
    result = 0.0
    while not valid:
        try:
            text = input(prompt).strip()
            value = float(text)
            if min_value is not None and value < min_value:
                print(f"กรุณากรอกตัวเลขที่มากกว่าหรือเท่ากับ {min_value}")
            elif max_value is not None and value > max_value:
                print(f"กรุณากรอกตัวเลขที่น้อยกว่าหรือเท่ากับ {max_value}")
            else:
                result = value
                valid = True
        except ValueError:
            print("กรุณากรอกเป็นตัวเลขเท่านั้น")
    return result


def input_text(prompt):
    """รับข้อความจากผู้ใช้ ห้ามเป็นค่าว่าง (return: str)"""
    valid = False
    result = ""
    while not valid:
        try:
            text = input(prompt).strip()
            if text == "":
                print("ห้ามเว้นว่าง กรุณากรอกใหม่")
            else:
                result = text
                valid = True
        except Exception:
            print("เกิดข้อผิดพลาดในการรับข้อมูล กรุณาลองใหม่")
    return result


def input_yes_no(prompt):
    """รับคำตอบ ใช่/ไม่ใช่ จากผู้ใช้ (return: bool)"""
    valid = False
    result = False
    while not valid:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer == "y":
            result = True
            valid = True
        elif answer == "n":
            result = False
            valid = True
        else:
            print("กรุณาตอบ y หรือ n เท่านั้น")
    return result


# ============================================================
# 1) จัดการเมนูอาหาร
# ============================================================

def load_menu():
    """โหลดข้อมูลเมนูจากไฟล์ (return: list of dict)"""
    return load_json(MENU_FILE, create_default_menu())


def save_menu(menu_list):
    """บันทึกข้อมูลเมนูลงไฟล์ (return: bool)"""
    return save_json(MENU_FILE, menu_list)


def generate_next_id(item_list):
    """หา id ถัดไปที่ยังไม่ถูกใช้ในลิสต์ของ dict ที่มีคีย์ 'id' (return: int)"""
    max_id = 0
    for item in item_list:                # for loop วนหาค่า id สูงสุด
        if item["id"] > max_id:
            max_id = item["id"]
    return max_id + 1


def add_menu_item(menu_list, name, category, price, image):
    """
    เพิ่มเมนูใหม่เข้า menu_list
    parameter: menu_list (list), name (str), category (str), price (float), image (str)
    return: menu_list ที่อัปเดตแล้ว (list)
    """
    new_item = {
        "id": generate_next_id(menu_list),
        "name": name,
        "category": category,
        "price": float(price),
        "image": image,
        "out_of_stock": False
    }
    menu_list.append(new_item)
    return menu_list


def find_menu_item(menu_list, menu_id):
    """ค้นหาเมนูจาก id (return: dict หรือ None)"""
    found_item = None
    for item in menu_list:
        if item["id"] == menu_id:
            found_item = item
    return found_item


def edit_menu_price(menu_list, menu_id, new_price):
    """แก้ไขราคาของเมนู (return: bool สำเร็จหรือไม่)"""
    item = find_menu_item(menu_list, menu_id)
    success = False
    if item is not None and new_price >= 0:
        item["price"] = float(new_price)
        success = True
    return success


def toggle_stock_status(menu_list, menu_id):
    """สลับสถานะหมด/มี ของเมนู (return: bool สำเร็จหรือไม่)"""
    item = find_menu_item(menu_list, menu_id)
    success = False
    if item is not None:
        item["out_of_stock"] = not item["out_of_stock"]
        success = True
    return success


def delete_menu_item(menu_list, menu_id):
    """ลบเมนูออกจากลิสต์ (return: bool สำเร็จหรือไม่)"""
    item = find_menu_item(menu_list, menu_id)
    success = False
    if item is not None:
        menu_list.remove(item)
        success = True
    return success


def show_menu(menu_list):
    """แสดงรายการเมนูทั้งหมด (return: None)"""
    if len(menu_list) == 0:
        print("ยังไม่มีเมนูในระบบ")
    else:
        print(f"{'ID':<4}{'ชื่อเมนู':<20}{'หมวดหมู่':<16}{'ราคา':>8}   สถานะ")
        print("-" * 60)
        for item in menu_list:
            if item["out_of_stock"]:
                status_text = "หมด"
            else:
                status_text = "มี"
            print(f"{item['id']:<4}{item['name']:<20}{item['category']:<16}"
                  f"{item['price']:>8.2f}   {status_text}")


# ============================================================
# 2) จัดการโต๊ะ
# ============================================================

def load_tables():
    """โหลดข้อมูลโต๊ะจากไฟล์ (return: list of dict)"""
    return load_json(TABLE_FILE, create_default_tables())


def save_tables(tables):
    """บันทึกข้อมูลโต๊ะลงไฟล์ (return: bool)"""
    return save_json(TABLE_FILE, tables)


def find_table(tables, table_id):
    """ค้นหาโต๊ะจาก id (return: dict หรือ None)"""
    result = None
    for table in tables:
        if table["id"] == table_id:
            result = table
    return result


def change_table_status(tables, table_id, new_status):
    """
    เปลี่ยนสถานะโต๊ะ
    parameter: tables (list), table_id (int), new_status (str)
    return: bool สำเร็จหรือไม่
    """
    table = find_table(tables, table_id)
    success = False
    if table is not None and new_status in TABLE_STATUSES:
        table["status"] = new_status
        success = True
    return success


def show_tables(tables):
    """แสดงสถานะโต๊ะทั้งหมด (return: None)"""
    for table in tables:
        print(f"โต๊ะ {table['id']:<3} สถานะ: {table['status']}")


# ============================================================
# 3) รับออเดอร์ต่อโต๊ะ
# ============================================================

def load_orders():
    """โหลดข้อมูลออเดอร์ทั้งหมด (return: dict {table_id(str): [items]})"""
    return load_json(ORDER_FILE, {})


def save_orders(orders):
    """บันทึกข้อมูลออเดอร์ลงไฟล์ (return: bool)"""
    return save_json(ORDER_FILE, orders)


def add_order_item(orders, table_id, menu_item, qty):
    """
    เพิ่มรายการอาหารลงในออเดอร์ของโต๊ะ
    parameter: orders (dict), table_id (int), menu_item (dict), qty (int)
    return: bool สำเร็จหรือไม่ (ไม่สำเร็จถ้าเมนูหมด หรือ qty ไม่ถูกต้อง)
    """
    success = False
    if menu_item is not None and not menu_item["out_of_stock"] and qty > 0:
        key = str(table_id)
        if key not in orders:
            orders[key] = []
        order_line = {
            "menu_id": menu_item["id"],
            "name": menu_item["name"],
            "price": menu_item["price"],
            "qty": qty,
            "status": "รอทำ",
            "time": datetime.datetime.now().strftime("%H:%M:%S")
        }
        orders[key].append(order_line)
        success = True
    return success


def update_order_qty(orders, table_id, line_index, new_qty):
    """
    ปรับจำนวนรายการอาหารในออเดอร์ ถ้า new_qty <= 0 จะลบรายการนั้นทิ้ง
    parameter: orders (dict), table_id (int), line_index (int, เริ่มที่ 0), new_qty (int)
    return: bool สำเร็จหรือไม่
    """
    key = str(table_id)
    success = False
    if key in orders and 0 <= line_index < len(orders[key]):
        if new_qty <= 0:
            del orders[key][line_index]
        else:
            orders[key][line_index]["qty"] = new_qty
        success = True
    return success


def show_table_order(orders, table_id):
    """แสดงออเดอร์ปัจจุบันของโต๊ะที่ระบุ (return: float ยอดรวมของโต๊ะนั้น)"""
    key = str(table_id)
    subtotal = 0.0
    if key not in orders or len(orders[key]) == 0:
        print("โต๊ะนี้ยังไม่มีรายการอาหาร")
    else:
        print(f"{'#':<3}{'รายการ':<20}{'จำนวน':>6}{'ราคา/หน่วย':>12}{'รวม':>10}  สถานะ")
        index = 0
        while index < len(orders[key]):        # while loop แบบ index-based ตามที่ถนัด
            line = orders[key][index]
            line_total = line["price"] * line["qty"]
            subtotal += line_total
            print(f"{index:<3}{line['name']:<20}{line['qty']:>6}"
                  f"{line['price']:>12.2f}{line_total:>10.2f}  {line['status']}")
            index += 1
    return subtotal


# ============================================================
# 4) หน้าจอครัว (Kitchen Display)
# ============================================================

def kitchen_display(orders):
    """
    แสดงรายการอาหารทุกโต๊ะที่ยังไม่เสร็จ เรียงตามเวลาสั่ง
    parameter: orders (dict)
    return: None
    """
    pending_items = []
    for table_key in orders:
        for line in orders[table_key]:
            if line["status"] != "เสร็จแล้ว":
                pending_items.append((table_key, line))

    if len(pending_items) == 0:
        print("ไม่มีออเดอร์ค้างในครัว")
    else:
        pending_items.sort(key=lambda pair: pair[1]["time"])  # เรียงตามเวลา
        print(f"{'เวลา':<10}{'โต๊ะ':<6}{'เมนู':<20}{'จำนวน':>6}  สถานะ")
        for table_key, line in pending_items:
            print(f"{line['time']:<10}{table_key:<6}{line['name']:<20}"
                  f"{line['qty']:>6}  {line['status']}")


def update_kitchen_status(orders, table_id, line_index, new_status):
    """อัปเดตสถานะของรายการอาหารในครัว (return: bool สำเร็จหรือไม่)"""
    key = str(table_id)
    success = False
    if key in orders and 0 <= line_index < len(orders[key]) and new_status in ORDER_STATUSES:
        orders[key][line_index]["status"] = new_status
        success = True
    return success


# ============================================================
# 5) เช็คบิล
# ============================================================

def calculate_bill(order_items, discount_percent, tax_percent, service_percent):
    """
    คำนวณยอดบิล
    parameter: order_items (list of dict), discount_percent/tax_percent/service_percent (float, 0-100)
    return: dict รายละเอียดบิลทั้งหมด
    """
    subtotal = 0.0
    for line in order_items:
        subtotal += line["price"] * line["qty"]

    discount_amount = subtotal * (discount_percent / 100)
    after_discount = subtotal - discount_amount
    service_amount = after_discount * (service_percent / 100)
    tax_amount = (after_discount + service_amount) * (tax_percent / 100)
    total = after_discount + service_amount + tax_amount

    bill = {
        "subtotal": round(subtotal, 2),
        "discount_percent": discount_percent,
        "discount_amount": round(discount_amount, 2),
        "service_percent": service_percent,
        "service_amount": round(service_amount, 2),
        "tax_percent": tax_percent,
        "tax_amount": round(tax_amount, 2),
        "total": round(total, 2)
    }
    return bill


def print_receipt(bill, table_id, order_items):
    """แสดง/พิมพ์ใบเสร็จรับเงิน (return: None)"""
    print("=" * 40)
    print("            ใบเสร็จรับเงิน")
    print("=" * 40)
    print(f"โต๊ะ: {table_id}")
    print(f"วันที่: {datetime.date.today()}")
    print("-" * 40)
    for line in order_items:
        line_total = line["price"] * line["qty"]
        print(f"{line['name']:<20}{line['qty']:>3} x {line['price']:>7.2f} = {line_total:>8.2f}")
    print("-" * 40)
    print(f"ยอดรวม:            {bill['subtotal']:>10.2f}")
    print(f"ส่วนลด ({bill['discount_percent']}%):     -{bill['discount_amount']:>9.2f}")
    print(f"ค่าบริการ ({bill['service_percent']}%):   {bill['service_amount']:>10.2f}")
    print(f"ภาษี ({bill['tax_percent']}%):          {bill['tax_amount']:>10.2f}")
    print("-" * 40)
    print(f"ยอดสุทธิ:           {bill['total']:>10.2f}")
    print("=" * 40)


def load_sales():
    """โหลดประวัติการขายทั้งหมด (return: list)"""
    return load_json(SALES_FILE, [])


def save_sales(sales):
    """บันทึกประวัติการขายลงไฟล์ (return: bool)"""
    return save_json(SALES_FILE, sales)


def record_sale(sales, table_id, order_items, bill):
    """
    บันทึกการขายที่ปิดบิลแล้วเข้า sales list
    parameter: sales (list), table_id (int), order_items (list), bill (dict)
    return: sales list ที่อัปเดตแล้ว
    """
    record = {
        "date": str(datetime.date.today()),
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "table_id": table_id,
        "items": order_items,
        "bill": bill
    }
    sales.append(record)
    return sales


# ============================================================
# 6) รายงานยอดขาย
# ============================================================

def daily_sales_report(sales, target_date):
    """
    สรุปยอดขายของวันที่ระบุ
    parameter: sales (list), target_date (str เช่น '2026-09-27')
    return: dict {"total_bills": int, "total_amount": float}
    """
    total_bills = 0
    total_amount = 0.0
    for record in sales:
        if record["date"] == target_date:
            total_bills += 1
            total_amount += record["bill"]["total"]
    return {"total_bills": total_bills, "total_amount": round(total_amount, 2)}


def best_selling_items(sales, target_date=None, top_n=5):
    """
    หาสรุปเมนูขายดี นับจากจำนวนที่ขายได้
    parameter: sales (list), target_date (str หรือ None สำหรับทุกวัน), top_n (int)
    return: list of tuple (ชื่อเมนู, จำนวนที่ขายรวม) เรียงจากมากไปน้อย
    """
    qty_by_name = {}   # dict สำหรับสะสมจำนวนขายต่อเมนู
    for record in sales:
        if target_date is None or record["date"] == target_date:
            for line in record["items"]:
                name = line["name"]
                if name in qty_by_name:
                    qty_by_name[name] += line["qty"]
                else:
                    qty_by_name[name] = line["qty"]

    ranking = list(qty_by_name.items())
    ranking.sort(key=lambda pair: pair[1], reverse=True)
    return ranking[:top_n]
