let star_rating = document.querySelectorAll(".star_rating");
for(let counter=0; counter < star_rating.length; counter++){
    star_rating[counter].addEventListener("click", function(){
        for(let inner_counter = 0; inner_counter <= counter; inner_counter++){
            star_rating[inner_counter].classList.add("active_rating");
        }
    });
}