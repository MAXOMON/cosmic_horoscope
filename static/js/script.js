function createStars() {
    const numStars = 100;
    const container = document.querySelector('.container');
  
    for (let i = 0; i < numStars; i++) {
      const star = document.createElement('div');
      star.classList.add('star');
  
      // Генерация случайного размера звезды
      const size = Math.random() * 2 + 1; // Размер от 1 до 3 пикселей
      star.style.width = `${size}px`;
      star.style.height = `${size}px`;
  
      // Генерация случайного положения
      star.style.left = `${Math.random() * 100}vw`;
      star.style.top = `${Math.random() * 100}vh`;
  
      // Добавление эффекта мерцания
      star.style.animationDelay = `${Math.random() * 2}s`;
      star.style.opacity = Math.random(); // Случайная яркость звезды
  
      // Добавление эффекта размытия
      const blurEffect = Math.random() * 3; // Размытие от 0 до 3px
      star.style.filter = `blur(${blurEffect}px)`;
  
      // Добавляем звезду в контейнер
      container.appendChild(star);
    }
  }
  createStars();