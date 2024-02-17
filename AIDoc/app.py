import pickle
from utils.database import *
from utils.different import *
from utils.doc import *
from utils.user import *
from utils.encdata import *
from utils.pharmacy import *
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_login import __login__
from streamlit_login.utils import register_new_usr
import re
from io import BytesIO
from streamlit_calendar1 import calendar
from datetime import timedelta, datetime
from datetime import *
import folium
from streamlit_folium import folium_static


def get_working_hours(username,day):
    conn = create_connection()
    cursor = conn.cursor()
    doc_id = get_user_id_by_username(conn,username)
    st.write(f"**Работно време за {day}:**")
    col1, col2 = st.columns([1, 1])
    not_working = st.checkbox(f"Неработен ден", key=f"not_working_{day}")

    start_time, end_time = None, None

    if not not_working:
        with col1:
            start_time = st.time_input(f"Начало на работния ден ", key=f"start_time_{day}")
        with col2:
            end_time = st.time_input(f"Край на работния ден ", key=f"end_time_{day}")
    else:
        start_time = None
        end_time = None
        

    return start_time, end_time


def init_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = True
    if 'selected_hour' not in st.session_state:
        st.session_state.selected_hour = None

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

conn = create_connection()
cursor = conn.cursor()
init_session_state()

diabetes_model = pickle.load(open(rb'AIDoc/Trained models/diabetes_model_medassist.sav', 'rb'))

__login__obj = __login__(auth_token = "dk_test_7KR409DTD7M8R6N7R803TVBDK9V7", 
                         
                    company_name = "AIDoc",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')


LOGGED_IN = __login__obj.build_login_ui()

extracted_text = ""
if 'Glucose' not in st.session_state:
    st.session_state.Glucose = None
if 'BloodPressure' not in st.session_state:
    st.session_state.BloodPressure = None
if 'Insulin' not in st.session_state:
    st.session_state.Insulin = None
if LOGGED_IN == True:
    username = __login__obj.cookies['__streamlit_login_signup_ui_username__']
    role_user = get_user_role(conn,username)
    if role_user is None:
        if username == "admin":
            role_user = 2
        elif role_user == 3:
            role_user = 3
        else:
            role_user = 1
        
    save_user_role(conn,username,role_user)
    if role_user == 1:
        option1 = 'Профил'
        option2 = "Вашите часове"
        option3 = 'Тествай се'
        option4 = 'Намери лекарство'
        with st.sidebar:
            container = st.container (border=True)
            with container:
                selected = option_menu('AIDoc',
                                
                                [
                                    option1,
                                    option2,
                                    option3,
                                    option4
                                ],
                                icons=['person','activity','bandaid','heart','bandaid'],
                                default_index=0)
            
            if selected == 'Вашите часове':
                        with container:
                            with st.expander("",expanded=True):
                                selected = option_menu( '',
                                                        [   
                                                            'Запиши си час онлайн',
                                                            'Вашите записани часове'
                                                        ],
                                                        icons=['calendar2-plus-fill','calendar2-check-fill'],
                                                        default_index=0)
            if selected == 'Тествай се':
                        with container:
                            with st.expander("",expanded=True):
                                selected = option_menu( '',
                                                        [   
                                                            'Диабет',
                                                        ],
                                                        icons=['capsule-pill'],
                                                        default_index=0)
        if(selected == 'Профил'):
            col6,col7,col8 = st.columns([0.5,1,0.5])
            with col7:
                st.title("Вашият Профил")
            output = '1'
            first_name = get_first_name(conn,username)
            second_name = get_last_name(conn,username)
            tel_num = get_tel_num(conn, username)
            age = get_age_of_user(conn, username)
            height = get_height_of_user(conn, username)
            sex = get_sex_of_user(conn, username)
            kilo = get_kilo_of_user(conn, username)
            pregnancies = get_pregnancies_of_user(conn, username)
            if height != None:
                bmi = kilo/(height*height)
            if age:
                col1,col2 = st.columns([1,1])
                col3,col4,col5 = st.columns([1,1,1])
                with col1:
                    create_basic_custom_markdown_card(
                        f"Име: {first_name}\n" 
                        f"Фамилия: {second_name}\n"
                        f"Телефонен номер: {tel_num}\n"
                        f"\n"
                    )
                with col2:
                    if sex == "жена":
                        create_basic_custom_markdown_card(
                        f"Възраст: {age} г.\n"
                        f"Височина: {height} м.\n"
                        f"Пол: {sex}\n"
                        f"Бременности: {pregnancies}\n"
                        f"Тегло: {kilo} кг.\n"
                    )
                    else:
                        create_basic_custom_markdown_card(
                        f"Възраст: {age} г.\n"
                        f"Височина: {height} м.\n"
                        f"Пол: {sex}\n"
                        f"Тегло: {kilo} кг.\n"
                        )
                    BMI = height/(kilo*kilo)
                with col4:
                    if st.button("Променете вашите данни"):
                        age = None
                        result = None
                        save_user_profile(conn,username, age, sex, pregnancies, height, kilo)
                        st.rerun()
            else:
                col1, col2 = st.columns([1.5,2])
                with col1:
                    first_name = st.text_input("Първо име",placeholder="Иван")
                    second_name = st.text_input("Фамилия",placeholder="Иванов")
                    tel_number = st.text_input("Телефонен номер",placeholder="+359888888888")
                with col2:
                    result = None
                    Age = st.number_input("Възраст",1,100,None,1)
                    Sex = st.radio("Пол",["мъж","жена"])
                    if Sex=="мъж":
                        Pregnancies = 0
                    else:
                        Pregnancies = st.text_input("Бременности" , placeholder = 'Брой бременности')
                    Height = st.number_input("Височина",0.01,300.00,None,0.01, placeholder="Височината ви в метри(Пример 181см->1.81)")
                    Kilo = st.number_input("Тегло", 0.01, 300.00,None, 0.01 , placeholder="Теглото ви в килограми")
                    if height != None:
                        BMI = kilo/(height*height)
                    if st.button("Запази") == True:
                        auth_par_check = check_parameters_filled(Age,Sex,Height,Kilo)
                        info_filled = bool(first_name.strip()) and bool(second_name.strip()) and bool(tel_number.strip())  # Check if text inputs are filled
                        if auth_par_check == False or not info_filled:
                            st.error("Въведете вашите данни във всички полета!")
                        else:
                            save_user_info(conn,first_name,second_name,None,tel_number,username,role_user,1)
                            save_user_profile(conn,username,Age,Sex,Pregnancies,Height,Kilo)
                            conn.commit()
                            user_profile = get_user_profile(conn, username)
                            data_created = True
                            if data_created:
                                st.rerun()
            medical_tests = st.file_uploader("Качете вашите изследвания в PDF формат тук:", type=['pdf'])
            if medical_tests is not None:
                extracted_text = extract_text_from_pdf(BytesIO(medical_tests.read()))
            if findWholeWord('Глюкоза')(extracted_text) is not None:
                glucose_match = re.search(r'Глюкоза: (\d+)', extracted_text)
                Glucose = int(glucose_match.group(1)) if glucose_match else None
                st.session_state.Glucose = Glucose
            if findWholeWord('Кръвно')(extracted_text) is not None:
                pressure_match = re.search(r'Кръвно налягане: (\d+)', extracted_text)
                BloodPressure = int(pressure_match.group(1)) if pressure_match else None
                st.session_state.BloodPressure = BloodPressure
            if findWholeWord('Инсулин')(extracted_text) is not None:
                insulin_match = re.search(r'Инсулин: (\d+)', extracted_text)
                Insulin = int(insulin_match.group(1)) if insulin_match else None
                st.session_state.Insulin = Insulin
        if selected == 'Диабет':
            age = get_age_of_user(conn,username)
            height = get_height_of_user(conn,username)
            sex = get_sex_of_user(conn, username)
            kilo = get_kilo_of_user(conn, username)
            pregnancies = get_pregnancies_of_user(conn, username)
            result = None
            if height != None:
                bmi = kilo/(height*height)
            if st.session_state.Glucose is not None:
                Glucose = st.session_state.Glucose
                output = 1
            else:
                Glucose = None
            if st.session_state.BloodPressure is not None:
                BloodPressure = st.session_state.BloodPressure
                output = 1
            if st.session_state.Insulin is not None:
                Insulin = st.session_state.Insulin
                output = 1
            output = 1
            col1, col2, col3  = st.columns([1,1,1])
            col4,col5 = st.columns([1.6,0.1])
            col6,col7,col8 = st.columns([1,1,1])
            col9,col10 = st.columns([1.6,0.1])
            with col2:
                    if st.button("Резулат за диабет"):
                        if Glucose is None:
                            with col12:
                                st.markdown("<p style='text-align: center; color: #F75D59;background-color:white;border-radius:25px;border: 2px solid #F75D59   ;'>Моля прикачете вашите изследвания в PDF формат в секция Профил</p>", unsafe_allow_html=True)
                        else:
                            diab_prediction = diabetes_model.predict([[pregnancies, Glucose, BloodPressure, Insulin, bmi, age]])
                            if (diab_prediction[0] == 1):
                                diab_diagnosis = 'Пациентът е възможно да страда от диабет'
                                output = '0'   
                            else:
                                diab_diagnosis = 'Пациентът не страда от диабет'
                                output = '2'  
                
            with col4:
                    if(output == '0'):
                        with col12:
                            st.markdown("<p style='text-align: center; color: #F75D59;background-color:white;border-radius:25px;border: 2px solid #F75D59   ;'>Пациентът е възможно да страда от диабет</p>", unsafe_allow_html=True)
                    elif(output == '2'):
                        with col12:
                            st.markdown("<p style='text-align: center; color: #F75D59;background-color:white;border-radius:25px;border: 2px solid #F75D59   ;'>Пациентът не страда от диабет</p>", unsafe_allow_html=True)
            with col7:
                st.markdown("<h1 style=' color: black;'> " "Диабет</h1>", unsafe_allow_html=True)
                with col9:
                    st.markdown("<b style='text-align: justify;color:black;text-decoration-style: solid;'>Диабетът е сериозно заболяване, което може да оказва значително влияние върху живота на хората. Неконтролираният диабет може да има дългосрочни последици за здравето, но разбирането на типовете диабет и начините за управление може да направи голяма разлика.</b>", unsafe_allow_html=True)
                    st.markdown("<h2 style=' color: black;text-align: center;'> " "Тип 1 Диабет</h1>", unsafe_allow_html=True)
                    st.markdown("<b style='text-align: justify;color:black;text-decoration-style: solid;'>Тип 1 диабет обикновено се развива при по-млади хора и е свързан с недостатъчно произвеждане на инсулин от тялото. Инсулинът е ключов хормон, който регулира нивата на захар в кръвта. Хората с този тип диабет обикновено се нуждаят от външен източник на инсулин, като инсулинови инжекции или помпи, за да контролират нивата на глюкоза.</b>", unsafe_allow_html=True)
                    st.markdown("<h2 style=' color: black;text-align: center;'> " "Тип 2 Диабет</h1>", unsafe_allow_html=True)
                    st.markdown("<b style='text-align: justify;color:black;text-decoration-style: solid;'>Тип 2 диабет е по-често срещан и обикновено се развива по-късно в живота. Тук тялото не използва инсулина ефективно или не произвежда достатъчно. Здравословен начин на живот, като здравословно хранене и редовна физическа активност, често помагат за контролиране на този вид диабет. В случаи, когато тези мерки не са достатъчни, могат да се използват и лекарства.</b>", unsafe_allow_html=True)
                    st.markdown("<h2 style=' color: black;text-align: center;'> " "Управление и Превенция</h1>", unsafe_allow_html=True)
                    st.markdown("<b style='text-align: justify;color:black;text-decoration-style: solid;'>Редовното следене на нивата на глюкоза в кръвта е от изключително значение за контролирането на диабета. Това включва редовни изследвания и следене на хранителните навици, физическата активност и приема на лекарства.</b>", unsafe_allow_html=True)
                    st.markdown("<b style='text-align: justify;color:black;text-decoration-style: solid;'>Важно е и предпазването от развитието на диабет. Здравословният начин на живот, включително балансирано хранене, поддържане на оптимално тегло и редовна физическа активност, може да намали риска от появата на диабет тип 2.</b>", unsafe_allow_html=True)
                    st.markdown("<b style='text-align: justify;color:black;text-decoration-style: solid;'>Диабетът е хронично заболяване, но разбирането му и вземането на мерки за контрол могат да помогнат за подобряване на качеството на живот и предотвратяване на дългосрочни здравни проблеми.</b>", unsafe_allow_html=True)
        if selected == "Намери лекарство":
            st.title('Намери своето лекарство')
            medication_name = st.text_input('Въведете името на лекарството')
            if st.button('Потърси'):
                c = conn.cursor()
                c.execute('''SELECT info FROM medication WHERE name = ?''', (medication_name,))
                medication_info = c.fetchone()
                if medication_info:
                    c.execute('''SELECT url FROM medication WHERE name = ?''',(medication_name,))
                    info_image_url =  c.fetchone()[0]
                    clean_url = info_image_url.strip().strip('\'"')
                    if info_image_url and clean_url:
                        create_custom_markdown_card(medication_info[0], clean_url)
                    else:
                        create_custom_markdown_card(medication_info[0])
                else:
                    st.write('Няма намерена информация за {}'.format(medication_name))
                pharmacies = select_pharmacies_by_medication(cursor, medication_name)
                if pharmacies:
                    st.subheader('Аптеки с {} в наличност:'.format(medication_name))
                    # Create a folium map centered at the first pharmacy
                    map_center = (pharmacies[0][1], pharmacies[0][2])
                    m = folium.Map(location=map_center, zoom_start=14)

                    # Iterate through pharmacies to add markers
                    for pharmacy in pharmacies:
                        pharmacy_name = pharmacy[0]
                        pharmacy_lat = pharmacy[1]
                        pharmacy_long = pharmacy[2]

                        # Fetch street name from the database for the current pharmacy
                        c.execute('''SELECT street FROM pharmacies WHERE name = ?''', (pharmacy_name,))
                        street_name = c.fetchone()[0]  # Assuming street name is fetched properly

                        # Create the popup content with both pharmacy name and street name
                        popup_content = f'{pharmacy_name}<br>{street_name}'  # Modify this as per your data structure

                        # Create the marker with the concatenated content
                        folium.Marker(
                            location=(pharmacy_lat, pharmacy_long),
                            popup=popup_content,
                            icon=folium.Icon(icon='tablets', prefix='fa', color='red')
                        ).add_to(m)

                    # Display the map after adding all markers
                    folium_static(m)

                else:
                    st.write('Не бяха намерени аптеки с {} в наличност.'.format(medication_name))
        if selected == "Запиши си час онлайн":
            st.title('Намерете лекар и запазете час за преглед')
            col1,col2,col3 = st.columns([4,0.5,4])
            with col1:
                filtered = False
                selected_city = st.selectbox('Изберете град', ['София','Бургас','Варна','Пловдид'])
                selected_specialty = st.selectbox('Изберете специалност', ['Кардиолог', 'Дерматолог','Ортопед'])
                filtered_doctors = get_doctors_by_city_and_specialty(conn, selected_city, selected_specialty)
                if filtered_doctors:
                    for doctors in filtered_doctors:
                        filtered = True
                else:
                    st.write('Не бяха намерени доктори от тази специалност в града')
                if filtered:
                    formatted_names = ['Д-р ' + first_name_doc + ' ' + last_name_doc for first_name_doc, last_name_doc in filtered_doctors]
                    selected_doctor = st.selectbox('Изберете лекар:', formatted_names)
                    
                    if selected_doctor:
                        selected_date = st.date_input('Избери дата')
                        if selected_date:
                            available_hours = get_available_hours(conn, selected_doctor, selected_date)
                            with col3:
                                if available_hours:
                                    st.write(f"Свободни часове за  {selected_doctor} на {selected_date}:")
                                    num_rows = (len(available_hours) + 2) // 3
                                    for i in range(num_rows):
                                        row_hours = available_hours[i * 3: (i + 1) * 3]  # Get hours for each row
                                        columns = st.columns(3)
                                        for j, hour in enumerate(row_hours):
                                            if st.session_state.selected_hour == hour:
                                                columns[j].button(hour, key=hour, help="color:red;")
                                            else:
                                                if columns[j].button(hour, key=hour):
                                                    st.session_state.selected_hour = hour

                                    col20,col21,col22=st.columns([0.7,1,0.75])
                                    col23,col24 = st.columns([1,0.0001])
                                    with col21:
                                                st.write("")
                                                if col21.button("Запази час"):
                                                    if st.session_state.selected_hour:
                                                        save_appointment(conn, selected_doctor, username, selected_date, st.session_state.selected_hour)
                                                        with col23:
                                                            st.success(f"{username} вие записахте вашият час при {selected_doctor}, вашият час е от {st.session_state.selected_hour} на {selected_date}")
        if selected == "Вашите записани часове":
            st.header("Вашият график за следния месец")
            user_appointments = get_user_appointments(conn,username)
            if user_appointments:
                appointments_for_calendar = []
                for appointment in user_appointments:
                    doctor_username, appointment_date, appointment_hour = appointment
                    # Append each appointment to a separate list for calendar events
                    appointments_for_calendar.append(
                        {
                            "doctor_username": doctor_username,
                            "appointment_date": appointment_date,
                            "appointment_hour": appointment_hour,
                        }
                    )
                events = []
                for appointment in appointments_for_calendar:
                    doctor_details = get_doctor_names(conn,appointment["doctor_username"])

                    first_name, last_name, tele = doctor_details
                    
                    title = f"Д-р {first_name} {last_name}, тел. номер:{tele}"
                    


                    event = {
                        "title": title,
                        "color": "#FF4B4B",  # Red color
                        "start": f"{appointment['appointment_date']}T{appointment['appointment_hour']}",
                        "end": f"{appointment['appointment_date']}T{appointment['appointment_hour']}",
                        "resourceId": "a",  # resourceId - modify this as needed
                    }
                    events.append(event)
                    if isinstance(appointment["doctor_username"], list):
                        for test in appointment["doctor_username"]:
                            doctor_details = get_doctor_names(test)
                            first_name, last_name, tele = doctor_details
                            title = f"{appointment['appointment_hour']} - Dr. {first_name} {last_name}"
                    else:
                        doctor_details = get_doctor_names(conn,appointment["doctor_username"])
                        first_name, last_name, tele = doctor_details
                        title = f"{appointment['appointment_hour']} - Dr. {first_name} {last_name}"
                current_date = datetime.now()
                year = current_date.year
                month = current_date.month

                initial_date = f"{year}-{month:02d}-01"

                # Define calendar options
                calendar_options = {
                    "initialDate": initial_date,
                    "initialView": "listMonth",  # Display the calendar in list mode
                }

                # Display the calendar with the events
                state = calendar(events=events, options=calendar_options, key="my_calendar")   

                st.write(state)
            else:
                st.write("Вие нямате записани часове")

    if role_user == 2:
        with st.sidebar:
            selected = st.selectbox('AIDoc', ['Admin panel'], index=0, format_func=lambda x: ' Admin panel' if x == 'Admin panel' else x)
        if selected == 'Admin panel':
            st.header("Нов доктор")
            doctor_first_name = st.text_input("Име")
            doctor_sec_name = st.text_input("Фамилия")
            doc_city = st.selectbox("Град",('София','Варна','Бургас'))
            if doc_city == 'София':
                doc_city = 1
            elif doc_city == "Бургас":
                doc_city = 3
            elif doc_city == "Варна":
                doc_city = 2
            elif doc_city == "Пловдив":
                doc_city = 4
            doc_tel = st.text_input("тел.номер")
            doctor_specialty = st.selectbox("Специалност",('Кардиолог','Ортопед','Дерматолог'))
            if doctor_specialty == 'Кардиолог':
                id_spec = 1
            elif doctor_specialty =='Ортопед':
                id_spec = 2
            elif doctor_specialty == 'Дерматолог':
                id_spec = 3
            doctor_email = st.text_input("Имейл")
            if st.button("Add Doctor"):
                doc_username = 'doc_' + doctor_first_name
                doc_pass = doctor_first_name + doctor_sec_name + '123'
                if doctor_first_name and doctor_specialty and doctor_email and doc_city and doctor_sec_name and doc_tel:
                    save_user_info(conn,doctor_first_name,doctor_sec_name,doctor_email,doc_tel,doc_username,3,doc_city)
                    add_info_doc(conn,doc_username,id_spec)
                    register_new_usr(doctor_first_name,doctor_email,doc_username,doc_pass)
                    #set_default_schedule(doc_username)
                    #set_default_schedule_av_hours(doc_username)
                    st.success("Успешно!")
                else:
                    st.warning("Моля, въведете всички полета.")
    if role_user == 3:
        with st.sidebar:
        
            selected = option_menu('AIDoc',
                            
                            [
                                'Вашият график',
                                'Записани часове',
                            ],
                            icons=['person','bandaid'],
                            default_index=0)
        if selected == "Вашият график":
            col1, col2, col3 = st.columns([0.25,1,0.1])
            col4, col5, col6 = st.columns([1,1.1,0.8])
            with col2:
                st.header(f"Здравейте, {username}")
            doctor_schedule = get_doctor_schedule(conn, username)
            doc_id = get_user_id_by_username(conn, username)
            today = datetime.today()
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            if st.session_state.data:
                with col5:
                    st.write("Вашият график:")
                doc_sched = get_doctor_schedule(conn, username)
                col7, col8, col9 = st.columns([0.1,2,0.1])
                with col8:
                    for date, (first_hour, last_hour) in doc_sched.items():
                        st.write(f"Дата: {date}, Начало на работния ден: {first_hour}, Край на работния ден: {last_hour}")
                col10, col11, col12 = st.columns([0.47,1,0.1])
                with col11:
                    if st.button("Променете графика си"):
                        modify_schedule_for_doctor(conn,doc_id)
                        st.session_state.data = False
                        st.rerun()
            else:   
                x=0
                start = []
                end =[]
                for current_day in weekdays:
                    # Move the creation of start_time and end_time inside the loop
                    start_time, end_time = get_working_hours(username, current_day)
                    start.append(start_time)
                    end.append(end_time)
            
                for i in range(7):
                        current_date = today + timedelta(days=i)
                        current_d = current_date.strftime('%A')
                        day_index = weekdays.index(current_d)
                        start_time_of_day = start[day_index]
                        end_time_of_day = end[day_index]
                        current_date = current_date.strftime('%Y-%m-%d')
                        save_doc_sched(conn, username, current_date, start_time_of_day, end_time_of_day)
                if st.button("Запази"):
                    st.session_state.data = True
                    st.rerun()
        if selected == "Записани часове":
            doctor_appointments = get_doctor_appointments(conn,username)
            if doctor_appointments:
                appointments_for_calendar = []  # A separate list to hold appointments for the calendar

                for appointment in doctor_appointments:
                    patient_username, appointment_date, appointment_hour = appointment
                        
                    # Append each appointment to a separate list for calendar events
                    appointments_for_calendar.append(
                        {
                            "patient_username": patient_username,
                            "appointment_date": appointment_date,
                            "appointment_hour": appointment_hour,
                        }
                    )
                events = []
                for appointment in appointments_for_calendar:
                    patient_first_name = get_firsty_name(conn,appointment['patient_username'])
                    patient_second_name = get_lasty_name(conn,appointment['patient_username'])
                    patient_telephone = get_tel_number(conn,appointment['patient_username'])
                    title = f"{patient_first_name} {patient_second_name}, tel:{patient_telephone}"

                    # Create event for each appointment
                    event = {
                        "title": title,
                        "color": "#FF4B4B",  # Red color
                        "start": f"{appointment['appointment_date']}T{appointment['appointment_hour']}",
                        "end": f"{appointment['appointment_date']}T{appointment['appointment_hour']}",
                        "resourceId": "a",  # resourceId - modify this as needed
                    }
                    events.append(event)
                    

                current_date = datetime.now()
                year = current_date.year
                month = current_date.month

                initial_date = f"{year}-{month:02d}-01"

                # Define calendar options
                calendar_options = {
                    "initialDate": initial_date,
                    "initialView": "listMonth",  # Display the calendar in list mode
                }

                # Display the calendar with the events
                state = calendar(events=events, options=calendar_options, key="my_calendar")   

                st.write(state)
            else:
                st.write("Нямате записани часове за следващия месец")
