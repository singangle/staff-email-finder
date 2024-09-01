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