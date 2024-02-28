$(document).ready(function() {
    // Convert preSelectedExercises from string to array of strings
    preSelectedExercises = JSON.parse(preSelectedExercises.replace(/'/g, '"'));

    // Show the workoutPage div when the Add Exercise button is clicked
    // Hide the modal dialog when the page loads
    $('#addExerciseModal').modal('hide');

    // Show the modal dialog when the Add Exercise button is clicked
    $('#addExerciseButton').click(function() {
        $('#addExerciseModal').modal('show');
    });
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
            for (let i = 0; i < preSelectedExercises.length; i++) {
                if (preSelectedExercises[i] == exercise.name) {
                    if (!selectedExercisesByMuscleGroup[exercise.muscleGroup].some(item => item.name === exercise.name)) {
                        selectedExercisesByMuscleGroup[exercise.muscleGroup].push(exercise);
                    }
                }
            };
            exerciseGroups[exercise.muscleGroup].push(exercise);
        });
        add_exercise_to_page()

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
        for (var i = 0; i < (savedExerciseInfo[exercise.name] ? 
            savedExerciseInfo[exercise.name].sets : 1); i++) {
            var repBox = $('<input type="text" class="form-control mb-2 mr-2" placeholder="Reps' +
             'for set ' + (i+ 1) + '">').val(savedExerciseInfo[exercise.name] ?
                 savedExerciseInfo[exercise.name].reps[i] || '' : '');
            var weightBox = $('<input type="text" class="form-control mb-2" placeholder="Weight' +
             'for set ' + (i+ 1) + '">').val(savedExerciseInfo[exercise.name] ?
                 savedExerciseInfo[exercise.name].weights[i] || '' : '');
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
                'placeholder="Reps for set ' + (i+ 1) + '">').val(savedExerciseInfo[exercise.name] ?
                     savedExerciseInfo[exercise.name].reps[i] || '' : '');
                var weightBox = $('<input type="text" class="form-control mb-2" placeholder='+
                '"Weight for set ' + (i+ 1) + '">').val(savedExerciseInfo[exercise.name] ?
                     savedExerciseInfo[exercise.name].weights[i] || '' : '');
                var row = $('<div class="row"></div>').append($('<div class="col-md-6">'+
                    '</div>').append(repBox), $('<div class="col-md-6"></div>').append(weightBox));
                container.append(row);
            }
        });

        // Add close and submit buttons outside the Add button click event handler
        var submitButton = $('<button type="button" class="btn btn-primary">'+
                             'Submit</button>').on('click', function() {
            // Save the values
            savedExerciseInfo[exercise.name] = {
                sets: setsInput.val(),
                reps: [],
                weights: []
            };
            container.find('input[type="text"]').each(function(index) {
                if (index % 2 === 0) {
                    savedExerciseInfo[exercise.name].reps.push($(this).val());
                } else {
                    savedExerciseInfo[exercise.name].weights.push($(this).val());
                }
            });
            modal.modal('hide');
            // Additional logic for submission if needed
        });

        var buttonsDiv = $('<div class="text-right"></div>').append(submitButton);
        modalBody.append(buttonsDiv);
    });
});
