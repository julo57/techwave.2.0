// Pobierz koszyk z localStorage
var cart = JSON.parse(localStorage.getItem('cart')) || [];
var cartItemsElement = document.getElementById('cart-items');

// Funkcja usuwająca produkt z koszyka i odświeżająca wyświetlanie
function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCart();
}

// Funkcja wyświetlająca produkty w koszyku
function displayCart() {
    cartItemsElement.innerHTML = ''; // Wyczyść zawartość przed aktualizacją

    cart.forEach(function(product, index) {
        var li = document.createElement('li');
        li.classList.add('cart-item');

        // Tworzenie elementu obrazu
        var img = document.createElement('img');
        img.src = product.image;
        img.alt = product.name;
        img.classList.add('product-image'); // Dodaj klasę do obrazka

        // Tworzenie elementów nazwy, ceny i przycisku usuwania
        var name = document.createElement('span');
        name.textContent = product.name;
        name.classList.add('product-name'); // Dodaj klasę do nazwy

        var price = document.createElement('span');
        price.textContent = product.price;
        price.classList.add('product-price'); // Dodaj klasę do ceny

        var removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.classList.add('remove-button'); // Dodaj klasę do przycisku usuwania
        removeButton.onclick = function() {
            removeFromCart(index);
        };

        // Dodanie wszystkich elementów do elementu <li>
        li.appendChild(img);
        li.appendChild(name);
        li.appendChild(price);
        li.appendChild(removeButton);

        // Dodanie <li> do listy
        cartItemsElement.appendChild(li);
    });
}

// Wyświetl produkty w koszyku po załadowaniu strony
displayCart();

// Pobierz przyciski
var checkoutButton = document.querySelector('.checkout-button');
var continueShoppingButton = document.querySelector('.continue-shopping-button');

// Przycisk "Przejdź do kasy"
checkoutButton.onclick = function() {
    // Przekieruj do strony kasy
    window.location.href = '/payment';
};

// Przycisk "Kontynuuj zakupy"
continueShoppingButton.onclick = function() {
    // Przekieruj do strony głównej
    window.location.href = '/productsite';
};
