function deleteNote(noteId){ //This function takes the note id we passed
    fetch('/delete-note', { //and sends a note request to the delete-note endpoint 
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res)=> {
        windows.location.href = '/'; //when the above gets a response, we reload the window here
    });
}
