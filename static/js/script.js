function showNotification(res, status) {
    Swal.fire({
        // `${status}`,
        // `${res.message}`,
        // `${res.status}`,
        title: status,
        text: res.message,
        icon: res.status,
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'باشه'
    }).then(result => {
        if (result.isConfirmed) {
            if (res.callBack) {
                res.callBack()
            }
        }
    });
}

var dp = new HaDateTimePicker("#datetime", {
    isSolar: true,
    disableTime: true,
    resultFormat: '{year}-{month}-{day}',
});
$('#datetime').click(function () {
    dp.show()
})