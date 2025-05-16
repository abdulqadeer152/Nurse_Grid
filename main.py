import streamlit as st
from datetime import datetime, timedelta
import json

# ------------------ OOP Classes ------------------
class User:
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role
        self.is_pro = False  # Track if user has pro subscription

class Nurse(User):
    def __init__(self, name, email):
        super().__init__(name, email, role="nurse")
        self.swap_history = []

class Admin(User):
    def __init__(self, name, email):
        super().__init__(name, email, role="admin")

class Shift:
    def __init__(self, shift_id, nurse_name, date, time):
        self.shift_id = shift_id
        self.nurse_name = nurse_name
        self.date = date
        self.time = time

class SwapRequest:
    def __init__(self, request_id, shift_id, requester, reason):
        self.request_id = request_id
        self.shift_id = shift_id
        self.requester = requester
        self.reason = reason
        self.status = "Pending"
        self.created_at = datetime.now()

# ------------------ Dummy Data ------------------
dummy_shifts = [
    Shift(1, "John Doe", "2024-03-20", "Morning (6AM-2PM)"),
    Shift(2, "John Doe", "2024-03-22", "Night (10PM-6AM)"),
    Shift(3, "Jane Smith", "2024-03-20", "Evening (2PM-10PM)"),
    Shift(4, "Jane Smith", "2024-03-21", "Morning (6AM-2PM)")
]

# ------------------ Helper Functions ------------------
def save_data():
    """Save session state data to a JSON file"""
    data = {
        'swap_requests': [
            {
                'request_id': req.request_id,
                'shift_id': req.shift_id,
                'requester': req.requester,
                'reason': req.reason,
                'status': req.status,
                'created_at': req.created_at.isoformat()
            }
            for req in st.session_state.swap_requests
        ]
    }
    with open('data.json', 'w') as f:
        json.dump(data, f)

def load_data():
    """Load data from JSON file"""
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            st.session_state.swap_requests = [
                SwapRequest(
                    req['request_id'],
                    req['shift_id'],
                    req['requester'],
                    req['reason']
                )
                for req in data.get('swap_requests', [])
            ]
    except FileNotFoundError:
        st.session_state.swap_requests = []

# ------------------ Login Simulation ------------------
def login():
    st.sidebar.title("Login NursegridX")
    st.sidebar.image("https://via.placeholder.com/150x50?text=NurseGridX", width=150)
    
    username = st.sidebar.text_input("Name")
    email = st.sidebar.text_input("Email")
    role = st.sidebar.selectbox("Role", ["nurse", "admin"])

    if st.sidebar.button("Login"):
        if not username or not email:
            st.sidebar.error("Please fill in all fields")
            return
            
        if role == "nurse":
            st.session_state.user = Nurse(username, email)
        else:
            st.session_state.user = Admin(username, email)
        st.session_state.logged_in = True
        st.rerun()

# ------------------ Nurse Dashboard ------------------
def nurse_dashboard(user):
    st.title(f"Welcome Nurse {user.name}")
    
    # Subscription Status
    if user.is_pro:
        st.success("✨ You are on the Pro Hospital Plan")
    else:
        st.warning("Upgrade to Pro Hospital Plan for unlimited swaps!")
        if st.button("Upgrade Now"):
            user.is_pro = True
            st.success("Upgraded to Pro Plan!")
            st.rerun()

    # Current Shifts Section
    st.subheader("📅 Current Shifts")
    today = datetime.now().date()
    current_shifts = [s for s in dummy_shifts if s.nurse_name == user.name and datetime.strptime(s.date, "%Y-%m-%d").date() >= today]
    
    if not current_shifts:
        st.info("No upcoming shifts scheduled")
    else:
        # Sort shifts by date
        current_shifts.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d"))
        
        # Display shifts in a more organized way
        for shift in current_shifts:
            shift_date = datetime.strptime(shift.date, "%Y-%m-%d").date()
            days_until = (shift_date - today).days
            
            # Create a container for each shift
            with st.container():
                col1, col2, col3 = st.columns([2,2,1])
                with col1:
                    st.markdown(f"**Date:** {shift.date}")
                with col2:
                    st.markdown(f"**Time:** {shift.time}")
                with col3:
                    if days_until == 0:
                        st.markdown("🔄 **Today**")
                    elif days_until == 1:
                        st.markdown("📅 **Tomorrow**")
                    else:
                        st.markdown(f"📅 **In {days_until} days**")
                st.markdown("---")

    # Past Shifts Section
    st.subheader("📚 Past Shifts")
    past_shifts = [s for s in dummy_shifts if s.nurse_name == user.name and datetime.strptime(s.date, "%Y-%m-%d").date() < today]
    
    if not past_shifts:
        st.info("No past shifts")
    else:
        # Sort shifts by date (most recent first)
        past_shifts.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d"), reverse=True)
        
        for shift in past_shifts:
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Date:** {shift.date}")
                with col2:
                    st.markdown(f"**Time:** {shift.time}")
                st.markdown("---")

    # Request Swap Section
    st.subheader("🔄 Request a Shift Swap")
    if current_shifts:
        shift_options = {f"{s.date} - {s.time}": s.shift_id for s in current_shifts}
        selected_shift = st.selectbox("Select Shift to Swap", options=list(shift_options.keys()))
        shift_id = shift_options[selected_shift]
        reason = st.text_area("Reason for Swap")
        
        if st.button("Request Swap"):
            if not reason:
                st.error("Please provide a reason for the swap")
            else:
                swap = SwapRequest(len(st.session_state.swap_requests)+1, shift_id, user.name, reason)
                st.session_state.swap_requests.append(swap)
                save_data()
                st.success("Swap request submitted!")
    else:
        st.info("No shifts available for swapping")

    # View Pending Requests
    st.subheader("⏳ Pending Swap Requests")
    pending_requests = [req for req in st.session_state.swap_requests 
                       if req.status == "Pending" and req.requester != user.name]
    
    if not pending_requests:
        st.info("No pending swap requests")
    else:
        for req in pending_requests:
            with st.container():
                st.markdown(f"**Request #{req.request_id}** from {req.requester}")
                st.markdown(f"**Reason:** {req.reason}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Accept #{req.request_id}"):
                        req.status = "Accepted"
                        save_data()
                        st.success("Request accepted!")
                        st.rerun()
                with col2:
                    if st.button(f"Decline #{req.request_id}"):
                        req.status = "Declined"
                        save_data()
                        st.warning("Request declined")
                        st.rerun()
                st.markdown("---")

# ------------------ Admin Dashboard ------------------
def admin_dashboard(user):
    st.title(f"Welcome Admin {user.name}")
    
    # Analytics
    total_requests = len(st.session_state.swap_requests)
    pending_requests = len([r for r in st.session_state.swap_requests if r.status == "Pending"])
    st.metric("Total Swap Requests", total_requests)
    st.metric("Pending Requests", pending_requests)

    # Manage Swap Requests
    st.subheader("Manage Swap Requests")
    for req in st.session_state.swap_requests:
        if req.status == "Pending":
            st.markdown(f"🔁 Request #{req.request_id} from {req.requester}")
            st.markdown(f"📝 Reason: {req.reason}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Approve #{req.request_id}"):
                    req.status = "Approved"
                    save_data()
                    st.success(f"Approved request #{req.request_id}")
                    st.rerun()
            with col2:
                if st.button(f"Reject #{req.request_id}"):
                    req.status = "Rejected"
                    save_data()
                    st.warning(f"Rejected request #{req.request_id}")
                    st.rerun()

    # Manual Shift Assignment
    st.subheader("Manual Shift Assignment")
    nurse_name = st.text_input("Nurse Name")
    shift_date = st.date_input("Shift Date")
    shift_time = st.selectbox("Shift Time", ["Morning (6AM-2PM)", "Evening (2PM-10PM)", "Night (10PM-6AM)"])
    
    if st.button("Assign Shift"):
        new_shift = Shift(len(dummy_shifts)+1, nurse_name, str(shift_date), shift_time)
        dummy_shifts.append(new_shift)
        st.success(f"Assigned {shift_time} shift on {shift_date} to {nurse_name}")

# ------------------ Main App ------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    try:
        load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.session_state.swap_requests = []

if not st.session_state.logged_in:
    login()
else:
    try:
        user = st.session_state.user
        if user.role == "nurse":
            nurse_dashboard(user)
        else:
            admin_dashboard(user)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.logged_in = False
        st.rerun()

        
