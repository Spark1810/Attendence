
import sqlite3
import streamlit as st
import qrcode
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import os

def create_attendance_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, date TEXT);")
    conn.commit()
    conn.close()

def generate_qr_code(student_name):
    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,  # QR code version
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the QR code
        border=4  # Border size
    )
    
    # Add data (student name) to the QR code
    qr.add_data(student_name)
    qr.make(fit=True)

    # Create the "qrcodes" directory if it doesn't exist
    os.makedirs("qrcodes", exist_ok=True)

    # Create an image from the QR code
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image
    qr_img.save(f"qrcodes/{student_name}.png")
    st.write("Qr Generated")


def scan_qr_code():
    cap = cv2.VideoCapture(0)  # Use the default camera (change the parameter to use a different camera)

    while True:
        _, frame = cap.read()
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            st.write(f"Scanned: {data}")
            mark_attendance(data)

        cv2.imshow("Barcode Scanner", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

def mark_attendance(student_name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (name, date) VALUES (?, ?);", (student_name, datetime.now()))
    conn.commit()
    conn.close()
def display_attendance_records():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance;")
    records = cursor.fetchall()
    conn.close()

    for record in records:
        st.write(f"ID: {record[0]}, Name: {record[1]}, Date: {record[2]}")


if __name__ == "__main__":
    create_attendance_db()

    st.write("1. Generate QR Codes ")
    st.write("2. Scan QR Codes and Mark Attendance")
    st.write("3. Display Attendance Records")
    st.write("4. Quit ")
    choice = st.text_input("Select an option: ")
    if choice == '1':
        student_name = st.text_input("Enter student's name: ")
        generate_qr_code(student_name)
    elif choice == '2':
        scan_qr_code()
    elif choice == '3':
        display_attendance_records()
    
    else:
        st.warning("Enter Your Choice")

# Get user rating
rating = st.slider("Rate this app (1-10)", 1, 10, 5)
st.write(f"Your rating: {rating}")
st.success("Thanks For Using Our App...")
