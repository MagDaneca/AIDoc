import PyPDF2
import re
import streamlit as st


def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        text += page.extract_text()
    return text

def hide_streamlit_style():
    return """
        <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        </style>
        """

def init_session_state():
    if 'Glucose' not in st.session_state:
        st.session_state.Glucose = None
    if 'BloodPressure' not in st.session_state:
        st.session_state.BloodPressure = None
    if 'Insulin' not in st.session_state:
        st.session_state.Insulin = None

def check_parameters_filled(age, sex, height, kilo):
    if age is None or sex is None or height is None or kilo is None or age == 0 or height == 0 or kilo == 0:
        return False  
    return True  

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def init_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = True

custom_css = """
    <style>
    .card {
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
    }
    .card-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-content {
        font-size: 16px;
        color: black;
    }
    </style>
    """ 


def create_custom_markdown_card(text, image_url=None):
    # Apply custom CSS styles to the card
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Create the card
    st.markdown(
        """
        <div class="card" style="display: flex; align-items: center;">
            <div style="flex: 1;">
                <div class="card-title">Информация</div>
                <div class="card-content">
                """
        + text
        + """
                </div>
            </div>
            """
        # Add the image if URL is provided
        + (f'<img src="{image_url}" style="max-width:100%; border-radius: 5px; flex-shrink: 0; margin-left: 20px;">' if image_url else '')
        + """
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.write("")
    st.write("")

def apply_white_theme():
    # Custom CSS to force a white theme regardless of system theme
    custom_css = """
        <style>
            /* Set background color of the entire app to white */
            body {
                background-color: white !important;
                color: black !important;  /* Make text black for readability */
            }
         </style>
    """
    # Apply the custom CSS to the app
    st.markdown(custom_css, unsafe_allow_html=True)

def create_basic_custom_markdown_card(text, image_url=None):
    # Define custom CSS for styling
    custom_css = """
        <style>
            .card {
                display: flex;
                align-items: center;
                background-color: transparent; /* Dark background for contrast */
                padding: 15px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
                margin-bottom: 10px;
            }
            .card-content {
                color: white;  /* Make text white */
                font-size: 16px;
            }
        </style>
    """
    
    # Apply custom CSS styles to the card
    st.markdown(custom_css, unsafe_allow_html=True)
    
    text_lines = text.split('\n')
    formatted_text = '<br>'.join(text_lines)
    
    # Create the card
    st.markdown(
        f"""
        <div class="card">
            <div style="flex: 1;">
                <div class="card-content">
                    {formatted_text}
                </div>
            </div>
            """
        # Add the image if URL is provided
        + (f'<img src="{image_url}" style="max-width:100%; border-radius: 5px; flex-shrink: 0; margin-left: 20px;">' if image_url else '')
        + """
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.write("")
    st.write("")

def init_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = True

def check_valid_name_bulgarian(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid Bulgarian name while creating the account.
    """
    name_regex_bulgarian = r'^[А-Яа-я]+$'

    if re.search(name_regex_bulgarian, name_sign_up):
        return True
    return False

def check_valid_username(username: str) -> bool:
    """
    Checks if the user entered a valid username while creating the account.
    """
    regex = re.compile(r'^[A-Za-z0-9_.-]+$')

    if re.fullmatch(regex, username):
        return True
    return False

def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False

def check_valid_phone_number(phone_number: str) -> bool:
    """
    Checks if the provided string is a valid phone number with exactly 10 digits.
    """
    phone_regex = r'^[0-9]{10}$'

    if re.search(phone_regex, phone_number):
        return True
    return False

def check_strong_password(password: str) -> bool:
    """
    Checks if the provided string is a strong password.
    """
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_=+{}\[\]:;<>,.?\\/]).{6,}$'

    if re.search(password_regex, password):
        return True
    return False
