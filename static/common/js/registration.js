let r_nickname = getId("nickname");
let r_fname = getId("first_name");
let r_lname = getId("last_name");
let r_age = getId("age");
let r_sex = getId("sex");
let r_gdpr = getId("gdpr");

getId("after_signature").style.opacity = 0;

r_nickname.addEventListener('keyup', function () {
    let before = ".character::before{content: '" + this.value + ": '}";
    let head = document.head.innerHTML;
    document.head.innerHTML = head + "<style>" + before + "</style>";
    document.getElementById("signature").innerHTML = this.value;
});

r_fname.addEventListener('keyup', function () {
    getId("text_fname").innerHTML = this.value;
});

r_lname.addEventListener('keyup', function () {
    getId("text_lname").innerHTML = this.value;
});

r_age.addEventListener('keyup', function () {
    getId("text_age").innerHTML = this.value;
});

r_age.addEventListener('change', function () {
    getId("text_age").innerHTML = this.value;
});

r_sex.addEventListener('change', function () {
    let sex_suffix = this.value == 1 ? "a" : "";
    let spans = document.querySelectorAll('.sex_suffix');

    let motive = "Co tě dovedlo k rozhodnutí zaregistrovat se na náš web? Je nějaký speciální důvod, proč bys rád" + sex_suffix + " patřil" + sex_suffix + " mezi nás?";
    let source = "Odkud ses dozvěděl" + sex_suffix + " o existenci tohoto města (webu)?";

    getId("motive").placeholder = motive;
    getId("source").placeholder = source;

    for (span of spans) {
        span.innerHTML = sex_suffix;
    }
});

// Udělat přes CSS
r_gdpr.addEventListener("change", function () {
    let agreed = this.value == 1;
    let opacity = agreed ? 1 : 0;
    getId("after_signature").style.opacity = opacity;
});


function getId(id) {
    return document.getElementById(id);
}


$(document).ready(function () {



    $(".rsadgeg_gdpr").on("change", function () {
        var seal = $(".after_agreement");
        var agreement = $(this).val() == 1;
        /*
        if (agreement) {
            seal.css("display", "block");
        }
        else {
            seal.css("display", "none");
        }*/
        seal.slideToggle(2000);
    });

});
