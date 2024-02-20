document.addEventListener("DOMContentLoaded", function() {
    var today = new Date();
    var monthElement = document.getElementById("monthElement");
    var yearElement = document.getElementById("yearElement");
    var calendarElement = document.getElementById("calendarElement");
    var selectedYear;
    var selectedMonth;
    var selectedDate;

    for (let i = 0; i < 12; i++) {
        let optionElement = document.createElement("option");
        optionElement.value = i;
        optionElement.text = new Date(today.getFullYear(), i, 1).toLocaleString('default', { month: 'long' });
        if (i === today.getMonth()) {
            optionElement.selected = true;
        }
        monthElement.add(optionElement);
    }

    for (let i = today.getFullYear() - 10; i <= today.getFullYear() + 10; i++) {
        let optionElement = document.createElement("option");
        optionElement.value = i;
        optionElement.text = i;
        if (i === today.getFullYear()) {
            optionElement.selected = true;
        }
        yearElement.add(optionElement);
    }

    function load_calendar() {
        selectedMonth = monthElement.value;
        selectedYear = yearElement.value;
        var month = monthElement.value;
        var year = yearElement.value;
        var firstDay = (new Date(year, month)).getDay();
        var daysInMonth = 32 - new Date(year, month, 32).getDate();
        var date = 1;
    
        // Get all the rows in the calendar
        let rows = calendarElement.getElementsByTagName("tr");
    
        // Delete all rows except for the first one (the header row)
        for (let i = rows.length - 1; i > 0; i--) {
            calendarElement.deleteRow(i);
        }
    
        for (let i = 0; i < 6; i++) {
            var rowElement = document.createElement("tr");
    
            for (let j = 0; j < 7; j++) {
                if (i === 0 && j < firstDay) {
                    let cellElement = document.createElement("td");
                    let cellText = document.createTextNode("");
                    cellElement.appendChild(cellText);
                    rowElement.appendChild(cellElement);
                } else if (date > daysInMonth) {
                    break;
                } else {
                    let cellElement = document.createElement("td");
                    cellElement.id = date;
                    let cellText = document.createTextNode(date);
                    if (date === today.getDate() && year == today.getFullYear() && month == today.getMonth()) {
                        cellElement.classList.add("bgInfo");
                    }
                    cellElement.appendChild(cellText);
                    rowElement.appendChild(cellElement);
                    date++;
                }
            }
            calendarElement.appendChild(rowElement);
        }
    }

    load_calendar();

    monthElement.addEventListener("change", load_calendar);
    yearElement.addEventListener("change", load_calendar);

    // Fetch exercises when the page loads
    console.log("Fetching exercises");
    fetch('/exercises')
        .then(response => response.json())
        .then(data => {
            console.log("Exercises fetched", data);
            let selectElement = document.getElementById('exercisesDropdown');
            data.forEach(exercise => {
                let optionElement = document.createElement('option');
                optionElement.value = exercise.name;
                optionElement.text = exercise.name;
                selectElement.add(optionElement);
            });
        });
    

    $("#calendarElement").on("click", "td", function() {
        var selectedExercise = $("#exercisesDropdown").val();
        var selectedDate = $(this).text();
        var date = new Date(selectedYear, selectedMonth, selectedDate);
        var formattedDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        $("#selectedDate").text(formattedDate + ", Exercise: " + selectedExercise);
    });
});
