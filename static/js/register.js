let form = document.querySelector(".quiz-form");
let submitBtn = document.querySelector('.send-otp-btn');
let formSubmitBtn = document.querySelector(".quiz-form-submit-btn");
let phoneNumberInput = document.querySelector("input[name='phone-number']");
let otpInput = document.createElement("input");
otpInput.setAttribute("name", "otp-code")
otpInput.setAttribute("placeholder", "کد تایید ارسال شده...")
otpInput.setAttribute("id", "otp-code")
otpInput.classList.add("form-control")
let otpLabel = document.querySelector("#otp-code-label")

submitBtn.addEventListener("click", (event) => {
    event.preventDefault();
    $body = $("body");
    $(document).ajaxStart(function () {
        $body.addClass("loading");
    });
    $(document).ajaxStop(function () {
        $body.removeClass("loading");
    })
    if (form.hasAttribute("sent")) {
        let formData = new FormData();
        formData.append("phone-number", phoneNumberInput.value)
        formData.append("otp-code", otpInput.value)
        formData.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value)
        $.ajax({
            async: true,
            type: "post",
            url: "/quiz/submit-phone-number/",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (res) {
                if (res.status === 'success') {
                    showNotification(res, "موفق")
                    otpInput.setAttribute("disabled", "")
                    submitBtn.setAttribute("disabled", "")
                    submitBtn.classList.add("disabled-otp-btn")
                    submitBtn.innerText = "تایید شده";
                    formSubmitBtn.classList.remove("disabled-otp-btn")
                    formSubmitBtn.removeAttribute("disabled")
                } else {
                    showNotification(res, "شکست")
                }
            },
            error: function (request, status, error) {
                console.log(error)
            }
        });
    } else {
        let formData = new FormData();
        formData.append("phone-number", phoneNumberInput.value)
        formData.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value)
        $.ajax({
            async: true,
            type: "post",
            url: "/quiz/send-otp/",
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            success: function (res) {
                if (res.status === 'success') {
                    phoneNumberInput.setAttribute("disabled", "");
                    otpLabel.style.display = "block";
                    otpLabel.parentNode.insertBefore(otpInput, otpLabel.nextSibling);
                    submitBtn.innerText = "تایید کد ارسال شده";
                    form.setAttribute("sent", "")
                } else {
                    showNotification(res, "شکست")
                }
            },
            error: function (request, status, error) {
                console.log(error)
            }
        });
    }
})