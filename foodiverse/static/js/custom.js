function initAutoComplete () {
        const options = {
            types: ["establishment",'geocode'],
        };
      const input = document.getElementById("id_address")


      let autocomplete = new google.maps.places.Autocomplete(input, options)
    
    
      autocomplete.addListener("place_changed", ()=>{
        const place = autocomplete.getPlace();
        if (!place.geometry || !place.geometry.location) {
          // User entered the name of a Place that was not suggested and
          // pressed the Enter key, or the Place Details request failed.
          window.alert("No details available for input: '" + place.name + "'");
          return;
        }
      })
      
      
}
google.maps.event.addDomListener(window, 'load', initAutoComplete);
  


$(document).ready(function(){
    $('.restaurant-add-menu-btn').on('click',function(e){
      e.preventDefault();
      console.log('test')
      alert('Add');
    })
})