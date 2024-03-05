// JavaScript to handle starting workout
document.addEventListener('DOMContentLoaded', function() {
    const startButtons = document.querySelectorAll('.start-workout-btn');
    startButtons.forEach(button => {
        button.addEventListener('click', function() {
            const workoutName = this.dataset.workout;
            const workoutData = JSON.parse(this.dataset.workoutData);

            // Initialize an empty array to store exercise names
            var exerciseNames = [];

            // Extract exercise names from workoutData and append to exerciseNames array
            workoutData.exercises.forEach(function(exercise) {
                exerciseNames.push(exercise.name);
            });

            $.ajax({
                type: 'POST',
                url: '/save_workout_data',  // Use the new route for saving workout data
                contentType: 'application/json',
                data: JSON.stringify({ workoutName: workoutName, workoutData: workoutData }),
                success: function(response) {
                    // Handle success response from the server if needed
                    console.log('Workout data sent successfully.');
                    console.log('Server response:', response);
                    // Perform any additional actions as needed
                    // Redirect to the process_workout_data route
                    window.location.href = '/save_workout_data';
                },
                error: function(xhr, status, error) {
                    console.error('Error sending workout data:', error);
                }
            });
        });
    });
});