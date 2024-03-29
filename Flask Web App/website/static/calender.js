document.addEventListener("DOMContentLoaded", function() {
    var today = new Date();
    var monthElement = document.getElementById("monthElement");
    var yearElement = document.getElementById("yearElement");
    var calendarElement = document.getElementById("calendarElement");
    var selectedYear;
    var selectedMonth;
    var selectedDate;
    var selectedExercise;

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

    console.log("Fetching workout names");
    fetch('/workout_names')
        .then(response => response.json())
        .then(workoutNames => {
            console.log("Workout names fetched", workoutNames);
            let selectElement = document.getElementById('workoutDropdown');
            workoutNames.forEach(workoutName => {
                let optionElement = document.createElement('option');
                optionElement.value = workoutName;
                optionElement.text = workoutName;
                selectElement.add(optionElement);
            });
        });

        function fetch_and_display_workouts(date) {
            $.get('/get_scheduled_workouts', {date: date}, function(workout_names) {
                var workoutsContainer = document.getElementById('workoutsContainer');
                workoutsContainer.innerHTML = '';
                workout_names.forEach(function(workout_name) {
                    var p = document.createElement('p');
                    p.textContent = 'You currently have "' + workout_name + '" scheduled for this date';
                    workoutsContainer.appendChild(p);
                });
            });
        }
        
        
        $(document).on("click", "#calendarElement td", function() {
            $("#calendarElement td").removeClass("bgInfo");
            $(this).addClass("bgInfo");
        
            selectedDate = $(this).text();
            selectedExercise = $("#workoutDropdown").val();
        
            var date = new Date(selectedYear, selectedMonth, selectedDate);
            var formattedDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        
            fetch_and_display_workouts(formattedDate);
        });

        $(document).on("click", "#calendarElement td", function() {
            $("#calendarElement td").removeClass("bgInfo");
            $(this).addClass("bgInfo");
        
            selectedDate = $(this).text();
            selectedExercise = $("#workoutDropdown").val();
        
            var date = new Date(selectedYear, selectedMonth, selectedDate);
            var formattedDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        
            fetch_and_display_workouts(formattedDate);
        });

    $(document).on("click", "#scheduleWorkoutButton", function() {
        var date = new Date(selectedYear, selectedMonth, selectedDate);
        var formattedDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    
        var workoutData = {
            date: formattedDate,
            workoutName: selectedExercise,
        };
    
        $.ajax({
            type: 'POST',
            url: '/save_scheduled_workout',
            contentType: 'application/json',
            data: JSON.stringify({ workoutData: workoutData }),
            success: function(response) {
                // Handle success response from the server if needed
                console.log('Scheduled workout data sent successfully.');
            },
            error: function(xhr, status, error) {
                // Handle error response from the server if needed
                console.error('Error sending scheduled workout data:', error);
                alert('' + xhr.responseText);
            }
        });
        
    
        $("#selectedDate").text(formattedDate + ", Exercise: " + selectedExercise);
    });
    
});
