let activateNurse = false;
let nurseIndicator = document.querySelector(".nurseIndicator");
var startRecording = async function() {
    activateNurse = true;
    nurseIndicator.innerHTML = "Nurse Active";
    nurseIndicator.style.background = "#96E6B3";
    while (activateNurse) {
        res = await fetch('/nurse')
        console.log(res)
        text = await res.text()
        console.log(text);
        if (text !== 'null') {
            sentences = text.split('.').length
            let wait_time = (text.length/(165*5) * 60) * 1000;
            let output_box = document.querySelector(".outputText");
            let output_text = ""
            for (let i = 0; i < text.length; i++) {
                output_text += text[i];
                output_box.innerHTML = output_text;
                await new Promise(res => setTimeout(res, wait_time / text.length - 3))
            }
            await new Promise(res => setTimeout(res, 1000 * sentences));
        }
    }
}
var stopRecording = function() {
    activateNurse = false;
    nurseIndicator.innerHTML = "Nurse Inactive";
    nurseIndicator.style.background = "#D90429";
}
var setPatient = function() {
    fetch('/set_patient',)
}
var getPatient = function() {
    window.location.replace('/get_patient',)
}