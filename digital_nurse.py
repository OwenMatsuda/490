"""Digital Nurse"""
import datetime
import pyttsx3
import speech_recognition as sr
import time

class DigitalNurse:
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.energy_threshold = 150
        self.r.pause_threshold = 1
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=0.2)


        self.patient = None

        self.patients = [
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


    def any_text(self, substrings, text):
        """check if any of the list of substrings are in text"""
        return any(substring in text for substring in substrings)


    def tts(self, command):
        """run tts"""
        # wait_time = len(command)/(165*4) * 60 + 1
        self.engine.say(command)
        self.engine.runAndWait()
        # time.sleep(wait_time)

    def get_text(self, speak_text, duration=3):
        """call google API to interpret audio recording"""
        try:
            with sr.Microphone() as src:
                if speak_text != "":
                    self.tts(speak_text)
                print("recording")
                audio = self.r.listen(src)
                print("received audio")
                text = self.r.recognize_google(audio)
                print(text)
                return text.lower()

        except Exception as err:
            print(err)
            return None


    def loop_get_text(self, speak_text):
        """continue looping until proper audio transcription is successful"""
        text = None
        while not text:
            text = self.get_text(speak_text)

        return text


    def get_patient(self):
        return self.patient

    def set_patient(self):
        """get patient from database"""
        while True:
            name = self.loop_get_text("Please say the patient name")
            confirm = self.loop_get_text("To confirm, the patient's name is" + name)
            print("confirm: " + confirm)
            if "yes" in confirm:
                self.patient = next(
                    (patient for patient in self.patients if patient["name"].lower() == name),
                    None,
                )

    def get_vaccinations(self):
        """get the list of vaccinations from the database"""
        vaccine = self.patient["vaccinations"][0]
        output = ""
        shots = vaccine["shots"]
        output1 = ""
        if len(shots) == 0:
            output1 = self.patient["pronouns"][0] + " hasn't got the " + vaccine["name"] + "\n"
        vaccine_text = " and ".join(
            [
                "the " + shot["brand"] + " in " + shot["date"].strftime("%B %Y")
                for shot in shots
            ]
        )
        
        output2 = self.patient["pronouns"][0] + " got " + vaccine_text + "\n"
        time_since_last_shot = datetime.datetime.today() - shots[-1]["date"]
        time_in_years = time_since_last_shot.days / 365
        output3 = ""
        if time_in_years > vaccine["boosterPeriod"]:
            output3 = "However, " + self.patient["pronouns"][0] + " is due for a booster"
        output = output1 + output2 + output3
        self.tts(output)
        return output1 + output2 + output3


    def add_vaccination(self, text):
        """add a vaccination to database"""
        if "moderna" in text:
            brand = "Moderna"
        elif "pfizer" in text:
            brand = "Pfizer"
        elif "Johnson" in text:
            brand = "Johnson and Johnson"
        self.tts(
            "OK, I am adding a " + brand + " booster to " + self.patient["name"] + "'s records"
        )
        self.patient["vaccinations"][0]["shots"].append(
            {
                "brand": brand,
                "date": datetime.datetime.today(),
            }
        )


    def get_allergies(self):
        """get the list of allergies from the database"""
        allergies = self.patient["allergies"]
        message = ""
        if len(allergies) == 0:
            message = self.patient["pronouns"][0] + " doesn't have any allergies"
            self.tts(message)
        allergy_text = " and ".join(
            [
                "has a " + allergy["severity"] + " " + allergy["allergen"] + " allergy "
                for allergy in allergies
            ]
        )
        message2 = self.patient["name"] + " " + allergy_text
        message += message2
        self.tts(message2)

        return message


    def add_allergen(self, text):
        """add an allergen to the database"""

        if "deadly" in text:
            severity = "deadly"
        elif "mild" in text:
            severity = "mild"
        else:
            severity = "unspecified"

        allergen = text.partition("allergen for")[2].strip()
        self.tts(
            "OK, I am adding an allergen for " + allergen + " to " + self.patient["name"] + "'s records"
        )

        for i in range(len(self.patient["allergies"])):
            allergy = self.patient["allergies"][i]
            if allergy["allergen"] == allergen:
                del self.patient["allergies"][i]

        self.patient["allergies"].append(
            {
                "allergen": allergen,
                "severity": severity
            }
        )

    def add_note(self, text):
        note = text.partition("note")[2].strip()
        self.tts (
            "OK, I am adding a note for " + note + " to " + self.patient["name"] + "'s records"
        )
        self.patient["notes"].append(note)

    
    def get_notes(self):
        notes = self.patient["notes"]
        self.tts (
            "OK, here are the notes for " + patient["name"]
        )

        for i in range(len(notes)):
            self.tts (
                "Note " + str(i+1) + ": " + notes[i]
            )

        self.tts (
            "End of notes"
        )


    def process_audio(self, text):
        """speech processing to determine proper action"""
        output = ""
        if self.any_text(["note", "notes"], text):
            if "get" in text:
                output = self.get_notes()
            else:
                output = self.add_note(text)
        elif self.any_text(["vaccination", "vaccine", "booster"], text):
            if "get" in text:
                output = self.get_vaccinations()
            elif self.any_text(["add", "give"], text):
                soutput = self.add_vaccination(text)
        elif self.any_text(["allergies", "allergy", "allergen"], text):
            if "get" in text:
                output = self.get_allergies()
            elif self.any_text(["add", "give"], text):
                output = self.add_allergen(text)
        elif self.any_text(["thanks", "thank you"], text):
            output = self.tts("You're welcome!")
        elif self.any_text(["patient"], text):
            if self.any_text(["update", "change"], text):
                output = self.set_patient()

        print(output)
        return output

    def audio_loop(self):
        if self.engine._inLoop:
            self.engine.endLoop()
        self.patient = self.patients[0]
        cur_text = self.get_text("", 5)
        if cur_text:
            return_text = self.process_audio(cur_text)
            return return_text
