from imports import *
from streamlit_login import __login__


def profile_page(conn, username):
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
                col3,col4, col5 = st.columns([0.75,0.75,0.5])
                col6,col7,col8 = st.columns([0.4,1,0.6])
                with col1:
                    first_name = st.text_input("Първо име",placeholder="Иван")
                    ch_fn = check_valid_name_bulgarian(first_name)
                    second_name = st.text_input("Фамилия",placeholder="Иванов")
                    ch_sn = check_valid_name_bulgarian(second_name)
                    tel_number = st.text_input("Телефонен номер",placeholder="+35988888888")
                    ch_tel = check_valid_phone_number(tel_number)
                with col2:
                    result = None
                    Age = st.number_input("Възраст",1,100,None,1)
                    Sex = st.radio("Пол",["мъж","жена"])
                    if Sex=="мъж":
                        Pregnancies = 0
                    else:
                        Pregnancies = st.number_input("Бременности",0,50,None,1, placeholder = 'Брой бременности')
                    Height = st.number_input("Височина",0.01,4.00,None,0.01, placeholder="Височината ви в метри(Пример 181см->1.81)")
                    Kilo = st.number_input("Тегло", 0.01, 300.00,None, 0.01 , placeholder="Теглото ви в килограми")
                    if height != None:
                        BMI = kilo/(height*height)
                with col4:
                    save_btn = st.button("Запази")
                    if save_btn == True:
                        auth_par_check = check_parameters_filled(Age,Sex,Height,Kilo)
                        if auth_par_check == False:
                            with col7:
                                st.error("Въведете вашите данни във всички полета!")
                        elif ch_fn == False:
                            with col7:
                                st.error("Въведете вашето име на кирилица")
                        elif ch_sn == False:
                            with col7:
                                st.error("Въведете вашата фамилия на кирилица")
                        elif ch_tel == False:
                            with col7:
                                st.error("Въведете валиден телефонен номер")
                        else:
                            save_user_info(conn,first_name,second_name,None,tel_number,username,role_user,1)
                            save_user_profile(conn,username,Age,Sex,Pregnancies,Height,Kilo)
                            conn.commit()
                            user_profile = get_user_profile(conn, username)
                            data_created = True
                            if data_created:
                                st.rerun()
            medical_tests = st.file_uploader("Качете вашите изследвания в PDF формат тук:", type=['pdf'])
            modal = Modal(key = "Demo",title = "Начална страница", padding = -10, max_width= 700)
            info = st.button("Как се използва?")
            if info:
                modal.open()
            if modal.is_open():
                st.session_state.info = True
                with modal.container():
                    st.markdown("<p style='text-align: center; color: black;'>В секцията профил Вие трябва да въведете вашите данни:</p>", unsafe_allow_html=True)
                    st.image(r'AIDoc/images/profile.png')
                    st.markdown("<p style='text-align: center; color: black;'>При натискане на бутона 'Запази' Вашите данни ще бъдат запазени в системата, като винаги можете да ги промените чрез бутона 'Променете вашите данни'.</p>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: black;'>Тук можете да прикачите вашите лабораторни изследвания в PDF формат и да продължите напред към тестовете:</p>", unsafe_allow_html=True)
                    st.image(r'AIDoc/images/pdf.png')
            find(medical_tests)