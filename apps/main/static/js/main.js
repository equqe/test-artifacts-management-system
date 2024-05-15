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
  