import streamlit as st
from auth import signup_user, login_user
import requests
import time

# --- Page Config ---
st.set_page_config(page_title="Loan Prediction App", page_icon="💰", layout="wide")

# --- Session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- Top Section: Logo + Theme Toggle + Logout ---
top_col1, top_col2, top_col3 = st.columns([1, 2, 1])

# with top_col1:
#     st.image("https://cdn-icons-png.flaticon.com/512/727/727606.png", width=60)

with top_col2:
    st.markdown("<h2 style='text-align: center;'>Loan Prediction App</h2>", unsafe_allow_html=True)

with top_col3:
    # dark_toggle = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
    # st.session_state.dark_mode = dark_toggle
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.success("You have been logged out.")

# --- Navbar ---
nav_options = ["🏠 Home", "✍️ Signup", "🔑 Login", "ℹ️ About", "📊 Predict Loan"]
nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
with nav_col2:
    nav = st.radio("Navigation", nav_options, horizontal=True, label_visibility="collapsed")

# --- HOME PAGE ---
if nav == "🏠 Home":
    st.title("🏠 Welcome to Loan Status Predictor")
    st.subheader("Predict your loan approval status using our AI-powered system.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**How It Works**")
        st.markdown("1. Create an account\n2. Fill in your details\n3. Get instant prediction")
    with col2:
        st.info("**Features**")
        st.markdown("- Fast predictions\n- Secure data handling\n- User-friendly interface")
    with col3:
        st.info("**Requirements**")
        st.markdown("- Income details\n- Loan amount\n- Credit history")

    if st.session_state.logged_in:
        st.success("✅ You're logged in! Go to 'Prediction' to check your eligibility.")
    else:
        st.warning("🔒 Please login or signup to use the prediction feature.")

# --- SIGNUP PAGE ---
elif nav == "✍️ Signup":
    st.title("✍️ Create an Account")
    with st.form("signup_form"):
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        new_pass_confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            if new_pass != new_pass_confirm:
                st.error("Passwords do not match!")
            elif len(new_pass) < 6:
                st.error("Password must be at least 6 characters")
            elif signup_user(new_user, new_pass):
                st.success("🎉 Account created successfully! You can now login.")
                time.sleep(2)
                st.experimental_rerun()
            else:
                st.error("Username already exists. Try logging in instead.")

# --- LOGIN PAGE ---
elif nav == "🔑 Login":
    st.title("🔑 Login to Your Account")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back {username}!")
                time.sleep(1)
                # st.experimental_rerun()
            else:
                st.error("Invalid username or password")

# --- ABOUT PAGE ---
elif nav == "ℹ️ About":
    st.title("ℹ️ About This App")
    st.markdown("""
        This AI-powered app helps banks and customers quickly determine the likelihood of loan approval.
        It uses historical financial data and machine learning to provide reliable predictions.
    """)

# --- PREDICTION PAGE ---
elif nav == "📊 Predict Loan":
    if not st.session_state.logged_in:
        st.warning("🔒 Please login to access the prediction feature.")
    else:
        st.title("📊 Loan Status Prediction")
        st.markdown(f"Welcome, **{st.session_state.username}**! Fill in your details below.")
        with st.form("loan_form"):
            col1, col2 = st.columns(2)
            with col1:
                Gender = st.radio("Gender", ["Male", "Female"])
                Married = st.radio("Married", ["No", "Yes"])
                Dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
                Education = st.radio("Education", ["Graduate", "Not Graduate"])
                Self_Employed = st.radio("Self Employed", ["No", "Yes"])
            with col2:
                ApplicantIncome = st.number_input("Applicant Income", min_value=0.0)
                CoapplicantIncome = st.number_input("Coapplicant Income", min_value=0.0)
                LoanAmount = st.number_input("Loan Amount", min_value=0.0)
                Loan_Amount_Term = st.slider("Loan Term (months)", 12, 360, 120)
                Credit_History = st.radio("Credit History", ["No", "Yes"])
                Property_Area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

            # submitted = st.form_submit_button("🔮 Get Prediction")
            # if submitted:
            #     with st.spinner("Analyzing your application..."):
            #         data = {
            #             "Gender": 1.0 if Gender == "Male" else 0.0,
            #             "Married": 1.0 if Married == "Yes" else 0.0,
            #             "Dependents": float(Dependents.replace("+", "")),
            #             "Education": 0.0 if Education == "Graduate" else 1.0,
            #             "Self_Employed": 1.0 if Self_Employed == "Yes" else 0.0,
            #             "ApplicantIncome": ApplicantIncome,
            #             "CoapplicantIncome": CoapplicantIncome,
            #             "LoanAmount": LoanAmount,
            #             "Loan_Amount_Term": float(Loan_Amount_Term),
            #             "Credit_History": 1.0 if Credit_History == "Yes" else 0.0,
            #             "Property_Area": {"Urban": 2.0, "Semiurban": 1.0, "Rural": 0.0}[Property_Area]
            #         }
            #         try:
            #             res = requests.post("http://127.0.0.1:8000/predict", json=data)
            #             if res.status_code == 200:
            #                 result = res.json()
            #                 if result['Loan Status'] == "Approved":
            #                     st.balloons()
            #                     st.success("🎉 Congratulations! Your loan is approved!")
            #                 else:
            #                     st.warning(" Loan not approved. Try adjusting inputs.")
            #                 with st.expander("Details"):
            #                     st.json(data)
            #                     st.write("Prediction result:", result)
            #             else:
            #                 st.error(f"Server error: {res.status_code}")
            #         except Exception as e:
            #             st.error(f"Prediction failed: {e}")
           
            submitted = st.form_submit_button("🔮 Get Prediction")
if submitted:
    if ApplicantIncome <= 100 or CoapplicantIncome <= 50:
        st.error("❗ Applicant and Coapplicant income must each be greater than 100 to proceed.")
    else:
        with st.spinner("Analyzing your application..."):
            data = {
                "Gender": 1.0 if Gender == "Male" else 0.0,
                "Married": 1.0 if Married == "Yes" else 0.0,
                "Dependents": float(Dependents.replace("+", "")),
                "Education": 0.0 if Education == "Graduate" else 1.0,
                "Self_Employed": 1.0 if Self_Employed == "Yes" else 0.0,
                "ApplicantIncome": ApplicantIncome,
                "CoapplicantIncome": CoapplicantIncome,
                "LoanAmount": LoanAmount,
                "Loan_Amount_Term": float(Loan_Amount_Term),
                "Credit_History": 1.0 if Credit_History == "Yes" else 0.0,
                "Property_Area": {"Urban": 2.0, "Semiurban": 1.0, "Rural": 0.0}[Property_Area]
            }
            try:
                res = requests.post("http://127.0.0.1:8000/predict", json=data)
                if res.status_code == 200:
                    result = res.json()
                    if result['Loan Status'] == "Approved":
                        st.success("🎉 Congratulations! Your loan is approved!")
                    else:
                        st.warning(" Loan not approved. Try adjusting inputs.")
                    with st.expander("Details"):
                        st.json(data)
                        st.write("Prediction result:", result)
                else:
                    st.error(f"Server error: {res.status_code}")
            except Exception as e:
                st.error(f"Prediction failed: {e}")


# --- Footer ---
st.markdown("""
    <hr style="margin-top: 50px;">
    <div style='text-align: center; color: gray; font-size: 14px;'>
        &copy; 2025 Loan Predictor App | Built with using Streamlit
    </div>
""", unsafe_allow_html=True)
