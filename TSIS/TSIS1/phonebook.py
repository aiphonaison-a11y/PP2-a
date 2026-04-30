import json
from connect import get_connection


# ---------------- CREATE BASE DISPLAY ----------------
def fetch_all(order_by="name"):
    conn = get_connection()
    cur = conn.cursor()

    query = f"""
    SELECT c.id, c.name, c.email, c.birthday, g.name as group_name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY {order_by};
    """

    cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


# ---------------- FILTER BY GROUP ----------------
def filter_by_group():
    group = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s;
    """, (group,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# ---------------- EMAIL SEARCH ----------------
def search_email():
    keyword = input("Email keyword: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, email
        FROM contacts
        WHERE email ILIKE %s;
    """, ('%' + keyword + '%',))

    print(cur.fetchall())

    cur.close()
    conn.close()


# ---------------- PAGINATION ----------------
def paginate():
    limit = 3
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT name, email
            FROM contacts
            ORDER BY name
            LIMIT %s OFFSET %s;
        """, (limit, offset))

        rows = cur.fetchall()
        for r in rows:
            print(r)

        cur.close()
        conn.close()

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev" and offset > 0:
            offset -= limit
        else:
            break


# ---------------- EXPORT JSON ----------------
def export_json():
    data = fetch_all()

    result = []
    for c in data:
        result.append({
            "id": c[0],
            "name": c[1],
            "email": c[2],
            "birthday": str(c[3]),
            "group": c[4]
        })

    with open("contacts.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Exported to contacts.json")


# ---------------- IMPORT JSON ----------------
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for c in data:
        choice = input(f"{c['name']} exists? skip/overwrite: ")

        if choice == "skip":
            continue

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
            ON CONFLICT (name)
            DO UPDATE SET email = EXCLUDED.email;
        """, (c["name"], c["email"], c["birthday"]))

    conn.commit()
    cur.close()
    conn.close()


# ---------------- CALL PROCEDURES ----------------
def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
    conn.commit()

    cur.close()
    conn.close()


def move_group():
    name = input("Contact name: ")
    group = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s,%s)", (name, group))
    conn.commit()

    cur.close()
    conn.close()


def search_all():
    q = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# ---------------- MENU ----------------
def menu():
    while True:
        print("""
--- PHONEBOOK UPGRADED ---
1. Filter by group
2. Search email
3. Pagination
4. Export JSON
5. Import JSON
6. Add phone (procedure)
7. Move group (procedure)
8. Global search (SQL function)
9. Exit
        """)

        choice = input("Select: ")

        if choice == "1":
            filter_by_group()
        elif choice == "2":
            search_email()
        elif choice == "3":
            paginate()
        elif choice == "4":
            export_json()
        elif choice == "5":
            import_json()
        elif choice == "6":
            add_phone()
        elif choice == "7":
            move_group()
        elif choice == "8":
            search_all()
        elif choice == "9":
            break
        else:
            print("Invalid option. As usual.")


if __name__ == "__main__":
    menu()