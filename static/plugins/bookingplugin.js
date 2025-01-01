class AppointmentBooking {
    constructor(apiBaseUrl) {
        this.apiBaseUrl = apiBaseUrl;
    }

    handleError(error) {
        console.error(error);
        alert(`Error: ${error.message || error}`);
    }

    async getAvailableSlots(date) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/slots?date=${date}`);
            if (!response.ok) {
                throw new Error(`Error fetching slots: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            this.handleError(error);
            return [];
        }
    }

    async getAppointments() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/appointments`);
            if (!response.ok) {
                throw new Error(`Error fetching appointments: ${response.statusText}`);
            }
            return await response.json(); 
        } catch (error) {
            this.handleError(error);
            return [];
        }
    }

    async bookAppointment(data) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/book`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || "Unknown error occurred");
            }

            const result = await response.json();
            alert(result.success || "Appointment booked successfully!");

            // After successful booking, fetch the updated appointments
            const appointments = await this.getAppointments();
            this.updateAppointmentsList(appointments);

            return result;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    async render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with id "${containerId}" not found.`);
            return;
        }

        container.innerHTML = `
            <div class="appointment-booking-form">
                <form id="appointmentForm">
                    <label for="name">Name:</label>
                    <input type="text" id="name" required>

                    <label for="phonenumber">Phone Number:</label>
                    <input type="text" id="phonenumber" required>

                    <label for="date">Date:</label>
                    <input type="date" id="date" required>

                    <label for="timeslot">Timeslot:</label>
                    <select id="timeslot" required>
                        <option value="">Select a timeslot</option>
                    </select>

                    <button type="submit">Book Appointment</button>
                </form>

                <button id="toggleAppointmentsBtn">Show Existing Appointments</button>

                <div id="appointmentsContainer" style="display: none;">
                    <h3>Existing Appointments</h3>
                    <ul id="appointmentsList"></ul>
                </div>
            </div>
        `;

        const toggleAppointmentsBtn = container.querySelector("#toggleAppointmentsBtn");
        const appointmentsContainer = container.querySelector("#appointmentsContainer");
        const appointmentsList = container.querySelector("#appointmentsList");

        toggleAppointmentsBtn.addEventListener("click", async () => {
            if (appointmentsContainer.style.display === "none") {
                appointmentsContainer.style.display = "block";
                toggleAppointmentsBtn.textContent = "Hide Existing Appointments";

                const appointments = await this.getAppointments();
                this.displayAppointments(appointments, appointmentsList);
            } else {
                appointmentsContainer.style.display = "none";
                toggleAppointmentsBtn.textContent = "Show Existing Appointments";
            }
        });

        const dateInput = container.querySelector("#date");
        const timeslotDropdown = container.querySelector("#timeslot");

        dateInput.addEventListener("change", async () => {
            const selectedDate = dateInput.value;
            timeslotDropdown.innerHTML = `<option value="">Select a timeslot</option>`;

            if (selectedDate) {
                try {
                    const slots = await this.getAvailableSlots(selectedDate);

                    if (slots.length === 0) {
                        const option = document.createElement("option");
                        option.value = "";
                        option.textContent = "No available slots";
                        timeslotDropdown.appendChild(option);
                        return;
                    }

                    slots.forEach((slot) => {
                        const option = document.createElement("option");
                        option.value = slot;
                        option.textContent = slot;
                        timeslotDropdown.appendChild(option);
                    });
                } catch (error) {
                    this.handleError(error);
                }
            }
        });

        const form = container.querySelector("#appointmentForm");
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const name = document.querySelector("#name").value;
            const phonenumber = document.querySelector("#phonenumber").value;
            const date = document.querySelector("#date").value;
            const timeslot = document.querySelector("#timeslot").value;


            if (!name || !phonenumber || !date || !timeslot) {
                alert("Please fill in all fields.");
                return;
            }

            const data = { name, phonenumber, date, timeslot };

            try {
                await this.bookAppointment(data);


                const appointments = await this.getAppointments();
                this.updateAppointmentsList(appointments);
            } catch (error) {
                this.handleError(error);
            }
        });
    }

    displayAppointments(appointments, appointmentsList) {
        appointments.forEach((appointment) => {
            if (appointment && appointment.name) {
                this.addAppointmentToList(appointment, appointmentsList);
            }
        });
    }

    updateAppointmentsList(appointments) {
        const appointmentsList = document.querySelector("#appointmentsList");
        appointmentsList.innerHTML = '';  

        this.displayAppointments(appointments, appointmentsList);
    }

    addAppointmentToList(appointment, appointmentsList) {
        if (!appointment || !appointment.name || !appointment.date || !appointment.timeslot) {
            console.error("Invalid appointment data", appointment);
            return;
        }

        const listItem = document.createElement("li");
        listItem.textContent = `${appointment.name} - ${appointment.date} at ${appointment.timeslot}`;
        appointmentsList.appendChild(listItem);
    }
}
