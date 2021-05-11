getById = id => document.getElementById(id);


let nick = getById("nickname");
let firstName = getById("first_name");
let lastName = getById("last_name");
let age = getById("age");
let sex = getById("sex");
let gdpr = getById("gdpr");

getById("after_signature").style.opacity = 0;
firstName.addEventListener('keyup', () => getById("text_fname").innerHTML = firstName.value);
lastName.addEventListener('keyup', () => getById("text_lname").innerHTML = lastName.value);
age.addEventListener('keyup', () => getById("text_age").innerHTML = age.value);
age.addEventListener('change', () => getById("text_age").innerHTML = age.value);

nick.addEventListener('keyup', () => {
    let before = ".character::before{content: '" + nick.value + ": '}";
    let head = document.head.innerHTML;
    document.head.innerHTML = head + "<style>" + before + "</style>";
    document.getElementById("signature").innerHTML = nick.value;
});

sex.addEventListener('change', () => {
    let sex_suffix = sex.value == 1 ? "a" : "";
    let spans = document.querySelectorAll('.sex_suffix');

    let motive = "Co tě dovedlo k rozhodnutí zaregistrovat se na náš web? Je nějaký speciální důvod, proč bys rád" + sex_suffix + " patřil" + sex_suffix + " mezi nás?";
    let source = "Odkud ses dozvěděl" + sex_suffix + " o existenci tohoto města (webu)?";

    getById("motive").placeholder = motive;
    getById("source").placeholder = source;

    for (span of spans) {
        span.innerHTML = sex_suffix;
    }
});


gdpr.addEventListener("change", () => {
    let agreed = gdpr.value == 1;
    let opacity = agreed ? 1 : 0;
    getById("after_signature").style.opacity = opacity;
});



