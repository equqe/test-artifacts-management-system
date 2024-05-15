document.querySelectorAll('.edit').forEach(function(button) {
    button.addEventListener('click', function(event) {
      event.preventDefault();
  
      // Находим меню по атрибуту data-menu-target
      const menuId = event.target.getAttribute('data-menu-target');
      const menu = document.getElementById(menuId);
  
      // Получаем координаты кнопки относительно окна
      const buttonRect = event.target.getBoundingClientRect();
  
      // Устанавливаем координаты меню относительно кнопки
      menu.style.left = buttonRect.left + 'px';
      menu.style.top = buttonRect.bottom + 'px';
  
      // Меняем стиль отображения меню
      if (menu.style.display === 'none') {
        menu.style.display = 'block';
      } else {
        menu.style.display = 'none';
      }
  
      // Добавляем обработчик событий клика по документу для закрытия меню
      function handleDocumentClick(e) {
        if (!menu.contains(e.target) && e.target !== button) {
          menu.style.display = 'none';
          document.removeEventListener('click', handleDocumentClick);
        }
      }
  
      document.addEventListener('click', handleDocumentClick);
    });
  });
  