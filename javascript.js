//https://chatgpt.com/share/1fd464af-c160-4858-9183-17b8eab367b7
//Mdm Miss Mr Mrs Ms
//run localhost first using "python: -m http.server"
//the visit http://localhost:8000 python


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

document.addEventListener('DOMContentLoaded', function() {
    let dropdownItems = document.querySelectorAll('.dropdown-item');
    let dropdownButton = document.getElementById('dropdownMenuButton');

    TitleBeingSet = false;

    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            selectedTitle = this.textContent.trim();
            dropdownButton.innerHTML = '&nbsp;&nbsp;' + selectedTitle + '&nbsp;&nbsp;';
            TitleBeingSet = true;
        });
    });
});

fetch('all_teachers_info.json')
    .then(response => response.json())
    .then(data => {
        document.getElementById('submitButton').addEventListener('click', function(event) {
            event.preventDefault();
            const inputName = document.getElementById('staffInput').value.trim().toLowerCase();

            if (!TitleBeingSet) {
                selectedTitle = "ALL"
                let dropdownButton = document.getElementById('dropdownMenuButton');
                dropdownButton.innerHTML = '&nbsp;&nbsp;' + selectedTitle + '&nbsp;&nbsp;';
            }

            const filteredTeachers = filterTeachers(data, inputName, selectedTitle);
            updateTable(filteredTeachers);
        });
    })
    .catch(error => {
        console.error('Error fetching teacher data:', error);
    });

fetch('timestamp.json')
.then(response => response.json())
.then(data => {
    let timestamp = document.getElementById('timestamp');
    timestamp.innerHTML = 'Namelist Last updated: ' + data;

    let table_div = document.getElementById('table-div');
    timestamp.style.marginLeft = getComputedStyle(table_div).marginLeft

})

function filterTeachers(teachersData, inputName, selectedTitle) {
    const filtered = [];
    const nameRegex = new RegExp(`[a-zA-Z]*${inputName}[a-zA-Z]*`, 'i');

    for (let name in teachersData) {
        const [designation, email] = teachersData[name];
        if (nameRegex.test(name)) {
            if (selectedTitle === 'ALL' || name.startsWith(selectedTitle)) {
                filtered.push({ name, designation, email });
            }
        }
    }
    return filtered;
}

function updateTable(filteredTeachers) {
    const tbody = document.querySelector('table tbody');
    tbody.innerHTML = '';

    filteredTeachers.sort((a, b) => a.name.localeCompare(b.name));

    filteredTeachers.forEach(teacher => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${teacher.name}</td>
            <td>${teacher.designation}</td>
            <td><a href="mailto:${teacher.email}" style='color: #EB8100; font-weight: 900'>${teacher.email}</a></td>
        `;
        tbody.appendChild(row);
    });

    if (filteredTeachers.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `<td colspan="3">No teachers found.</td>`;
        tbody.appendChild(row);
    }

    if (filteredTeachers.length > 7) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="3"> </td>';
        tbody.appendChild(row);
    }
}

function update_time(){
    let timestamp = document.getElementById('timestamp');
    let table_div = document.getElementById('table-div');
    timestamp.style.marginLeft = getComputedStyle(table_div).marginLeft;
}

window.addEventListener('resize', update_time);

 