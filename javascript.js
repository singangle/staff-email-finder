//https://chatgpt.com/share/1fd464af-c160-4858-9183-17b8eab367b7
//Mdm Miss Mr Mrs Ms
//run localhost first using python: -m http.server
//the visit http://localhost:8000 python


fetch('all_teachers_info.json')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
  })
  .then(data => {
    console.log(data); // The JSON data will be available here
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });


function updateElements() {
      const container = document.getElementById('form');

      if (window.innerWidth < 420) {
        // Use innerHTML to update the input and button elements
        container.innerHTML = `
          <input id="staffInput" type="text" autofocus placeholder="Enter staff name" autocomplete="off" class="form-control d-inline w-auto" size="15">
          <button id="submitButton" class="btn btn-primary" style="padding: 5px 10px; font-size: 10px; background-color: #008fa0; border: none;">Submit</button>
        `;
      } else {
        // Revert the innerHTML back to the default (larger screen) state
        container.innerHTML = `
          <input id="staffInput" type="text" autofocus placeholder="Enter staff name" autocomplete="off" class="form-control d-inline w-auto">
          <button id="submitButton" class="btn btn-primary" style="background-color: #008fa0; border: none;">Submit</button>
        `;
      }
    }

    // Run the function when the DOM is fully loaded
    document.addEventListener('DOMContentLoaded', updateElements);

    // Add event listener to handle window resizing
    window.addEventListener('resize', updateElements);


