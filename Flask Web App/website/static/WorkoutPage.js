$(document).ready(function() {
    console.log(preSelectedExercises)
    if (preSelectedExercises != null){
        preSelectedExercises = JSON.parse(preSelectedExercises.replace(/'/g, '"'));
    }
    // Show the workoutPage div when the Add Exercise button is clicked
    // Hide the modal dialog when the page loads
    $('#addExerciseModal').modal('hide');

    // Show the modal dialog when the Add Exercise button is clicked
    $('#addExerciseButton').click(function() {
        $('#addExerciseModal').modal('show');
    });

    // Hide the modal dialog when the Close button is clicked
    toggle_submit_button(); // Enable or disable submit button based on the number of exercises
    
    // Initialize an object to store selected exercises grouped by muscle group
    var selectedExercisesByMuscleGroup = {};

    // Fetch exercises from the server and organize them by muscle group
    $.getJSON("/exercises", function(data) {
        var exerciseGroups = {};
    
        // Group exercises by muscle group
        $.each(data, function(index, exercise) {
            if (!exerciseGroups[exercise.muscleGroup]) {
                exerciseGroups[exercise.muscleGroup] = [];
                // Initialize an empty array for this muscle group
                selectedExercisesByMuscleGroup[exercise.muscleGroup] = []; 
            }
            if(preSelectedExercises != null){
                for (let i = 0; i < preSelectedExercises.length; i++) {
                    if (preSelectedExercises[i] == exercise.name) {
                        if (!selectedExercisesByMuscleGroup[exercise.muscleGroup].some(item => item.name === exercise.name)) {
                            selectedExercisesByMuscleGroup[exercise.muscleGroup].push(exercise);
                        }
                    }
                }
            }
            exerciseGroups[exercise.muscleGroup].push(exercise);
        });
        if(preSelectedExercises != null){
            add_exercise_to_page()
        }

        // Append exercises grouped by muscle group to the modal list
        var exerciseList = $('#exerciseList');
        $.each(exerciseGroups, function(muscleGroup, exercises) {
            exerciseList.append('<h3>' + muscleGroup + '</h3>');
            $.each(exercises, function(index, exercise) {
                var listItem = $('<li class="list-group-item"></li>').text(exercise.name);
                listItem.data('exercise', exercise); // Store exercise data with the list item
                exerciseList.append(listItem);
            });
        });
    });

    // Function to enable or disable submit button based on the number of exercises
    function toggle_submit_button() {
        var numExercises = $('#workoutPage').children().length;
        if (numExercises > 0) {
            $('#submitWorkoutButton').prop('disabled', false); // Corrected selector
        } else {
            $('#submitWorkoutButton').prop('disabled', true); // Corrected selector
        }
    }

    // Function to add exercise to the workout page
    function add_exercise_to_page() {
        // Clear existing exercises on the page
        $('#workoutPage').empty();

        // Append exercises grouped by muscle group with section headers
        $.each(selectedExercisesByMuscleGroup, function(muscleGroup, exercises) {
            if (exercises.length > 0) {
                $('#workoutPage').append('<h3>' + muscleGroup + '</h3>');
                $.each(exercises, function(index, exercise) {
                    var infoButton = $('<button class="btn btn-sm btn-info info-exercise">Exercise'+
                                        ' Info</button>');
                    var removeButton = $('<button class="btn btn-sm btn-danger remove-exercise">'+
                    'Remove</button>');
                    // Add space between exercise and button
                    var exerciseItem = $('<p></p>').text(exercise.name + ' '); 
                    exerciseItem.append(infoButton);
                    exerciseItem.append(' '); // Add space
                    exerciseItem.append(removeButton);
                    exerciseItem.append(' '); // Add space
                    // Store exercise data with the info button
                    infoButton.data('exercise', exercise); 
                    // Store exercise data with the remove button
                    removeButton.data('exercise', exercise); 
                    $('#workoutPage').append(exerciseItem);
                });
            }
        });
        toggle_submit_button(); // Enable or disable submit button based on the number of exercises
    }

    // Handle click event on exercise items in the modal list
    $(document).on('click', '#exerciseList li', function() {
        var exercise = $(this).data('exercise');
        var index = selectedExercisesByMuscleGroup[exercise.muscleGroup].findIndex(function(item) {
            return item.name === exercise.name;
        });
        if (index === -1) {
            selectedExercisesByMuscleGroup[exercise.muscleGroup].push(exercise);
        } else {
            selectedExercisesByMuscleGroup[exercise.muscleGroup].splice(index, 1);
        }
        add_exercise_to_page();
    });


    // Define an object to store saved values for each exercise
    var savedExerciseInfo = {};

    // Handle click event on remove buttons
    $(document).on('click', '.remove-exercise', function() {
        var exercise = $(this).data('exercise');
        var muscleGroup = exercise.muscleGroup;
        var index = selectedExercisesByMuscleGroup[muscleGroup].findIndex(function(item) {
            return item.name === exercise.name;
        });
        if (index !== -1) {
            delete savedExerciseInfo[exercise.name];
            selectedExercisesByMuscleGroup[muscleGroup].splice(index, 1);
        }
        add_exercise_to_page(); // Update the workout page after removing the exercise
        toggle_submit_button(); // Enable or disable submit button based on the number of exercises
    });

    // Handle click event on info buttons
    $(document).on('click', '.info-exercise', function() {
        var exercise = $(this).data('exercise');
        
        // Create a new modal element
        var modal = $('<div class="modal fade" tabindex="-1" role="dialog"></div>');
        
        // Create modal dialog
        var modalDialog = $('<div class="modal-dialog" role="document"></div>');
        
        // Create modal content
        var modalContent = $('<div class="modal-content"></div>');
        var modalHeader = $('<div class="modal-header"></div>').append('<h5 class="modal-title">' +
                             exercise.name + '</h5>');
        var closeButton = $('<button type="button" class="close" data-dismiss="modal" aria-label='+
                            '"Close"><span aria-hidden="true">&times;</span></button>');
        modalHeader.append(closeButton);
        var modalBody = $('<div class="modal-body"></div>');

        // Add input, button, and container to modal body
        var setsInput = $('<input type="number" id="sets" name="sets" value="' +
                             (savedExerciseInfo[exercise.name] ?
                                 savedExerciseInfo[exercise.name].sets : 1) + '" min="1">');
        var confirmButton = $('<button type="button" id="modalButton" class="btn btn-primary btn-xs">'+
                            'Confirm</button>'); // Changed to btn-xs class
        var lineBreak1 = $('<br>'); // First line break element
        var lineBreak2 = $('<br>'); // Second line break element
        var container = $('<div id="container"></div>');

        modalBody.append(setsInput);
        modalBody.append(lineBreak1); // Append first line break
        modalBody.append(lineBreak2); // Append second line break
        modalBody.append(container);
        modalBody.append(confirmButton);

        modalContent.append(modalHeader, modalBody);
        modalDialog.append(modalContent);
        modal.append(modalDialog);

        // Append modal to the body
        $('body').append(modal);

        // Show the modal
        modal.modal('show');

        // Function to update number of reps and weights inputs based on sets
        function update_inputs(sets) {
            container.empty(); // Clear existing inputs
            
            for (var i = 0; i < sets; i++) {
                var repBox = $('<input type="text" class="form-control mb-2 mr-2" placeholder="Reps' +
                                ' for set ' + (i + 1) + '">');
                var weightBox = $('<input type="text" class="form-control mb-2" placeholder="Weight' +
                                    ' for set ' + (i + 1) + '">');
            
                // Restrict user input to only numeric values
                repBox.on('input', function() {
                    this.value = this.value.replace(/[^0-9]/g, '');
                });
                weightBox.on('input', function() {
                    this.value = this.value.replace(/[^0-9]/g, '');
                });
            
                var row = $('<div class="row"></div>').append($('<div class="col-md-6">'+
                                '</div>').append(repBox), $('<div class="col-md-6"></div>').append(weightBox));
                container.append(row);
            }

            // Display stored values if available
            if (savedExerciseInfo[exercise.name]) {
                var reps = savedExerciseInfo[exercise.name].reps;
                var weights = savedExerciseInfo[exercise.name].weights;

                // Update rep and weight inputs with stored values
                container.find('input[type="text"]').each(function(index) {
                    if (index % 2 === 0) {
                        $(this).val(reps[index / 2] || '');
                    } else {
                        $(this).val(weights[(index - 1) / 2] || '');
                    }
                });
            }
        }

        // Handle click event on confirm button
        confirmButton.on('click', function() {
            var sets = parseInt(setsInput.val());
            var reps = [];
            var weights = [];

            // Collect reps and weights values
            container.find('input[type="text"]').each(function(index) {
                if (index % 2 === 0) {
                    reps.push($(this).val());
                } else {
                    weights.push($(this).val());
                }
            });

            // Store data in savedExerciseInfo object
            savedExerciseInfo[exercise.name] = {
                sets: sets,
                reps: reps,
                weights: weights
            };

            // Close the modal
            modal.modal('hide');
        });

        // Handle input change event on sets input
        setsInput.on('input', function() {
            var sets = parseInt($(this).val());
            update_inputs(sets);
        });

        var initialSets = parseInt(setsInput.val());
        update_inputs(initialSets);

        // Checks if preselectedInfo is not null and if the exercise is in the preselectedInfo has been loaded already
        if (preselectedInfo[exercise.name] != null && !preselectedInfo[exercise.name].loaded) {
            // Set the value of setsInput to true
            preselectedInfo[exercise.name].loaded = true;
            // Define the new value for setsInput
            var newSetsValue = preselectedInfo[exercise.name].sets;

            // Set the value of setsInput
            setsInput.val(newSetsValue);

            // Store data in savedExerciseInfo object
            savedExerciseInfo[exercise.name] = {
                sets: newSetsValue,
                reps: preselectedInfo[exercise.name].reps,
                weights: preselectedInfo[exercise.name].weights
            };
            
            // Trigger the 'input' event to ensure the event handler function runs
            setsInput.trigger('input');
        }

    });
    

    // Handle click event on submit workout button
    $('#submitWorkoutButton').click(function() {
        // Get the workout name value
        var workoutName = $('#workoutName').val().trim();

        // Validate workout name
        if (workoutName === '') {
            $('#workoutNameError').show(); // Show error message
            return; // Prevent submission
        }

        // Check if workoutName already exists in workoutNames
        if (workoutNames.includes(workoutName)) {
            $('#workoutNameExistsError').show(); // Show error message
            return; // Prevent submission
        }


        // Clear error message if validation passed
        $('#workoutNameError').hide();
        $('#workoutNameExistsError').hide();

        var workoutName = $('#workoutName').val(); // Get the workout name from the input field
        var workoutData = {
            name: workoutName,
            exercises: []
        };

        // Iterate over savedExerciseInfo and add each exercise to workoutData
        $.each(savedExerciseInfo, function(exerciseName, exerciseInfo) {
            var exerciseData = {
                name: exerciseName,
                sets: exerciseInfo.sets,
                reps: exerciseInfo.reps,
                weights: exerciseInfo.weights
            };
            workoutData.exercises.push(exerciseData);
        });

        // Send workoutData to Flask endpoint
        $.ajax({
            type: 'POST',
            url: '/save_workout',
            contentType: 'application/json',
            data: JSON.stringify({ workoutData: workoutData }),
            success: function(response) {
                // Handle success response from the server if needed
                console.log('Workout data sent successfully.');
                // Redirect to home.html
                window.location.href = '/';
            },
            error: function(xhr, status, error) {
                // Handle error response from the server if needed
                console.error('Error sending workout data:', error);
            }
        });
    });
});
