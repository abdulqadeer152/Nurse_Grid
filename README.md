🩺 NurseGridX – Nurse Shift Swapper App
A web application designed to help nurses manage their shifts and request swaps efficiently, while allowing hospital administrators to approve or reject those requests — all powered by Python OOP and Streamlit.

🚀 Features
👥 Role-Based Login: Nurses and Admins

🗓️ Shift View: Nurses can view their assigned shifts

🔁 Shift Swap Requests: Nurses can submit swap requests

✅ Admin Dashboard: Admins can approve or reject requests

💡 OOP-Based Architecture: Clean Python class structure

🔐 Simulated authentication (with session state)

📦 Ready for real-world database & payment integration

🏗️ Tech Stack
Frontend: Streamlit

Backend Logic: Python 3.x (OOP Principles)

Data Layer: In-memory lists (extendable to SQLite/PostgreSQL)

Authentication: Simulated via Streamlit session state

🧱 Folder Structure
bash
Copy
Edit
nursegridx/
│
├── app.py                   # Main application entry point
├── models/                  # OOP class definitions
│   ├── user.py
│   ├── shift.py
│   └── swap_request.py
├── services/
│   └── data_service.py      # (Future) persistent data service
└── assets/
    └── logo.png             # Logo or other branding assets
🔑 How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/nursegridx.git
cd nursegridx
Install dependencies:

bash
Copy
Edit
pip install streamlit
Run the app:

bash
Copy
Edit
streamlit run app.py
🧠 How It Works
🧑‍⚕️ For Nurses:
Login using your name and email

View upcoming shifts

Submit a shift swap request with a reason

👨‍💼 For Admins:
View pending swap requests

Approve or reject requests in one click

💼 Business Model Ideas
SaaS for hospitals with per-nurse/month pricing

Offer premium features: notifications, auto-scheduling, analytics

Integrate with payroll and HR software (future)

