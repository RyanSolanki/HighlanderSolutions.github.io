document.addEventListener("DOMContentLoaded", function() {
    var today = new Date();
    var monthElement = document.getElementById("month");
    var yearElement = document.getElementById("year");
    var calendar = document.getElementById("calendar");
    var selectedYear;
    var selectedMonth;
    var selectedDate;

    for (let i = 0; i < 12; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.text = new Date(today.getFullYear(), i, 1).toLocaleString('default', { month: 'long' });
        if (i === today.getMonth()) {
            option.selected = true;
        }
        monthElement.add(option);
    }

    for (let i = today.getFullYear() - 10; i <= today.getFullYear() + 10; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.text = i;
        if (i === today.getFullYear()) {
            option.selected = true;
        }
        yearElement.add(option);
    }

    function loadCalendar() {
        selectedMonth = monthElement.value;
        selectedYear = yearElement.value;
        var month = monthElement.value;
        var year = yearElement.value;
        var firstDay = (new Date(year, month)).getDay();
        var daysInMonth = 32 - new Date(year, month, 32).getDate();
        var date = 1;
        calendar.innerHTML = "";

        for (let i = 0; i < 6; i++) {
            var row = document.createElement("tr");

            for (let j = 0; j < 7; j++) {
                if (i === 0 && j < firstDay) {
                    let cell = document.createElement("td");
                    let cellText = document.createTextNode("");
                    cell.appendChild(cellText);
                    row.appendChild(cell);
                } else if (date > daysInMonth) {
                    break;
                } else {
                    let cell = document.createElement("td");
                    cell.id = date;
                    let cellText = document.createTextNode(date);
                    if (date === today.getDate() && year == today.getFullYear() && month == today.getMonth()) {
                        cell.classList.add("bg-info");
                    }
                    cell.appendChild(cellText);
                    row.appendChild(cell);
                    date++;
                }
            }
            calendar.appendChild(row);
        }
    }

    loadCalendar();

    monthElement.addEventListener("change", loadCalendar);
    yearElement.addEventListener("change", loadCalendar);

    $("#calendar").on("click", "td", function() {
        var selectedExercise = $("#exercises").val();
        var selectedDate = $(this).text(); // get the text of the clicked cell
        var date = new Date(selectedYear, selectedMonth, selectedDate);
        var formattedDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        $("#selected-date").text(formattedDate + ", Exercise: " + selectedExercise);
    });
});
