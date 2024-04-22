//food menu  tabs
const buttons = document.querySelectorAll('.button');
const menus = document.querySelectorAll('.menu');

const highlight = document.createElement('span');
document.body.appendChild(highlight);
highlight.classList.add('highlight');

// Set initial dimensions and position of 'highlight' based on activeButton coords 
function initialHightlightLocation() {
  const activeButton = document.querySelector('.button--is-active');
  const activeButtonCoords = activeButton.getBoundingClientRect();

  const initialCoords = {
    width: activeButtonCoords.width,
    height: activeButtonCoords.height,
    left: activeButtonCoords.left + window.scrollX,
    top: activeButtonCoords.top + window.scrollY
  }

  highlight.style.width = `${initialCoords.width}px`;
  highlight.style.height = `${initialCoords.height}px`;
  highlight.style.transform = `translate(${initialCoords.left}px, ${initialCoords.top}px)`;
}

function handleClick(e) {
  e.preventDefault();

  buttons.forEach(button => button.classList.remove('button--is-active'));
  this.classList.add('button--is-active');

  // Set current dimensions and position of 'highlight' based on the clicked button 
  const buttonCoords = this.getBoundingClientRect();
  const coords = {
    width: buttonCoords.width,
    height: buttonCoords.height,
    left: buttonCoords.left + window.scrollX,
    top: buttonCoords.top + window.scrollY
  }
  highlight.style.width = `${coords.width}px`;
  highlight.style.height = `${coords.height}px`;
  highlight.style.transform = `translate(${coords.left}px, ${coords.top}px)`;

  // Show the menu associated to the clicked button
  const targetMenu = document.querySelector(`#${this.dataset.target}`);
  menus.forEach(menu => {
    menu.classList.remove('menu--is-visible');
    targetMenu.classList.add('menu--is-visible');
  })
}

window.addEventListener('load', initialHightlightLocation);
window.addEventListener('resize', initialHightlightLocation);
buttons.forEach(button => button.addEventListener('click', handleClick));


document.addEventListener("DOMContentLoaded", function() {
  // Check every half second to see if the cart container is ready
  var checkExist = setInterval(function() {
     var cartContainer = document.querySelector('.modal-footer') || document.querySelector('.cart-container');
     if (cartContainer) {
        console.log("Exists!");
        clearInterval(checkExist);
        addDiscountCodeFeature(cartContainer);
     }
  }, 500); // check every 500ms
});

function addDiscountCodeFeature(cartContainer) {
  // Ensure this runs only once and elements are definitely available
  if (document.querySelector('.discount-code-container')) {
      return; // Avoid adding the discount section multiple times
  }

  var discountContainer = document.createElement('div');
  discountContainer.className = 'discount-code-container';
  
  var discountInput = document.createElement('input');
  discountInput.type = 'text';
  discountInput.id = 'discountCode';
  discountInput.placeholder = 'Enter discount code';
  discountInput.className = 'discount-code-input';

  var applyButton = document.createElement('button');
  applyButton.textContent = 'Apply Discount';
  applyButton.onclick = applyDiscount; // Function to apply the discount
  applyButton.className = 'apply-discount-button';

  discountContainer.appendChild(discountInput);
  discountContainer.appendChild(applyButton);

  cartContainer.insertBefore(discountContainer, cartContainer.firstChild);
}

function applyDiscount() {
  var discountCode = document.getElementById('discountCode').value.trim();
  var discountAmount = 0;

  // Example discount validations
  if (discountCode === 'SAVE10') {
      discountAmount = 0.10; // 10% discount
  } else if (discountCode === 'SAVE20') {
      discountAmount = 0.20; // 20% discount
  }

  // Update total assuming a function to calculate and display new total exists
  updateCartTotal(discountAmount);
}

function updateCartTotal(discountPercentage) {
  var totalElement = document.querySelector('#cartTotal'); // This should be your total element ID
  if (totalElement) {
      var currentTotal = parseFloat(totalElement.textContent.replace(/^\$/, ''));
      var newTotal = currentTotal - (currentTotal * discountPercentage);
      totalElement.textContent = '$' + newTotal.toFixed(2);
  } else {
      console.error('Cart total element not found');
  }
}




//mycart
$(function () {

  var goToCartIcon = function($addTocartBtn){
    var $cartIcon = $(".my-cart-icon");
    var $image = $('<img width="30px" height="30px" src="' + $addTocartBtn.data("image") + '"/>').css({"position": "fixed", "z-index": "999"});
    $addTocartBtn.prepend($image);
    var position = $cartIcon.position();
    $image.animate({
      top: position.top,
      left: position.left
    }, 500 , "linear", function() {
      $image.remove();
    });
  }

  $('.my-cart-btn').myCart({
    classCartIcon: 'my-cart-icon',
    classCartBadge: 'my-cart-badge',
    affixCartIcon: true,
    checkoutCart: function(products) {
      $.each(products, function(){
        console.log(this);
      });
    },
    clickOnAddToCart: function($addTocart){
      goToCartIcon($addTocart);
    },
    getDiscountPrice: function(products) {
      var total = 0;
      $.each(products, function(){
        total += this.quantity * this.price;
      });
      return total * 0.5;

      

    }

    

  });

});