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
    console.log(data);
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });


function updateElements() {
      const container = document.getElementById('form');

      if (window.innerWidth < 420) {
        container.innerHTML = `
          <input id="staffInput" type="text" autofocus placeholder="Enter staff name" autocomplete="off" class="form-control d-inline w-auto" size="15">
          <button id="submitButton" class="btn btn-primary" style="padding: 5px 10px; font-size: 10px; background-color: #008fa0; border: none;">Submit</button>
        `;
      } else {
        container.innerHTML = `
          <input id="staffInput" type="text" autofocus placeholder="Enter staff name" autocomplete="off" class="form-control d-inline w-auto">
          <button id="submitButton" class="btn btn-primary" style="background-color: #008fa0; border: none;">Submit</button>
        `;
      }
    }

    document.addEventListener('DOMContentLoaded', updateElements);
    window.addEventListener('resize', updateElements);


let dropdownItems = document.querySelectorAll('.dropdown-item');
let dropdownButton = document.getElementById('dropdownMenuButton');


dropdownItems.forEach(item => {
  item.addEventListener('click', function() {
      dropdownButton.innerHTML = '&nbsp;&nbsp;' + this.textContent + '&nbsp;&nbsp;';
  });
});

