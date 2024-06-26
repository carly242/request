(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);


// Ajoutez ce JavaScript à votre fichier main.js
function initSlider(slider) {
	if(!slider) {
	  return;
	}
	
	let currentIndex = 1;
	const interval = slider.dataset.interval ? parseInt(slider.dataset.interval) : 2500;
	const duration = slider.dataset.duration ? parseInt(slider.dataset.duration) : 250;
	let sliderItems = slider.querySelectorAll('.slot-slider-item');
	const sliderContainer = slider.querySelector('.slot-slider-items');
	
	if(!sliderItems.length || !sliderContainer) {
	  return;
	}
	
	function gotoSlidePosition(slideIndex) {
	  if(sliderItems[slideIndex]) {
		currentIndex = slideIndex;
		const offsetY = (slider.offsetHeight / 2) - (sliderItems[slideIndex].offsetHeight / 2) - sliderItems[slideIndex].offsetTop;
		sliderContainer.style.transform = `translateY(${offsetY}px)`;
		setActiveSlide(slideIndex);
  
		if(slideIndex === sliderItems.length - 2) {
		  window.setTimeout(() => {
			sliderContainer.classList.add('no-transition');
			window.setTimeout(() => {
			  gotoSlidePosition(1);
			  window.setTimeout(() => {
				  sliderContainer.classList.remove('no-transition');
				}, 0);
			}, duration);
		  }, duration);
		}
	  }
	}
  
	function getNextPosition() {
	  if(currentIndex < sliderItems.length - 1) {
		return currentIndex + 1;
	  }
	  else {
		return 1;
	  }
	}
  
	function setActiveSlide(slideIndex) {
	  sliderItems.forEach((item) => {
		item.classList.remove('active');
	  });
	  sliderItems[slideIndex]?.classList.add('active');
	}
	
	sliderContainer.insertBefore(sliderItems[sliderItems.length - 1].cloneNode(true), sliderItems[0]).setAttribute('aria-hidden', 'true');
	sliderContainer.appendChild(sliderItems[0].cloneNode(true)).setAttribute('aria-hidden', 'true');
	sliderContainer.appendChild(sliderItems[1].cloneNode(true)).setAttribute('aria-hidden', 'true');
	
	sliderItems = slider.querySelectorAll('.slot-slider-item');
	
	gotoSlidePosition(currentIndex);
	window.setTimeout(() => {
	  slider.classList.add('active');
	}, duration * 2);
  
	window.setInterval(() => {
	  gotoSlidePosition(getNextPosition());
	}, interval);
  }
  
  document.addEventListener('DOMContentLoaded', function() {
	const sliders = document.querySelectorAll('[data-slot-slider]');
	sliders.forEach((slider) => {
	  initSlider(slider);
	});
  });
  
