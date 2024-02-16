$(document).ready(function() {
    // Show the workoutPage div when the Add Workout button is clicked
    // Hide the modal dialog when the page loads
    $('#addWorkoutModal').modal('hide');

    // Show the modal dialog when the Add Workout button is clicked
    $('#addWorkoutButton').click(function() {
        $('#addWorkoutModal').modal('show');
    });
    // Initialize an object to store selected workouts grouped by muscle group
    var selectedWorkoutsByMuscleGroup = {};

    // Fetch workouts from the server and organize them by muscle group
    $.getJSON("/exercises", function(data) {
        var workoutGroups = {};
    
        // Group workouts by muscle group
        $.each(data, function(index, workout) {
            if (!workoutGroups[workout.muscleGroup]) {
                workoutGroups[workout.muscleGroup] = [];
                // Initialize an empty array for this muscle group
                selectedWorkoutsByMuscleGroup[workout.muscleGroup] = []; 
            }
            workoutGroups[workout.muscleGroup].push(workout);
        });

        // Append workouts grouped by muscle group to the modal list
        var workoutList = $('#workoutList');
        $.each(workoutGroups, function(muscleGroup, workouts) {
            workoutList.append('<h3>' + muscleGroup + '</h3>');
            $.each(workouts, function(index, workout) {
                var listItem = $('<li class="list-group-item"></li>').text(workout.name);
                listItem.data('workout', workout); // Store workout data with the list item
                workoutList.append(listItem);
            });
        });
    });

    // Function to add workout to the workout page
    function add_workout_to_page() {
        // Clear existing workouts on the page
        $('#workoutPage').empty();

        // Append workouts grouped by muscle group with section headers
        $.each(selectedWorkoutsByMuscleGroup, function(muscleGroup, workouts) {
            if (workouts.length > 0) {
                $('#workoutPage').append('<h3>' + muscleGroup + '</h3>');
                $.each(workouts, function(index, workout) {
                    var infoButton = $('<button class="btn btn-sm btn-info info-workout">Exercise'+
                                        ' Info</button>');
                    var removeButton = $('<button class="btn btn-sm btn-danger remove-workout">'+
                    'Remove</button>');
                    // Add space between exercise and button
                    var workoutItem = $('<p></p>').text(workout.name + ' '); 
                    workoutItem.append(infoButton);
                    workoutItem.append(' '); // Add space
                    workoutItem.append(removeButton);
                    workoutItem.append(' '); // Add space
                    infoButton.data('workout', workout); // Store workout data with the info button
                    // Store workout data with the remove button
                    removeButton.data('workout', workout); 
                    $('#workoutPage').append(workoutItem);
                });
            }
        });
    }

    // Handle click event on workout items in the modal list
    $(document).on('click', '#workoutList li', function() {
        var workout = $(this).data('workout');
        var index = selectedWorkoutsByMuscleGroup[workout.muscleGroup].findIndex(function(item) {
            return item.name === workout.name;
        });
        if (index === -1) {
            selectedWorkoutsByMuscleGroup[workout.muscleGroup].push(workout);
        } else {
            selectedWorkoutsByMuscleGroup[workout.muscleGroup].splice(index, 1);
        }
        add_workout_to_page();
    });


    // Define an object to store saved values for each exercise
    var savedExerciseInfo = {};

    // Handle click event on remove buttons
    $(document).on('click', '.remove-workout', function() {
        var workout = $(this).data('workout');
        var muscleGroup = workout.muscleGroup;
        var index = selectedWorkoutsByMuscleGroup[muscleGroup].findIndex(function(item) {
            return item.name === workout.name;
        });
        if (index !== -1) {
            delete savedExerciseInfo[workout.name];
            selectedWorkoutsByMuscleGroup[muscleGroup].splice(index, 1);
        }
        add_workout_to_page(); // Update the workout page after removing the workout
    });

    // Handle click event on info buttons
    $(document).on('click', '.info-workout', function() {
        var workout = $(this).data('workout');
        
        // Create a new modal element
        var modal = $('<div class="modal fade" tabindex="-1" role="dialog"></div>');
        
        // Create modal dialog
        var modalDialog = $('<div class="modal-dialog" role="document"></div>');
        
        // Create modal content
        var modalContent = $('<div class="modal-content"></div>');
        var modalHeader = $('<div class="modal-header"></div>').append('<h5 class="modal-title">' +
                             workout.name + '</h5>');
        var closeButton = $('<button type="button" class="close" data-dismiss="modal" aria-label='+
                            '"Close"><span aria-hidden="true">&times;</span></button>');
        modalHeader.append(closeButton);
        var modalBody = $('<div class="modal-body"></div>');

        // Add input, button, and container to modal body
        var setsInput = $('<input type="number" id="sets" name="sets" value="' +
                             (savedExerciseInfo[workout.name] ?
                                 savedExerciseInfo[workout.name].sets : 1) + '" min="1">');
        var addButton = $('<button type="button" id="modalButton" class="btn btn-primary btn-xs">'+
                            'Confirmed Number of Sets</button>'); // Changed to btn-xs class
        var lineBreak1 = $('<br>'); // First line break element
        var lineBreak2 = $('<br>'); // Second line break element
        var container = $('<div id="container"></div>');

        modalBody.append(setsInput);
        modalBody.append(addButton);
        modalBody.append(lineBreak1); // Append first line break
        modalBody.append(lineBreak2); // Append second line break
        modalBody.append(container);

        modalContent.append(modalHeader, modalBody);
        modalDialog.append(modalContent);
        modal.append(modalDialog);

        // Append modal to the body
        $('body').append(modal);

        // Show the modal
        modal.modal('show');

        // Populate text boxes with saved values
        for (var i = 0; i < (savedExerciseInfo[workout.name] ? 
            savedExerciseInfo[workout.name].sets : 1); i++) {
            var repBox = $('<input type="text" class="form-control mb-2 mr-2" placeholder="Reps' +
             'for set ' + (i+ 1) + '">').val(savedExerciseInfo[workout.name] ?
                 savedExerciseInfo[workout.name].reps[i] || '' : '');
            var weightBox = $('<input type="text" class="form-control mb-2" placeholder="Weight' +
             'for set ' + (i+ 1) + '">').val(savedExerciseInfo[workout.name] ?
                 savedExerciseInfo[workout.name].weights[i] || '' : '');
            var row = $('<div class="row"></div>').append($('<div class="col-md-6">'+
                '</div>').append(repBox), $('<div class="col-md-6"></div>').append(weightBox));
            container.append(row);
        };

        // Handle click event on Add button
        addButton.on('click', function() {
            var sets = parseInt(setsInput.val());
            container.empty(); // Clear existing text boxes
            
            // Create and append pairs of text boxes for each set
            for (var i = 0; i < sets; i++) {
                var repBox = $('<input type="text" class="form-control mb-2 mr-2"' +
                'placeholder="Reps for set ' + (i+ 1) + '">').val(savedExerciseInfo[workout.name] ?
                     savedExerciseInfo[workout.name].reps[i] || '' : '');
                var weightBox = $('<input type="text" class="form-control mb-2" placeholder='+
                '"Weight for set ' + (i+ 1) + '">').val(savedExerciseInfo[workout.name] ?
                     savedExerciseInfo[workout.name].weights[i] || '' : '');
                var row = $('<div class="row"></div>').append($('<div class="col-md-6">'+
                    '</div>').append(repBox), $('<div class="col-md-6"></div>').append(weightBox));
                container.append(row);
            }
        });

        // Add close and submit buttons outside the Add button click event handler
        var submitButton = $('<button type="button" class="btn btn-primary">'+
                             'Submit</button>').on('click', function() {
            // Save the values
            savedExerciseInfo[workout.name] = {
                sets: setsInput.val(),
                reps: [],
                weights: []
            };
            container.find('input[type="text"]').each(function(index) {
                if (index % 2 === 0) {
                    savedExerciseInfo[workout.name].reps.push($(this).val());
                } else {
                    savedExerciseInfo[workout.name].weights.push($(this).val());
                }
            });
            modal.modal('hide');
            // Additional logic for submission if needed
        });

        var buttonsDiv = $('<div class="text-right"></div>').append(submitButton);
        modalBody.append(buttonsDiv);
    });
});
