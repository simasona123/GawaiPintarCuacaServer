var formDiv = document.querySelector(".formItem");
var submit = document.querySelector("#submit");
console.log(submit);
var pilihan = () => {
    var i = document.querySelector("#pilihan").value;
    document.querySelector("form").style.display = 'block';
    if (i == 1) {
        formDiv.innerHTML = form;
        submit.style.display = "block";
        document.querySelector("#download1").style.display = 'none';
        window.scrollTo(0, document.body.scrollHeight);
    }
    else {
        document.querySelector("form").style.display = 'none';
        document.querySelector("#download1").style.display = 'block';
        window.scrollTo(0, document.body.scrollHeight);
    }
}