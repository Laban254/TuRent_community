//select all the sliders on the document

let sliderHolders = document.getElementsByClassName("slider-holder");

/*-------------------------------------------------------------------------*/
/*since the width and height of slider holdrs is declared using css, 
we can use the pre-defined width and height to make the width and height of 
the sliders equal to that of the slider holder without touching on the 
slider*/
/*--------------------------------------------------------------------------*/

/*we can use a nested loop for this reason. this is to make sure that the 
slider holder that we are using to set the width of the slides is the ancestor 
of those particular slides*/

/*our variable that we can use to hold the available slides in any given slider holder*/
let carouselSlides = null;

let carouselContainers = document.getElementsByClassName("carousel-container");

/*our variable that we can use to hold the available carousel buttons in any given carousel container*/
let carouselButtons = null;

for(let slideHoldersCount = 0; slideHoldersCount < sliderHolders.length; slideHoldersCount++){

    /*select all the slides in the currently looped slider holder*/
    carouselSlides = sliderHolders[slideHoldersCount].getElementsByClassName("carousel-slide");
    /*get the width of the currently looped slider holder*/
    sliderHolderWidth = sliderHolders[slideHoldersCount].getBoundingClientRect().width;
     
    /*loop through the slides*/
    for(let slidesCount = 0; slidesCount < carouselSlides.length; slidesCount++){
        /*set the width of each slide to that of the corresponding slide holder*/
        carouselSlides[slidesCount].style.width = sliderHolderWidth + "px";

        /*push each slideto the left in order to create somesort of flex effect*/
        carouselSlides[slidesCount].style.left = slidesCount *sliderHolderWidth + "px";
    }
}

let currentCarouselSliderHolder = null;
let activeCarouselSlide = null;
let activeSlideIndex = null;
let previousCarouselSlide = null;
let rightCarouselButton = null;
let leftCarouselButton = null;


/*loop through each carousel container*/
for(let carouselContainersCount = 0; carouselContainersCount < carouselContainers.length; carouselContainersCount++){
    
    /*get all the carousel buttons in a given carousel container*/
    carouselButtons = carouselContainers[carouselContainersCount].getElementsByClassName("carousel-button");

    /*loop through the carousel buttons, setting respective event listeners to each one of them*/
    for(let carouselButtonscount = 0; carouselButtonscount < carouselButtons.length; carouselButtonscount++){

        carouselButtons[carouselButtonscount].addEventListener("click", function(){
            /*get the right carouselbutton*/
            rightCarouselButton = carouselContainers[carouselContainersCount].getElementsByClassName("right-carousel-button")[0];
         
            /*get the left carouselbutton*/
            leftCarouselButton = carouselContainers[carouselContainersCount].getElementsByClassName("left-carousel-button")[0];
    
            carouselSlides = carouselContainers[carouselContainersCount].getElementsByClassName("carousel-slide");
            for(let carouselSlidesCount = 0; carouselSlidesCount < carouselSlides.length; carouselSlidesCount++){
                console.log("time");
                if(carouselSlides[carouselSlidesCount].classList.contains("active-slide")){
                    activeCarouselSlide = carouselSlides[carouselSlidesCount];
                    activeSlideIndex = carouselSlidesCount;
                }
            }
            if(this.classList.contains("left-carousel-button")){
                if(isNaN(activeCarouselSlide.previousElementSibling)){
                    previousCarouselSlide = activeCarouselSlide.previousElementSibling;
                    currentCarouselSlider = carouselContainers[carouselContainersCount].getElementsByClassName("slider")[0];
                    currentCarouselSlider.style.right = sliderHolderWidth  * (activeSlideIndex - 1) + "px";
                    activeCarouselSlide.classList.remove("active-slide");
                    previousCarouselSlide.classList.add("active-slide");
                    rightCarouselButton.style.display = "inline";
                    if(!isNaN(previousCarouselSlide.previousElementSibling)){
                        this.style.display = "none";
                    }
                }
                else{
                    this.style.display = "none";
                }
            }
            else if(this.classList.contains("right-carousel-button")){
                if(isNaN(activeCarouselSlide.nextElementSibling)){
                    nextCarouselSlide = activeCarouselSlide.nextElementSibling;
                    currentCarouselSlider = carouselContainers[carouselContainersCount].getElementsByClassName("slider")[0];
                    currentCarouselSlider.style.right = sliderHolderWidth * (activeSlideIndex + 1) + "px";
                    activeCarouselSlide.classList.remove("active-slide");
                    nextCarouselSlide.classList.add("active-slide");
                    leftCarouselButton.style.display = "inline";
                    if(!isNaN(nextCarouselSlide.nextElementSibling)){
                        this.style.display = "none";
                    }
                }
                else{
                    this.style.display = "none";
                }
                
            }
        });
    }
}
