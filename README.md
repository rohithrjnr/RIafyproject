# Appointment Booking System

A simple web-based **Appointment Booking System** developed using **Flask** (Python) for the backend and **HTML, CSS, JavaScript** for the frontend. This system allows users to book appointments by selecting a time slot, viewing available slots, and prevents double-booking.

## Features

### 1. Appointment Slots
- Available time slots are in 30-minute intervals between **10:00 AM** and **5:00 PM**.
- **1:00 PM to 2:00 PM** is a break time and will not be available for booking.

### 2. Booking Functionality
- Users can book an appointment by providing:
  - **Name**
  - **Phone Number**
  - **Date**
  - **Selected Time Slot**
- Prevents double-booking of the same slot.

### 3. Slot Availability
- Users can view available slots for a specific date.

### 4. Reusable Frontend Plugin
- A **frontend UI** that can be embedded into any website via a `<script>` tag for users to book and view available slots.

---

## Installation

Follow the steps below to get the project up and running.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/appointment-booking-system.git
cd appointment-booking-system


pip install -r requirements.txt

python app.py


