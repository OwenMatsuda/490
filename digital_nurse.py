"""Digital Nurse"""
import datetime
import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()
r.energy_threshold = 150
r.pause_threshold = 1
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=0.2)

engine = pyttsx3.init()
engine.setProperty("rate", 165)

patients = [
    {
        "name": "Owen Matsuda",
        "age": 22,
        "sex": "Male",
        "pronouns": ["he", "him", "his"],
        "allergies": [
            {
                "allergen": "eggplant",
                "severity": "minor",
            },
            {
                "allergen": "kiwi",
                "severity": "minor",
            },
        ],
        "vaccinations": [
            {
                "type": "covid",
                "shots": [
                    {
                        "brand": "Johnson and Johnson",
                        "date": datetime.datetime(2021, 12, 13),
                    },
                    {
                        "brand": "Moderna",
                        "date": datetime.datetime(2021, 7, 21),
                    },
                ],
                "boosterPeriod": 0.5,  # in years,
            }
        ],
        "notes": [],
    },
    {
        "name": "Ishwar Desai",
        "age": 22,
        "sex": "Male",
        "pronouns": ["he", "him", "his"],
        "allergies": [
            {
                "allergen": "peanuts",
                "severity": "deadly",
            },
            {
                "allergen": "dairy",
                "severity": "deadly",
            },
        ],
        "vaccinations": [],
        "notes": [],
    },
]


def any_text(substrings, text):
    """check if any of the list of substrings are in text"""
    return any(substring in text for substring in substrings)


def tts(command):
    """run tts"""
    engine.say(command)
    engine.runAndWait()

def get_text(speak_text, duration=3):
    """call google API to interpret audio recording"""
    try:
        with sr.Microphone() as src:
            if speak_text != "":
                tts(speak_text)
            print("recording")
            audio = r.listen(src)
            print("received audio")
            text = r.recognize_google(audio)
            print(text)
            return text.lower()

    except Exception as err:
        print(err)
        return None


def loop_get_text(speak_text):
    """continue looping until proper audio transcription is successful"""
    text = None
    while not text:
        text = get_text(speak_text)

    return text


def get_patient():
    """get patient from database"""
    global patient
    while True:
        name = loop_get_text("Please say the patient name")
        confirm = loop_get_text("To confirm, the patient's name is" + name)
        print("confirm: " + confirm)
        if "yes" in confirm:
            patient = next(
                (patient for patient in patients if patient["name"].lower() == name),
                None,
            )
            return patient

def get_vaccinations():
    """get the list of vaccinations from the database"""
    vaccine = patient["vaccinations"][0]
    shots = vaccine["shots"]
    if len(shots) == 0:
        tts(patient["pronouns"][0] + " hasn't got the " + vaccine["name"])
    vaccine_text = " and ".join(
        [
            "the " + shot["brand"] + " in " + shot["date"].strftime("%B %Y")
            for shot in shots
        ]
    )

    tts(patient["pronouns"][0] + " got " + vaccine_text)
    time_since_last_shot = datetime.datetime.today() - shots[-1]["date"]
    time_in_years = time_since_last_shot.days / 365
    if time_in_years > vaccine["boosterPeriod"]:
        tts("However, " + patient["pronouns"][0] + " is due for a booster")


def add_vaccination(text):
    """add a vaccination to database"""
    if "moderna" in text:
        brand = "Moderna"
    elif "pfizer" in text:
        brand = "Pfizer"
    elif "Johnson" in text:
        brand = "Johnson and Johnson"
    tts(
        "OK, I am adding a " + brand + " booster to " + patient["name"] + "'s records"
    )
    patient["vaccinations"][0]["shots"].append(
        {
            "brand": brand,
            "date": datetime.datetime.today(),
        }
    )

def add_allergen(text):
    """add an allergen to the database"""

    if "deadly" in text:
        severity = "deadly"
    elif "mild" in text:
        severity = "mild"
    else:
        severity = "unspecified"

    allergen = text.partition("allergen for")[2].strip()
    tts(
        "OK, I am adding an allergen for " + allergen + " to " + patient["name"] + "'s records"
    )

    for i in range(len(patient["allergies"])):
        allergy = patient["allergies"][i]
        if allergy["allergen"] == allergen:
            del patient["allergies"][i]

    patient["allergies"].append(
        {
            "allergen": allergen,
            "severity": severity
        }
    )


def get_allergies():
    """get the list of allergies from the database"""
    allergies = patient["allergies"]
    if len(allergies) == 0:
        tts(patient["pronouns"][0] + " doesn't have any allergies")
    allergy_text = " and ".join(
        [
            "has a " + allergy["severity"] + " " + allergy["allergen"] + " allergy "
            for allergy in allergies
        ]
    )
    tts(patient["name"] + " " + allergy_text)

def add_note(text):
    note = text.partition("note")[2].strip()
    tts (
        "OK, I am adding a note for " + note + " to " + patient["name"] + "'s records"
    )
    patient["notes"].append(note)

def get_notes():
    notes = patient["notes"]
    tts (
        "OK, here are the notes for " + patient["name"]
    )

    for i in range(len(notes)):
        tts (
            "Note " + str(i+1) + ": " + notes[i]
        )

    tts (
        "End of notes"
    )


def process_audio(text):
    """speech processing to determine proper action"""
    global patient
    if any_text(["note", "notes"], text):
        if "get" in text:
            get_notes()
        else:
            add_note(text)
    elif any_text(["vaccination", "vaccine", "booster"], text):
        if "get" in text:
            get_vaccinations()
        elif any_text(["add", "give"], text):
            add_vaccination(text)
    elif any_text(["allergies", "allergy", "allergen"], text):
        if "get" in text:
            get_allergies()
        elif any_text(["add", "give"], text):
            add_allergen(text)
    elif any_text(["thanks", "thank you"], text):
        tts("You're welcome!")
    elif any_text(["patient"], text):
        if any_text(["update", "change"], text):
            patient = get_patient()


patient = get_patient()
print(patient)
while True:
    print("looping")
    cur_text = get_text("", 5)
    if cur_text:
        process_audio(cur_text)
