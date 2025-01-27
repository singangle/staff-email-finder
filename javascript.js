//Hello there! This website is developed by Anderson in October 2024!

function updateElements() {
        let button = document.getElementById('submitButton');
        let inputBox = document.getElementById('staffInput');
        let inputBoxShrink = false

        if (window.innerWidth < 420) {
            button.style.padding = "5px 10px";
            button.style.fontSize = "10px";
        } 

        if (window.innerWidth < 380) {
            inputBoxShrink = true
        }
        else {
            inputBoxShrink = false
        }

        if (inputBoxShrink) {
            inputBox.setAttribute("size", "12")
        }
        else {
            inputBox.setAttribute("size", "15")
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

fetch('json/all_teachers_info.json')
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

fetch('json/timestamp.json')
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

    // for (let name in teachersData) {
    //     const [designation, email] = teachersData[name];
    //     if (nameRegex.test(name)) {
    //         if (selectedTitle === 'ALL' || name.startsWith(selectedTitle)) {
    //             filtered.push({ name, designation, email });
    //         }
    //     }
    // }
    // return filtered;  (this is old logic of 2024. The structure of all_teachers_info has changed. 2025.1.27)

    for (let designation in teachersData) {
        const [name, email] = teachersData[designation];
        if (nameRegex.test(name.replace(/^\w+\s/, ''))) {
            if (selectedTitle === 'ALL' || name.startsWith(selectedTitle)) {
                filtered.push({ designation, name, email });
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

document.getElementById('staffInput').addEventListener('click', function() {
    setTimeout(() => {
        this.focus();
    }, 100);
});
