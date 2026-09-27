# main.py
# โปรแกรมหลัก: ระบบจัดการร้านอาหาร (Restaurant Management System)
# รันไฟล์นี้เพื่อเริ่มโปรแกรม:  python main.py

import restaurant as rs


def menu_management_menu():
    """เมนูย่อย: จัดการเมนูอาหาร (return: None)"""
    menu_list = rs.load_menu()
    running = True
    while running:
        print("\n--- จัดการเมนูอาหาร ---")
        print("1. แสดงเมนูทั้งหมด")
        print("2. เพิ่มเมนูใหม่")
        print("3. แก้ไขราคาเมนู")
        print("4. เปลี่ยนสถานะหมด/มี")
        print("5. ลบเมนู")
        print("0. กลับเมนูหลัก")
        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            rs.show_menu(menu_list)
        elif choice == "2":
            name = rs.input_text("ชื่อเมนู: ")
            category = rs.input_text("หมวดหมู่: ")
            price = rs.input_float("ราคา: ", min_value=0)
            image = rs.input_text("ชื่อไฟล์รูปภาพ (เช่น food.jpg): ")
            rs.add_menu_item(menu_list, name, category, price, image)
            rs.save_menu(menu_list)
            print("เพิ่มเมนูสำเร็จ")
        elif choice == "3":
            rs.show_menu(menu_list)
            menu_id = rs.input_int("ใส่ ID เมนูที่จะแก้ไขราคา: ")
            new_price = rs.input_float("ราคาใหม่: ", min_value=0)
            if rs.edit_menu_price(menu_list, menu_id, new_price):
                rs.save_menu(menu_list)
                print("แก้ไขราคาสำเร็จ")
            else:
                print("ไม่พบเมนูนี้")
        elif choice == "4":
            rs.show_menu(menu_list)
            menu_id = rs.input_int("ใส่ ID เมนูที่จะเปลี่ยนสถานะ: ")
            if rs.toggle_stock_status(menu_list, menu_id):
                rs.save_menu(menu_list)
                print("เปลี่ยนสถานะสำเร็จ")
            else:
                print("ไม่พบเมนูนี้")
        elif choice == "5":
            rs.show_menu(menu_list)
            menu_id = rs.input_int("ใส่ ID เมนูที่จะลบ: ")
            if rs.delete_menu_item(menu_list, menu_id):
                rs.save_menu(menu_list)
                print("ลบเมนูสำเร็จ")
            else:
                print("ไม่พบเมนูนี้")
        elif choice == "0":
            running = False
        else:
            print("กรุณาเลือกตัวเลขในเมนูเท่านั้น")


def table_management_menu():
    """เมนูย่อย: จัดการโต๊ะ (return: None)"""
    tables = rs.load_tables()
    running = True
    while running:
        print("\n--- จัดการโต๊ะ ---")
        print("1. แสดงสถานะโต๊ะทั้งหมด")
        print("2. เปลี่ยนสถานะโต๊ะ")
        print("0. กลับเมนูหลัก")
        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            rs.show_tables(tables)
        elif choice == "2":
            rs.show_tables(tables)
            table_id = rs.input_int("ใส่หมายเลขโต๊ะ: ")
            print("สถานะที่เลือกได้: 1) ว่าง  2) มีลูกค้า  3) รอเช็คบิล")
            status_choice = rs.input_int("เลือกสถานะ: ", min_value=1)
            if status_choice == 1:
                new_status = "ว่าง"
            elif status_choice == 2:
                new_status = "มีลูกค้า"
            elif status_choice == 3:
                new_status = "รอเช็คบิล"
            else:
                new_status = None

            if new_status is not None and rs.change_table_status(tables, table_id, new_status):
                rs.save_tables(tables)
                print("เปลี่ยนสถานะโต๊ะสำเร็จ")
            else:
                print("ไม่สำเร็จ: ไม่พบโต๊ะนี้ หรือสถานะไม่ถูกต้อง")
        elif choice == "0":
            running = False
        else:
            print("กรุณาเลือกตัวเลขในเมนูเท่านั้น")


def order_menu():
    """เมนูย่อย: รับออเดอร์ต่อโต๊ะ (return: None)"""
    menu_list = rs.load_menu()
    tables = rs.load_tables()
    orders = rs.load_orders()
    running = True
    while running:
        print("\n--- รับออเดอร์ ---")
        print("1. เพิ่มรายการอาหารให้โต๊ะ")
        print("2. ลดจำนวน/ยกเลิกรายการ")
        print("3. แสดงออเดอร์ปัจจุบันของโต๊ะ")
        print("0. กลับเมนูหลัก")
        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            table_id = rs.input_int("ใส่หมายเลขโต๊ะ: ")
            table = rs.find_table(tables, table_id)
            if table is None:
                print("ไม่พบโต๊ะนี้")
            else:
                # เงื่อนไขประกอบ: ถ้าโต๊ะว่างอยู่ ให้เปลี่ยนเป็นมีลูกค้าโดยอัตโนมัติ
                if table["status"] == "ว่าง" or table["status"] == "รอเช็คบิล":
                    rs.change_table_status(tables, table_id, "มีลูกค้า")
                    rs.save_tables(tables)

                rs.show_menu(menu_list)
                menu_id = rs.input_int("ใส่ ID เมนูที่ต้องการสั่ง: ")
                menu_item = rs.find_menu_item(menu_list, menu_id)
                if menu_item is not None and menu_item["out_of_stock"]:
                    print("เมนูนี้หมดแล้ว ไม่สามารถสั่งได้")
                elif menu_item is None:
                    print("ไม่พบเมนูนี้")
                else:
                    qty = rs.input_int("จำนวน: ", min_value=1)
                    rs.add_order_item(orders, table_id, menu_item, qty)
                    rs.save_orders(orders)
                    print("เพิ่มรายการสำเร็จ")
        elif choice == "2":
            table_id = rs.input_int("ใส่หมายเลขโต๊ะ: ")
            rs.show_table_order(orders, table_id)
            line_index = rs.input_int("ใส่หมายเลข # รายการที่จะแก้ไข: ", min_value=0)
            new_qty = rs.input_int("จำนวนใหม่ (ใส่ 0 เพื่อยกเลิกรายการ): ", min_value=0)
            if rs.update_order_qty(orders, table_id, line_index, new_qty):
                rs.save_orders(orders)
                print("อัปเดตรายการสำเร็จ")
            else:
                print("ไม่พบรายการนี้")
        elif choice == "3":
            table_id = rs.input_int("ใส่หมายเลขโต๊ะ: ")
            subtotal = rs.show_table_order(orders, table_id)
            print(f"ยอดรวมโต๊ะนี้: {subtotal:.2f} บาท")
        elif choice == "0":
            running = False
        else:
            print("กรุณาเลือกตัวเลขในเมนูเท่านั้น")


def kitchen_menu():
    """เมนูย่อย: หน้าจอครัว (return: None)"""
    orders = rs.load_orders()
    running = True
    while running:
        print("\n--- หน้าจอครัว (Kitchen Display) ---")
        rs.kitchen_display(orders)
        print("\n1. อัปเดตสถานะรายการอาหาร")
        print("0. กลับเมนูหลัก")
        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            table_id = rs.input_int("ใส่หมายเลขโต๊ะ: ")
            rs.show_table_order(orders, table_id)
            line_index = rs.input_int("ใส่หมายเลข # รายการ: ", min_value=0)
            print("สถานะ: 1) รอทำ  2) กำลังทำ  3) เสร็จแล้ว")
            status_choice = rs.input_int("เลือกสถานะ: ", min_value=1)
            if status_choice == 1:
                new_status = "รอทำ"
            elif status_choice == 2:
                new_status = "กำลังทำ"
            elif status_choice == 3:
                new_status = "เสร็จแล้ว"
            else:
                new_status = None

            if new_status is not None and rs.update_kitchen_status(orders, table_id, line_index, new_status):
                rs.save_orders(orders)
                print("อัปเดตสถานะสำเร็จ")
            else:
                print("ไม่สำเร็จ")
        elif choice == "0":
            running = False
        else:
            print("กรุณาเลือกตัวเลขในเมนูเท่านั้น")


def checkout_menu():
    """เมนูย่อย: เช็คบิล (return: None)"""
    tables = rs.load_tables()
    orders = rs.load_orders()
    sales = rs.load_sales()
    running = True
    while running:
        print("\n--- เช็คบิล ---")
        print("1. เช็คบิลโต๊ะ")
        print("0. กลับเมนูหลัก")
        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            table_id = rs.input_int("ใส่หมายเลขโต๊ะ: ")
            key = str(table_id)
            if key not in orders or len(orders[key]) == 0:
                print("โต๊ะนี้ยังไม่มีรายการอาหาร ไม่สามารถเช็คบิลได้")
            else:
                subtotal = rs.show_table_order(orders, table_id)
                discount = rs.input_float("ส่วนลด (%): ", min_value=0, max_value=100)
                tax = rs.input_float("ภาษี (%) [เช่น 7]: ", min_value=0, max_value=100)
                service = rs.input_float("ค่าบริการ (%) [เช่น 10]: ", min_value=0, max_value=100)

                bill = rs.calculate_bill(orders[key], discount, tax, service)
                rs.print_receipt(bill, table_id, orders[key])

                confirm = rs.input_yes_no("ยืนยันปิดบิลนี้หรือไม่?")
                if confirm and bill["total"] >= 0:
                    rs.record_sale(sales, table_id, orders[key], bill)
                    rs.save_sales(sales)
                    orders[key] = []
                    rs.save_orders(orders)
                    rs.change_table_status(tables, table_id, "ว่าง")
                    rs.save_tables(tables)
                    print("ปิดบิลสำเร็จ โต๊ะถูกเปลี่ยนเป็นสถานะว่างแล้ว")
                else:
                    print("ยกเลิกการปิดบิล")
        elif choice == "0":
            running = False
        else:
            print("กรุณาเลือกตัวเลขในเมนูเท่านั้น")


def report_menu():
    """เมนูย่อย: รายงานยอดขาย (return: None)"""
    sales = rs.load_sales()
    running = True
    while running:
        print("\n--- รายงานยอดขาย ---")
        print("1. รายงานยอดขายวันนี้")
        print("2. เมนูขายดี (ทุกวัน)")
        print("0. กลับเมนูหลัก")
        choice = input("เลือกเมนู: ").strip()

        if choice == "1":
            import datetime
            today = str(datetime.date.today())
            report = rs.daily_sales_report(sales, today)
            print(f"\nวันที่: {today}")
            print(f"จำนวนบิล: {report['total_bills']} บิล")
            print(f"ยอดขายรวม: {report['total_amount']:.2f} บาท")
        elif choice == "2":
            top_items = rs.best_selling_items(sales, target_date=None, top_n=5)
            if len(top_items) == 0:
                print("ยังไม่มีข้อมูลการขาย")
            else:
                print("\nอันดับเมนูขายดี:")
                rank = 1
                for name, qty in top_items:       # for loop วนแสดงผลลัพธ์
                    print(f"{rank}. {name}  ขายได้ {qty} รายการ")
                    rank += 1
        elif choice == "0":
            running = False
        else:
            print("กรุณาเลือกตัวเลขในเมนูเท่านั้น")


def main():
    """ฟังก์ชันหลักของโปรแกรม: แสดงเมนูหลักและควบคุมการทำงานทั้งหมด (return: None)"""
    print("=" * 40)
    print("  ระบบจัดการร้านอาหาร (Restaurant System)")
    print("=" * 40)

    running = True
    while running:
        print("\n===== เมนูหลัก =====")
        print("1. จัดการเมนูอาหาร")
        print("2. จัดการโต๊ะ")
        print("3. รับออเดอร์")
        print("4. หน้าจอครัว")
        print("5. เช็คบิล")
        print("6. รายงานยอดขาย")
        print("0. ออกจากโปรแกรม")

        try:
            choice = input("เลือกเมนู: ").strip()
        except Exception:
            choice = ""

        if choice == "1":
            menu_management_menu()
        elif choice == "2":
            table_management_menu()
        elif choice == "3":
            order_menu()
        elif choice == "4":
            kitchen_menu()
        elif choice == "5":
            checkout_menu()
        elif choice == "6":
            report_menu()
        elif choice == "0":
            running = False
            print("ขอบคุณที่ใช้บริการ โปรแกรมกำลังปิด...")
        else:
            print("กรุณาเลือกตัวเลขในเมนูเท่านั้น (0-6)")


if __name__ == "__main__":
    main()
