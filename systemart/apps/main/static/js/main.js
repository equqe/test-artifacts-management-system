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
document.addEventListener('DOMContentLoaded', function() {
  var deleteLinks = document.querySelectorAll('.delete-link');
  deleteLinks.forEach(function(link) {
      link.addEventListener('click', function(e) {
          e.preventDefault();
          var testcaseId = e.target.closest('tr').querySelector('.pick').value;
          if (confirm('Вы уверены, что хотите удалить этот тест-кейс?')) {
              fetch('/testcases/delete/' + testcaseId, {
                  method: 'POST',
              }).then(function(response) {
                  if (response.ok) {
                      alert('Тест-кейс успешно удален.');
                      location.reload();
                  } else {
                      alert('Произошла ошибка при удалении тест-кейса.');
                  }
              });
          }
      });
  });
});