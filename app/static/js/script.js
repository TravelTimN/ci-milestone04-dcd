$(document).ready(function () {

    // add today into hidden input field for database
    let now = new Date();
    let date = now.getDate();
    let month = new Array();
    month[0] = "January";
    month[1] = "February";
    month[2] = "March";
    month[3] = "April";
    month[4] = "May";
    month[5] = "June";
    month[6] = "July";
    month[7] = "August";
    month[8] = "September";
    month[9] = "October";
    month[10] = "November";
    month[11] = "December";
    let monthName = month[now.getMonth()];
    let year = now.getFullYear();
    if (date < 10) {
        date = "0" + date;
    }
    let today = date + " " + monthName + ", " + year;
    $("#date_added").val(today);

});