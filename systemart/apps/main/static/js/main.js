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

  document.querySelector('#delete-form').addEventListener('submit', function(e) {
    e.preventDefault();

    var testcase_id = this.dataset.testcaseId;

    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

    var formData = new FormData();
    formData.append('password', document.querySelector('#password').value);
    formData.append('csrfmiddlewaretoken', csrfToken);

    fetch('/testcases/delete/' + testcase_id + '/', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        document.querySelector('#password-form').style.display = 'none';

        var rowToRemove = document.querySelector('tr[data-testcase-id="' + this.dataset.testcaseId + '"]');
        rowToRemove.parentNode.removeChild(rowToRemove);
      } else {
        alert(data.error);
      }
    })
    .catch(error => {
      location.reload();
    });
  });

});


