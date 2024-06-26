document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');

  searchInput.addEventListener('input', function () {
    const value = this.value.toLowerCase();
    const projectRows = document.querySelectorAll('.projectlist thead:not(:first-child)');

    projectRows.forEach(function (row) {
      const projectName = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
      row.style.display = (projectName.indexOf(value) > -1) ? 'table-row' : 'none';
    });
  });

  document.querySelectorAll('.edit').forEach(function(button) {
    button.addEventListener('click', function(event) {
      event.preventDefault();
  
      const menuId = event.target.getAttribute('data-menu-target');
      const menu = document.getElementById(menuId);
  
      const buttonRect = event.target.getBoundingClientRect();
  
      menu.style.left = buttonRect.left + 'px';
      menu.style.top = buttonRect.bottom + 'px';

      if (menu.style.display === 'none') {
        menu.style.display = 'block';
      } else {
        menu.style.display = 'none';
      }
  
      function handleDocumentClick(e) {
        if (!menu.contains(e.target) && e.target !== button) {
          menu.style.display = 'none';
          document.removeEventListener('click', handleDocumentClick);
        }
      }
  
      document.addEventListener('click', handleDocumentClick);
    });
  });

  // delete obj
  document.querySelectorAll('.delete-link').forEach(function(link) {
      link.addEventListener('click', function(e) {
        e.preventDefault();

        document.querySelector('#password-form').style.display = 'block';

        document.querySelector('#delete-form').dataset.testcaseId = this.dataset.testcaseId;
      });
    });

  let input = document.querySelector("#searchInput");
  let arrData = document.getElementsByClassName('name');
  input.addEventListener('input', showChoice);

  function showChoice(event){
  let value = event.target.value.toLowerCase();
  if (value === ""){
      for (let i=0; i<arrData.length; i++){
          let item = arrData[i]
          item.parentElement.style.display = ""
      }
      return
  }
  for (let i=0; i<arrData.length; i++){
      let item = arrData[i]
      if (!item.textContent.toLowerCase().includes(value)) {
          item.parentElement.style.display = "none"
      } else {
          item.parentElement.style.display = ""
      }
  }
  }

});


