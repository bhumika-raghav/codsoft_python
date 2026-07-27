"""
Task 5: Contact Book
A simple command-line contact management application.

Features:
- Add Contact
- View Contact List
- Search Contact (by name or phone number)
- Update Contact
- Delete Contact
"""

contacts = []


def add_contact():
    print("\n--- Add New Contact ---")
    name = input("Name: ").strip()
    phone = input("Phone number: ").strip()
    email = input("Email: ").strip()
    address = input("Address: ").strip()

    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }
    contacts.append(contact)
    print(f"Contact '{name}' added successfully!\n")


def view_contacts():
    print("\n--- Contact List ---")
    if not contacts:
        print("No contacts saved yet.\n")
        return

    for i, c in enumerate(contacts, start=1):
        print(f"{i}. {c['name']} - {c['phone']}")
    print()


def find_matches(query):
    query = query.lower().strip()
    return [c for c in contacts if query in c["name"].lower() or query in c["phone"]]


def search_contact():
    print("\n--- Search Contact ---")
    if not contacts:
        print("No contacts saved yet.\n")
        return

    query = input("Enter name or phone number to search: ")
    matches = find_matches(query)

    if not matches:
        print("No matching contacts found.\n")
        return

    print(f"Found {len(matches)} match(es):")
    for i, c in enumerate(matches, start=1):
        print(f"{i}. Name: {c['name']}")
        print(f"   Phone: {c['phone']}")
        print(f"   Email: {c['email']}")
        print(f"   Address: {c['address']}")
    print()


def update_contact():
    print("\n--- Update Contact ---")
    if not contacts:
        print("No contacts saved yet.\n")
        return

    query = input("Enter name or phone number of the contact to update: ")
    matches = find_matches(query)

    if not matches:
        print("No matching contacts found.\n")
        return

    contact = matches[0]
    if len(matches) > 1:
        print("Multiple matches found, updating the first one:")
    print(f"Updating: {contact['name']} - {contact['phone']}")

    print("Leave a field blank to keep its current value.")
    new_name = input(f"Name [{contact['name']}]: ").strip()
    new_phone = input(f"Phone [{contact['phone']}]: ").strip()
    new_email = input(f"Email [{contact['email']}]: ").strip()
    new_address = input(f"Address [{contact['address']}]: ").strip()

    if new_name:
        contact["name"] = new_name
    if new_phone:
        contact["phone"] = new_phone
    if new_email:
        contact["email"] = new_email
    if new_address:
        contact["address"] = new_address

    print("Contact updated successfully!\n")


def delete_contact():
    print("\n--- Delete Contact ---")
    if not contacts:
        print("No contacts saved yet.\n")
        return

    query = input("Enter name or phone number of the contact to delete: ")
    matches = find_matches(query)

    if not matches:
        print("No matching contacts found.\n")
        return

    contact = matches[0]
    confirm = input(f"Delete '{contact['name']}' - {contact['phone']}? (y/n): ").strip().lower()
    if confirm == "y":
        contacts.remove(contact)
        print("Contact deleted successfully!\n")
    else:
        print("Deletion cancelled.\n")


def show_menu():
    print("=" * 30)
    print("        CONTACT BOOK")
    print("=" * 30)
    print("1. Add Contact")
    print("2. View Contact List")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.\n")


if __name__ == "__main__":
    main()