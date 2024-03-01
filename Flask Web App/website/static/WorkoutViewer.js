// JavaScript to handle starting workout
document.addEventListener('DOMContentLoaded', function() {
    const startButtons = document.querySelectorAll('.start-workout-btn');
    startButtons.forEach(button => {
        button.addEventListener('click', function() {
            const workoutName = this.dataset.workout;
            const workoutData = JSON.parse(this.dataset.workoutData);

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
                    // window.location.href = '/WorkoutPage';
                },
                error: function(xhr, status, error) {
                    // Handle error response from the server if needed
                    window.location.href = '/WorkoutPage';
                    console.error('Error sending workout data:', error);
                }
            });
        });
    });
});