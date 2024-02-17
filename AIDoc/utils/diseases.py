from utils.different import *
from utils.user import *
from io import BytesIO

def session():
    if 'Glucose' not in st.session_state:
        st.session_state.Glucose = None
    if 'BloodPressure' not in st.session_state:
        st.session_state.BloodPressure = None
    if 'Insulin' not in st.session_state:
        st.session_state.Insulin = None
    if 'TotalBilirubin' not in st.session_state:
        st.session_state.TotalBilirubin = None
    if 'DirectBilirubin' not in st.session_state:
        st.session_state.DirectBilirubin = None
    if 'AlkalinePhosphatase' not in st.session_state:
        st.session_state.AlkalinePhosphatase = None
    if 'AlanineAminotransferase' not in st.session_state:
        st.session_state.AlanineAminotransferase = None
    if 'AspartateAminotransferase' not in st.session_state:
        st.session_state.AspartateAminotransferase = None
    if 'TotalProtein' not in st.session_state:
        st.session_state.TotalProtein = None
    if 'Albumin' not in st.session_state:
        st.session_state.Albumin = None
    if 'AlbuminAndGlobulinRatio' not in st.session_state:
        st.session_state.AlbuminAndGlobulinRatio = None
    if 'cp' not in st.session_state:
        st.session_state.cp = None
    if 'chol' not in st.session_state:
        st.session_state.chol = None
    if 'fbs' not in st.session_state:
        st.session_state.fbs = None
    if 'restecg' not in st.session_state:
        st.session_state.restecg = None
    if 'thalach' not in st.session_state:
        st.session_state.thalach = None
    if 'exang' not in st.session_state:
        st.session_state.exang = None
    if 'oldpeak' not in st.session_state:
        st.session_state.oldpeak = None
    if 'slope' not in st.session_state:
        st.session_state.slope = None
    if 'ca' not in st.session_state:
        st.session_state.ca = None
    if 'thal' not in st.session_state:
        st.session_state.thal = None
    if 'Hemoglobin' not in st.session_state:
        st.session_state.Hemoglobin = None

def find(medical_tests):
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
        if findWholeWord('Общ билирубин')(extracted_text) is not None:
            total_bilirubin_match = re.search(r'Общ билирубин: (\d+(\.\d+)?)', extracted_text)
            TotalBilirubin = float(total_bilirubin_match.group(1)) if total_bilirubin_match else None
            st.session_state.TotalBilirubin = TotalBilirubin
        if findWholeWord('Директен билирубин')(extracted_text) is not None:
            direct_bilirubin_match = re.search(r'Директен билирубин: (\d+(\.\d+)?)', extracted_text)
            DirectBilirubin = float(direct_bilirubin_match.group(1)) if direct_bilirubin_match else None
            st.session_state.DirectBilirubin = DirectBilirubin
        if findWholeWord('Алкална фосфатаза')(extracted_text) is not None:
            alkaline_phosphatase_match = re.search(r'Алкална фосфатаза: (\d+)', extracted_text)
            AlkalinePhosphatase = int(alkaline_phosphatase_match.group(1)) if alkaline_phosphatase_match else None
            st.session_state.AlkalinePhosphatase = AlkalinePhosphatase
        if findWholeWord('Аланин аминотрансфераза')(extracted_text) is not None:
            alanine_aminotransferase_match = re.search(r'Аланин аминотрансфераза: (\d+)', extracted_text)
            AlanineAminotransferase = int(alanine_aminotransferase_match.group(1)) if alanine_aminotransferase_match else None
            st.session_state.AlanineAminotransferase = AlanineAminotransferase
        if findWholeWord('Аспартат аминотрансфераза')(extracted_text) is not None:
            aspartate_aminotransferase_match = re.search(r'Аспартат аминотрансфераза: (\d+)', extracted_text)
            AspartateAminotransferase = int(aspartate_aminotransferase_match.group(1)) if aspartate_aminotransferase_match else None
            st.session_state.AspartateAminotransferase = AspartateAminotransferase
        if findWholeWord('Общ протеин')(extracted_text) is not None:
            total_protein_match = re.search(r'Общ протеин: (\d+(\.\d+)?)', extracted_text)
            TotalProtein = float(total_protein_match.group(1)) if total_protein_match else None
            st.session_state.TotalProtein = TotalProtein
        if findWholeWord('Албумин')(extracted_text) is not None:
            albumin_match = re.search(r'Албумин: (\d+(\.\d+)?)', extracted_text)
            Albumin = float(albumin_match.group(1)) if albumin_match else None
            st.session_state.Albumin = Albumin
        if findWholeWord('A/G')(extracted_text) is not None:
            albumin_and_globulin_ratio_match = re.search(r'A/G: (\d+(\.\d+)?)', extracted_text)
            AlbuminAndGlobulinRatio = float(albumin_and_globulin_ratio_match.group(1)) if albumin_and_globulin_ratio_match else None
            st.session_state.AlbuminAndGlobulinRatio = AlbuminAndGlobulinRatio
        if findWholeWord('cp')(extracted_text) is not None:
            cp_match = re.search(r'cp: (\d+)', extracted_text)
            cp = float(cp_match.group(1)) if cp_match else None
            st.session_state.cp = cp
        if findWholeWord('chol')(extracted_text) is not None:
            chol_match = re.search(r'chol: (\d+)', extracted_text)
            chol = float(chol_match.group(1)) if chol_match else None
            st.session_state.chol = chol
        if findWholeWord('fbs')(extracted_text) is not None:
            fbs_match = re.search(r'fbs: (\d+)', extracted_text)
            fbs = float(fbs_match.group(1)) if fbs_match else None
            st.session_state.fbs = fbs
        if findWholeWord('restecg')(extracted_text) is not None:
            restecg_match = re.search(r'restecg: (\d+)', extracted_text)
            restecg = float(restecg_match.group(1)) if restecg_match else None
            st.session_state.restecg = restecg
        if findWholeWord('thalach')(extracted_text) is not None:
            thalach_match = re.search(r'thalach: (\d+)', extracted_text)
            thalach = float(thalach_match.group(1)) if thalach_match else None
            st.session_state.thalach = thalach
        if findWholeWord('exang')(extracted_text) is not None:
            exang_match = re.search(r'exang: (\d+)', extracted_text)
            exang = float(exang_match.group(1)) if exang_match else None
            st.session_state.exang = exang
        if findWholeWord('oldpeak')(extracted_text) is not None:
            oldpeak_match = re.search(r'oldpeak: (\d+(\.\d+)?)', extracted_text)
            oldpeak = float(oldpeak_match.group(1)) if oldpeak_match else None
            st.session_state.oldpeak = oldpeak
        if findWholeWord('slope')(extracted_text) is not None:
            slope_match = re.search(r'slope: (\d+)', extracted_text)
            slope = float(slope_match.group(1)) if slope_match else None
            st.session_state.slope = slope
        if findWholeWord('ca')(extracted_text) is not None:
            ca_match = re.search(r'ca: (\d+)', extracted_text)
            ca = float(ca_match.group(1)) if ca_match else None
            st.session_state.ca = ca
        if findWholeWord('thal')(extracted_text) is not None:
            thal_match = re.search(r'thal: (\d+)', extracted_text)
            thal = float(thal_match.group(1)) if thal_match else None
            st.session_state.thal = thal
        if findWholeWord('Hemoglobin')(extracted_text) is not None:
            hemoglobin_match = re.search(r'Hemoglobin: (\d+(\.\d+)?)', extracted_text)
            Hemoglobin = float(hemoglobin_match.group(1)) if hemoglobin_match else None
            st.session_state.Hemoglobin = Hemoglobin

def get_data_diabetes(conn, username):
    age = get_age_of_user(conn,username)
    height = get_height_of_user(conn,username)
    kilo = get_kilo_of_user(conn, username)
    pregnancies = get_pregnancies_of_user(conn, username)
    if height != None:
        bmi = kilo/(height*height)
    if st.session_state.Glucose is not None:
        Glucose = st.session_state.Glucose
    else:
        Glucose = None
    if st.session_state.BloodPressure is not None:
        BloodPressure = st.session_state.BloodPressure
    else:
        BloodPressure = None
    if st.session_state.Insulin is not None:
        Insulin = st.session_state.Insulin
    else:
        Insulin = None

    return age, bmi, pregnancies, Glucose, BloodPressure, Insulin

def get_data_heart(conn, username):
    age = get_age_of_user(conn, username)
    sex = get_sex_of_user(conn, username)
    if sex == "мъж":
        heart_sex = 0
    if sex == "жена":
        heart_sex = 1
    if st.session_state.cp is not None:
        cp = st.session_state.cp
    else:
        cp = None
    if st.session_state.BloodPressure is not None:
        BloodPressure = st.session_state.BloodPressure
    else:
        BloodPressure = None
    if st.session_state.chol is not None:
        chol = st.session_state.chol
    else:
        chol = None
    if st.session_state.fbs is not None:
        fbs = st.session_state.fbs
    else:
        fbs = None
    if st.session_state.restecg is not None:
        restecg = st.session_state.restecg
    else:
        restecg = None
    if st.session_state.thalach is not None:
        thalach = st.session_state.thalach
    else:
        thalach = None
    if st.session_state.exang is not None:
        exang = st.session_state.exang
    else:
        exang = None
    if st.session_state.oldpeak is not None:
        oldpeak = st.session_state.oldpeak
    else:
        oldpeak = None
    if st.session_state.slope is not None:
        slope = st.session_state.slope
    else:
        slope = None
    if st.session_state.ca is not None:
        ca = st.session_state.ca
    else:
        ca = None
    if st.session_state.thal is not None:
        thal = st.session_state.thal
    else:
        thal = None
        
    return age, heart_sex, cp, BloodPressure, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal

def get_data_liver(conn, username):
    age = get_age_of_user(conn, username)
    if st.session_state.TotalBilirubin is not None:
        TotalBilirubin = st.session_state.TotalBilirubin
    else:
        TotalBilirubin = None
    if st.session_state.DirectBilirubin is not None:
        DirectBilirubin = st.session_state.DirectBilirubin
    else:
        DirectBilirubin = None
    if st.session_state.AlkalinePhosphatase is not None:
        AlkalinePhosphatase = st.session_state.AlkalinePhosphatase
    else:
        AlkalinePhosphatase = None
    if st.session_state.AlanineAminotransferase is not None:
        AlanineAminotransferase = st.session_state.AlanineAminotransferase
    else:
        AlanineAminotransferase = None
    if st.session_state.AspartateAminotransferase is not None:
        AspartateAminotransferase = st.session_state.AspartateAminotransferase
    else:
        AspartateAminotransferase = None
    if st.session_state.TotalProtein is not None:
        TotalProtein = st.session_state.TotalProtein
    else:
        TotalProtein = None
    if st.session_state.Albumin is not None:
        Albumin = st.session_state.Albumin
    else:
        Albumin = None
    if st.session_state.AlbuminAndGlobulinRatio is not None:
        AlbuminAndGlobulinRatio = st.session_state.AlbuminAndGlobulinRatio
    else:
        AlbuminAndGlobulinRatio = None

    return age, TotalBilirubin, DirectBilirubin, AlkalinePhosphatase, AlanineAminotransferase, AspartateAminotransferase, TotalProtein, Albumin, AlbuminAndGlobulinRatio