let getById = id => document.getElementById(id);

let formData = {
    "nick": getById("nickname"),
    "firstName": getById("first_name"),
    "lastName": getById("last_name"),
    "age": getById("age"),
    "sex": getById("sex"),
    "gdpr": getById("gdpr"),
    "motive": getById("motive"),
    "source": getById("source")
}

let textData = {
    "firstName": getById("text_fname"),
    "lastName": getById("text_lname"),
    "age": getById("text_age"),
    "signature": getById("signature"),
    "afterSignature": getById("after_signature"),
    "sexSuffices": document.querySelectorAll(".sex_suffix")
}


export let handleRegistrationForm = () => {
    formData.firstName.addEventListener("keyup", () => textData.firstName.innerHTML = formData.firstName.value);
    formData.lastName.addEventListener("keyup", () => textData.lastName.innerHTML = formData.lastName.value);
    formData.age.addEventListener("keyup", () => textData.age.innerHTML = formData.age.value);
    formData.age.addEventListener("change", () => textData.age.innerHTML = formData.age.value);
    formData.gdpr.addEventListener("change", () => {
        let agreed = formData.gdpr.value == "T";
        let opacity = agreed ? 1 : 0;
        textData.afterSignature.style.opacity = opacity;
    });

    formData.nick.addEventListener("keyup", () => {
        let before = ".character::before{content: '" + formData.nick.value + ": '}";
        let head = document.head.innerHTML;
        document.head.innerHTML = head + "<style>" + before + "</style>";
        textData.signature.innerHTML = formData.nick.value;
    });

    formData.sex.addEventListener("change", () => {
        let sex_suffix = formData.sex.value == "F" ? "a" : "";
        textData.sexSuffices.forEach((span) => span.innerHTML = sex_suffix);
        let motive = "Co tě dovedlo k rozhodnutí zaregistrovat se na náš web? Je nějaký speciální důvod, proč bys rád" + sex_suffix + " patřil" + sex_suffix + " mezi nás?";
        let source = "Odkud ses dozvěděl" + sex_suffix + " o existenci tohoto města (webu)?";
        formData.motive.placeholder = motive;
        formData.source.placeholder = source;

    });

    let opacity = formData.gdpr.value == "T" ? 1 : 0;
    textData.afterSignature.style.opacity = opacity;
}



